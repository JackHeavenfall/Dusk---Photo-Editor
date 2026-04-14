# __init__.py
from .core import ExportDialog
from components.registry import register
register(__name__, ExportDialog)   # __name__ = "components.UI.ExportDialog"