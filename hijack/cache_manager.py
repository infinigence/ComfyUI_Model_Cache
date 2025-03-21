
from dataclasses import dataclass, field
from functools import _make_key
from typing import Dict, Tuple
import torch
import logging

logger = logging.getLogger(__name__)

class ModelValidChecker:
    def __init__(self, result):
        self.result = result
        # module dict should be the first place
        self.module = result[0] if isinstance(result, tuple) else result
        self.key_count = self.get_latest_key_count()

    def is_valid(self) -> bool:
        # if tensors on gpu are released, the module keys are incomplete
        if self.key_count == self.get_latest_key_count():
            return True
        return False

    def get_latest_key_count(self) -> int:
        if isinstance(self.module, torch.nn.Module):
            return len(self.module.state_dict().keys())
        elif isinstance(self.module, Dict):
            return len(self.module.keys())

        logger.warning(f"\033[92mModel_Cache: result is not torch.nn.Module or dict, but {type(self.module)}\033[0m")
        logger.warning(f"\033[92mModel_Cache: So cache will never happen for this result! \033[0m")
        # will nevel equal and never cache the result
        return -1
    
    def get_result(self) -> torch.nn.Module | Tuple[torch.nn.Module, ...]:
        return self.result

@dataclass
class ModelCache:
    models: Dict[str, ModelValidChecker] = field(default_factory=dict)

    def generate_cache_key(self, *args, **kwargs):
        args_key = _make_key(args, kwargs, typed=True)
        return args_key
    
    def cached(self, model_key) -> bool:
        checker = self.models.get(model_key, None)
        if checker:
            return checker.is_valid()
        return False
        
    def register_model(
        self,
        model_key: str,
        result: torch.nn.Module | Tuple[torch.nn.Module, ...],
    ) -> None:
        """
        Register an cache model result to be used in Comfy.

        :code:`result` can be either:

        - A :class:`torch.nn.Module` class directly referencing the model.
        - B :A tuple with `torch.nn.Module` Dict at the first place and other kwargs follow-up
        """
        self.models[model_key] = ModelValidChecker(result)
            
    def get_result(self, model_key):
        logger.info(f"\033[92mModel_Cache: Return a cached module result with args:{model_key}\033[0m")
        return self.models[model_key].get_result()
    
_model_cache = ModelCache()

def get_model_cache():
    global _model_cache
    assert _model_cache is not None, "Model Cache has not been initialized."
    return _model_cache

def cache_model(func):
    def wrapper(*args, **kwargs):
        model_key = get_model_cache().generate_cache_key(*args, **kwargs)
        if get_model_cache().cached(model_key):
            return get_model_cache().get_result(model_key)

        result = func(*args, **kwargs)
        get_model_cache().register_model(model_key, result)
        return result
    return wrapper