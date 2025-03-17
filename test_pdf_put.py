import unittest
import tempfile
import os
import re
import spacy
import PyPDF2
import logging
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from pdf_put import parse_pdf, extract_keywords, ner_analysis, sort_marketing_content, pdf_main


class TestPDFProcessing(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.test_pdf_path = os.path.join(self.temp_dir.name, "test.pdf")
        self._create_test_pdf()

    def _create_test_pdf(self):
        writer = PyPDF2.PdfWriter()
        writer.add_blank_page(width=400, height=400)
        with open(self.test_pdf_path, 'wb') as file:
            writer.write(file)

    def test_parse_pdf_normal(self):
        text = parse_pdf(self.test_pdf_path)
        # 空白 PDF 文件，预期文本为空
        self.assertEqual(isinstance(text, str), True)

    def test_parse_pdf_invalid_path(self):
        text = parse_pdf("non_existent.pdf")
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
