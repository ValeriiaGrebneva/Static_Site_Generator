import unittest

from textnode import TextNode, TextType, BlockType, markdown_to_blocks, block_to_block_type
from split_to_nodes import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from collecting_to_html import markdown_to_html_node

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

    def test_split_all(self):
        node = TextNode(
            "This is **text** with an _italic_ word and a `code block` and an ![image](Image) and a [link](Link)",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "Image"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "Link"),
            ],
            new_nodes
        )

    def test_split_all_grouped(self):
        node = TextNode(
            "![image](link for image)[link](link for link)`some code` and _italic_**bold**",
            TextType.TEXT,
        )
        new_nodes = text_to_textnodes([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "link for image"),
                TextNode("link", TextType.LINK, "link for link"),
                TextNode("some code", TextType.CODE),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode("bold", TextType.BOLD)
            ],
            new_nodes
        )

    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    
    - This is a list
    - with items
    
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_blocks_to_types_heading(self):
        md1 = """# Heading"""
        block_type1 = block_to_block_type(md1)
        self.assertEqual(block_type1, BlockType.HEADING)

    def test_blocks_to_types_heading_no(self):
        md1 = """##Not heading because no space"""
        block_type1 = block_to_block_type(md1)
        md2 = """####### Not heading because too many #"""
        block_type2 = block_to_block_type(md2)
        self.assertEqual(block_type1, block_type2, BlockType.PARAGRAPH)

    def test_blocks_to_types_code(self):
        md1 = """```Code```"""
        block_type1 = block_to_block_type(md1)
        self.assertEqual(block_type1, BlockType.CODE)

    def test_blocks_to_types_code_no(self):
        md1 = """``Not code because wrong amount of backticks```"""
        block_type1 = block_to_block_type(md1)
        md2 = """``````"""
        block_type2 = block_to_block_type(md2)
        self.assertEqual(block_type1, block_type2, BlockType.PARAGRAPH)

    def test_blocks_to_types_quote(self):
        md1 = """>This is a quote
        >with two lines"""
        block_type1 = block_to_block_type(md1)
        self.assertEqual(block_type1, BlockType.QUOTE)

    def test_blocks_to_types_quote_no(self):
        md1 = """>Not quote because the next line is without >
        """
        block_type1 = block_to_block_type(md1)
        self.assertEqual(block_type1, BlockType.PARAGRAPH)

    def test_blocks_to_types_unordered_list(self):
        md1 = """- List 1
        - List 2
        - List 3"""
        block_type1 = block_to_block_type(md1)
        self.assertEqual(block_type1, BlockType.UNORDERED_LIST)

    def test_blocks_to_types_unordered_list_no(self):
        md1 = """- Not unordered_list because
        -no space"""
        block_type1 = block_to_block_type(md1)
        md2 = """- No dash and space
        """
        block_type2 = block_to_block_type(md2)
        self.assertEqual(block_type1, BlockType.PARAGRAPH)
        self.assertEqual(block_type2, BlockType.PARAGRAPH)

    def test_blocks_to_types_ordered_list(self):
        md1 = """1. List 1
        2. List2
        3. List3"""
        block_type1 = block_to_block_type(md1)
        self.assertEqual(block_type1, BlockType.ORDERED_LIST)

    def test_blocks_to_types_ordered_list_no(self):
        md1 = """1. Not ordered_list because
        2.no space"""
        block_type1 = block_to_block_type(md1)
        md2 = """1. No number after
        just text"""
        block_type2 = block_to_block_type(md2)
        md3 = """1. No space after number 
        2.just text"""
        block_type3 = block_to_block_type(md3)
        md4 = """1. Wrong numbers
        3. just text"""
        block_type4 = block_to_block_type(md4)
        self.assertEqual(block_type1, block_type2, BlockType.PARAGRAPH)
        self.assertEqual(block_type3, block_type4, BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
    This is **bolded** paragraph
    text in a p
    tag here

    This is another paragraph with _italic_ text and `code` here

    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
    ```
    This is text that _should_ remain
    the **same** even with inline stuff
    ```
    """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )
    
    def test_headings(self):
        md = """
    # Heading 1
    
    ### Heading _3_

    ###### Heading **6**
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading 1</h1><h3>Heading <i>3</i></h3><h6>Heading <b>6</b></h6></div>", 
        )

    def test_quotes(self):
        md = """
    >Quote 1.1
    >Quote 1.2
    
    >Quote 2 with **bold** and _italic_
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>Quote 1.1\nQuote 1.2</blockquote><blockquote>Quote 2 with <b>bold</b> and <i>italic</i></blockquote></div>", 
        )

    def test_unordered_list(self):
        md = """
    - List 1.1
    - List 1.2
    - List **1.3**

    - List 2
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>List 1.1</li><li>List 1.2</li><li>List <b>1.3</b></li></ul><ul><li>List 2</li></ul></div>", 
        )

    def test_ordered_list(self):
        md = """
    1. List 1.1
    2. List 1.2
    3. List **1.3**

    1. List 2
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>List 1.1</li><li>List 1.2</li><li>List <b>1.3</b></li></ol><ol><li>List 2</li></ol></div>", 
        )
    
    def test_alltogether(self):
        md = """
    #### Heading 4!

    This is **bolded** paragraph

    This is another [paragraph](link) with _italic_ text and `code` here.
    This is the same ![paragraph](link) on a new line

    
    - This is a list
    - with items
    - and `code`

    1. This is an ordered list
    2. Several items

    ```
    Code should be also here
    ```

    >Quotes
    >More quotes
    """
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><h4>Heading 4!</h4><p>This is <b>bolded</b> paragraph</p><p>This is another <a href="link">paragraph</a> with <i>italic</i> text and <code>code</code> here. This is the same <img src="link" alt="paragraph"> on a new line</p><ul><li>This is a list</li><li>with items</li><li>and <code>code</code></li></ul><ol><li>This is an ordered list</li><li>Several items</li></ol><pre><code>Code should be also here</code></pre><blockquote>Quotes\nMore quotes</blockquote></div>')


if __name__ == "__main__":
    unittest.main()