# __init__.py - Export the fully assembled ImportPanel class
from .core import ImportPanel
from .add_buttons import extend_add_buttons
from .drop_target import extend_drop_target
from .queue_management import extend_queue_management
from .card_rendering import extend_card_rendering
from .thumb_loading import extend_thumb_loading

# Attach all method groups to the class
extend_add_buttons(ImportPanel)
extend_drop_target(ImportPanel)
extend_queue_management(ImportPanel)
extend_card_rendering(ImportPanel)
extend_thumb_loading(ImportPanel)

from components.registry import register
register(__name__, ImportPanel)   # __name__ = "components.UI.ImportPanel"

__all__ = ["ImportPanel"]