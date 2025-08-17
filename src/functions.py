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
        if node_type != "text":
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






