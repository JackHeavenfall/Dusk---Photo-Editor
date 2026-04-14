# Settings Panel

The `SettingsPanel` (in `components/UI/SettingsPanel/`) contains all adjustment sliders and preset buttons.

## Files

- `core.py` – class definition, `__init__`, `_var()`, `get_settings()`.
- `build.py` – `_build()` – creates the scrollable frame, sections, sliders, and presets.
- `preset_reset.py` – `_preset()` and `_reset()`.

## Slider Management

- Each slider has a `tk.DoubleVar` stored in `self._vars[key]`.
- When a variable is written, it calls `self._on_change()` (callback provided by `DuskApp`).
- `get_settings()` returns a dictionary mapping key → current value.

## Presets

Four built‑in presets:

- **dusk** – warm, slightly desaturated, vignette, grain.
- **noir** – high contrast, low saturation, strong vignette.
- **golden** – bright, warm, saturated.
- **raw** – neutral (brightness=100, contrast=100, saturation=100, vignette=0, grain=0, tone=0).

Preset buttons apply only the settings they override; other settings remain unchanged.

## Reset

`_reset()` restores all sliders to the default values from `default_settings()`.