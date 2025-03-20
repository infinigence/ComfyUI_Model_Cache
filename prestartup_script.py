import torch
import sys
import os
torch._C._cuda_init()
infinigence_path = os.path.join(os.path.dirname(__file__))
sys.path.append(infinigence_path)
from hijack.utils import hijack_func
from hijack.hijack_list import load_torch_file_cache_model
from comfy.utils import load_torch_file
sys.path.remove(infinigence_path)

hijack_func(load_torch_file, load_torch_file_cache_model)