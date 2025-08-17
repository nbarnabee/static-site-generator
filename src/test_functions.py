import unittest
from textnode import TextNode, TextType
from functions import split_nodes_delimiter, text_node_to_html_node

class TestTextNodeToHTML(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def text_ital(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def text_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")

    def text_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://www.example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props_to_html(), 'https="https://www.example.com"')

    def text_img(self):
        node = TextNode("This is an image", TextType.IMG, "picture.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props_to_html(), 'src="https://www.example.com" alt="This is an image"')


class TestDelimiterSplit(unittest.TestCase):
    def type_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text_type.value, "code")
        self.assertEqual(new_nodes[1].text, "code block")

    def type_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node, "**", TextType.BOLD)
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text_type.value, "bold")
        self.assertEqual(new_nodes[1].text, "bold")

    def type_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node, "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text_type.value, "italic")
        self.assertEqual(new_nodes[1].text, "italic")

    def type_mixed(self):
        node = TextNode("This is text with a `code block` and a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter(node, "`", TextType.CODE)
        self.assertEqual(new_nodes[0].text_type.value, "text")
        self.assertEqual(new_nodes[1].text_type.value, "code")
        self.assertTrue("**bold**" in new_nodes[-1].text)
