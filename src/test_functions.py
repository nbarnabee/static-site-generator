import unittest
from textnode import TextNode, TextType
from functions import *

class TestFunctions(unittest.TestCase):
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
        print("testing image node")
        node = TextNode("This is an image", TextType.IMG, "picture.jpg")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.props_to_html(), 'src="https://www.example.com" alt="This is an image"')

    def type_code(self):
        print("testing code delimiter")
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

    def test_image_extract(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        self.assertEqual(extract_markdown_images(text), [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_link_extract(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        self.assertEqual(extract_markdown_links(text), [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def singleImgNoExtra(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev)",
            TextType.TEXT,)
        self.assertEqual(split_nodes_image(node), [TextNode("This is text with an image ", TextType.TEXT, None), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")])

    def singleImgOneExtra(self):
        node = TextNode(
              "This is text with an image ![to boot dev](https://www.boot.dev)!",
               TextType.TEXT,)
        self.assertEqual(split_nodes_image(node), [TextNode("This is text with an image ", TextType.TEXT, None), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"), TextNode("!", TextType.TEXT, None)])

    def singleImgSomeExtra(self):
        node = TextNode(
              "This is text with an image ![to boot dev](https://www.boot.dev) with more text!",
               TextType.TEXT,)
        self.assertEqual(split_nodes_image(node), [TextNode("This is text with an image ", TextType.TEXT, None), TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"), TextNode("with more text!", TextType.TEXT, None)])

    def multiImgNoExtraAfter(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and a second ![to boot dev](https://www.boot.dev)",
            TextType.TEXT,)
        self.assertEqual(split_nodes_image(node),
        [TextNode("This is text with an image ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode(" and a second ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        ])

    def multiImgOneExtraAfter(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and a second ![to boot dev](https://www.boot.dev)!",
            TextType.TEXT,)
        self.assertEqual(split_nodes_image(node),
        [TextNode("This is text with an image ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode(" and a second ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode("!", TextType.TEXT, None)
        ])

    def multiImgSomeExtra(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev) and a second ![to boot dev](https://www.boot.dev) happy little image",
            TextType.TEXT,)
        self.assertEqual(split_nodes_image(node),
        [TextNode("This is text with an image ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode(" and a second ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode(" happy little image", TextType.TEXT, None)
        ])

    def noExtraBetweenImg(self):
        print("testing no extra space between images")
        node = TextNode(
            "This is text with adjacent images ![to boot dev](https://www.boot.dev)![to b00t dev](https://www.boot.dev)",
            TextType.TEXT,)
        self.assertEqual(split_nodes_image(node),
        [TextNode("This is text with adjacent images ", TextType.TEXT, None),
        TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
        TextNode("to b00t dev", TextType.IMAGE, "https://www.boot.dev")
        ])


    def singleLinkNoExtra(self):
        print("testing singlenoextra")
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev)",
            TextType.TEXT,)
        self.assertEqual(split_nodes_link(node), [TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")])

    def singleLinkOneExtra(self):
        node = TextNode(
              "This is text with a link [to boot dev](https://www.boot.dev)!",
               TextType.TEXT,)
        self.assertEqual(split_nodes_link(node), [TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode("!", TextType.TEXT, None)])

    def singleLinkSomeExtra(self):
        node = TextNode(
              "This is text with a link [to boot dev](https://www.boot.dev) with more text!",
               TextType.TEXT,)
        self.assertEqual(split_nodes_link(node), [TextNode("This is text with a link ", TextType.TEXT, None), TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"), TextNode("with more text!", TextType.TEXT, None)])

# these are literally the same function; if I really want to I can modify the multi-tester functions later

    def text_to_nodes(self):
        print("testing text to nodes")
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text),
        [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ])


if __name__ == "__main__":
    unittest.main()