from htmlnode import HTMLNode, LeafNode
from textnode import TextNode, TextType

def main():
    node = TextNode("This is some text", TextType.PLAIN, "https://www.example.com")
    print(node)

    html = HTMLNode("a", "A link", None,{"href": "https://www.google.com", "class": "button",})
    print(html)

    leaf = LeafNode("p", "Hello, world!", {"href": "https://www.example.com"})
    print(leaf.tag)
    print(leaf.children)
    print(leaf.props)
    print(leaf.props.items())
    print(leaf.props_to_html())
    print(leaf.to_html())

if __name__ == "__main__":
    main()
