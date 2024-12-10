from htmlnode import HTMLNode

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("LeafNode must have a value.")
        if self.tag is None:
            return self.value
        return "<{0}{1}>{2}</{0}>".format(self.tag, self.props_to_html(), self.value)

    def __str__(self):
        return "<{0}{1}>{2}</{0}>".format(self.tag, self.props_to_html(), self.value)
