from htmlnode import HTMLNode

from typing import Dict, List


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: List[HTMLNode], props: Dict[str, str] | None = None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if not self.tag:
            raise ValueError("ParentNode must have tag populated")
        if not self.children:
            raise ValueError("ParentNode must have children populated")
        child_text = ""
        for child in self.children:
            child_text += child.to_html()
        return f"<{self.tag}>{child_text}</{self.tag}>"
