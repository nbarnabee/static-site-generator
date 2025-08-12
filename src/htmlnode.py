class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children = {self.children}, props = {self.props})"

    def to_html(self):
        raise NotImplementedError("This function has not yet been implemented.  Please try again later.")

    def props_to_html(self):
        html_string = ""
        if self.props is not None:
            for key, value in self.props.items():
                html_string += f" {key}=\"{value}\""
        return html_string
