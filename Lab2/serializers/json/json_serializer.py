import codecs
import inspect
import re
from serializers.abstract_serializer.abstract_serializer import Serializer
from converter.converter import extract_global_ops
from types import FunctionType, CodeType, LambdaType


class JsonSerializer(Serializer):
    def dumps(self, obj: object) -> str:

        return self.serialize(obj, 0)

    def dump(self, obj: object, fp: str):

        with open(fp, 'w') as file:
            file.write(self.dumps(obj))

    def serialize_object(self, obj: object, level: int, name="") -> str:
        if name == "":
            result = self.nesting(level) + "{\n"
        else:
            result = self.nesting(level) + f"\"{name}\": {{\n"

        result += self.nesting(level + 1) + f"\"__class__\": \"{obj.__class__.__name__}\""

        objects = [p for p in dir(obj) if not p.startswith('__')]

        if len(objects) != 0:
            result += ",\n"

        for prop in objects:
            result += self.serialize(getattr(obj, prop), level + 1, prop)

            if prop == list(objects)[-1]:
                result += "\n"
            else:
                result += ",\n"

        result += self.nesting(level) + "}"

        return result

    def serialize_list(self, objects: list or set or tuple, level: int, name="") -> str:
        if name == "":
            result = self.nesting(level) + "[\n"
        else:
            result = self.nesting(level) + f"\"{name}\": [\n"

        if isinstance(objects, list):
            result += self.nesting(level) + "\"__list__\""
        elif isinstance(objects, tuple):
            result += self.nesting(level) + "\"__tuple__\""
        elif isinstance(objects, set):
            result += self.nesting(level) + "\"__set__\""

        if len(objects) != 0:
            result += ",\n"

        for index, obj in enumerate(objects):
            result += self.serialize(obj, level + 1)

            if index == len(objects) - 1:
                result += "\n"
            else:
                result += ",\n"

        result += self.nesting(level) + "]"

        return result

    def serialize_dict(self, obj: dict, level: int, name="") -> str:
        if name == "":
            result = self.nesting(level) + "{\n"
        else:
            result = self.nesting(level) + f"\"{name}\": {{\n"

        for prop, value in obj.items():
            result += self.serialize(value, level + 1, prop)

            if prop == list(obj.keys())[-1]:
                result += "\n"
            else:
                result += ",\n"

        result += self.nesting(level) + "}"

        return result

    def serialize_property(self, obj: object, level: int, name="") -> str:
        if name == "":
            return self.nesting(level) + f"{self.convert_to_string(obj)}"
        else:
            return self.nesting(level) + f"\"{name}\": {self.convert_to_string(obj)}"

    def serialize_func(self, obj, level: int, name="") -> str:
        if name == "":
            result = self.nesting(level) + "{\n"
        else:
            result = self.nesting(level) + f"\"{name}\": {{\n"

        result += self.nesting(level + 1) + f"\"__func__\": \"{obj.__name__}\",\n"

        f_globals_ref = {obj.__code__.co_names[arg] for arg in extract_global_ops(obj.__code__)}
        f_globals = {key: obj.__globals__[key] for key in f_globals_ref if key in obj.__globals__}

        for c in obj.__code__.__dir__():
            if c.startswith("co_"):
                attr = getattr(obj.__code__, c)
                if isinstance(attr, bytes):
                    attr = codecs.decode(attr, 'raw_unicode_escape')
                result += self.serialize(attr, level + 1, c) + ",\n"

        result += self.nesting(level + 1) + f"\"globals\": {self.serialize(f_globals, level + 1)}\n"
        result += self.nesting(level) + "}"
        return result

    def serialize_class(self, obj, level: int, name="") -> str:
        if name == "":
            result = self.nesting(level) + "{\n"
        else:
            result = self.nesting(level) + f"\"{name}\": {{\n"

        result += self.nesting(level + 1) + f"\"__class_name__\": \"{obj.__name__}\""

        objects = [p for p in dir(obj) if not p.startswith('__')]

        if len(objects) != 0:
            result += ",\n"

        for prop in objects:
            result += self.serialize(getattr(obj, prop), level + 1, prop)

            if prop == list(objects)[-1]:
                result += "\n"
            else:
                result += ",\n"

        result += self.nesting(level) + "}"

        return result

    def serialize(self, obj, level: int, name="") -> str:
        if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, LambdaType):
            return self.serialize_func(obj, level, name)
        elif inspect.isclass(obj):
            return self.serialize_class(obj, level, name)
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            return self.serialize_list(obj, level, name)
        elif isinstance(obj, dict):
            return self.serialize_dict(obj, level, name)
        elif hasattr(obj, '__dict__'):
            return self.serialize_object(obj, level, name)
        else:
            return self.serialize_property(obj, level, name)

    @staticmethod
    def nesting(level: int) -> str:
        result = ""
        for i in range(level):
            result += "\t"
        return result

    @staticmethod
    def convert_to_string(obj: object) -> str:
        if isinstance(obj, str):
            return f"\"{obj}\""
        elif isinstance(obj, bool):
            return "true" if obj else "false"
        elif obj is None:
            return "null"
        elif obj == float("nan"):
            return "NaN"
        elif obj == float("inf") or obj == float("+inf"):
            return "Infinity"
        elif obj == float("-inf"):
            return "-Infinity"
        else:
            return str(obj)

    def loads(self, data: str):
        data = data.replace('\t', '').replace('\n', '')

        return self.parse(data, 0)[0]

    def load(self, fp: str):
        with open(fp, "r") as file:
            return self.loads(file.read())

    def parse_object(self, data: str, pos: int) -> tuple:
        obj_dict, pos = self.parse_dict(data, pos)

        cls = type(obj_dict["__class__"], (), {})
        result = cls()

        for key, value in obj_dict.items():
            if key != "__class__":
                setattr(result, key, value)

        return result, pos

    def parse_class(self, data: str, pos: int) -> tuple:
        class_dict, pos = self.parse_dict(data, pos)

        cls = type(class_dict["__class_name__"], (), {})

        for key, value in class_dict.items():
            if key != "__class__":
                setattr(cls, key, value)

        return cls, pos

    def parse_dict(self, data: str, pos: int) -> tuple:
        result = {}
        pos += 1

        while data[pos] != '}':
            key, pos = self.parse_string(data, pos)
            pos += 2
            value, pos = self.parse(data, pos)
            result[key] = value

            if data[pos] == ',':
                pos += 1
                self.validate(data[pos], data[pos] != '}')
            else:
                self.validate(data[pos], data[pos] == '}')

        return result, pos + 1

    def parse_list(self, data: str, pos: int) -> tuple:
        self.validate(data[pos], data[pos] == '[')

        pos += 1
        result = []
        temp = ""

        while data[pos] != ']':
            value, pos = self.parse(data, pos)

            if value != "__list__" and value != "__tuple__" and value != "__set__":
                result.append(value)
            else:
                temp = value

            if data[pos] == ',':
                pos += 1
                self.validate(data[pos], data[pos] != ']')
            else:
                self.validate(data[pos], data[pos] == ']')

        if temp == "__tuple__":
            result = tuple(result)
        elif temp == "__set__":
            result = set(result)

        return result, pos + 1

    def parse_string(self, data: str, pos: int) -> tuple:
        self.validate(data[pos], data[pos] == '"')

        pos += 1
        pos_start = pos

        while data[pos] != '"':
            pos += 1

        return data[pos_start:pos], pos + 1

    def parse_null(self, data: str, pos: int) -> tuple:
        self.validate(data[pos:pos + 4], data[pos:pos + 4] == "null")
        return None, pos + 4

    def parse_true(self, data: str, pos: int) -> tuple:
        self.validate(data[pos:pos + 4], data[pos:pos + 4] == "true")
        return True, pos + 4

    def parse_false(self, data: str, pos: int) -> tuple:
        self.validate(data[pos:pos + 5], data[pos:pos + 5] == "false")
        return False, pos + 5

    def parse_number(self, data: str, pos: int) -> tuple:
        self.validate(data[pos], data[pos] in "-IN" or '0' <= data[pos] <= '9')

        if data[pos] == 'N':
            self.validate(data[pos:pos + 3], data[pos:pos + 3] == "NaN")
            return float("nan"), pos + 3
        elif data[pos] == 'I':
            self.validate(data[pos:pos + 8], data[pos:pos + 8] == "Infinity")
            return float("inf"), pos + 8
        elif data[pos] == '-' and data[pos] == 'I':
            self.validate(data[pos:pos + 9], data[pos:pos + 9] == "-Infinity")
            return float("-inf"), pos + 9

        regex_find = re.findall("-?(?:0|[1-9]\\d*)(?:\\.\\d+)?(?:[eE][+-]?\\d+)?", data[pos:])

        if not regex_find:
            raise JsonValidationError(data[pos:])
        try:
            return int(regex_find[0]), pos + len(regex_find[0])
        except ValueError:
            return float(regex_find[0]), pos + len(regex_find[0])

    def parse_func(self, data: str, pos: int) -> tuple:
        func_dict, pos = self.parse_dict(data, pos)

        co = CodeType(func_dict["co_argcount"], func_dict["co_posonlyargcount"],
                      func_dict["co_kwonlyargcount"], func_dict["co_nlocals"],
                      func_dict["co_stacksize"], func_dict["co_flags"],
                      codecs.encode(func_dict["co_code"], 'raw_unicode_escape'), func_dict["co_consts"],
                      func_dict["co_names"], func_dict["co_varnames"],
                      func_dict["co_filename"], func_dict["co_name"],
                      func_dict["co_firstlineno"], codecs.encode(func_dict["co_lnotab"], 'raw_unicode_escape'),
                      func_dict["co_freevars"], func_dict["co_cellvars"])

        func_dict["globals"]["__builtins__"] = __builtins__
        f = FunctionType(co, func_dict["globals"], func_dict["co_name"])

        return f, pos

    def parse(self, data: str, pos: int) -> tuple:
        if data[pos] == "<":
            return self.parse_func(data, pos)
        elif data[pos] == '"':
            return self.parse_string(data, pos)
        elif data[pos] == 'n':
            return self.parse_null(data, pos)
        elif data[pos] == 't':
            return self.parse_true(data, pos)
        elif data[pos] == 'f':
            return self.parse_false(data, pos)
        elif data[pos:pos + 17] == "{\"__class_name__\"":
            return self.parse_class(data, pos)
        elif data[pos:pos + 12] == "{\"__class__\"":
            return self.parse_object(data, pos)
        elif data[pos:pos + 11] == "{\"__func__\"":
            return self.parse_func(data, pos)
        elif data[pos] == "{":
            return self.parse_dict(data, pos)
        elif data[pos] == '[':
            return self.parse_list(data, pos)
        else:
            return self.parse_number(data, pos)

    @staticmethod
    def validate(value, condition: bool):
        if not condition:
            raise JsonValidationError(value)


class JsonValidationError(Exception):
    def __init__(self, value):
        self.value = value
        super().__init__(f"Unexpected json value: {value}")
