from textnode import TextType, TextNode


class InvalidMarkdownError(Exception):
    pass


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
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
            raise InvalidMarkdownError('no closing delimiter detected')
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

