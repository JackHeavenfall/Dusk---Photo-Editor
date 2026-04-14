# __init__.py
from .core import SettingsPanel
from components.registry import register
register(__name__, SettingsPanel)   # __name__ = "components.UI.SettingsPanel"