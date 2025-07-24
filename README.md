# Country Picker Task

Python GUI app built with PySide6. It fetches a list of countries from an API and displays them in a dropdown. Selecting a country updates the label below.

## Functionality

- The app fetches country data from `https://www.apicountries.com/countries`.
- The data is processed to extract and sort country names alphabetically.
- A dropdown (combobox) is populated with the country names.
- When a country is selected, the label updates to show the selected country.
- If a pre-selected country is provided with the --select argument, it is selected if valid.

## Implementation

- **GUI**: Built using PySide6 with a QComboBox for the dropdown and a QLabel for displaying the selected country.
- **Networking**: Country data is fetched in a background thread to keep the UI responsive.
- **Error Handling**: Invalid pre-selections or any network errors are handled with warnings or error messages.
- **Testing**: Includes unit tests for the JSON parsing logic.

## Run the App

Run the app with the following command (subsitute France with any country for pre-selection):

```bash
python -m country_picker --select France
```
