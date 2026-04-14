# __init__.py
from .core import PreviewPanel
from components.registry import register
register(__name__, PreviewPanel)   # __name__ = "components.UI.PreviewPanel"