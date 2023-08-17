# the BUILTIN features also uses this API
# the only things in the core language are the literal values (Number, String, List, Object, Function)
# to get api features
from api import *
# User-made features are inside DSAPI class. User must use core features too.

# NOTE: all variables must be of a core "Value" type, like NumberValue etc.
# all functions must return any "Value" type.

# Value objects have a lot of methods
# all methods that interact with the language somehow are surrounded by single "_"
# Value objects have this extra attributes:
#   name: the type name ex. Number
#   value: the python object behind. Number->int,float; String->str, List->list[Value], Object->dict[str,Value]
#   methods_data: data containing method info. it's used to create methods objects bound to the object
#   methods: the methods created from methods_data
#   method_lookup: used by the interpreter to use operators on values. + -> _add_

# DSPD is meant to use as a type hint for functions. it's dict[str, Value]

# FunctionValue are functions defined by the user in damuscript. DSFunctionValue are functions which the code
# operates on the python level without interpreter
# both can be bound to an object, granting the this parameter

# Create custom objects. you should only inherit from the object type, it's the only one that has fields
# field behaviour on non-object types are accessible overriding the _dot_get_ and _dot_set_
def fun_Apple_new(data:DSPD):
    # methods always have an internally passed "this" parameter that is the object attached
    new_apple = data["this"]._copy_() # return a new object with the same fields and methods

    DSAPI.type_error(data["color"], "String", "color") # check the type and error. type_check do not error
    DSAPI.type_error(data["size"], "Number", "size")

    new_apple._dot_set_("color", data["color"]) # _dot_set_ is used for field modification
    # override _index_get/set_ for custom object indexing
    # override _call_ for custom object calling
    # and so on
    new_apple._dot_set_("size", data["size"])
    return new_apple

class AppleObject(ObjectValue):
    name = "Apple(Object)"
    methods_data = {
        "new": [fun_Apple_new, ["color", "size"]]
    }

    def __str__(self):
        # this should return a normal python string. _to_string_ should return a StringValue, but it's done automatically
        return f"My Apple! {self.value['color']}, {self.value['size']}"

# declare the function objects to use in the module dict
def fun_do_stuff(data:DSPD):
    # use the data to retrieve parameters passed by the user like so:
    message:Value = data["message"] # remember this is a "Value" object.
    print(message)
    return NullValue()# always return a "Value" object

# add methods to builtin values
def fun_List_cool_print(data:DSPD):
    string_list = data["this"].__str__()
    # dumb implementation, just for example
    return StringValue(string_list.replace("[","").replace("]",""))

# declare the module data dict
module = {
    "name": "module_name",
    # global variables
    "variables": {
        # use "Value" objects
        "variable_name": NumberValue(5),
    },
    # global functions
    "functions": {
        # name: [function object, parameters]
        "do_stuff": [fun_do_stuff, ["message"]]
    },
    # global objects
    "objects": {
        "Apple": AppleObject({
            "color":NullValue(), # default fields changed when .new is called based on our behaviour
            "size":NullValue(),
        })
    },
    # add internal methods
    "internal-methods":{
        ListValue : { # use the object type, not the name
            "cool_print": [fun_List_cool_print, []]
        }
    }
}

# register the module
# the content will appear after "use module_name" is found
DSAPI.add_module(module)