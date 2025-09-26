from enum import Enum


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
            self.text == other.text and
            self.texttype == other.texttype and
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.texttype.value}, {self.url})"
