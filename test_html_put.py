import unittest
import tempfile
import os
from bs4 import BeautifulSoup
from html_put import parse_html, extract_keywords, ner_analysis, sort_marketing_content, html_main


class TestHTMLProcessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_html_path = os.path.join(self.temp_dir.name, "test.html")
        self._create_test_html()

    def _create_test_html(self):
        html_content = "<html><body><p>Test content</p></body></html>"
        with open(self.test_html_path, 'w', encoding='utf-8') as file:
            file.write(html_content)

    def test_parse_html_normal(self):
        text = parse_html(self.test_html_path)
        self.assertEqual(isinstance(text, str), True)

    def test_parse_html_invalid_path(self):
        text = parse_html("non_existent.html")
        self.assertEqual(text, "")

    def test_extract_keywords(self):
        test_text = "This is a sample text for testing keyword extraction."
        keywords = extract_keywords(test_text)
        self.assertEqual(isinstance(keywords, list), True)

    def test_ner_analysis(self):
        test_text = "Apple launches new iPhone. Microsoft releases Windows 11."
        brand_names, keywords = ner_analysis(test_text)
        self.assertEqual(isinstance(brand_names, list), True)
        self.assertEqual(isinstance(keywords, list), True)
        self.assertIn("Apple", brand_names)
        self.assertIn("Microsoft", brand_names)

    def test_sort_marketing_content(self):
        test_content = """
        AI is the future.
        Machine learning is powerful.
        Data science is in demand.
        """
        keywords = ["AI", "machine learning", "data science"]
        sorted_content = sort_marketing_content(test_content, keywords)
        self.assertEqual(isinstance(sorted_content, list), True)

    def tearDown(self):
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
