import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        # TextNode equality matches text and type.
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
        node = TextNode("Testing repr", TextType.CODE, "https://matsson.dev")
        expected = "TextNode(Testing repr, code, https://matsson.dev)"
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

if __name__ == "__main__":
    unittest.main()
