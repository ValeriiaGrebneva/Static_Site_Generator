import unittest

from textnode import TextNode, TextType
from split_to_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link

class TestSplitNodes(unittest.TestCase):
    def test_eq_text(self):
        node = TextNode("This is text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.TEXT)
        self.assertEqual([node], new_nodes)

    def test_eq_bold_text(self):
        node = TextNode("**Bold block** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("Bold block", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, result)

    def test_eq_text_bold(self):
        node = TextNode("This is text with **bold text**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("This is text with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD)
            ]
        self.assertEqual(new_nodes, result)

    def test_eq_italic(self):
        node = TextNode("_Italic text_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        result = [TextNode("Italic text", TextType.ITALIC)]
        self.assertEqual(new_nodes, result)

    def test_eq_text_code_text(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        result = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, result)

    def test_err_delimiter(self):
        node = TextNode("This is text with a `code block", TextType.TEXT)
        try:
            split_nodes_delimiter([node], "`", TextType.CODE)
        except Exception as v_e:
            self.assertEqual(str(v_e), "Invalid Mardown syntax - no closing `")

    def test_eq_several_delimiters(self):
        node = TextNode("This is **bold1** and **bold2** text", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold1", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("bold2", TextType.BOLD),
            TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(new_nodes, result)

    def test_eq_different_delimiters(self):
        node = TextNode("This is **bold** and _italic_ text", TextType.TEXT)
        new_nodes_1 = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes_2 = split_nodes_delimiter(new_nodes_1, "_", TextType.ITALIC)
        result = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" text", TextType.TEXT)
            ]
        self.assertEqual(new_nodes_2, result)

    def test_extract_markdown_image(self):
        matches = extract_markdown_images(
            "This is text with an ![image](Link)"
        )
        self.assertListEqual([("image", "Link")], matches)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image1](Link1) and an ![image2](Link2)"
        )
        self.assertListEqual([("image1", "Link1"), ("image2", "Link2")], matches)

    def test_extract_markdown_link(self):
        matches = extract_markdown_links(
            "This is text with a [link](Link)"
        )
        self.assertListEqual([("link", "Link")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a [link1](Link1) and a [link2](Link2)"
        )
        self.assertListEqual([("link1", "Link1"), ("link2", "Link2")], matches)

    def test_extract_markdown_link_for_image(self):
        matches = extract_markdown_links(
            "This is text with an ![image1](Link1)"
        )
        self.assertListEqual([], matches)

    def test_extract_markdown_image_for_link(self):
        matches = extract_markdown_images(
            "This is text with a [link](Link)"
        )
        self.assertListEqual([], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image1](link1) and second ![image2](link2) - done!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "link1"),
                TextNode(" and second ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "link2"),
                TextNode(" - done!", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_only(self):
        node = TextNode(
            "![image1](link1)![image2](link2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image1", TextType.IMAGE, "link1"),
                TextNode("image2", TextType.IMAGE, "link2")
            ],
            new_nodes,
        )

    def test_split_images_empty(self):
        node = TextNode(
            "This is text without images but with a [link](Link)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text without images but with a [link](Link)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link1](Link1) and second [link2](Link2) - done!",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "Link1"),
                TextNode(" and second ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "Link2"),
                TextNode(" - done!", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_links_only(self):
        node = TextNode(
            "[link1](Link1)[link2](Link2)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link1", TextType.LINK, "Link1"),
                TextNode("link2", TextType.LINK, "Link2")
            ],
            new_nodes,
        )

    def test_split_links_empty(self):
        node = TextNode(
            "This is text without links but with an ![image](Link)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text without links but with an ![image](Link)", TextType.TEXT)
            ],
            new_nodes,
        )

    def test_split_images_links(self):
        node = TextNode(
            "This is text with an ![image](link of the image) and a [link](Link) - done!",
            TextType.TEXT,
        )
        new_nodes1 = split_nodes_link(split_nodes_image([node]))
        new_nodes2 = split_nodes_image(split_nodes_link([node]))
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "link of the image"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "Link"),
                TextNode(" - done!", TextType.TEXT)
            ],
            new_nodes1,
            new_nodes2
        )

if __name__ == "__main__":
    unittest.main()