from enum import Enum
from htmlnode import LeafNode
import re

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

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
    markdown_stripped = "\n".join(list(map(lambda x: x.strip(),markdown.split("\n"))))
    blocks = markdown_stripped.split("\n\n")
    return_blocks = []
    for block in blocks:
        if block[0:2] == "\n":
            block = block[2:]
        block = block.strip()
        block = "\n".join(list(map(lambda x: x.strip(),block.split("\n"))))
        if block != "":
            return_blocks.append(block)
    return return_blocks

def block_to_block_type(block_original):
    helper = block_original.strip(" ")
    check_start = False
    check_end = False
    if len(helper) >=2 and helper[:2] == "\n":
        check_start = True
    if len(helper) >=2 and helper[-2:] == "\n":
        check_end = True
    block = "\n".join(list(map(lambda x: x.strip(),helper.split("\n"))))
    if check_start:
        block.insert(0, "\n")
    if check_end:
        block.append("\n")

    if block[0] == "#":
        count = 1
        while block[count] == "#":
            count += 1
        if block[count] == " " and count <= 6:
            return BlockType.HEADING
        
    if len(block) >= 7 and block[0:3] == "```" and block[-3:] == "```":
        return BlockType.CODE
    
    if block[0] == ">":
        wrong = re.findall(r"\n[^>]", block)
        if len(block) >= 2 and block[-1:] == "\n":
            wrong.append(False)
        if wrong == []:
            return BlockType.QUOTE
        
    if len(block) >= 2 and block[0:2] == "- ":
        wrong = re.findall(r"\n[^-]", block)
        wrong.extend(re.findall(r"\n-[^ ]", block))
        if len(block) >= 2 and block[-1:] == "\n":
            wrong.append(False)
        if wrong == []:
            return BlockType.UNORDERED_LIST
        
    if len(block) >= 3 and block[0:3] == "1. ":
        count = 1
        i = 0
        good = True
        while i < len(block) - 1:
            if block[i:i+2] == "\n":
                number = len(str(count))
                if i + 2 + number < len(block) and block[i+2:i+3+number] == str(count) + ". ":
                    i = i + 3 + number
                    count += 1
                else:
                    good = False
                    break
            i += 1
        if "\n" not in block[i:] and good:
            return BlockType.ORDERED_LIST
        
    return BlockType.PARAGRAPH
