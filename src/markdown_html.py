from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType, text_node_to_html
from src.inline_markdown import text_to_textnode
from src.markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div", children, None)

def block_to_html_node(block):
    block_type = block_to_block_type(block)
    if block_type == BlockType.PARAGRAPH:
        return block_to_paragraph(block)
    if block_type == BlockType.HEADING:
        return block_to_heading(block)
    if block_type == BlockType.CODE:
        return block_to_code(block)
    if block_type == BlockType.QUOTE:
        return block_to_quote(block)
    if block_type == BlockType.UNORDERED_LIST:
        return block_to_ul(block)
    if block_type == BlockType.ORDERED_LIST:
        return block_to_ol(block)
    raise ValueError("Invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnode(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html(text_node)
        children.append(html_node)
    return children

def block_to_paragraph(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)

def block_to_heading(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if len(block) <= level or block[level] != " ":
        raise ValueError(f"Invalid heading level: {level}")
    text = block[level + 1 :].strip()
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def block_to_code(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")
    text = block[3:-3]
    if text.startswith("\n"):
        text = text[1:]
    code = LeafNode("code", text)
    return ParentNode("pre", [code])

def block_to_quote(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)

def block_to_ul(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)

def block_to_ol(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item.split(". ", 1)[1]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)
