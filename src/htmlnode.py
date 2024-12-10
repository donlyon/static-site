class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if self.props == None:
            return ""
        result = ""
        for k,v in self.props.items():
            result += f' {k}="{v}"'
        return result

    def __repr__(self):
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

