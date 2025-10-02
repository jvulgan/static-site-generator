from blocks import block_to_block_type, BlockType
from leafnode import LeafNode
from parentnode import ParentNode
from splitter import markdown_to_blocks, text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType


def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Convert markdown doc to HTML ParentNode with children
    """
    # split raw markdown to text blocks
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            children.append(handle_paragraph(block))
        elif block_type == BlockType.QUOTE:
            children.append(handle_quote(block))
        elif block_type == BlockType.HEADING:
            children.append(handle_heading(block))
        elif block_type in (BlockType.UNORDERED_LIST, BlockType.ORDERED_LIST):
            children.append(handle_lists(block, block_type))
        elif block_type == BlockType.CODE:
            children.append(handle_code(block))
        else:
            raise Exception(
                f"got unexpected block type {block_type.value} in markdown_to_html_node"
            )
    return ParentNode("div", children)


def handle_paragraph(block: str) -> ParentNode:
    children = text_to_children(" ".join(block.split("\n")))
    return ParentNode("p", children)


def handle_quote(block: str) -> ParentNode:
    lines = [line.lstrip(">").strip() for line in block.split("\n")]
    children = text_to_children(" ".join(lines))
    return ParentNode("blockquote", children)


def handle_heading(block: str) -> ParentNode:
    nr_of_hashes = 0
    for char in block:
        if char != "#":
            break
        nr_of_hashes += 1
    children = text_to_children(block[nr_of_hashes + 1 :])
    return ParentNode(f"h{nr_of_hashes}", children)


def handle_lists(block: str, block_type: BlockType) -> ParentNode:
    def create_line_children(block: str, nr: int) -> list[ParentNode]:
        children = []
        for line in block.split("\n"):
            line_children = text_to_children(line[nr:])
            children.append(ParentNode("li", line_children))
        return children

    if block_type == BlockType.UNORDERED_LIST:
        return ParentNode("ul", create_line_children(block, 2))
    if block_type == BlockType.ORDERED_LIST:
        return ParentNode("ol", create_line_children(block, 3))
    else:
        raise Exception(f"got unexpected block type {BlockType.value} in handle_lists")


def handle_code(block: str) -> ParentNode:
    block = block.strip("```").lstrip("\n")
    code_node = text_node_to_html_node(TextNode(block, TextType.CODE))
    return ParentNode("pre", [code_node])


def text_to_children(text: str) -> list[LeafNode]:
    """
    Convert text to a list of children LeafNodes.
    """
    return [text_node_to_html_node(textnode) for textnode in text_to_textnodes(text)]
