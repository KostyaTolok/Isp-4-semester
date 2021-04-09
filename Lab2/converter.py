import inspect
import dis
import opcode
from types import FunctionType, LambdaType

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
        result.append(to_dict(o))
    return result


def dict_to_dict(obj: dict):
    result = {}
    for key, value in obj.items():
        result[key] = to_dict(value)
    return result


def class_to_dict(obj: type):
    result = {"__name__": obj.__name__, "source": inspect.getsource(obj).replace("\"", "\\\"")}
    return result


def func_to_dict(obj):
    result = {"__func__": obj.__name__}
    f_globals_ref = extract_code_globals(obj.__code__)
    f_globals = {k: obj.__globals__[k] for k in f_globals_ref if k in obj.__globals__}
    source = inspect.getsource(obj).strip()
    result["source"] = source.replace('"', "\\\"").replace("\n", '')
    result["globals"] = f_globals
    return result


def extract_code_globals(co):
    names = co.co_names
    out_names = {names[arg] for _, arg in walk_global_ops(co)}
    return out_names


def walk_global_ops(code):
    for instr in dis.get_instructions(code):
        if instr.opcode in GLOBAL_OPS:
            yield instr.opcode, instr.arg


def to_dict(obj: object):
    if inspect.ismethod(obj) or inspect.isfunction(obj) or isinstance(obj, LambdaType):
        return func_to_dict(obj)
    elif isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        return list_to_dict(obj)
    elif isinstance(obj, dict):
        return dict_to_dict(obj)
    elif isinstance(obj, type):
        return class_to_dict(obj)
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


def from_dict(obj):
    if isinstance(obj, list) or isinstance(obj, tuple) or isinstance(obj, set):
        return list_from_dict(obj)
    elif isinstance(obj, dict):
        if '__class__' in obj.keys():
            return obj_from_dict(obj)
        elif '__func__' in obj.keys():
            return func_from_dict(obj)
        elif '__name__' and 'source' in obj.keys():
            return class_from_dict(obj)
        else:
            return dict_from_dict(obj)
    else:
        return obj


def class_from_dict(obj: dict):
    classes = {}
    exec(obj["source"].replace("\\\"", '"'), classes)
    return classes[obj["__name__"]]


def func_from_dict(data):
    co = compile(data["source"].replace("\\\"", '"'), '<string>', "exec")
    co = co.co_consts[0]
    data["globals"]["__builtins__"] = __builtins__
    f = FunctionType(co, data["globals"])
    return f

