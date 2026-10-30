"""Unit tests for Word (.docx) and Markdown (.md) document generation."""
import os
import shutil
import tempfile
import unittest
from services.document_service import save_doc, save_markdown_doc


class TestDocumentService(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_save_markdown_doc(self):
        sections = [
            ("Objectives", ["Launch MVP in Q1", "Onboard 500 users"]),
            ("Stakeholders", ["Store Owner", "End Customers"]),
            ("Metadata", {"Version": "1.0", "Author": "BA Agent"}),
        ]
        md_path = save_markdown_doc("test_doc.md", "Test Requirements", sections, output_dir=self.test_dir)
        self.assertTrue(os.path.exists(md_path))
        with open(md_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("# Test Requirements", content)
        self.assertIn("## Objectives", content)
        self.assertIn("Launch MVP in Q1", content)
        self.assertIn("**Version**: 1.0", content)

    def test_save_doc_creates_both_docx_and_md(self):
        sections = [
            ("Features", ["Shopping Cart", "Payment Gateway"]),
        ]
        docx_path = save_doc("sample_prd.docx", "Sample PRD", sections, output_dir=self.test_dir, save_markdown=True)
        self.assertTrue(os.path.exists(docx_path))
        self.assertTrue(docx_path.endswith(".docx"))

        md_path = os.path.join(self.test_dir, "sample_prd.md")
        self.assertTrue(os.path.exists(md_path))


if __name__ == "__main__":
    unittest.main()
