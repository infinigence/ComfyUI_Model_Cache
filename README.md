# ComfyUI_Model_Cache
A model cached-loader custom node for ComfyUI. Recommended Comfy version: v0.3.26.

# How does it work?
Some custom nodes call comfy.utils.load_torch_file whey they are executed. However, it is waste of time for these frequently executed workflows. Here is a easy implementation for ComfyUI to cache torch file and avoid from duplicated loading torch files. By Using symbols hijack, many functions that read disk freqently can be cached in host memory. So when they are called next time, it will take no time. In order to trap tensor status after user clicks **`Clear Execution Cache`**(After user clicks that button, the tensors on gpu will be released and the caches are dirty), I add decorator "cache_model" to get the tensor status. If the tensors are released, they will load them again instead of use the dirty cache. **As a reminder, this behavior will also take up some VRAM. This is the way to use VRAM to increase efficiency.**

# How to install?
This node has been registed to [Comfy Registry](https://registry.comfy.org/). If you have installed comfy manager, you can use command below:
```bash
python3 $CUSTOM_MANAGER_CLI/cm-cli.py install ComfyUI_Model_Cache
# or
python3 $CUSTOM_MANAGER_CLI/cm-cli.py install https://github.com/infinigence/ComfyUI_Model_Cache.git
```
Or you can use comfy-cli:
```bash
pip install comfy-cli
comfy node registry-install ComfyUI_Model_Cache
```
If you don't, you can easily use this custom node by moving the whole project to `ComfyUI/custom_nodes`.

# Examples
In `test/` directory, there are some sample workflows. They demonstrate the acceleration for some custom nodes.