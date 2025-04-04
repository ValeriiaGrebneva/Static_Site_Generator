from textnode import TextType, TextNode
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            splitted = node.text.split(delimiter)
            if len(splitted) % 2 == 0:
                raise Exception(f"Invalid Mardown syntax - no closing {delimiter}")
            count = 0
            for piece in splitted:
                if piece != "":
                    if count % 2 == 0:
                        new_nodes.append(TextNode(piece, TextType.TEXT))
                    else:
                        new_nodes.append(TextNode(piece, text_type))
                count += 1
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text)
