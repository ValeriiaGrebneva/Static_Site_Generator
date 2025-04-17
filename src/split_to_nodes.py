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
    result = re.findall(r"^\[(.*?)\]\((.*?)\)", text)
    result.extend(re.findall(r"[^!]\[(.*?)\]\((.*?)\)", text))
    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            images = extract_markdown_images(node.text)
            count_start = 0
            for image in images:
                image_text = "![" + image[0] + "](" + image[1] + ")"
                count_end = count_start + node.text[count_start:].find(image_text)
                if count_start != count_end:
                    new_nodes.append(TextNode(node.text[count_start:count_end], TextType.TEXT))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                count_start = count_end + len(image_text)
            if count_start != len(node.text):
                new_nodes.append(TextNode(node.text[count_start:], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT:
            links = extract_markdown_links(node.text)
            count_start = 0
            for link in links:
                link_text = "[" + link[0] + "](" + link[1] + ")"
                count_end = count_start + node.text[count_start:].find(link_text)
                if count_start != count_end:
                    new_nodes.append(TextNode(node.text[count_start:count_end], TextType.TEXT))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                count_start = count_end + len(link_text)
            if count_start != len(node.text):
                new_nodes.append(TextNode(node.text[count_start:], TextType.TEXT))
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    return split_nodes_image(split_nodes_link(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(text,"**",TextType.BOLD),"_",TextType.ITALIC),"`",TextType.CODE)))
