import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        html1 = HTMLNode("a", None, None, {"href": "https://www.example.com"})
        expected1 = ' href="https://www.example.com"'
        self.assertEqual(html1.props_to_html(), expected1)