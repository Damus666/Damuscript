from values import NumberValue, ListValue, ObjectValue, FunctionValue, Return, StringValue, NullValue, Stop, Skip
import values, sys
from data import Data
from api import DSAPI

class Interpreter:
    def __init__(self, data):
        self.data: Data = data

    def NumberNode(self, node):
        return NumberValue(node.token.value)
    
    def StringNode(self, node):
        return StringValue(node.token.value)
    
    def BinOpNode(self, node):
        left = self.interpret(node.left_node)
        right = self.interpret(node.right_node)

        return left.method_lookup[node.op_tok.value](right)
    
    def UnaryOpNode(self, node):
        right = self.interpret(node.node)

        if node.op_tok.value == "!":
            return right._not_()
        else:
            left = NumberValue(0)
            return left.method_lookup[node.op_tok.value](right)
        
    def NameAccessNode(self, node):
        return self.data.read(node.name_tok.value)
    
    def NameAssignNode(self, node):
        value = self.interpret(node.value_node)
        self.data.write(node.name_tok.value, value)
        return value
    
    def ListNode(self, node):
        values = []
        for element in node.elements:
            value = self.interpret(element)
            values.append(value)
        return ListValue(values)
    
    def ObjectNode(self, node):
        fields = {}
        for name_tok, value_node in node.fields.items():
            value = self.interpret(value_node)
            fields[name_tok.value] = value
        return ObjectValue(fields)
    
    def DotAccessNode(self, node):
        value = self.interpret(node.node)
        return value._dot_get_(node.name_tok.value)
    
    def DotAssignNode(self, node):
        main_value = self.interpret(node.node)
        value = self.interpret(node.value_node)
        return main_value._dot_set_(node.name_tok.value, value)
    
    def IndexAccessNode(self, node):
        value = self.interpret(node.node)
        index_value = self.interpret(node.index_node)
        return value._index_get_(index_value)
    
    def IndexAssignNode(self, node):
        main_value = self.interpret(node.node)
        index_value = self.interpret(node.index_node)
        value = self.interpret(node.value_node)
        return main_value._index_set_(index_value, value)
    
    def FunctionDefinitionNode(self, node):
        data = {
            "name": node.name_tok.value,
            "params": [param.value for param in node.params],
            "code": node.code,
            "default-args":{},
        }
        fun = FunctionValue(data)
        self.data.write(node.name_tok.value, fun)
        return fun
    
    def CallNode(self, node):
        value = self.interpret(node.node)
        params = []
        for param_node in node.param_nodes:
            param = self.interpret(param_node)
            params.append(param)
        return value._call_(params, self.data)
    
    def ReturnNode(self, node):
        value = self.interpret(node.value_node)
        return Return(value)
    
    def UseNode(self, node):
        DSAPI.import_module(node.name_tok.value)
        return NullValue()
    
    def WhileNode(self, node):
        while True:
            condition = self.interpret(node.cond_node)._bool_()
            if condition == False:
                return NullValue()
            result = self.interpret(node.code)
            if result.name == "Return":
                return result
            elif result.name == "Stop":
                return NullValue()
            elif result.name == "Skip":
                continue

    def RepeatNode(self, node):
        start_value = self.interpret(node.start_node)
        end_value = self.interpret(node.end_node)
        step_value = self.interpret(node.step_node)
        if not start_value.name == "Number":
            sys.exit(f"TypeError: iterator type must be Number")
        if not end_value.name == "Number":
            sys.exit(f"TypeError: iterator end value type must be Number")
        if not step_value.name == "Number":
            sys.exit(f"TypeError: iterator step type must be Number")
        for i in range(int(start_value.value), int(end_value.value), int(step_value.value)):
            self.data.write(node.iter_tok.value, NumberValue(i))
            result = self.interpret(node.code)
            if result.name == "Return":
                return result
            elif result.name == "Stop":
                return NullValue()
            elif result.name == "Skip":
                continue
        return NullValue()
    
    def ForNode(self, node):
        iterator = self.interpret(node.iterator_node)
        generator = iterator._iter_()
        while True:
            value = generator._iter_next_()
            if value.name == "Stop": return NullValue()
            self.data.write(node.element_tok.value, value)
            result = self.interpret(node.code)
            if result.name == "Return":
                return result
            elif result.name == "Stop":
                return NullValue()
            elif result.name == "Skip":
                continue

    def ListGeneratorNode(self, node):
        elements = []
        iterator = self.interpret(node.iterator_node)
        generator = iterator._iter_()
        while True:
            value = generator._iter_next_()
            if value.name == "Stop": break
            self.data.write(node.element_tok.value, value)
            result = self.interpret(node.expression_node)
            elements.append(result)
        return ListValue(elements)

    def IfNode(self, node):
        condition = self.interpret(node.cond_node)._bool_()
        if condition == True:
            return self.interpret(node.code)
        else:
            if node.else_node:
                return self.interpret(node.else_node)
        return NullValue()
    
    def ConditionNode(self, node):
        condition = self.interpret(node.cond_node)._bool_()
        if condition == True:
            return self.interpret(node.true_node)
        else:
            return self.interpret(node.false_node)

    def StopNode(self, node):
        return Stop()

    def SkipNode(self, node):
        return Skip()

    def StatementsNode(self, node):
        for statement in node.statements:
            res = self.interpret(statement)
            if res.name in ["Return","Stop","Skip"]: return res
            #print(str(res))
            # print(repr(res))
        return NullValue(None)

    def interpret(self, node):
        return getattr(self, node.__class__.__name__)(node)
    
values.INTERPRETER = Interpreter