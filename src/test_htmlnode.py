import unittest

from htmlnode import HTMLNode, LeafNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com"')

    def test_leaf(self):
        node = LeafNode("p", "Testing")
        node2 = LeafNode("a", "Testing link", None, {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Testing</p>")
        self.assertEqual(node2.to_html(), '<a href="https://www.google.com">Testing link</a>')


if __name__ == "__main__":
    unittest.main()
