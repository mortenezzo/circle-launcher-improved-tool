from PyQt6.QtCore import QThread, pyqtSignal

from app.services.powershell_handler import get_system_apps


class GetSystemAppsThread(QThread):
    """
    Thread to retrieve system applications using PowerShell.
    """
    result = pyqtSignal(list)
    error = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._is_running = True

    def run(self):
        try:
            while self._is_running:
                apps = get_system_apps()
                if self._is_running:
                    self.result.emit(apps) # type: ignore
                break
        except Exception as e:
            if self._is_running:
                self.error.emit(str(e)) # type: ignore

    def stop(self):
        """
        Stop the thread gracefully.
        """
        self._is_running = False