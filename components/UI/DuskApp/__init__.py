# components/UI/DuskApp/__init__.py
from .core import DuskAppCore
from .build import DuskAppBuildMixin
from .handlers import DuskAppHandlersMixin
from .export import DuskAppExportMixin
from .status import DuskAppStatusMixin

class DuskApp(DuskAppCore,
              DuskAppBuildMixin,
              DuskAppHandlersMixin,
              DuskAppExportMixin,
              DuskAppStatusMixin):
    pass

from components.registry import register
register(__name__, DuskApp)   # __name__ = "components.UI.DuskApp"