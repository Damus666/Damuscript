import sys
from data import Data

INTERPRETER = None

class Value:
    name = "Value"
    methods_data = {}

    def __init__(self, value=None):
        self.value = value

        self.method_lookup = {
            "+": self._add_,
            "-": self._subtract_,
            "*": self._mult_,
            "/": self._div_,
            "^": self._pow_,
            ">": self._gt_,
            "<": self._lt_,
            ">=": self._gte_,
            "<=": self._lte_,
            "==": self._equal_,
            "!": self._not_,
            "|": self._or_,
            "&": self._and_,
            "?": self._xor_,
        }

        self.methods = {
            name: DSFunctionValue(name, data[0], data[1], self) for name, data in self.methods_data.items()
        }

    def type_error(self, op, other):
        sys.exit(f"InvalidOperationError: '{op}' operation cannot be made between the types '{self.name}' and '{other.name}'")

    def _add_(self, value): self.type_error("+", value)
    def _subtract_(self, value): self.type_error("-", value)
    def _mult_(self, value): self.type_error("*", value)
    def _div_(self, value): self.type_error("/", value)
    def _pow_(self, value): self.type_error("^", value)

    def _bool_(self): return bool(self.value)
    def _equal_(self, value): return BoolValue(self.value == value.value)

    def _gt_(self, value): self.type_error(">", value)
    def _lt_(self, value): self.type_error("<", value)
    def _gte_(self, value): self.type_error(">=", value)
    def _lte_(self, value): self.type_error("<=", value)

    def _not_(self): return BoolValue((not self._bool_()))
    def _and_(self, value): return BoolValue((self._bool_() and value._bool_()))
    def _or_(self, value): return BoolValue((self._bool_() or value._bool_()))
    def _xor_(self, value): return BoolValue((self._bool_() ^ value._bool_()))

    def _index_get_(self, value): sys.exit(f"IndexError: '{self.name}' does not support indexing")
    def _index_set_(self, value): sys.exit(f"IndexError: '{self.name}' does not support index modifying")
    def _dot_set_(self, name, value): sys.exit(f"DotError: '{self.name}' does not support dot modifying")
    def _call_(self, arguments): sys.exit(f"CallError: '{self.name}' does not support calling")
    def _dot_has_(self, name): return BoolValue(name in self.methods)

    def _dot_get_(self, value):
        if value in self.methods:
            return self.methods[value]
        sys.exit(f"FieldError: '{self.name}' has no field/method '{value}'")

    def _len_(self): sys.exit(f"LenError: '{self.name}' does not support length")
    def _copy_(self): sys.exit(f"CopyError: '{self.name}' does not support copying")

    def _to_string_(self): return StringValue(self.__str__())
    def _to_int_(self): sys.exit(f"ConvertError: Cannot convert '{self.name}' to int")
    def _to_float_(self): sys.exit(f"ConvertError: Cannot convert '{self.name}' to float")
    def _to_list_(self): sys.exit(f"ConvertError: Cannot convert '{self.name}' to list")

    def _iter_(self): sys.exit(f"IterError: '{self.name}' does not support iterating")
    def _iter_next_(self): sys.exit(f"IterError: '{self.name}' does not support iterating")

    def __str__(self): return f"{self.value.__str__()}"
    def __repr__(self): return f"{self.value.__str__()}"

class NumberValue(Value):
    name = "Number"

    def _add_(self, value): return NumberValue(self.value+value.value)
    def _subtract_(self, value): return NumberValue(self.value-value.value)
    def _mult_(self, value): return NumberValue(self.value*value.value)
    def _div_(self, value): return NumberValue(self.value/value.value)
    def _pow_(self, value): return NumberValue(self.value**value.value)
    def _bool_(self): return bool(self.value)

    def _gt_(self, value): return BoolValue(self.value > value.value)
    def _lt_(self, value): return BoolValue(self.value < value.value)
    def _gte_(self, value): return BoolValue(self.value >= value.value)
    def _lte_(self, value): return BoolValue(self.value <= value.value)

    def _to_int_(self): return NumberValue(int(self.value))
    def _to_float_(self): return NumberValue(float(self.value))

    def _copy_(self): return NumberValue(self.value)

