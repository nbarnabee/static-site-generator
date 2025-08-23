import re
from htmlnode import LeafNode
from textnode import TextNode, TextType


def text_node_to_html_node(text_node):
    if text_node.text_type.value not in TextType:
        raise Exception("Invalid text type given")
    else:
        match text_node.text_type.value:
            case "text":
                return LeafNode(None, text_node.text)
            case "bold":
                return LeafNode("b", text_node.text)
            case "italic":
                return LeafNode("i", text_node.text)
            case "code":
                return LeafNode("code", text_node.text)
            case "link":
                return LeafNode("a", text_node.text, {"href": "text_node.url"})
            case "img":
                return LeafNode("img", None, {"src": "text_node.url", "alt": "text_node.text"})
            case _:
                raise Exception("Invalid text type given")


def split_nodes_delimiter(nodes, delimiter, text_type):
    new_nodes = []
    nodes = nodes if isinstance(nodes, list) else [nodes]
    for node in nodes:
        node_type = node.text_type.value
        if node_type not in TextType:
            raise Exception("Invalid text type given")
        # for now we will disallow nested inline text types
        # or rather we will assume that they don't exist
        if node_type != "text" or delimiter not in node.text:
            new_nodes.append(node)
        else:
            split_nodes = []
            split_node = node.text.split(delimiter)
            # we should end up with an odd number of elements
            if len(split_node)%2 == 0:
                raise Exception("Invalid Markdown syntax: no closing delimiter found")
            else:
                for i in range(len(split_node)):
                    # the elements at odd indices, e.g. 1, 3, 5
                    # are the ones contained within the delimiter blocks
                    if i%2:
                        split_nodes.append(TextNode(split_node[i], text_type))
                    # strip empty sections (e.g., if the text block ends on the delimiter)
                    elif len(split_node[i]):
                        split_nodes.append(TextNode(split_node[i], TextType.TEXT))
            new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text):
    return re.findall(r"\!\[(.*?)\]\((.*?)\)", text)


def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)


def split_nodes_image(nodes):
    new_nodes = []
    nodes = nodes if isinstance(nodes, list) else [nodes]
    for node in nodes:
        split_nodes = []
        if node.text_type not in TextType:
            raise Exception("Invalid text type given")
        images = extract_markdown_images(node.text)
        if len(images) == 0:
            split_nodes.append(node)
        else:
            min_index = 0
            for image in images:
                pattern = f"![{image[0]}]({image[1]})"
                start_index = node.text.index(pattern, min_index)
                if min_index < start_index:
                    split_nodes.append(TextNode(node.text[min_index:start_index], TextType.TEXT))
                split_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                min_index = start_index + len(pattern)
            # if we've run out of images but aren't at the end of the string, there must be more text
            if min_index < len(node.text) - 1:
                split_nodes.append(TextNode(node.text[min_index:], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(nodes):
    new_nodes = []
    nodes = nodes if isinstance(nodes, list) else [nodes]
    for node in nodes:
        split_nodes = []
        if node.text_type not in TextType:
            raise Exception("Invalid text type given")
        links = extract_markdown_links(node.text)
        if len(links) == 0:
            split_nodes.append(node)
        else:
            min_index = 0
            for link in links:
                pattern = f"[{link[0]}]({link[1]})"
                start_index = node.text.index(pattern, min_index)
                if min_index < start_index:
                    split_nodes.append(TextNode(node.text[min_index:start_index], TextType.TEXT))
                split_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                min_index = start_index + len(pattern)
            # if we've run out of images but aren't at the end of the string, there must be more text
            if min_index < len(node.text) - 1:
                print(node.text[min_index:])
                split_nodes.append(TextNode(node.text[min_index:], TextType.TEXT))
        new_nodes.extend(split_nodes)
    return new_nodes


def text_to_textnodes(text):
    delimiters = ["**", "_", "`"]
    text_nodes = split_nodes_delimiter(TextNode(text, TextType.TEXT), "**", TextType.BOLD)
    text_nodes = split_nodes_delimiter(text_nodes, "_", TextType.ITALIC)
    text_nodes = split_nodes_delimiter(text_nodes, "`", TextType.CODE)
    text_nodes = split_nodes_image(text_nodes)
    text_nodes = split_nodes_link(text_nodes)
    return text_nodes