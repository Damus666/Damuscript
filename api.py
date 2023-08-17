from values import *

class DSPD(dict[str, Value]):...

class _DSModule:
    def __init__(self, data_dict, name):
        self.data = data_dict
        self.name = name

    def import_all(self, damuscript):
        if "variables" in self.data:
            for variable_name, variable_value in self.data["variables"].items():
                damuscript.data.write(variable_name, variable_value)
        if "functions" in self.data:
            for function_name, function_data in self.data["functions"].items():
                func = DSFunctionValue(function_name, function_data[0], function_data[1])
                damuscript.data.write(function_name, func)
        if "internal-methods" in self.data:
            for value, methods_data in self.data["internal-methods"].items():
                value.methods_data = methods_data
        if "objects" in self.data:
            for obj_name, obj in self.data["objects"].items():
                damuscript.data.write(obj_name, obj)

class DSAPI:
    modules = {}
    damuscript = None

    @classmethod
    def set_context(cls, damuscript):
        cls.damuscript = damuscript

    @classmethod
    def import_module(cls, name):
        if name not in cls.modules:
            sys.exit(f"ModuleError: No module named '{name}'")
        cls.modules[name].import_all(cls.damuscript)

    @classmethod
    def add_module(cls, data_dict):
        cls.modules[data_dict["name"]] = _DSModule(data_dict, data_dict["name"])

    @staticmethod
    def type_check(value, string_types):
        if not isinstance(string_types, list): string_types = [string_types]
        return value.name in string_types
    
    @staticmethod
    def type_error(value, string_types, name="value"):
        if not isinstance(string_types, list): string_types = [string_types]
        if not value.name in string_types:
            sys.exit(f"TypeError: {name} was expected to be one of the types: {string_types}, got: '{value.name}'")
        return True
    
    @staticmethod
    def check_ret(data, value_name, string_types)->Value:
        if not isinstance(string_types, list): string_types = [string_types]
        if not data[value_name].name in string_types:
            sys.exit(f"TypeError: '{value_name}' was expected to be one of the types: {string_types}, got: '{data[value_name].name}'")
        return data[value_name]
