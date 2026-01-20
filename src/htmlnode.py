class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props if props is not None else {}

    def to_html(self):
        raise NotImplementedError
    def props_to_html(self):
        if not self.props:
            return ""
        attributes = [f'{key}="{value}"' for key, value in self.props.items()]
        return " " + " ".join(attributes)

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, props: {self.props})"

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        if value is None:
            raise ValueError("LeafNode must have a non-empty value")

        super().__init__(tag, value, None, props)
    
    def to_html(self):
        if self.value is None:
            raise ValueError("All leaf nodes must have a value")
        if self.tag == None:
            return self.value
        props_html = self.props_to_html()
        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"
    
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, props: {self.props})"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        if not tag or not children:
            raise ValueError("All parent nodes must have non-empty tag and children")

        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Invalid HTML: ParentNode must have a tag")
        if self.children is None:
            raise ValueError("Invalid HTML: ParentNode must have children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"
