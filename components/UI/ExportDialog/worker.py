# worker.py
import zipfile
from pathlib import Path
from PIL import Image
from tkinter import messagebox
from components.LOGIC.image_processing import process_image
from components.LOGIC.logging_setup import log, log_error

def _worker(self):
    out_dir = Path(self._out_dir.get())
    fmt = self._fmt.get()
    quality = self._quality.get()
    exported, errors = [], []

    try:
        out_dir.mkdir(parents=True, exist_ok=True)
    except Exception as exc:
        log_error(f"Cannot create export dir: {out_dir}", exc)
        self.after(0, lambda: messagebox.showerror(
            "DUSK", f"Cannot create output folder:\n{out_dir}\n\n{exc}"))
        self._running = False
        return

    log(f"Export: {len(self._files)} -> {out_dir}  fmt={fmt}  q={quality}")

    for i, path in enumerate(self._files):
        if not self._running:
            log("Export cancelled by user")
            break
        # Update label: use lambda to set text
        self.after(0, lambda p=path, idx=i, total=len(self._files):
                   self._prog_lbl.config(text=f"{p.name}  ({idx+1}/{total})"))
        try:
            img = Image.open(path)
            out = process_image(img, self._settings)
            out_path = out_dir / f"{path.stem}_dusk.{fmt}"
            save_kw = {"quality": quality} if fmt in ("jpg", "jpeg") else {}
            out.save(out_path, **save_kw)
            exported.append(out_path)
        except Exception as exc:
            log_error(f"Export failed: {path.name}", exc)
            errors.append(path.name)
        self.after(0, self._prog.step)

    if self._do_zip.get() and exported:
        zip_path = out_dir / f"{self._zip_name.get()}.zip"
        try:
            with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for f in exported:
                    zf.write(f, f.name)
            log(f"Zipped {len(exported)} -> {zip_path.name}")
            self.after(0, lambda: self._prog_lbl.config(
                text=f"zipped {len(exported)} -> {zip_path.name}"))
        except Exception as exc:
            log_error("Zip creation failed", exc)
            self.after(0, lambda: self._prog_lbl.config(text="zip failed - see logs"))
    else:
        msg = f"done. {len(exported)} exported."
        if errors:
            msg += f"  {len(errors)} failed."
        self.after(0, lambda: self._prog_lbl.config(text=msg))

    log(f"Export complete: {len(exported)} ok, {len(errors)} failed")
    self.after(0, lambda: self._export_btn.config(text="done ✓"))
    self._running = False