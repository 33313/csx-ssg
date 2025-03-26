import re
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks
from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node


def markdown_to_html_node(md):
    blocks = markdown_to_blocks(md)
    elements = []
    for b in blocks:
        b_type = block_to_block_type(b)
        match b_type:
            case BlockType.PARAGRAPH:
                elements.append(block_paragraph_to_html(b))
            case BlockType.QUOTE:
                elements.append(block_quote_to_html(b))
            case BlockType.HEADING:
                elements.append(block_heading_to_html(b))
            case BlockType.CODE:
                elements.append(block_code_to_html(b))
            case BlockType.UNORDERED_LIST:
                elements.append(block_unordered_list_to_html(b))
            case BlockType.ORDERED_LIST:
                elements.append(block_ordered_list_to_html(b))
    return ParentNode("div", elements)


def text_to_children(text):
    nodes = text_to_textnodes(text)
    children = []
    for node in nodes:
        children.append(text_node_to_html_node(node))
    return children


def block_paragraph_to_html(block):
    return ParentNode("p", text_to_children(" ".join(block.split("\n"))))


def block_heading_to_html(block):
    res = re.search(r"^#{1,6}", block)
    if res is None:
        raise ValueError("Invalid heading level")
    return ParentNode(f"h{len(res.group())}", text_to_children(block.strip("# ")))


def block_code_to_html(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    return ParentNode("pre", [ParentNode("code", text_to_children(block[4:-3]))])


def block_quote_to_html(block):
    lines = block.split("\n")
    res = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        res.append(line.lstrip(">").strip())
    return ParentNode("blockquote", text_to_children(" ".join(res)))


def block_unordered_list_to_html(block):
    res = block.split("\n")
    children = []
    for line in res:
        children.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", children)


def block_ordered_list_to_html(block):
    res = block.split("\n")
    children = []
    for line in res:
        search = re.search(r"^[0-9]+\.", line)
        if search is None:
            raise ValueError("Invalid ordered list")
        children.append(
            ParentNode(
                "li",
                text_to_children(line[search.span()[1] :].strip()),
            )
        )
    return ParentNode("ol", children)
