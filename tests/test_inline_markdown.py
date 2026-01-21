import unittest
from src.inline_markdown import split_nodes_delimiter
from src.textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_split_nodes_delimiter_basic(self):
        # Basic formatting: middle of text
        node = TextNode("This is `code` node", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" node", TextType.TEXT),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_multiple(self):
        # Multiple delimiters in one node
        node = TextNode("This is **bold** and **more bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_start_end(self):
        # Delimiters at the very start and end
        node = TextNode("`code` at start and end `more code`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" at start and end ", TextType.TEXT),
            TextNode("more code", TextType.CODE),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_plain(self):
        # Plain text with no delimiters
        node = TextNode("Plain text with no special chars", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("Plain text with no special chars", TextType.TEXT)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_error(self):
        # Missing closing delimiter raises ValueError
        node = TextNode("This has no closing **bold", TextType.TEXT)
        with self.assertRaises(ValueError) as cm:
            split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(str(cm.exception), "Markdown Error: No closing '**' found.")

    def test_split_nodes_delimiter_mixed_input(self):
        # Input list containing non-TEXT nodes
        nodes = [
            TextNode("text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        expected = [
            TextNode("text", TextType.TEXT),
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_full(self):
        # Entire string is delimited
        node = TextNode("**bold**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected = [TextNode("bold", TextType.BOLD)]
        self.assertEqual(new_nodes, expected)

    def test_split_nodes_delimiter_sequential(self):
        # Sequential calls for different delimiter types
        node = TextNode("This is **bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
        ]
        self.assertEqual(new_nodes, expected)


if __name__ == "__main__":
    unittest.main()
