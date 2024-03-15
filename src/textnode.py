from enum import Enum

from htmlnode import LeafNode

TextType = Enum("TextType", ["TEXT", "BOLD", "ITALIC", "CODE", "LINK", "IMAGE"])


class TextNode:
    def __init__(self, text="", text_type=TextType.TEXT, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        return self.text == other.text

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def to_html_node(self):
        tag = None
        txt = self.text
        props = None
        match self.text_type:
            case TextType.TEXT:
                pass
            case TextType.BOLD:
                tag = "b"
            case TextType.ITALIC:
                tag = "i"
            case TextType.CODE:
                tag = "code"
            case TextType.LINK:
                tag = "a"
                props = {"href": self.url}
            case TextType.IMAGE:
                tag = "img"
                txt = None
                props = {"src": self.url, "alt": self.text}
            case _:
                raise Exception("Invalid TextType")

        return LeafNode(tag, txt, props)
