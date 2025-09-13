from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from inline_functions import *
from block_functions import *


def main():
    block = "######## This is a paragraph\n> This should be right`"
    print(block_to_block_type(block))

if __name__ == "__main__":
    main()
