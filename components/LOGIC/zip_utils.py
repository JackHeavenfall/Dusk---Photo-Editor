# components/LOGIC/zip_utils.py
import zipfile
from pathlib import Path
from tkinter import messagebox
from .logging_setup import log_error
from tkinter import messagebox

def extract_zip(zip_path, tmp_dir):
    """
    Extract a zip archive and return a list of image paths inside.
    tmp_dir is a Path to a temporary folder (should be created by caller).
    """
    try:
        tmp_dir.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(zip_path, "r") as z:
            z.extractall(tmp_dir)
        from components.constants import SUPPORTED
        imgs = sorted(f for f in tmp_dir.rglob("*")
                      if f.suffix.lower() in SUPPORTED)
        if not imgs:
            messagebox.showinfo("DUSK — Empty Archive",
                f"No supported images found inside:\n{zip_path.name}")
        return imgs
    except zipfile.BadZipFile as exc:
        log_error(f"Bad zip file: {zip_path.name}", exc)
        messagebox.showerror("DUSK — Bad Archive",
            f"Could not open the zip file:\n{zip_path.name}\n\n{exc}")
        return []
    except Exception as exc:
        log_error(f"Zip extraction failed: {zip_path}", exc)
        messagebox.showerror("DUSK — Error",
            f"Archive extraction failed:\n{exc}")
        return []