import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        node4 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        self.assertEqual(node, node2)
        self.assertEqual(node3, node4)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.example.com")
        node3 = TextNode("Thisis a text node", TextType.BOLD)
        node4 = TextNode("This is a text node", TextType.ITALIC)
        node5 = TextNode("This is a link node", TextType.LINK, "https://www.example.com")
        node6 = TextNode("This is a link node", TextType.IMAGE, "https://www.example.com")
        node7 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node, node4)
        self.assertNotEqual(node5, node6)
        self.assertNotEqual(node5, node7)

if __name__ == "__main__":
    unittest.main()