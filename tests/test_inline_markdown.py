import unittest
from src.inline_markdown import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    extract_markdown_images,
    extract_markdown_links,
)
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

    def test_extract_markdown_images_basic(self):
        # Basic image markdown extraction
        text = "Here is an image ![alt text](https://example.com/image.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("alt text", "https://example.com/image.png")],
        )

    def test_extract_markdown_links_basic(self):
        # Basic link markdown extraction
        text = "Here is a link [site](https://example.com)"
        self.assertEqual(
            extract_markdown_links(text),
            [("site", "https://example.com")],
        )

    def test_extract_markdown_links_and_images_separate(self):
        # Images and links should be extracted independently
        text = "![logo](/img.png) and [docs](/docs)"
        self.assertEqual(extract_markdown_images(text), [("logo", "/img.png")])
        self.assertEqual(extract_markdown_links(text), [("docs", "/docs")])

    def test_extract_markdown_images_empty_alt(self):
        # Empty alt text is allowed for images
        text = "![](/img.png)"
        self.assertEqual(extract_markdown_images(text), [("", "/img.png")])

    def test_extract_markdown_links_empty_text(self):
        # Empty link text is allowed for links
        text = "[](https://example.com)"
        self.assertEqual(extract_markdown_links(text), [("", "https://example.com")])

    def test_extract_markdown_multiple_matches(self):
        # Multiple matches should be returned in order
        text = "![one](a.png) then [two](b.com) and ![three](c.png)"
        self.assertEqual(
            extract_markdown_images(text),
            [("one", "a.png"), ("three", "c.png")],
        )
        self.assertEqual(extract_markdown_links(text), [("two", "b.com")])

    def test_extract_markdown_no_matches(self):
        # No markdown patterns should return empty lists
        text = "Just plain text without markdown."
        self.assertEqual(extract_markdown_images(text), [])
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_links_not_images(self):
        # Images should not be parsed as links
        text = "![alt](image.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_no_nested_parentheses(self):
        # Nested parentheses should not match current regex
        text = "![alt](https://example.com/(nested))"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_adjacent_text(self):
        # Link parsing should work when adjacent to other text
        text = "before[link](url)after"
        self.assertEqual(extract_markdown_links(text), [("link", "url")])

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )

    def test_split_nodes_image_no_match_single_node(self):
        # No images should return original node once
        node = TextNode("no images here", TextType.TEXT)
        self.assertEqual(split_nodes_image([node]), [node])

    def test_split_nodes_link_no_match_single_node(self):
        # No links should return original node once
        node = TextNode("no links here", TextType.TEXT)
        self.assertEqual(split_nodes_link([node]), [node])

    def test_split_nodes_image_multiple(self):
        # Multiple images should split into alternating nodes
        node = TextNode("a ![one](1.png) b ![two](2.png) c", TextType.TEXT)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.IMAGE, "1.png"),
            TextNode(" b ", TextType.TEXT),
            TextNode("two", TextType.IMAGE, "2.png"),
            TextNode(" c", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_image([node]), expected)

    def test_split_nodes_link_multiple(self):
        # Multiple links should split into alternating nodes
        node = TextNode("a [one](1) b [two](2) c", TextType.TEXT)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("one", TextType.LINK, "1"),
            TextNode(" b ", TextType.TEXT),
            TextNode("two", TextType.LINK, "2"),
            TextNode(" c", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_link([node]), expected)

    def test_split_nodes_image_preserves_non_text_nodes(self):
        # Non-text nodes should pass through unchanged
        nodes = [
            TextNode("bold", TextType.BOLD),
            TextNode("![alt](img.png)", TextType.TEXT),
        ]
        expected = [
            TextNode("bold", TextType.BOLD),
            TextNode("alt", TextType.IMAGE, "img.png"),
        ]
        self.assertEqual(split_nodes_image(nodes), expected)


if __name__ == "__main__":
    unittest.main()
