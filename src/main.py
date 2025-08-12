from htmlnode import HTMLNode
from textnode import TextNode, TextType

def main():
    node = TextNode("This is some text", TextType.PLAIN, "https://www.example.com")
    print(node)

    html = HTMLNode("a", "A link", None,{"href": "https://www.google.com", "class": "button",})
    print(html)

if __name__ == "__main__":
    main()
