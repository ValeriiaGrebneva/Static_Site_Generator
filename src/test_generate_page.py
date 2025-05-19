import unittest

from generate_page import extract_title

class TestPage(unittest.TestCase):
    def test_title1(self):
        markdown = "#   Hello    "
        self.assertEqual(extract_title(markdown), "Hello")
        
    def test_not_title1(self):
        markdown1 = "#Hello"
        markdown2 = "Hello"
        markdown3 = "## Hello"
        try:
            extract_title(markdown1)
        except Exception as md1:
            self.assertEqual(str(md1), "no header (# ) found")
        try:
            extract_title(markdown2)
        except Exception as md2:
            self.assertEqual(str(md2), "no header (# ) found")
        try:
            extract_title(markdown3)
        except Exception as md3:
            self.assertEqual(str(md3), "no header (# ) found")

if __name__ == "__main__":
    unittest.main()