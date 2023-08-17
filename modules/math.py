from api import *
import math

def fun_round(data:DSPD):
    return NumberValue(round(DSAPI.check_ret(data, "value", "Number").value))

def fun_min(data:DSPD):
    return NumberValue(min([el.value for el in DSAPI.check_ret(data, "valye", "List").value if DSAPI.type_error(el,"Number", "element in value")]))

def fun_max(data:DSPD):
    return NumberValue(max([el.value for el in DSAPI.check_ret(data, "value", "List").value if DSAPI.type_error(el,"Number", "element in value")]))

# VECTOR2
def fun_Vector2_new(data:DSPD):
    new = data["this"]._copy_()
    new._dot_set_("x", DSAPI.check_ret(data, "x", "Number"))
    new._dot_set_("y", DSAPI.check_ret(data, "y", "Number"))
    return new

class Vector2Object(ObjectValue):
    methods_data = {
        "new": [fun_Vector2_new, ["x","y"]]
    }

    def __str__(self):
        return f"Vector2({self.value['x']}; {self.value['y']})"

module = {
    "name": "math",
    "variables":{
        "pi": NumberValue(math.pi),
        "tau": NumberValue(math.tau),
        "e": NumberValue(math.e)
    },
    "objects": {
        "Vector2": Vector2Object({
            "x":NumberValue(0),"y":NumberValue(0),
        })
    },
    "functions": {
        "round": [fun_round, ["value"]],
        "min": [fun_min, ["value"]],
        "max": [fun_max, ["value"]],
    }
}

DSAPI.add_module(module)