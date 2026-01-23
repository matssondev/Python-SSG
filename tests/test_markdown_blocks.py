import unittest

from src.markdown_blocks import markdown_to_blocks


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


if __name__ == "__main__":
    unittest.main()
