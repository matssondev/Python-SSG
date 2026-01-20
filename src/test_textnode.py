import unittest

from textnode import TextNode, TextType, text_node_to_html


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # TextNode equality matches text and type.
        # Ensures __eq__ ignores object identity.
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        # TextNode inequality when text or type differ.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a code node", TextType.CODE)
        self.assertNotEqual(node, node2)
    def test_eq_false(self):
        # TextNode inequality when text differs.
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)
    def test_url_none(self):
        # URL defaults to None when omitted.
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)
    def test_repr(self):
        # __repr__ includes text, type value, and url.
        node = TextNode("Testing repr", TextType.CODE, "https://example.com")
        expected = "TextNode(Testing repr, code, https://example.com)"
        self.assertEqual(repr(node), expected)

    def test_url_not_equal(self):
        # TextNode inequality when url differs.
        node = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK, "https://example.org")
        self.assertNotEqual(node, node2)

    def test_url_none_not_equal(self):
        # TextNode inequality when one url is missing.
        node = TextNode("Link", TextType.LINK, "https://example.com")
        node2 = TextNode("Link", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_text(self):
        # TEXT creates a raw text LeafNode.
        node = TextNode("Hello", TextType.TEXT)
        html_node = text_node_to_html(node)
        self.assertIsNone(html_node.tag)
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_bold(self):
        # BOLD creates a <b> LeafNode.
        node = TextNode("Hello", TextType.BOLD)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_italic(self):
        # ITALIC creates an <i> LeafNode.
        node = TextNode("Hello", TextType.ITALIC)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_code(self):
        # CODE creates a <code> LeafNode.
        node = TextNode("Hello", TextType.CODE)
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {})

    def test_text_node_to_html_link(self):
        # LINK creates an <a> LeafNode with href.
        node = TextNode("Hello", TextType.LINK, "https://example.com")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Hello")
        self.assertEqual(html_node.props, {"href": "https://example.com"})

    def test_text_node_to_html_image(self):
        # IMAGE creates an <img> LeafNode with src and alt.
        node = TextNode("Alt", TextType.IMAGE, "https://example.com/img.png")
        html_node = text_node_to_html(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://example.com/img.png", "alt": "Alt"},
        )

    def test_text_node_to_html_invalid_type(self):
        # Invalid type raises an error.
        with self.assertRaises(ValueError):
            text_node_to_html(TextNode("Hello", "invalid"))

if __name__ == "__main__":
    unittest.main()
