import unittest

from src.markdown_html import markdown_to_html_node


class TestMarkdownHtml(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = """
# Heading with **bold** text
### Subheading with _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Heading with <b>bold</b> text</h1><h3>Subheading with <i>italic</i></h3></div>",
        )

    def test_unordered_list(self):
        md = """
- First item
- Second with _italic_
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>First item</li><li>Second with <i>italic</i></li></ul></div>",
        )

    def test_ordered_list(self):
        md = """
1. First item
2. Second with **bold**
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First item</li><li>Second with <b>bold</b></li></ol></div>",
        )

    def test_blockquote(self):
        md = """
> This is a quote
> with two lines and `code`
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with two lines and <code>code</code></blockquote></div>",
        )

    def test_mixed_blocks(self):
        md = """
# Title

Paragraph line one
line two

- Item A
- Item B
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>Title</h1><p>Paragraph line one line two</p><ul><li>Item A</li><li>Item B</li></ul></div>",
        )

    def test_paragraph_line_joining(self):
        md = """
Line one
line two
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>Line one line two</p></div>",
        )


if __name__ == "__main__":
    unittest.main()
