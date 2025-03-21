from .cache_manager import cache_model

@cache_model
def load_torch_file_cache_model(origin_func, *args, **kwargs):
    return origin_func(*args, **kwargs)

@cache_model
def hijack_from_pretrained(origin_func, *args, **kwargs):
    return origin_func(*args, **kwargs)