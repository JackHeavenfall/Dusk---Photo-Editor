# components/__init__.py
# Import all subpackages to trigger auto‑registration.

from . import constants
from . import registry

# Import UI and LOGIC packages so their register() calls run.
from . import UI
from . import LOGIC

# Optional: import operations
from . import operations