from htmlnode import ParentNode, LeafNode
from textnode import text_node_to_html_node, markdown_to_blocks, block_to_block_type, BlockType, TextNode, TextType
from split_to_nodes import text_to_textnodes


def text_to_children(text):
    textnodes = text_to_textnodes(text)
    list_of_nodes = []
    for singular_textnode in textnodes:
        list_of_nodes.append(text_node_to_html_node(singular_textnode))
    return list_of_nodes

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    return_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                new_node = ParentNode("p", text_to_children([TextNode(block.replace("\n", " "), TextType.TEXT)]))
            case BlockType.HEADING:
                count = 1
                while block[count] == "#":
                    count += 1
                new_node = ParentNode(f"h{count}", text_to_children([TextNode(block[count + 1:], TextType.TEXT)]))
            case BlockType.CODE:
                new_node = ParentNode("pre", [LeafNode("code", block[3:-3].strip())])
            case BlockType.QUOTE:
                new_node = ParentNode("blockquote", text_to_children([TextNode(block[1:].replace("\n>", "\n"), TextType.TEXT)]))
            case BlockType.UNORDERED_LIST:
                items = block.split("- ")
                parents_inside = []
                for item in items:
                    if item.strip() != "":
                        parents_inside.append(ParentNode("li", text_to_children([TextNode(item.strip(), TextType.TEXT)])))
                new_node = ParentNode("ul", parents_inside)
            case BlockType.ORDERED_LIST:
                items = block.split("\n")
                parents_inside = []
                for item in items:
                    parents_inside.append(ParentNode("li", text_to_children([TextNode(item[3:], TextType.TEXT)])))
                new_node = ParentNode("ol", parents_inside)
        return_blocks.append(new_node)
    return ParentNode("div", return_blocks)