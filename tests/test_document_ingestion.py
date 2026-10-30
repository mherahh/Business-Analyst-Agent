"""Unit tests for document extraction, hashing, and chunking."""
import os
import shutil
import tempfile
import unittest
from services.document_ingestion_service import (
    DocumentIngestionService,
    chunk_text,
    compute_document_hash,
    compute_chunk_id,
    extract_text,
)


class TestDocumentIngestion(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_chunk_text(self):
        sample = "This is a sentence. " * 30  # ~600 chars
        chunks = chunk_text(sample, chunk_size=200, overlap=50)
        self.assertGreater(len(chunks), 1)
        for c in chunks:
            self.assertLessEqual(len(c), 250)

    def test_deterministic_chunk_id(self):
        id1 = compute_chunk_id("doc.md", 0, "sample text")
        id2 = compute_chunk_id("doc.md", 0, "sample text")
        id3 = compute_chunk_id("doc.md", 1, "sample text")
        self.assertEqual(id1, id2)
        self.assertNotEqual(id1, id3)

    def test_load_directory_and_extract_md(self):
        file_path = os.path.join(self.test_dir, "test.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write("# Best Practices\n\nCheckout flows should require fewer than four steps.")

        service = DocumentIngestionService(chunk_size=300, chunk_overlap=50)
        res = service.load_directory(self.test_dir)
        self.assertEqual(len(res.errors), 0)
        self.assertGreater(len(res.chunks), 0)
        self.assertEqual(res.chunks[0].source_path, file_path)


if __name__ == "__main__":
    unittest.main()
