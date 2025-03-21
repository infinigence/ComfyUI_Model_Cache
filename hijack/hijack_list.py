from .cache_manager import cache_model
from .utils import hijack_func, hijack_class_func

from comfy.utils import load_torch_file
from transformers import AutoModel

@cache_model
def load_torch_file_cache_model(origin_func, *args, **kwargs):
    return origin_func(*args, **kwargs)

@cache_model
def hijack_from_pretrained(origin_func, *args, **kwargs):
    return origin_func(*args, **kwargs)

HIJACK_FUNC_MAP = {
    load_torch_file: load_torch_file_cache_model,
}

HIJACK_CLASS_FUNC_MAP = {
    AutoModel: ("from_pretrained", hijack_from_pretrained),
}

def hijack_all():
    for origin_func in HIJACK_FUNC_MAP:
        hijack_func(origin_func, HIJACK_FUNC_MAP[origin_func])

    for origin_class in HIJACK_CLASS_FUNC_MAP:
        hijack_class_func(origin_class, *HIJACK_CLASS_FUNC_MAP[origin_class])

