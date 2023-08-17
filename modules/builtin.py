from api import *

# CONSOLE
def fun_print(data:DSPD): return NullValue(print(data["value"]))
def fun_input(data:DSPD): return StringValue(input(str(data["message"])))

# VALUE DATA
def fun_len(data:DSPD): return data["value"]._len_()
def fun_copy(data:DSPD): return data["value"]._copy_()
def fun_id(data:DSPD): return NumberValue(id(data["value"]))
def fun_typename(data:DSPD): return StringValue(data["value"].name)

# CONVERSION
def fun_tostring(data:DSPD): return data["value"]._to_string_()
def fun_toint(data:DSPD): return data["value"]._to_int_()
def fun_tofloat(data:DSPD): return data["value"]._to_float_()
def fun_tolist(data:DSPD): return data["value"]._to_list_()
def fun_tobool(data:DSPD): return BoolValue(data["value"]._bool_())

# NEW VALUE
def fun_object(data:DSPD): return ObjectValue({})
def fun_list(data:DSPD): return ListValue([])

# DOT
def fun_getattr(data:DSPD): return data["value"]._dot_get_(DSAPI.check_ret(data, "name", "String").value)
def fun_setattr(data:DSPD): return data["value"]._dot_set_(DSAPI.check_ret(data, "name", "String").value, data["v"])
def fun_hasattr(data:DSPD): return data["value"]._dot_has_(DSAPI.check_ret(data, "name", "String").value)

# CONTROL
def fun_exit(data:DSPD): sys.exit(data["code"].__str__())

# UTILS
def fun_isinstance(data:DSPD):
    types = data["types"].value
    if not data["types"].name == "List": types = [types]
    for type_ in types:
        if data["value"].name not in type_: return BoolValue(False)
    return BoolValue(True)

# OBJECT
def fun_Object__get_(data:DSPD): return data["this"]._dot_get_(DSAPI.check_ret(data, "name", "String").value)
def fun_Object__set_(data:DSPD): return data["this"]._dot_set_(DSAPI.check_ret(data, "name", "String").value, data["value"])
def fun_Object__has_(data:DSPD): return data["this"]._dot_has_(DSAPI.check_ret(data, "name", "String").value)

# LIST
def fun_List_append(data): return NullValue(data["this"].value.append(data["value"]))
def fun_List_reverse(data:DSPD): return ListValue(reversed(data["this"].value))

def fun_List_pop(data:DSPD):
    DSAPI.type_error(data["index"], "Number")
    if data["index"].value > len(data["this"].value): sys.exit(f"IndexError: index is too large")
    return data["this"].value.pop(int(data["index"].value))

def fun_List_insert(data:DSPD):
    DSAPI.type_error(data["index"], "Number")
    if data["index"].value > len(data["this"].value): sys.exit(f"IndexError: index is too large")
    return NullValue(data["this"].value.insert(int(data["index"].value), data["value"]))

def fun_List_remove(data:DSPD):
    for i,thing in enumerate(data["this"].value.copy()):
        if thing.value == data["value"].value:
            data["this"].value.pop(i)
    return NullValue()

def fun_List_extend(data:DSPD):
    old_value = data["this"].value.copy()
    for element in DSAPI.check_ret(data, "list", "List").value: old_value.append(element)
    data["this"].value = old_value
    return data["this"]

# STRING
def fun_String_isdecimal(data:DSPD): return BoolValue(data["this"].value.isdecimal())
def fun_String_isalnum(data:DSPD): return BoolValue(data["this"].value.isalnum())
def fun_String_isalpha(data:DSPD): return BoolValue(data["this"].value.isalpha())
def fun_String_isascii(data:DSPD): return BoolValue(data["this"].value.isascii())
def fun_String_isdigit(data:DSPD): return BoolValue(data["this"].value.isdigit())
def fun_String_islower(data:DSPD): return BoolValue(data["this"].value.islower())
def fun_String_isnumeric(data:DSPD): return BoolValue(data["this"].value.isnumeric())
def fun_String_isidentifier(data:DSPD): return BoolValue(data["this"].value.isidentifier())
def fun_String_isspace(data:DSPD): return BoolValue(data["this"].value.isspace())
def fun_String_istitle(data:DSPD): return BoolValue(data["this"].value.istitle())
def fun_String_isprintable(data:DSPD): return BoolValue(data["this"].value.isprintable())
def fun_String_isupper(data:DSPD): return BoolValue(data["this"].value.isupper())

def fun_String_lower(data:DSPD): return StringValue(data["this"].value.lower())
def fun_String_upper(data:DSPD): return StringValue(data["this"].value.upper())
def fun_String_title(data:DSPD): return StringValue(data["this"].value.title())
def fun_String_capitalize(data:DSPD): return StringValue(data["this"].value.capitalize())
def fun_String_casefold(data:DSPD): return StringValue(data["this"].value.casefold())
def fun_String_swapcase(data:DSPD): return StringValue(data["this"].value.swapcase())

