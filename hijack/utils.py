import importlib
import inspect
from types import FunctionType
from typing import Callable, Union


always_true_func = lambda *args, **kwargs: True

def singleton(cls):
    instances = {}
    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return wrapper

class CondFunc:
    def __new__(cls, orig_func, sub_func, cond_func=always_true_func):
        self = super(CondFunc, cls).__new__(cls)
        if isinstance(orig_func, str):
            func_path = orig_func.split('.')
            for i in range(len(func_path)-1, -1, -1):
                try:
                    resolved_obj = importlib.import_module('.'.join(func_path[:i]))
                    break
                except ImportError:
                    pass
            try:
                for attr_name in func_path[i:-1]:
                    resolved_obj = getattr(resolved_obj, attr_name)
                orig_func = getattr(resolved_obj, func_path[-1])
                setattr(resolved_obj, func_path[-1], lambda *args, **kwargs: self(*args, **kwargs))
            except AttributeError:
                print(f"Warning: Failed to resolve {orig_func} for CondFunc hijack")
                pass
        self.__init__(orig_func, sub_func, cond_func)
        return lambda *args, **kwargs: self(*args, **kwargs)

    def __init__(self, orig_func, sub_func, cond_func):
        self.__orig_func = orig_func
        self.__sub_func = sub_func
        self.__cond_func = cond_func

    def __call__(self, *args, **kwargs):
        if not self.__cond_func or self.__cond_func(self.__orig_func, *args, **kwargs):
            return self.__sub_func(self.__orig_func, *args, **kwargs)
        else:
            return self.__orig_func(*args, **kwargs)

def get_func_full_name(func: FunctionType):
    module = inspect.getmodule(func)
    if module is None:
        raise ValueError(f"Cannot get module of function {func}")
    return f"{module.__name__}.{func.__qualname__}"

def hijack_func(
    orig_func: Union[str, Callable],
    sub_func: Callable,
):
    if isinstance(orig_func, FunctionType):
        orig_func = get_func_full_name(orig_func)
    else:
        raise ValueError(f"origin function is not function type")
    return CondFunc(orig_func, sub_func)

def hijack_class_func(
    orig_class,
    orig_class_func: str,
    sub_func: Callable,
):
    try:
        func = getattr(orig_class, orig_class_func)
    except:
        raise ValueError(f"{orig_class} has no function named:{orig_class_func}")
    module = inspect.getmodule(orig_class)
    orig_class_name = module.__name__ + "." + orig_class.__name__
    orig_func_name = orig_class_name + "." + orig_class_func
    return CondFunc(orig_func_name, sub_func)
