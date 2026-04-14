# components/LOGIC/image_processing.py
import numpy as np
from PIL import Image, ImageFilter, ImageEnhance

def process_image(img, settings):
    img = img.convert("RGB")
    w, h = img.size

    top    = settings["crop_top"]    / 100
    bottom = settings["crop_bottom"] / 100
    left   = settings["crop_left"]   / 100
    right  = settings["crop_right"]  / 100
    x1, y1 = int(w * left),        int(h * top)
    x2, y2 = int(w * (1 - right)), int(h * (1 - bottom))
    if x2 > x1 and y2 > y1:
        img = img.crop((x1, y1, x2, y2))

    if settings["smooth"] > 0:
        r = max(1, int(settings["smooth_radius"]))
        img = Image.blend(img, img.filter(ImageFilter.GaussianBlur(r)),
                          alpha=settings["smooth"] / 100)

    img = ImageEnhance.Brightness(img).enhance(settings["brightness"] / 100)
    img = ImageEnhance.Contrast(img).enhance(settings["contrast"]    / 100)
    img = ImageEnhance.Color(img).enhance(settings["saturation"]     / 100)
    img = ImageEnhance.Sharpness(img).enhance(settings["sharpness"]  / 100)

    v = settings["vignette"] / 100
    if v > 0:
        a = np.array(img).astype(float)
        rows, cols = a.shape[:2]
        sigma = max(0.05, 1.2 - v * 0.6)
        Xg, Yg = np.meshgrid(np.linspace(-1, 1, cols), np.linspace(-1, 1, rows))
        vig = np.exp(-((Xg**2 + Yg**2) / (2.0 * sigma**2)))[..., np.newaxis]
        img = Image.fromarray(np.clip(a * vig, 0, 255).astype("uint8"))

    g = settings["grain"]
    if g > 0:
        a = np.array(img).astype(float)
        img = Image.fromarray(
            np.clip(a + np.random.normal(0, g * 0.4, a.shape), 0, 255).astype("uint8"))

    t = settings["tone"]
    if t != 0:
        a = np.array(img).astype(float)
        if t > 0:
            a[:, :, 0] = np.clip(a[:, :, 0] + t * 0.4, 0, 255)
            a[:, :, 2] = np.clip(a[:, :, 2] - t * 0.2, 0, 255)
        else:
            a[:, :, 2] = np.clip(a[:, :, 2] - t * 0.4, 0, 255)
            a[:, :, 0] = np.clip(a[:, :, 0] + t * 0.2, 0, 255)
        img = Image.fromarray(np.clip(a, 0, 255).astype("uint8"))

    return img