# Component Registry System

The registry (`components/registry.py`) is a simple dictionary that stores component classes by their module name. It enables automatic discovery without manual imports.

## How It Works

1. Each component file (or its `__init__.py`) calls `register(__name__, ClassName)` at the end.
2. The top‑level `components/__init__.py` imports all sub‑packages, which triggers every registration.
3. Other parts of the program retrieve components using `get_component("full.module.name")`.

## Why Self‑Registration?

- **No central import list** – adding a new component does not require editing existing files.
- **Enforces fragmentation** – because each file registers itself, you must keep files small and focused.
- **Acts as a service locator** – useful for optional or plugin‑like features.

## Rules for Using the Registry

- **Use normal imports** for dependencies inside the same package (e.g., `from .DuskButton import DuskButton`).
- **Use `get_component()`** only when the dependency is in a different branch of the component tree (e.g., a UI component needing a logic module – though logic modules are usually imported directly).
- **Never call `get_component()` at module level** if it creates a circular import; call it inside a function or method instead.

## Registry API

```python
def register(module_name, cls_or_func):
    """Store a component."""
    
def get_component(module_name):
    """Retrieve a component. Raises ImportError if not found."""
    
def get_registry():
    """Return a copy of the entire registry (for debugging)."""

```

## Example Registration
### components/UI/DuskButton.py
```python
class DuskButton(tk.Label):
    ...
from components.registry import register
register(__name__, DuskButton)   # __name__ = "components.UI.DuskButton"

```

## Initialisation Flow

`main.py` does:
```python
import components # triggers all registrations
DuskApp = get_component("components.UI.DuskApp")

```

At that point, every component is already registered.