# preset_reset.py
from components.LOGIC.default_settings import default_settings
from components.LOGIC.logging_setup import log

def _preset(self, vals, name):
    for k, v in vals.items():
        if k in self._vars:
            self._vars[k].set(v)
    log(f"Preset: {name}")

def _reset(self):
    d = default_settings()
    for k, v in self._vars.items():
        if k in d:
            v.set(d[k])
    log("Settings reset")