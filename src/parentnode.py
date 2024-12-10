from htmlnode import HTMLNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag is required for ParentNode")
        if self.children is None:
            raise ValueError("Children are required for ParentNode")

        return f"<{self.tag}{self.props_to_html()}>{self.children_to_html(self.children)}</{self.tag}>"

    def children_to_html(self, children):
        html = ""
        if children is None or len(children) == 0:
            return ""
        html += children[0].to_html() + self.children_to_html(children[1:])
        return html;
