import unittest

from htmlnode import HTMLNode

class testHTMLNode(unittest.TestCase):

    def test_values(self):
        node = HTMLNode("p", "This is a Paragraph")
        self.assertEqual(node.tag,"p")
        self.assertEqual(node.value, "This is a Paragraph")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    def test_props_to_html(self):
        props = {
            "href": "https://www.matsson.dev",
            "target": "_blank",
        }
        node = HTMLNode("a", "click me", None, props)
        output= node.props_to_html()
        self.assertIn('href="https://www.matsson.dev"', output)
        self.assertIn('target="_blank"', output)
    def test_repr(self):
        node = HTMLNode("h1", "Title", None, {"class": "header"})
        expected = "HTMLNode(h1, Title, children: [], props: {'class': 'header'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_props(self):
        node = HTMLNode("div", "content")
        self.assertEqual(node.props_to_html(), "")

if __name__ == "__main__":
    unittest.main()
