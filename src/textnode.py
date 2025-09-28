from enum import Enum

from leafnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:

    def __init__(self, text: str, texttype: TextType, url: str | None = None):
        """
        Initialize TextNode.

        Args:
            text: Text content of the node
            texttype: Type of text this node contains
            url: URL of the link of image
        """
        self.text = text
        self.texttype = texttype
        self.url = url

    def __eq__(self, other):
        return (
            self.text == other.text
            and self.texttype == other.texttype
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.texttype.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.texttype:
        case TextType.TEXT:
            return LeafNode("", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid TextNode provided")
