import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html1 = HTMLNode("a", None, None, {"href": "https://www.example.com"})
        expected1 = ' href="https://www.example.com"'
        self.assertEqual(html1.props_to_html(), expected1)


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        big_node = LeafNode("a", "Click me", {"href": "https://www.example.com", "class": "button"})
        self.assertEqual(big_node.to_html(), "<a href=\"https://www.example.com\" class=\"button\">Click me</a>")