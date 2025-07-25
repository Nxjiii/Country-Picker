from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox, QMessageBox
from PySide6.QtCore import QThread, Signal
import requests


def parse_country_names(json_data: list[dict]) -> list[str]:
    """Extract and sort country names from the JSON response."""
    try:
        return sorted([c["name"] for c in json_data if isinstance(c, dict) and "name" in c])
    except Exception as e:
        # handle unexpected errors gracefully
        print(f"Error parsing country names: {e}")
        return []


class CountryFetcherThread(QThread):
    countries_fetched = Signal(list)
    fetch_failed = Signal(str)

    def run(self):
        """fetches country data in a background thread."""
        try:
            response = requests.get("https://www.apicountries.com/countries", timeout=10)
            response.raise_for_status()
            data = response.json()
            countries = parse_country_names(data)  # extract and sort country names from response
            self.countries_fetched.emit(countries)
        except Exception as e:
            self.fetch_failed.emit(str(e))


class CountryPickerWindow(QMainWindow):
    def __init__(self, preselect_country: str = "") -> None:
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

    def on_country_selected(self, text: str) -> None:
        """Update the label when a country is selected."""
        self.label.setText(f"Selected: {text}")

    def fetch_countries(self) -> None:
        """Start a background thread to fetch country data."""
        self.thread = CountryFetcherThread()
        self.thread.countries_fetched.connect(self.populate_countries)
        self.thread.fetch_failed.connect(self.handle_fetch_error)
        self.thread.start()

    def populate_countries(self, countries: list[str]) -> None:
        """Populate the combobox with the fetched countries."""
        self.combobox.addItems(countries)
        self.combobox.setEnabled(True)
        self.label.setText("Select a country")

        if self.preselect_country:  # only check if preselect_country is not empty
            if self.preselect_country in countries:
                index = self.combobox.findText(self.preselect_country)
                if index != -1:
                    self.combobox.setCurrentIndex(index)
            else:
                # display a message box for invalid pre-selection
                QMessageBox.warning(self, "Warning", f"'{self.preselect_country}' is not a valid country.")
                # log to console
                print(f"Pre-selected country '{self.preselect_country}' not found in the fetched list.")

    def handle_fetch_error(self, error_message: str) -> None:
        """Handle errors during country data fetching."""
        QMessageBox.critical(self, "Error", f"Failed to load countries: {error_message}")
        self.label.setText("Failed to load countries.")
