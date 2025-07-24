import unittest
from country_picker.ui import parse_country_names

# Test List
# test_parse_country_names: Valid and invalid data.
# test_parse_country_names_with_empty_list: Empty input list.
# test_parse_country_names_with_duplicates: Duplicate country names.
# test_parse_country_names_with_non_dict_elements: Non-dictionary elements in the list.

class TestCountryParsing(unittest.TestCase):
    def test_parse_country_names(self):
        sample_data = [
            {"name": "Brazil"},
            {"name": "Argentina"},
            {"bad_key": "NoName"},
            {"name": "Canada"}
        ]
        result = parse_country_names(sample_data)
        self.assertEqual(result, ["Argentina", "Brazil", "Canada"])

    def test_parse_country_names_with_empty_list(self):
        """Test with an empty list."""
        result = parse_country_names([])
        self.assertEqual(result, [])

    def test_parse_country_names_with_duplicates(self):
        """Test with duplicate country names."""
        sample_data = [
            {"name": "Brazil"},
            {"name": "Brazil"},
            {"name": "Argentina"}
        ]
        result = parse_country_names(sample_data)
        self.assertEqual(result, ["Argentina", "Brazil", "Brazil"])

    def test_parse_country_names_with_non_dict_elements(self):
        """Test with non-dictionary elements in the list."""
        sample_data = [
            {"name": "Brazil"},
            "NotADict",
            {"name": "Argentina"}
        ]
        result = parse_country_names(sample_data)
        self.assertEqual(result, ["Argentina", "Brazil"])

if __name__ == "__main__":
    unittest.main()