class StringValue(Value):
    name = "String"

    def _add_(self, value): return StringValue(self.value+value.value)
    def _mult_(self, value): return StringValue(self.value*value.value)
    def _len_(self): return NumberValue(len(self.value))
    def _copy_(self): return StringValue(self.value)
    def _to_list_(self): return ListValue([StringValue(el) for el in list(self.value)])

    def _to_int_(self):
        try: return NumberValue(int(self.value))
        except: sys.exit(f"ConvertError: failed to convert '{self.value}' to int")
    def _to_float_(self):
        try: return NumberValue(int(self.value))
        except: sys.exit(f"ConvertError: failed to convert '{self.value}' to float")

    def _iter_(self): return self._to_list_()._iter_()

class BoolValue(NumberValue):
    name = "Bool"
    def _copy_(self): return BoolValue(self.value)
    def __str__(self): return "true" if self.value else "false"

class NullValue(Value):
    name = "Null"
    def __str__(self): return "null"

class ListValue(Value):
    name = "List"

    def _index_get_(self, value):
        try:
            if not value.name == "Number": sys.exit(f"IndexError: List indices must be of Number type")
            return self.value[int(value.value)]
        except IndexError:
            sys.exit(f"IndexError: Max list index exceeded")

    def _index_set_(self, index, value):
        if not index.name == "Number": sys.exit(f"IndexError: List indices must be of Number type")
        if index.value > len(self.value)-1: sys.exit(f"IndexError: Max list index exceeded")
        self.value[index.value] = value
        return value
    
    def _len_(self): return NumberValue(len(self.value))
    def _copy_(self): return ListValue(self.value.copy())
    def _iter_(self): return ListIteratorValue(self)
    def _to_list_(self): return ListValue(self.value.copy())

    def __str__(self):
        return f"{self.value}"
    
class ListIteratorValue(Value):
    name = "ListIterator"

    def __init__(self, list):
        super().__init__({"list": list, "index": 0})

    def _iter_next_(self):
        if self.value["index"] >= len(self.value["list"].value):
            return Stop()
        value = self.value["list"].value[self.value["index"]]
        self.value["index"] += 1
        return value

class ObjectValue(Value):
    name = "Object"

    def __init__(self, value=None):
        super().__init__(value)
        for name, value in self.value.items():
            if value.name == "Function":
                value.method_bind(self, name)
        for name, method in self.methods.items():
            self.value[name] = method

    def _copy_(self): return self.__class__(self.value.copy())

    def _dot_get_(self, value):
        ret_value = self.value.get(value, None)
        if ret_value is None:
            sys.exit(f"FieldError: This object has no field '{value}'")
        return ret_value
    
    def _dot_has_(self, name):
        return BoolValue(name in self.value)

    def _dot_set_(self, name, value):
        self.value[name] = value
        return value
    
    def __str__(self):
        return f"{self.value}"
    
class FunctionValue(Value):
    name = "Function"

    def _call_(self, arguments, data_parent):
        data = Data(data_parent)
        interpreter = INTERPRETER(data)
        if len(arguments) != len(self.value["params"]):
            sys.exit(f"CallError: Wrong number of parameters passed to '{self.value['name']}'. Expected: {self.value['params']}")
        for i, argument in enumerate(arguments):
            data.write(self.value["params"][i], argument)
        for name, arg in self.value["default-args"].items():
            data.write(name, arg)
        result = interpreter.interpret(self.value["code"])
        if result.name == "Return": return result.value
        else: return result
    
    def method_bind(self, obj, name):
        self.value["name"] = name
        self.value["default-args"] = {"this":obj}

    def __str__(self):
        return f"{self.name}<{self.value['name']}>"
    def __repr__(self):
        return f"{self.name}<{self.value['name']}>"
    
class DSFunctionValue(Value):
    name = "DSFunction"

    def __init__(self, ds_name, function, params, method_bind=None):
        self.ds_name = ds_name
        self.function = function
        self.params = params
        self.value = True
        self.default_params = {}
        if method_bind:
            self.default_params = {"this": method_bind}

    def _call_(self, arguments, data_parent):
        data = {}
        if len(arguments) != len(self.params):
            sys.exit(f"CallError: Wrong number of parameters passed to '{self.ds_name}'. Expected: {self.params}")
        for i, argument in enumerate(arguments):
            data[self.params[i]] = argument
        for name, val in self.default_params.items():
            data[name]= val
        return self.function(data)

    def __str__(self):
        return f"{self.name}<{self.ds_name}>"
    def __repr__(self):
        return f"{self.name}<{self.ds_name}>"
    
class Return:
    name = "Return"

    def __init__(self, value):
        self.value = value

class Stop:
    name = "Stop"
    value = NullValue()

class Skip:
    name = "Skip"
    value = NullValue()
