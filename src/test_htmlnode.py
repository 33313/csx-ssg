import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), 'href="https://www.google.com"')

    def test_leaf(self):
        node = LeafNode("p", "Testing")
        node2 = LeafNode("a", "Testing link", None, {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<p>Testing</p>")
        self.assertEqual(
            node2.to_html(), '<a href="https://www.google.com">Testing link</a>'
        )

    def test_parent(self):
        leaf_list = [
            LeafNode("p", "Testing"),
            LeafNode("a", "Testing link", None, {"href": "https://www.google.com"}),
        ]
        node = ParentNode("div", leaf_list)
        self.assertEqual(
            node.to_html(),
            '<div><p>Testing</p><a href="https://www.google.com">Testing link</a></div>',
        )
        
        node2 = ParentNode("div", [LeafNode("p", "Hi mom")], {"test": "hello"})
        leaf_list2 = [
            LeafNode("p", "Testing"),
            LeafNode("a", "Testing link", None, {"href": "https://www.google.com"}),
            node2
        ]

        node = ParentNode("div", leaf_list2)

        self.assertEqual(
            node.to_html(),
            '<div><p>Testing</p><a href="https://www.google.com">Testing link</a><div test="hello"><p>Hi mom</p></div></div>',
        )


if __name__ == "__main__":
    unittest.main()
