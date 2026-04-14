# components/UI/DuskApp/status.py
# Optional helper methods for status updates.
# The core already has self._status; this mixin can be extended later.
class DuskAppStatusMixin:
    def _set_status(self, text):
        if hasattr(self, "_status"):
            self._status.config(text=text)