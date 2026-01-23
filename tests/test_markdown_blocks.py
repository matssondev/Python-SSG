import unittest

from src.markdown_blocks import markdown_to_blocks, BlockType, block_to_block_type


class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks_paragraphs_and_list(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "Just a single paragraph without blank lines"
        self.assertEqual(markdown_to_blocks(md), [md])

    def test_markdown_to_blocks_trims_whitespace(self):
        md = "\n\n  First block with padding  \n\nSecond block\n\n"
        self.assertEqual(
            markdown_to_blocks(md),
            ["First block with padding", "Second block"],
        )

    def test_markdown_to_blocks_ignores_empty_blocks(self):
        md = "First\n\n\n\nSecond"
        self.assertEqual(markdown_to_blocks(md), ["First", "Second"])

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_headings(self):
        block = "# Heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

        block = "#Heading"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_code_blocks(self):
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

        block = "```\ncode"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_quotes(self):
        block = "> quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

        block = "> quote\nnot quote"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_lists(self):
        block = "- one\n- two"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

        block = "- one\n* two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_ordered_lists(self):
        block = "1. one\n2. two"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

        block = "1. one\n3. three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
