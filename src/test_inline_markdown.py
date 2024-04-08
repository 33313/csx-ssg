import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_bold(self):
        node = TextNode("Some **bold** text")
        res = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Some "),
                TextNode("bold", TextType.BOLD),
                TextNode(" text"),
            ],
            res,
        )

    def test_double_bold(self):
        node = TextNode("Some **bold** text, **wow**!")
        res = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("Some "),
                TextNode("bold", TextType.BOLD),
                TextNode(" text, "),
                TextNode("wow", TextType.BOLD),
                TextNode("!"),
            ],
            res,
        )

    def test_code_block(self):
        node = TextNode("Some text with a `code block`.")
        res = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("Some text with a "),
                TextNode("code block", TextType.CODE),
                TextNode("."),
            ],
            res,
        )

    def test_invalid_md(self):
        node = TextNode("Some text with invalid **markdown")
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "Some ![image](https://imgs.xkcd.com/comics/exploits_of_a_mom.png)"
        )
        self.assertListEqual(
            [("image", "https://imgs.xkcd.com/comics/exploits_of_a_mom.png")], matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "Some text with [link one](https://google.com) and [link two](https://twitter.com)"
        )
        self.assertListEqual(
            [
                ("link one", "https://google.com"),
                ("link two", "https://twitter.com"),
            ],
            matches,
        )

    def test_split_image(self):
        node = TextNode("![image](https://google.com)")
        nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://google.com"),
            ],
            nodes,
        )

        node = TextNode("Some text ![image](https://google.com) more text")
        nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text "),
                TextNode("image", TextType.IMAGE, "https://google.com"),
                TextNode(" more text"),
            ],
            nodes,
        )

        node = TextNode(
            "Some text ![image](https://google.com) more text ![image](https://google.com)"
        )
        nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("Some text "),
                TextNode("image", TextType.IMAGE, "https://google.com"),
                TextNode(" more text "),
                TextNode("image", TextType.IMAGE, "https://google.com"),
            ],
            nodes,
        )

    def test_split_link(self):
        node = TextNode("[link](https://google.com)")
        nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
            nodes,
        )

        node = TextNode("Some text [link](https://google.com) more text")
        nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text "),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" more text"),
            ],
            nodes,
        )

        node = TextNode(
            "Some text [link](https://google.com) more text [link](https://google.com)"
        )
        nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("Some text "),
                TextNode("link", TextType.LINK, "https://google.com"),
                TextNode(" more text "),
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
            nodes,
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is "),
                TextNode("text", TextType.BOLD),
                TextNode(" with an "),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a "),
                TextNode("code block", TextType.CODE),
                TextNode(" and an "),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a "),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )


if __name__ == "__main__":
    unittest.main()
