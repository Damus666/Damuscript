class StatementsNode:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self): return f"STATEMENTS{self.statements}"

class NumberNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self): return f"N{self.token}"
    
class StringNode:
    def __init__(self, token):
        self.token = token

    def __repr__(self): return f"S'{self.token}'"

class BinOpNode:
    def __init__(self, left_node, op_tok, right_node):
        self.left_node = left_node
        self.op_tok = op_tok
        self.right_node = right_node

    def __repr__(self): return f"BIN({self.left_node} {self.op_tok} {self.right_node})"
    
class UnaryOpNode:
    def __init__(self, op_tok, node):
        self.op_tok = op_tok
        self.node = node

    def __repr__(self): return f"UNARY({self.op_tok} {self.node})"

class NameAccessNode:
    def __init__(self, name_tok):
        self.name_tok = name_tok

    def __repr__(self):
        return f"NAME {self.name_tok}"

class NameAssignNode:
    def __init__(self, name_tok, value_node):
        self.name_tok = name_tok
        self.value_node = value_node

    def __repr__(self): return f"ASSIGN({self.name_tok} = {self.value_node})"
    
class ListNode:
    def __init__(self, elements):
        self.elements = elements

    def __repr__(self): return f"LIST({self.elements})"

class ObjectNode:
    def __init__(self, fields):
        self.fields = fields

    def __repr__(self): return f"OBJECT({self.fields})"
    
class DotAccessNode:
    def __init__(self, node, name_tok):
        self.node = node
        self.name_tok = name_tok

    def __repr__(self): return f"DOTA({self.node}.{self.name_tok})"
    
class DotAssignNode:
    def __init__(self, node, name_tok, value_node):
        self.node = node
        self.name_tok = name_tok
        self.value_node = value_node

    def __repr__(self): return f"DOTM({self.node}.{self.name_tok}={self.value_node})"
    
class IndexAccessNode:
    def __init__(self, node, index_node):
        self.node = node
        self.index_node = index_node

    def __repr__(self): return f"INDEXA({self.node}[{self.index_node}])"
    
class IndexAssignNode:
    def __init__(self, node, index_node, value_node):
        self.node = node
        self.index_node = index_node
        self.value_node = value_node

    def __repr__(self): return f"INDEXM({self.node}[{self.index_node}]={self.value_node})"
    
class FunctionDefinitionNode:
    def __init__(self, name_tok, params, code):
        self.name_tok = name_tok
        self.params = params
        self.code = code

    def __repr__(self): return f"FUN({self.name_tok} {self.params} {self.code})"

class CallNode:
    def __init__(self, node, param_nodes):
        self.node = node
        self.param_nodes = param_nodes

    def __repr__(self): return f"CALL({self.node}{self.param_nodes})"
    
class ReturnNode:
    def __init__(self, value_node):
        self.value_node = value_node

    def __repr__(self): return f"RETURN {self.value_node}"
    
class UseNode:
    def __init__(self, name_tok):
        self.name_tok = name_tok

    def __repr__(self): return f"USE({self.name_tok})"

class WhileNode:
    def __init__(self, cond_node, code):
        self.cond_node = cond_node
        self.code = code

    def __repr__(self): return f"WHILE({self.cond_node}: {self.code})"

class RepeatNode:
    def __init__(self, iter_tok, start_node, end_node, step_node, code):
        self.iter_tok = iter_tok
        self.start_node = start_node
        self.end_node = end_node
        self.step_node = step_node
        self.code = code
    
    def __repr__(self): return f"REPEAT({self.iter_tok}={self.start_node} to {self.end_node} step {self.step_node} {self.code})"

class ForNode:
    def __init__(self, element_tok, iterator_node, code):
        self.element_tok = element_tok
        self.iterator_node = iterator_node
        self.code = code

    def __repr__(self): return f"FOR({self.element_tok} .. {self.iterator_node} {self.code})"

class IfNode:
    def __init__(self, cond_node, code, else_node):
        self.cond_node = cond_node
        self.code = code
        self.else_node = else_node

    def __repr__(self): return f"IF({self.cond_node} do {self.code} else {self.else_node})"

class ConditionNode:
    def __init__(self, true_node, cond_node, false_node):
        self.true_node = true_node
        self.cond_node = cond_node
        self.false_node = false_node

    def __repr__(self): return f"COND({self.true_node} if {self.cond_node} else {self.false_node})"

class ListGeneratorNode:
    def __init__(self, element_tok, iterator_node, expression_node):
        self.element_tok = element_tok
        self.iterator_node = iterator_node
        self.expression_node = expression_node

    def __repr__(self): return f"LISTGEN({self.expression_node} for {self.element_tok} in {self.iterator_node})"

class StopNode:...
class SkipNode:...
