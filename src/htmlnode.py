class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError()

    def props_to_html(self):
        if self.props:
            s = ""
            for p in self.props.keys():
                s += f'{p}="{self.props[p]}" '
            return s.strip()

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, children=None, props=None):
        super().__init__(tag, value, children, props)

    def to_html(self):
        if self.tag is None:
            return self.value
        if self.props is None:
            return f"<{self.tag}>{self.value}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag or None, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("ERROR: Parent node requires a tag.")
        if self.children == [] or self.children is None:
            raise ValueError("ERROR: Parent node has no children.")

        s = ""
        for x in self.children:
            s += x.to_html()
        if self.props is None:
            return f"<{self.tag}>{s}</{self.tag}>"
        return f"<{self.tag} {self.props_to_html()}>{s}</{self.tag}>"


