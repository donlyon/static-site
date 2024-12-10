import unittest

from main import extract_title


class TestMain(unittest.TestCase):
    def test_extract_title(self):
        text = "# My Title"
        self.assertEqual(extract_title(text), "My Title")

    def test_extract_title_no_title(self):
        text = "My Title"
        with self.assertRaises(Exception):
            extract_title(text)

if __name__ == "__main__":
    unittest.main()
