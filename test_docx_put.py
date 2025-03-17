import unittest
import tempfile
import os
from docx import Document
from docx_put import parse_docx, extract_keywords, ner_analysis, sort_marketing_content, docx_main


class TestDocxProcessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_docx_path = os.path.join(self.temp_dir.name, "test.docx")
        self._create_test_docx()

    def _create_test_docx(self):
        doc = Document()
        doc.add_paragraph("This is a test paragraph.")
        doc.save(self.test_docx_path)

    def test_parse_docx_normal(self):
        text = parse_docx(self.test_docx_path)
        self.assertEqual(isinstance(text, str), True)

    def test_parse_docx_invalid_path(self):
        text = parse_docx("non_existent.docx")
        self.assertEqual(text, "")

    def test_extract_keywords(self):
        test_text = "This is a sample text for testing keyword extraction."
        keywords = extract_keywords(test_text)
        self.assertEqual(isinstance(keywords, list), True)

    def test_ner_analysis(self):
        test_text = "Google develops new software. Apple releases iPhone 15."
        brand_names, keywords = ner_analysis(test_text)
        self.assertEqual(isinstance(brand_names, list), True)
        self.assertEqual(isinstance(keywords, list), True)
        self.assertIn("Google", brand_names)
        self.assertIn("Apple", brand_names)

    def test_sort_marketing_content(self):
        test_content = """
        AI revolutionizes industries.
        Big data drives business growth.
        Cloud computing offers scalability.
        """
        keywords = ["AI", "big data", "cloud computing"]
        sorted_content = sort_marketing_content(test_content, keywords)
        self.assertEqual(isinstance(sorted_content, list), True)

    def tearDown(self):
        self.temp_dir.cleanup()


if __name__ == "__main__":
    unittest.main()
