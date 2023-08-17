from nodes import NumberNode, StatementsNode, BinOpNode, NameAccessNode, NameAssignNode, CallNode, ReturnNode, ListGeneratorNode, \
    StringNode, UseNode, UnaryOpNode, ListNode, ObjectNode, DotAccessNode, IndexAccessNode, IndexAssignNode, \
    DotAssignNode, FunctionDefinitionNode, WhileNode, StopNode, SkipNode, RepeatNode, ForNode, IfNode, ConditionNode
import sys
from tokens import KEYWORDS, Token

class Parser:
    def __init__(self, tokens):
        self.tokens:list[Token] = tokens
        self.idx = 0
        self.token:Token = self.tokens[self.idx]

    # FACTORS
    def number_factor(self):
        token = self.token
        self.move()
        return NumberNode(token)
    
    def string_factor(self):
        token = self.token
        self.move()
        return StringNode(token)
    
    def paren_expression(self):
        self.move()
        expression = self.expression()
        self.move()
        return expression
    
    def unary_expression(self):
        operator = self.token
        self.move()
        operand = self.expression()
        return UnaryOpNode(operator, operand)
    
    def list_factor(self):
        self.move()
        elements = []
        if self.token.value == "]":
            self.move()
            return ListNode(elements)
        if self.token.type == "KW" and self.token.value == KEYWORDS["foreach"]:
            self.move()
            if not self.token.type == "NAME":
                sys.exit(f"SyntaxError: in list generator after for, a name is expected")
            element_tok = self.token
            self.move()
            if not self.token.type == "KW" and not self.token.value == KEYWORDS["in"]:
                sys.exit(f"SyntaxError: in list generator after iterator name in is expected")
            self.move()
            iterator_node = self.expression()
            if not self.token.value == ":":
                sys.exit(f"SyntaxError: after list generator iterator : is expected")
            self.move()
            expression_node = self.expression()
            self.move()
            return ListGeneratorNode(element_tok, iterator_node, expression_node)
        else:
            element = self.expression()
            elements.append(element)
            while self.token.value == ",":
                self.move()
                if self.token.value == "]":
                    self.move()
                    return ListNode(elements)
                element = self.expression()
                elements.append(element)
            self.move()
            return ListNode(elements)
    
    def object_factor(self):
        self.move()
        fields = {}
        if self.token.value == "}":
            self.move()
            return ObjectNode(fields)
        field_name, field_value = self.object_field()
        fields[field_name] = field_value
        while self.token.type == "SEMIC":
            self.move()
            if self.token.value == "}":
                self.move()
                return ObjectNode(fields)
            field_name, field_value = self.object_field()
            fields[field_name] = field_value
        self.move()
        return ObjectNode(fields)
    
    def object_field(self):
        if not self.token.type == "NAME":
            sys.exit("SyntaxError: expected field declaration inside object declaration")
        name = self.token
        self.move()
        if not self.token.value == "=":
            sys.exit("SyntaxError: expected = after field declaration inside object declaration")
        self.move()
        value = self.expression()
        return name, value

    def function_definition(self):
        self.move()
        if self.token.type == "NAME":
            name_tok = self.token
            self.move()
        else:
            name_tok = Token("NAME", "_")
        if not self.token.value == "(":
            sys.exit(f"SyntaxError: '(' is expected after function name declaration")
        params = []
        self.move()
        if self.token.value != ")":
            param = self.token
            params.append(param)
            self.move()
            while self.token.value == ",":
                self.move()
                if self.token.value == ")":
                    break
                param = self.token
                self.move()
                params.append(param)
            self.move()
        else:
            self.move()
        if not self.token.value == "{":
            sys.exit("SyntaxError: '{' is expected after function parameter declaration")
        self.move()
        code = self.statements()
        self.move()
        return FunctionDefinitionNode(name_tok, params, code)

    def variable(self):
        if self.token.type == "NAME":
            token = self.token
            self.move()
            if self.token.type == "NAME":
                sys.exit(f"SyntaxError: After '{token}' name, there can't be another name without operators in between")
            return NameAccessNode(token)
    
    def assignment(self):
        name_tok = self.token
        self.move()
        if self.token.value == "=":
            self.move()
            value_node = self.expression()
            return NameAssignNode(name_tok, value_node)

    def factor(self):
        if self.token.type == "INT" or self.token.type == "FLOAT":
            return self.number_factor()
        elif self.token.type == "STR":
            return self.string_factor()
        elif self.token.value == "(":
            return self.paren_expression()
        elif self.token.type == "NAME":
            if self.future().value == "=":
                return self.assignment()
            return self.variable()
        elif self.token.value == "+" or self.token.value == "-":
            return self.unary_expression()
        elif self.token.value == "[":
            return self.list_factor()
        elif self.token.value == "{":
            return self.object_factor()
        if self.token.type == "KW" and self.token.value == KEYWORDS["function"]:
            return self.function_definition()
        elif self.token.type == "EOF":
            sys.exit(f"SyntaxError: unexpected EOF")

    # EXTRA FACTOR
    def extra_factor(self, node=None):
        left_node = self.factor() if not node else node
        if self.token.value == ".":
            return self.dot_access_modify(left_node)
        elif self.token.value == "[":
            return self.index(left_node)
        elif self.token.value == "(":
            return self.call(left_node)
        return left_node
    
    def dot_access_modify(self, left_node):
        self.move()
        if not self.token.type == "NAME":
            sys.exit("SyntaxError: expected field name after '.'")
        name_tok = self.token
        self.move()
        if self.token.value == "=":
            self.move()
            value_node = self.expression()
            return DotAssignNode(left_node, name_tok, value_node)
        left_node = DotAccessNode(left_node, name_tok)
        while self.token.value == ".":
            self.move()
            if self.token.type == "NAME":
                name_tok = self.token
                self.move()
                if self.token.value == "=":
                    self.move()
                    value_node = self.expression()
                    return DotAssignNode(left_node, name_tok, value_node)
                left_node = DotAccessNode(left_node, name_tok)
        return self.extra_factor(left_node)
        
    def index(self, left_node):
        self.move()
        index = self.expression()
        self.move()
        if self.token.value == "=":
            self.move()
            value_node = self.expression()
            return IndexAssignNode(left_node, index, value_node)
        left_node = IndexAccessNode(left_node, index)
        while self.token.value == "[":
            self.move()
            index = self.expression()
            self.move()
            if self.token.value == "=":
                self. move()
                value_node = self.expression()
                return IndexAssignNode(left_node, index, value_node)
            left_node = IndexAccessNode(left_node, index)
        return self.extra_factor(left_node)
    
    def call(self, left_node):
        left_node = self.inner_call(left_node)
        while self.token.value == "(":
            left_node = self.inner_call(left_node)
        return self.extra_factor(left_node)

    def inner_call(self, left_node):
        self.move()
        params = []
        if self.token.value == ")":
            self.move()
            return CallNode(left_node, params)
        param = self.expression()
        params.append(param)
        while self.token.value == ",":
            self.move()
            if self.token.value == ")":
                self.move()
                return CallNode(left_node, params)
            param = self.expression()
            params.append(param)
        self.move()
        left_node = CallNode(left_node, params)
        return left_node
    
    # EXPRESSION
    def expression(self):
        left_node = self.logic_expression()
        if self.token.type == "KW" and self.token.value == KEYWORDS["if"]:
            self.move()
            condition = self.expression()
            if not self.token.type == "KW" and self.token.value == KEYWORDS["else"]:
                sys.exit(f"SyntaxError: after value if condition else value is expected")
            self.move()
            right_node = self.expression()
            return ConditionNode(left_node, condition, right_node)
        return left_node
    
    def term(self):
        return self.bin_op(self.extra_factor, ["*", "/", "^"])
    
    def arith_expression(self):
        return self.bin_op(self.term, ["+", "-"])
    
    def bool_expression(self):
        return self.bin_op(self.arith_expression, ["==", ">=", "<=", ">", "<"])
    
    def not_expression(self):
        if self.token.value == "!":
            op_tok = self.token
            self.move()
            return UnaryOpNode(op_tok, self.bool_expression())
        return self.bool_expression()
    
    def logic_expression(self):
        return self.bin_op(self.not_expression, ["|", "&", "?"])
    
    # STATEMENTS
    def return_statement(self):
        self.move()
        value_node = self.expression()
        return ReturnNode(value_node)
    
    def use_statement(self):
        self.move()
        if not self.token.type == "NAME":
            sys.exit(f"SyntaxError: Name expected after use statement")
        name_tok = self.token
        self.move()
        return UseNode(name_tok)
    
    def while_statement(self):
        self.move()
        condition_node = self.expression()
        if not self.token.value == "{":
            sys.exit("SyntaxError: After while condition code must be inside {}")
        self.move()
        code = self.statements()
        self.move()
        return WhileNode(condition_node, code)
    
    def repeat_statement(self):
        self.move()
        if not self.token.type == "NAME":
            sys.exit(f"SyntaxError: After repeat an iter count variable name definition is expected")
        iter_tok = self.token
        self.move()
        if not self.token.value == "=":
            sys.exit(f"SyntaxError: After iterator name '=' is expected")
        self.move()
        start_node = self.expression()
        if not self.token.type == "KW" and not self.token.value == KEYWORDS["to"]:
            sys.exit(f"SyntaxError: After iterator definition 'to' is expected")
        self.move()
        end_node = self.expression()
        step_node = NumberNode(Token("INT", 1))
        if self.token.type == "KW" and self.token.value == KEYWORDS["step"]:
            self.move()
            step_node = self.expression()
        if not self.token.value == "{":
            sys.exit("SyntaxError: After repeat statement code must be put in {}")
        self.move()
        code = self.statements()
        self.move()
        return RepeatNode(iter_tok, start_node, end_node, step_node, code)
    
    def for_statement(self):
        self.move()
        if not self.token.type == "NAME":
            sys.exit(f"SyntaxError: After repeat an iter count variable name definition is expected")
        element_tok = self.token
        self.move()
        if not self.token.type == "KW" and not self.token.value == KEYWORDS["in"]:
            sys.exit(f"SyntaxError: After element name definition 'in' is expected")
        self.move()
        iterator_node = self.expression()
        if not self.token.value == "{":
            sys.exit("SyntaxError: After repeat statement code must be put in {}")
        self.move()
        code = self.statements()
        self.move()
        return ForNode(element_tok, iterator_node, code)
    
    def if_statement(self):
        self.move()
        condition_node = self.expression()
        if not self.token.value == "{":
            sys.exit("SyntaxError: After if condition code must be put in {}")
        self.move()
        code = self.statements()
        self.move()
        else_statement = None
        if self.token.type == "KW" and self.token.value == KEYWORDS["else"]:
            self.move()
            else_statement = self.statement()
        return IfNode(condition_node, code, else_statement)
    
    def stop_statement(self):
        self.move()
        return StopNode()

    def skip_statement(self):
        self.move()
        return SkipNode()

    # statements
    def statement(self):
        if self.token.type == "KW" and self.token.value == KEYWORDS["return"]:
            return self.return_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["while"]:
            return self.while_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["for"]:
            return self.repeat_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["foreach"]:
            return self.for_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["if"]:
            return self.if_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["import"]:
            return self.use_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["break"]:
            return self.stop_statement()
        elif self.token.type == "KW" and self.token.value == KEYWORDS["continue"]:
            return self.skip_statement()
        elif self.token.value == "{":
            self.move()
            return self.statements()
        return self.expression()
        
    def statements(self):
        statements = []
        statement = self.statement()
        statements.append(statement)
        while self.token.type == "SEMIC" or self.previous().value == "}":
            if self.token.type == "SEMIC":
                self.move()
            if self.token.type == "EOF" or self.token.value == "}": break
            statement = self.statement()
            statements.append(statement)
        return StatementsNode(statements)

    # MAIN
    def parse(self):
        return self.statements()

    def bin_op(self, left_func, tok_values, right_func=None):
        if right_func is None: right_func = left_func
        left_node = left_func()
        while self.token.value in tok_values:
            operation = self.token
            self.move()
            right_node = right_func()
            left_node = BinOpNode(left_node, operation, right_node)
        return left_node

    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]

    def future(self):
        idx = self.idx
        idx += 1
        if idx < len(self.tokens):
            return self.tokens[idx]
        
    def previous(self):
        if self.idx-1 >= 0:
            return self.tokens[self.idx-1]
        return self.token