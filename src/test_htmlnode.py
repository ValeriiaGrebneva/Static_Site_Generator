import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node1 = HTMLNode("Tag", "Value",
                        ["c", "h", "i", "l", "d", "r", "e", "n"],
                        {
                            "href": "https://www.google.com",
                            "target": "blank",
                        })
        node2 = HTMLNode("Tag", "Value",
                        ["c", "h", "i", "l", "d", "r", "e", "n"],
                        {
                            "href": "https://www.google.com",
                            "target": "blank",
                        })
        self.assertEqual(node1.tag, node2.tag)
        self.assertEqual(node1.value, node2.value)
        self.assertEqual(node1.children, node2.children)
        self.assertEqual(node1.props, node2.props)
        
    def test_not_eq(self):
        node1 = HTMLNode("Tag", "Value", 
                        ["c", "h", "i", "l", "d", "r", "e", "n"],
                        {
                            "href": "https://www.google.com",
                            "target": "_blank",
                        })
        node3 = HTMLNode("Tag3", "Value3", 
                        [3, "c", "h", "i", "l", "d", "r", "e", "n"],
                        {
                            "href": "https://www.boot.dev",
                            "target": "something",
                        })
        self.assertNotEqual(node1, node3)

    def test_props(self):
        node1 = HTMLNode("Tag", "Value", 
                        ["c", "h", "i", "l", "d", "r", "e", "n"],
                        {
                            "href": "https://www.google.com",
                            "target": "_blank",
                        })
        self.assertEqual(node1.props_to_html(), 'href="https://www.google.com" target="_blank"')
        


if __name__ == "__main__":
    unittest.main()