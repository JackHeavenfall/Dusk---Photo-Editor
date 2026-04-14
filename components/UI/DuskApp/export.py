# components/UI/DuskApp/export.py
from tkinter import messagebox

from components.registry import get_component
ExportDialog = get_component("components.UI.ExportDialog")


class DuskAppExportMixin:
    def _export_all(self):
        files = self._import.get_all()
        if not files:
            messagebox.showinfo("DUSK",
                "No images in queue.\n\n"
                "Use the buttons on the left to add images first.")
            return
        ExportDialog(self, files, self._settings.get_settings())