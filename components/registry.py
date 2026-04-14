# components/registry.py
_registry = {}

def register(module_name, cls_or_func):
    _registry[module_name] = cls_or_func

def get_component(module_name):
    """Raise ImportError if not registered, to mimic normal import behaviour."""
    if module_name not in _registry:
        raise ImportError(f"Component '{module_name}' not registered")
    return _registry[module_name]

def get_registry():
    return _registry.copy()