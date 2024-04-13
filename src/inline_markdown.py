from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    rx = r"!\[.*?\]\(.*?\)"
    matches = re.findall(rx, text)
    res = []
    for x in matches:
        arr = x.split("(")
        arr[0] = arr[0].strip("![]")
        arr[1] = arr[1][:-1]
        res.append((arr[0], arr[1]))
    return res


def extract_markdown_links(text):
    rx = r"\[.*?\]\(.*?\)"
    matches = re.findall(rx, text)
    res = []
    for x in matches:
        arr = x.split("(")
        arr[0] = arr[0].strip("[]")
        arr[1] = arr[1][:-1]
        res.append((arr[0], arr[1]))
    return res


def split_nodes_image(old_nodes):
    new = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new.append(n)
            continue
        images = extract_markdown_images(n.text)
        if len(images) == 0:
            new.append(n)
            continue
        text = n.text
        for image in images:
            s = text.split(f"![{image[0]}]({image[1]})", 1)
            if len(s) != 2:
                raise Exception("ERROR: Invalid markdown, image was not closed.")
            if s[0] != "":
                new.append(TextNode(s[0]))
            new.append(TextNode(image[0], TextType.IMAGE, image[1]))
            text = s[1]
        if text != "":
            new.append(TextNode(text))
    return new


def split_nodes_link(old_nodes):
    new = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new.append(n)
            continue
        links = extract_markdown_links(n.text)
        if len(links) == 0:
            new.append(n)
            continue
        text = n.text
        for link in links:
            s = text.split(f"[{link[0]}]({link[1]})", 1)
            if len(s) != 2:
                raise Exception("ERROR: Invalid markdown, link was not closed.")
            if s[0] != "":
                new.append(TextNode(s[0]))
            new.append(TextNode(link[0], TextType.LINK, link[1]))
            text = s[1]
        if text != "":
            new.append(TextNode(text))
    return new


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
