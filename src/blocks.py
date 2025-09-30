from enum import Enum
import re


HEADING_REGEX = re.compile(r"^\#{1,6}\ ")

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def block_to_block_type(block: str) -> BlockType:
    """
    Take string with a single block and return corresponding BlockType object.
    """
    if re.match(HEADING_REGEX, block):
        return BlockType.HEADING
    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    block_lines = block.splitlines()
    if all([line.startswith(">") for line in block_lines]):
        return BlockType.QUOTE
    if all([line.startswith("- ") for line in block_lines]):
        return BlockType.UNORDERED_LIST
    if all([line.startswith(f"{i}. ") for i, line in enumerate(block_lines, start=1)]):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
