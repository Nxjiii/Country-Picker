from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QMessageBox
from PySide6.QtCore import QThread, Signal
import requests


class CountryFetcherThread(QThread):
    countries_fetched = Signal(list)
    fetch_failed = Signal(str)

    def run(self):
        """fetches country data in a background thread."""
        try:
            response = requests.get("https://www.apicountries.com/countries", timeout=10)
            response.raise_for_status()
            data = response.json()
            countries = sorted([c["name"] for c in data if "name" in c])
            self.countries_fetched.emit(countries)
        except Exception as e:
            self.fetch_failed.emit(str(e))


class CountryPickerWindow(QMainWindow):
    def __init__(self, preselect_country: str = ""):
        """Country Picker Window."""
        super().__init__()
        self.setWindowTitle("Country Picker")
        self.setGeometry(100, 100, 300, 100)

        # UI Elements
        self.label = QLabel("Loading countries...")
        self.combobox = QComboBox()
        self.combobox.setEnabled(False)  # disable until data is loaded

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.combobox.currentTextChanged.connect(self.on_country_selected)

        self.preselect_country = preselect_country
        self.fetch_countries()

    def on_country_selected(self, text: str):
        """Update the label when a country is selected."""
        self.label.setText(f"Selected: {text}")

    def fetch_countries(self):
        """Start a background thread to fetch country data."""
        self.thread = CountryFetcherThread()
        self.thread.countries_fetched.connect(self.populate_countries)
        self.thread.fetch_failed.connect(self.handle_fetch_error)
        self.thread.start()

    def populate_countries(self, countries: list):
        """Populate the combobox with the fetched countries."""
        self.combobox.addItems(countries)
        self.combobox.setEnabled(True)
        self.label.setText("Select a country")

        if self.preselect_country in countries:
            index = self.combobox.findText(self.preselect_country)
            if index != -1:
                self.combobox.setCurrentIndex(index)

    def handle_fetch_error(self, error_message: str):
        """Handle errors during country data fetching."""
        QMessageBox.critical(self, "Error", f"Failed to load countries: {error_message}")
        self.label.setText("Failed to load countries.")
