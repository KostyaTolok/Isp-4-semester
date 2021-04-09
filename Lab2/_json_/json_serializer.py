import inspect
import re
from abstract_serializer.abstract_serializer import Serializer
from converter import walk_global_ops, extract_code_globals
from types import FunctionType


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

        result += self.nesting(level + 1) + f"\"class\": \"{obj.__class__.__name__}\""

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
        source = inspect.getsource(obj).strip()

        f_globals_ref = extract_code_globals(obj.__code__)
        f_globals = {k: obj.__globals__[k] for k in f_globals_ref if k in obj.__globals__}

        source = source.replace("\"", "\\\"").replace("\n", '')
        result += self.nesting(level + 1) + f"\"source\": {self.serialize(source, level + 1)},\n"
        result += self.nesting(level + 1) + f"\"globals\": {self.serialize(f_globals, level + 1)}\n"
        result += self.nesting(level) + "}"
        return result

    def serialize_class(self, obj, level: int, name="") -> str:
        if name == "":
            result = self.nesting(level) + "{\n"
        else:
            result = self.nesting(level) + f"\"{name}\": {{\n"

        result += self.nesting(level + 1) + f"\"__name__\": \"{obj.__name__}\",\n"
        source = inspect.getsource(obj).strip()

        source = source.replace("\"", "\\\"").replace("\n", '')
        result += self.nesting(level + 1) + f"\"source\": {self.serialize(source, level + 1)}\n"
        result += self.nesting(level) + "}"
        return result

    def serialize(self, obj: object, level: int, name="") -> str:
        if inspect.ismethod(obj) or inspect.isfunction(obj):
            return self.serialize_func(obj, level, name)
        elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
            return self.serialize_list(obj, level, name)
        elif isinstance(obj, dict):
            return self.serialize_dict(obj, level, name)
        elif isinstance(obj, type):
            return self.serialize_class(obj, level, name)
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
        pos += 1
        self.validate(data[pos:pos + 9], data[pos:pos + 9] == "\"class\": ")
        pos += 10
        class_name_end = data.index("\"", pos)

        cls = type(data[pos:class_name_end], (), {})
        result = cls()

        pos = class_name_end + 2

        while data[pos] != '}':
            key, pos = self.parse_string(data, pos)
            pos += 2
            value, pos = self.parse(data, pos)

            if key != "__class__":
                setattr(result, key, value)

            if data[pos] == ',':
                pos += 1
                self.validate(data[pos], data[pos] != '}')
            else:
                self.validate(data[pos], data[pos] == '}')

        return result, pos + 1

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
        temp_len = len('"__func__": ')
        self.validate(data[pos + 1:pos + temp_len + 1], data[pos + 1:pos + temp_len + 1] == '"__func__": ')
        pos += temp_len + 2
        name_ind = data.index('"', pos)
        pos = name_ind + 2
        temp_len = len('"source": ')
        self.validate(data[pos:pos + temp_len], data[pos:pos + temp_len] == '"source": ')
        pos += temp_len + 1
        pos_start = pos

        while data[pos] != '"':
            if data[pos] == '\\':
                pos += 2
            else:
                pos += 1

        code = data[pos_start:pos].replace("\\\"", '"')

        co = compile(code, '<string>', "exec")
        co = co.co_consts[0]
        pos += 2
        temp_len = len('"globals": ')
        self.validate(data[pos:pos + temp_len], data[pos:pos + temp_len] == '"globals": ')
        pos += temp_len
        gl, pos = self.parse(data, pos)
        gl["__builtins__"] = __builtins__
        func = FunctionType(co, gl)

        return func, pos + 1

    def parse_class(self, data: str, pos: int) -> tuple:
        self.validate(data[pos + 1:pos + 13], data[pos + 1:pos + 13] == '"__name__": ')
        pos += 14
        name_ind = data.index('"', pos)
        pos = name_ind + 2
        self.validate(data[pos:pos + 10], data[pos:pos + 10] == "\"source\": ")
        pos += 11
        pos_start = pos
        classes = {}
        while data[pos] != '"':
            if data[pos] == '\\':
                pos += 2
            else:
                pos += 1

        code = data[pos_start:pos].replace("\\\"", '"')
        exec(code, classes)

        return classes, pos + 1

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
        elif data[pos:pos + 8] == "{\"class\"":
            return self.parse_object(data, pos)
        elif data[pos:pos + 11] == "{\"__func__\"":
            return self.parse_func(data, pos)
        elif data[pos:pos + 11] == "{\"__name__\"":
            return self.parse_class(data, pos)
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
