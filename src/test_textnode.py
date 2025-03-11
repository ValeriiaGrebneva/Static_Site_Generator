import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq_none(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_not_eq_none(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node too", TextType.IMAGE)
        self.assertNotEqual(node, node2)
    def test_eq_not_none(self):
        node = TextNode("This is a text", TextType.LINK, "Not None")
        node2 = TextNode("This is a text", TextType.LINK, "Not None")
        self.assertEqual(node, node2)
    def test_not_eq_type_none(self):
        node = TextNode("This is a node", TextType.IMAGE, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)
    def test_not_eq_type(self):
        node = TextNode("This is a text node", TextType.LINK)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()