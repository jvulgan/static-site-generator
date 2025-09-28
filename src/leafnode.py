from htmlnode import HTMLNode

from typing import Dict


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: Dict[str, str] | None = None):
        super().__init__(tag, value, None, props)

    def to_html(self) -> str:
        if not self.value:
            raise ValueError("LeafNode must have value populated")
        if not self.tag:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
