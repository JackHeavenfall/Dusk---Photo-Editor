# __init__.py
from .core import LogViewer
from components.registry import register
register(__name__, LogViewer)   # __name__ = "components.UI.LogViewer"