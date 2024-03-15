from textnode import TextNode, TextType
import re


def split_nodes_delimiter(old, delim, text_type):
    new = []
    for n in old:
        if type(n) is not TextNode:
            new.append(n)
            continue
        if delim not in n.text:
            raise Exception(f'ERROR: Delimiter "{delim}" not found.')
        text_list = n.text.split(delim)
        if len(text_list) % 2 == 0:
            raise Exception("ERROR: Invalid markdown, delimiter was not closed.")
        nodes = []
        apply = False
        for x in text_list:
            if apply:
                nodes.append(TextNode(x, TextType.TEXT))
            else:
                nodes.append(TextNode(x, text_type))
            apply = not apply
        new.extend(nodes)
    return new


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
