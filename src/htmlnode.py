from typing import Dict, List


class HTMLNode:

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: List["HTMLNode"] | None = None,
        props: Dict[str, str] | None = None,
    ):
        """
        Initialize HTMLNode.

        Args:
            tag: HTML tag name
            value: Value of the HTML tag
            children: List of children nodes
            props: HTML attributes of the tag
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props:
            for k, v in self.props.items():
                result += f' {k}="{v}"'
        return result

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props}"
