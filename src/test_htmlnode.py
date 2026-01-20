import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class testHTMLNode(unittest.TestCase):

    def test_values(self):
        # HTMLNode stores constructor values and defaults.
        node = HTMLNode("p", "This is a Paragraph")
        self.assertEqual(node.tag,"p")
        self.assertEqual(node.value, "This is a Paragraph")
        self.assertEqual(node.children, [])
        self.assertEqual(node.props, {})
    def test_props_to_html(self):
        # props_to_html renders attributes when props exist.
        props = {
            "href": "https://www.matsson.dev",
            "target": "_blank",
        }
        node = HTMLNode("a", "click me", None, props)
        output= node.props_to_html()
        self.assertIn('href="https://www.matsson.dev"', output)
        self.assertIn('target="_blank"', output)
        self.assertTrue(output.startswith(" "))
    def test_repr(self):
        # __repr__ includes tag, value, children, and props.
        node = HTMLNode("h1", "Title", None, {"class": "header"})
        expected = "HTMLNode(h1, Title, children: [], props: {'class': 'header'})"
        self.assertEqual(repr(node), expected)

    def test_to_html_props(self):
        # props_to_html returns an empty string when no props.
        node = HTMLNode("div", "content")
        self.assertEqual(node.props_to_html(), "")

    def test_leaf_to_html_p(self):
        # LeafNode renders a paragraph tag.
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_to_html_h1(self):
        # LeafNode renders a header tag.
        node = LeafNode("h1", "Header")
        self.assertEqual(node.to_html(), "<h1>Header</h1>")

    def test_to_html_not_implemented(self):
        # HTMLNode.to_html is abstract and should raise.
        node = HTMLNode("div", "content")
        with self.assertRaises(NotImplementedError):
            node.to_html()

    def test_leaf_to_html_no_tag(self):
        # LeafNode with no tag returns its value only.
        node = LeafNode(None, "Just text")
        self.assertEqual(node.to_html(), "Just text")

    def test_leaf_to_html_with_props(self):
        # LeafNode renders props in the opening tag.
        node = LeafNode("a", "Link", {"href": "https://example.com"})
        self.assertEqual(node.to_html(), "<a href=\"https://example.com\">Link</a>")

    def test_leaf_requires_value(self):
        # LeafNode allows empty string values.
        node = LeafNode("p", "")
        self.assertEqual(node.to_html(), "<p></p>")

    def test_leaf_requires_value_none(self):
        # LeafNode rejects None values.
        with self.assertRaises(ValueError):
            LeafNode("p", None)

    def test_props_to_html_single_prop(self):
        # props_to_html returns a leading space for a single prop.
        node = HTMLNode("p", "content", None, {"class": "intro"})
        self.assertEqual(node.props_to_html(), " class=\"intro\"")

    def test_parent_to_html_with_children(self):
        # ParentNode renders children in order.
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parent_to_html_with_grandchildren(self):
        # ParentNode renders nested children.
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_requires_children(self):
        # ParentNode rejects empty children.
        with self.assertRaises(ValueError):
            ParentNode("div", [])

    def test_parent_requires_tag(self):
        # ParentNode rejects missing tag.
        with self.assertRaises(ValueError):
            ParentNode(None, [LeafNode("span", "child")])

    def test_parent_to_html_with_props(self):
        # ParentNode includes props in the opening tag.
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(
            parent_node.to_html(),
            "<div class=\"container\"><span>child</span></div>",
        )

    def test_parent_to_html_multiple_children(self):
        # ParentNode renders multiple children in sequence.
        child_one = LeafNode("span", "first")
        child_two = LeafNode("span", "second")
        parent_node = ParentNode("div", [child_one, child_two])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first</span><span>second</span></div>",
        )

    def test_parent_to_html_raises_without_children(self):
        # ParentNode.to_html rejects None children.
        parent_node = ParentNode("div", [LeafNode("span", "child")])
        parent_node.children = None
        with self.assertRaises(ValueError):
            parent_node.to_html()

if __name__ == "__main__":
    unittest.main()
