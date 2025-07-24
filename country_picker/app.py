from PySide6.QtWidgets import QApplication
import sys
from .ui import CountryPickerWindow

def run_app(preselect_country: str = ""):
    app = QApplication(sys.argv)
    window = CountryPickerWindow(preselect_country=preselect_country)
    window.show()
    sys.exit(app.exec())
