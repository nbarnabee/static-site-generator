from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from functions import *


def main():
    node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
    new_nodes = split_nodes_image([node])
    print(new_nodes)

if __name__ == "__main__":
    main()
