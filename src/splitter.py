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


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split provided TextNodes to new TextNodes with TEXT and IMAGE type.
    """
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        images = extract_markdown_images(node.text)
        if not images:
            new_nodes.append(node)
            continue
        text = node.text
        for image_alt, image_link in images:
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """
    Split provided TextNodes to new TextNodes with TEXT and LINK type.
    """
    new_nodes = []
    for node in old_nodes:
        if not node.text:
            continue
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue
        text = node.text
        for link_anchor, link_url in links:
            sections = text.split(f"[{link_anchor}]({link_url})", 1)
            if sections[0]:
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_anchor, TextType.LINK, link_url))
            text = sections[1]
        if text:
            new_nodes.append(TextNode(text, TextType.TEXT))
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


def text_to_textnodes(text: str) -> list[TextNode]:
    return split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([TextNode(text, TextType.TEXT)], "`", TextType.CODE),
                    "_",
                    TextType.ITALIC,
                ),
                "**",
                TextType.BOLD,
            )
        )
    )

def markdown_to_blocks(markdown: str) -> list[str]:
    """
    Take raw markdown text and split it into blocks defined by empty line.
    """
    blocks = markdown.split('\n\n')
    return [block.strip() for block in blocks if block]
