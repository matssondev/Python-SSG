import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    def test_noteq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a code node", TextType.CODE)
        self.assertNotEqual(node, node2)
    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
    def test_url_none(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertIsNone(node.url)
    def test_repr(self):
        node = TextNode("Testing repr", TextType.CODE, "https://matsson.dev")
        expected = "TextNode(Testing repr, code, https://matsson.dev)"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
