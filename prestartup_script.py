import torch
import sys
import os
torch._C._cuda_init()
model_cache_custom_path = os.path.join(os.path.dirname(__file__))
sys.path.append(model_cache_custom_path)
from hijack.hijack_list import hijack_all
sys.path.remove(model_cache_custom_path)

hijack_all()