def fun_String_center(data:DSPD): return StringValue(data["this"].value.center(int(DSAPI.check_ret(data,"width","Number").value), DSAPI.check_ret(data, "fillchar", "String").value))
def fun_String_count(data:DSPD): return NumberValue(data["this"].value.count(DSAPI.check_ret(data,"sub","String").value))
def fun_String_startswith(data:DSPD): return BoolValue(data["this"].value.startswith(DSAPI.check_ret(data, "prefix", "String").value))
def fun_String_endswith(data:DSPD): return BoolValue(data["this"].value.endswith(DSAPI.check_ret(data, "suffix", "String").value))
def fun_String_find(data:DSPD): return NumberValue(data["this"].value.find(DSAPI.check_ret(data, "sub", "String").value))
def fun_String_join(data:DSPD): return StringValue(data["this"].value.join([str(element) for element in DSAPI.check_ret(data, "list", "List").value]))
def fun_String_removeprefix(data:DSPD): return StringValue(data["this"].value.removeprefix(DSAPI.check_ret(data,"old","String").value, DSAPI.check_ret(data,"new","String").value))
def fun_String_removesuffix(data:DSPD): return StringValue(data["this"].value.removesuffix(DSAPI.check_ret(data,"old","String").value, DSAPI.check_ret(data,"new","String").value))
def fun_String_replace(data:DSPD): return StringValue(data["this"].value.replace(DSAPI.check_ret(data,"old","String").value, DSAPI.check_ret(data,"new","String").value, int(DSAPI.check_ret(data,"count","Number").value)))
def fun_String_split(data:DSPD): return ListValue([StringValue(element) for element in data["this"].value.split(DSAPI.check_ret(data,"sep","String").value, int(DSAPI.check_ret(data,"maxsplit","Number").value) )])
def fun_String_partition(data:DSPD): return ListValue([StringValue(element) for element in data["this"].value.partition(DSAPI.check_ret(data,"sep","String").value)])
def fun_String_strip(data:DSPD): return StringValue(data["this"].value.strip(DSAPI.check_ret(data,"chars","String").value))
def fun_String_zfill(data:DSPD): return StringValue(data["this"].value.zfill(int(DSAPI.check_ret(data, "width", "Number").value)))

# DICTIONARY
def fun_Dictionary_get(data:DSPD):
    value = data["this"].value.get(data["name"].value, None)
    if value is None: return data["default"]
    return value

def fun_Dictionary_set(data:DSPD): return data["this"]._index_set_(data["name"].value, data["value"])
def fun_Dictionary_has(data:DSPD): return BoolValue(data["name"].value in data["this"].value)
def fun_Dictionary_keys(data:DSPD): return ListValue([StringValue(key) for key in data["this"].value.keys()])
def fun_Dictionary_values(data:DSPD): return ListValue([value for value in data["this"].value.values()])
def fun_Dictionary_items(data:DSPD): return ListValue([[StringValue(item[0]), item[1]] for item in data["this"].value.items()])

def fun_dictionary(data:DSPD):
    obj = data["object"]._copy_()
    for name in list(obj.value.keys()):
        if name in obj.methods: del obj.value[name]
    return Dictionary(obj.value)

def fun_dictionary_fromkeys(data:DSPD): return Dictionary({key.value:data["value"] for key in data["keys"].value})

def fun_dictionary_fromitems(data:DSPD):
    dictionary = Dictionary({})
    for item in data["items"].value:
        dictionary._index_set_(item.value[0], item.value[1])
    return dictionary

class Dictionary(Value):
    name = "Dictionary"
    methods_data = {
        "get": [fun_Dictionary_get, ["name", "default"]],
        "set": [fun_Dictionary_set, ["name", "value"]],
        "has": [fun_Dictionary_has, ["name"]],
        "keys": [fun_Dictionary_keys, []],
        "values": [fun_Dictionary_values, []],
        "items": [fun_Dictionary_items, []]
    }

    def _index_get_(self, name):
        ret_value = self.value.get(name.value, None)
        if ret_value is None:
            sys.exit(f"FieldError: This object has no field '{name}'")
        return ret_value
    
    def _index_set_(self, name, value):
        self.value[name.value] = value
        return value
    
    def __str__(self): return f"{self.value}"

# RANGE
class RangeIterator(Value):
    name = "RangeIterator"

    def __init__(self, start, stop, step):
        super().__init__({"start":int(start), "stop":int(stop), "step":int(step), "cur":int(start)})

    def _iter_(self): return self
    def _to_list_(self): return ListValue([NumberValue(element) for element in range(self.value["start"], self.value["stop"], self.value["step"])])

    def _iter_next_(self):
        if self.value["cur"] + self.value["step"] > self.value["stop"]:
            return Stop()
        value = self.value["cur"]
        self.value["cur"] += self.value["step"]
        return NumberValue(value)
    
