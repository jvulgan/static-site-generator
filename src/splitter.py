import re
from textnode import TextType, TextNode


IMAGE_REGEX = re.compile(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)")
LINK_REGEX = re.compile(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)")


class InvalidMarkdownError(Exception):
    pass


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """
    Split provided TextNodes based on provided delimiter and text_type.

    Args:
        old_node: List of TextNodes to be processed
        delimiter: Markdown delimiter based on which splitting happens
        text_type: TextType associated with provided delimiter
    """
    new_nodes = []
    for node in old_nodes:
        if node.texttype != TextType.TEXT:
            new_nodes.append(node)
            continue
        splitted = node.text.split(delimiter)
        if len(splitted) % 2 == 0:
            raise InvalidMarkdownError("no closing delimiter detected")
        for idx, text in enumerate(splitted):
            if idx % 2 != 0:
                new_node = TextNode(text, text_type)
            elif text:
                new_node = TextNode(text, TextType.TEXT)
            else:
                # empty string text
                continue
            new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text: str) -> list[tuple]:
    """
    Extract markdown images from raw text and return a list of tuples (alt_text, url).
    """
    return re.findall(IMAGE_REGEX, text)


def extract_markdown_links(text: str) -> list[tuple]:
    """
    Extract markdown links from raw text and return a list of tuples (anchor_text, url).
    """
    return re.findall(LINK_REGEX, text)
