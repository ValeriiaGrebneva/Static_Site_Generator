from enum import Enum
from htmlnode import LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode():
    def __init__(self, text, text_type, url = None):
        self.text = text
        self.text_type = TextType(text_type)
        self.url = url
    def __eq__(self, text_node):
        return self.text == text_node.text and self.text_type == text_node.text_type and self.url == text_node.url
    def __repr__(self):
        return "TextNode(" + self.text + ", " + self.text_type.value + ", " + str(self.url) + ")"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case text_node.text_type.TEXT:
            return LeafNode(None, text_node.text)
        case text_node.text_type.BOLD:
            return LeafNode("b", text_node.text)
        case text_node.text_type.ITALIC:
            return LeafNode("i", text_node.text)
        case text_node.text_type.CODE:
            return LeafNode("code", text_node.text)
        case text_node.text_type.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case text_node.text_type.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt":text_node.text})
        case _:
            raise Exception("Not correct type of TextNode")
        
def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return_blocks = []
    for block in blocks:
        if block[0:2] == "\n":
            block = block[2:]
        block = block.strip()
        block = "\n".join(list(map(lambda x: x.strip(),block.split("\n"))))
        if block != "":
            return_blocks.append(block)
    return return_blocks
    