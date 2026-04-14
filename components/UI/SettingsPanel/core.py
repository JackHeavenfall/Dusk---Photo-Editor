# core.py
import tkinter as tk
from tkinter import ttk
from components.constants import BG2, BORDER, TEXT_MUTED
from components.LOGIC.default_settings import default_settings

from components.registry import register

from components.UI.DuskButton import DuskButton
from components.UI.DuskSlider import DuskSlider

class SettingsPanel(tk.Frame):
    def __init__(self, parent, on_change, **kw):
        super().__init__(parent, bg=BG2, **kw)
        self._on_change = on_change
        self._vars = {}
        self._build()

    def _var(self, key, val):
        v = tk.DoubleVar(value=val)
        v.trace_add("write", lambda *_: self._on_change())
        self._vars[key] = v
        return v

    def get_settings(self):
        return {k: v.get() for k, v in self._vars.items()}

    # _build, _preset, _reset in separate files

from .build import _build
from .preset_reset import _preset, _reset
SettingsPanel._build = _build
SettingsPanel._preset = _preset
SettingsPanel._reset = _reset

register(__name__, SettingsPanel)