# Image Processing Pipeline

The core function `process_image(img, settings)` in `components/LOGIC/image_processing.py` applies all edits in a fixed, deterministic order.

## Pipeline Steps (in order)

1. **Convert to RGB** – ensures a consistent colour space (discards alpha, converts palette images).
2. **Crop** – percentages from top, bottom, left, right. Crops only if the resulting rectangle has positive size.
3. **Smooth (Gaussian blur)** – if `smooth > 0`, blends the original with a blurred version. `smooth_radius` controls kernel size.
4. **Brightness, Contrast, Saturation, Sharpness** – using PIL’s `ImageEnhance` classes. Values are percentages (100 = no change).
5. **Vignette** – darkens edges using a radial gradient. Intensity controlled by `vignette`; higher values produce a smaller bright centre.
6. **Grain** – adds Gaussian noise. The standard deviation scales with `grain`.
7. **Tone (warm/cool)** – positive values increase red and decrease blue (warmer); negative values increase blue and decrease red (cooler).

## Settings Ranges and Defaults

See `components/LOGIC/default_settings.py`. All sliders are percentages except:
- `smooth_radius`: 1–8 (integer)
- `tone`: -100 (cool) to +100 (warm)

## Performance Characteristics

- Processing a 12 MP image takes <0.1 s on a modern CPU (mostly NumPy operations).
- Batch export processes images sequentially; memory usage is one image at a time.
- The preview uses a debounced timer (200 ms) to avoid recomputing on every slider tick.

## Why NumPy?

- Vignette, grain, and tone require per‑pixel arithmetic that would be extremely slow in pure Python.
- PIL’s built‑in filters do not provide these effects with the required flexibility.
- NumPy vectorisation makes them fast enough for real‑time preview.

## Edge Cases

- If crop percentages result in zero or negative width/height, cropping is skipped.
- If `smooth_radius` is 0, the filter is not applied (radius forced to at least 1).
- All NumPy operations are clipped to [0,255] to avoid overflow.