import inspect
import dis
import opcode
from types import FunctionType, LambdaType, CodeType
import codecs

STORE_GLOBAL = opcode.opmap['STORE_GLOBAL']
DELETE_GLOBAL = opcode.opmap['DELETE_GLOBAL']
LOAD_GLOBAL = opcode.opmap['LOAD_GLOBAL']
GLOBAL_OPS = (STORE_GLOBAL, DELETE_GLOBAL, LOAD_GLOBAL)


def object_to_dict(obj: object) -> dict:
    result = {"__class__": obj.__class__.__name__}
    props = [p for p in dir(obj) if not p.startswith('__')]
    for p in props:
        value = getattr(obj, p)
        result[p] = to_dict(value)
    return result


def list_to_dict(objects: list or tuple or set):
    result = []
    if isinstance(objects, list):
        result.append("__list__")
    elif isinstance(objects, tuple):
        result.append("__tuple__")
    elif isinstance(objects, set):
        result.append("__set__")
    for o in objects:
        if o is None:
            result.append("None")
            continue
        result.append(to_dict(o))
    return result


def dict_to_dict(obj: dict):
    result = {}
    for key, value in obj.items():
        result[key] = to_dict(value)
    return result


def func_to_dict(obj):
    result = {"__func__": obj.__name__}
    globals_keys = {obj.__code__.co_names[arg] for arg in extract_global_ops(obj.__code__)}
    f_globals = {key: obj.__globals__[key] for key in globals_keys if key in obj.__globals__}
    for c in obj.__code__.__dir__():
        if c.startswith("co_"):
            attr = getattr(obj.__code__, c)
            if isinstance(attr, bytes):
                attr = codecs.decode(attr, 'unicode_escape')
            result[c] = to_dict(attr)
    result["globals"] = f_globals
    return result


def extract_global_ops(code):
    for instr in dis.get_instructions(code):
        if instr.opcode in GLOBAL_OPS:
            yield instr.arg


def class_to_dict(obj: object) -> dict:
    result = {"__class_name__": obj.__name__}
    props = [p for p in dir(obj) if not p.startswith('__')]
    for p in props:
        value = getattr(obj, p)
        result[p] = to_dict(value)
    return result


def to_dict(obj: object):
    if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, LambdaType):
        return func_to_dict(obj)
    if inspect.isclass(obj):
        return class_to_dict(obj)
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        return list_to_dict(obj)
    elif isinstance(obj, dict):
        return dict_to_dict(obj)
    elif hasattr(obj, '__dict__'):
        return object_to_dict(obj)
    else:
        return obj


def obj_from_dict(obj: dict):
    cls = type(obj.get("__class__"), (), {})

    result = cls()

    for key, value in obj.items():
        if key == '__class__':
            continue
        setattr(result, key, from_dict(value))

    return result


def list_from_dict(obj: list or tuple or set):
    result = []

    for o in obj:
        if o == "__list__" or o == "__tuple__" or o == "__set__":
            continue
        if o == "None":
            result.append(None)
            continue
        result.append(from_dict(o))

    if obj[0] == "__tuple__":
        result = tuple(result)
    elif obj[0] == "__set__":
        result = set(result)

    return result


def dict_from_dict(obj: dict):
    result = {}

    for key, value in obj.items():
        result[key] = from_dict(value)

    return result


def class_from_dict(obj: dict):
    cls = type(obj.get("__class_name__"), (), {})

    for key, value in obj.items():
        if key == '__class__':
            continue
        setattr(cls, key, from_dict(value))

    return cls


def from_dict(obj):
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        return list_from_dict(obj)
    elif isinstance(obj, dict):
        if '__class__' in obj.keys():
            return obj_from_dict(obj)
        elif '__class_name__' in obj.keys():
            return class_from_dict(obj)
        elif '__func__' in obj.keys():
            return func_from_dict(obj)
        else:
            return dict_from_dict(obj)
    else:
        return obj


def func_from_dict(data):
    co = CodeType(data["co_argcount"], data["co_posonlyargcount"],
                  data["co_kwonlyargcount"], data["co_nlocals"],
                  data["co_stacksize"], data["co_flags"],
                  codecs.encode(data["co_code"], encoding="raw_unicode_escape"), from_dict(data["co_consts"]),
                  from_dict(data["co_names"]), from_dict(data["co_varnames"]),
                  data["co_filename"], data["co_name"],
                  data["co_firstlineno"], codecs.encode(data["co_lnotab"], encoding="raw_unicode_escape"),
                  from_dict(data["co_freevars"]), from_dict(data["co_cellvars"]))
    data["globals"]["__builtins__"] = __builtins__
    f = FunctionType(co, data["globals"], data["co_name"])
    return f
