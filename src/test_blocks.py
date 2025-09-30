from blocks import BlockType, block_to_block_type
from unittest import TestCase


class TestBlocks(TestCase):
    def test_block_to_block_type_heading(self):
        blocks = ["#"*i + " Heading" for i in range(1, 7)]
        for block in blocks:
            self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_code(self):
        block = """```
This is code block.
```"""
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_quote(self):
        block = """> This
> is a
> quote
> block"""
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        block = """- thing 1
- thing 2
- thing 3
- thing 4"""
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. thing 1
2. thing 2
3. thing 3
4. thing 4"""
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_paragraph(self):
        block = """some random stuff
more stuff
even more here"""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