def fun_range(data:DSPD):
    return RangeIterator(DSAPI.check_ret(data, "start", "Number").value,
                         DSAPI.check_ret(data, "stop", "Number").value,
                         DSAPI.check_ret(data, "step", "Number").value)

class EnumerateIterator(Value):
    name = "EnumerateIterator"

    def __init__(self, iterator):
        original = iterator._to_list_()
        super().__init__({"original":original, "iterator":original._iter_(), "index":0})

    def _to_list_(self):
        elements = []
        self.value["index"] = 0
        self.value["iterator"] = self.value["original"]._iter_()
        while True:
            val = self._iter_next_()
            if val.name == "Stop": return ListValue(elements)
            elements.append(val)

    def _iter_(self): return self
    def _iter_next_(self):
        value = self.value["iterator"]._iter_next_()
        if value.name == "Stop": return value
        ret_value = ListValue([NumberValue(self.value["index"]), value])
        self.value["index"] += 1
        return ret_value
    
def fun_enumerate(data:DSPD): return EnumerateIterator(data["iterator"])

module = {
    "name": "builtin",
    "variables": {
        "true": BoolValue(True),
        "false": BoolValue(False),
        "null": NullValue(None),
        "dsversion": StringValue("0.1.0"),
    },
    "functions": {
        "print": [fun_print, ["value"]],
        "len": [fun_len, ["value"]],
        "copy": [fun_copy, ["value"]],
        "id": [fun_id, ["value"]],
        "input": [fun_input, ["message"]],
        "typename": [fun_typename, ["value"]],
        "tostring": [fun_tostring, ["value"]],
        "toint": [fun_toint, ["value"]],
        "tofloat": [fun_tofloat, ["value"]],
        "tolist": [fun_tolist, ["value"]],
        "tobool": [fun_tobool, ["value"]],
        "list": [fun_list, []],
        "object": [fun_object, []],
        "isinstance": [fun_isinstance, ["value", "types"]],
        "exit": [fun_exit, ["code"]],
        "range": [fun_range, ["start", "stop", "step"]],
        "enumerate": [fun_enumerate, ["iterator"]],
        "getattr": [fun_getattr, ["value", "name"]],
        "setattr": [fun_getattr, ["value", "name", "v"]],
        "hasattr": [fun_getattr, ["value", "name"]],
        "dictionary": [fun_dictionary, ["object"]],
        "dictionary_fromkeys": [fun_dictionary_fromkeys, ["keys", "value"]],
        "dictionary_fromitems": [fun_dictionary_fromitems, ["items"]],
    },
    "internal-methods":{
        ListValue:{
            "append":[fun_List_append, ["value"]],
            "pop":[fun_List_pop, ["index"]],
            "insert": [fun_List_insert, ["index", "value"]],
            "remove": [fun_List_remove, ["value"]],
            "extend": [fun_List_extend, ["list"]],
            "reverse": [fun_List_reverse, []],
        },
        StringValue: {
            "isdecimal": [fun_String_isdecimal, []],
            "isalnum": [fun_String_isalnum, []],
            "isdigit": [fun_String_isdigit, []],
            "isprintable": [fun_String_isprintable, []],
            "isupper": [fun_String_isupper, []],
            "islower": [fun_String_islower, []],
            "isascii": [fun_String_isascii, []],
            "isidentifier": [fun_String_isidentifier, []],
            "istitle": [fun_String_istitle, []],
            "isnumeric": [fun_String_isnumeric, []],
            "isspace": [fun_String_isspace, []],
            "lower": [fun_String_lower, []],
            "upper": [fun_String_upper, []],
            "title": [fun_String_title, []],
            "capitalize": [fun_String_capitalize, []],
            "swapcase": [fun_String_swapcase, []],
            "casefold": [fun_String_casefold, []],
            "center": [fun_String_center, ["width","fillchar"]],
            "count": [fun_String_count, ["sub"]],
            "startswith": [fun_String_startswith, ["prefix"]],
            "endswidth": [fun_String_endswith, ["suffix"]],
            "find": [fun_String_find, ["sub"]],
            "join": [fun_String_join, ["list"]],
            "removeprefix": [fun_String_removeprefix, ["old","new"]],
            "removesuffix": [fun_String_removesuffix, ["old","new"]],
            "replace": [fun_String_replace, ["old","new","count"]],
            "split": [fun_String_split, ["sep","maxsplit"]],
            "partition": [fun_String_partition, ["sep"]],
            "strip": [fun_String_strip, ["chars"]],
            "zfill": [fun_String_zfill, ["width"]],
        },
        ObjectValue: {
            "_get_":[fun_Object__get_, ["name"]],
            "_set_":[fun_Object__set_, ["name", "value"]],
            "_has_":[fun_Object__has_, ["name"]],
        }
    }
}

DSAPI.add_module(module)