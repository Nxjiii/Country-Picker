from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLabel, QComboBox

class CountryPickerWindow(QMainWindow):
    def __init__(self, preselect_country: str = ""):
        super().__init__()
        self.setWindowTitle("Country Picker")
        self.setGeometry(100, 100, 300, 100)

        self.label = QLabel("")
        self.combobox = QComboBox()

        layout = QVBoxLayout()
        layout.addWidget(self.combobox)
        layout.addWidget(self.label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
