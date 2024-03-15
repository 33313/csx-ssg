import unittest

from inline_markdown import extract_markdown_images, extract_markdown_links, split_nodes_delimiter
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
        self.assertListEqual([("image", "https://imgs.xkcd.com/comics/exploits_of_a_mom.png")], matches)

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


if __name__ == "__main__":
    unittest.main()
