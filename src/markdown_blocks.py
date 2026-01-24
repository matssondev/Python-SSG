from enum import Enum
from src.htmlnode import HTMLNode

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    cleaned_blocks = []
    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        cleaned_blocks.append(block)
    return cleaned_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)

def block_to_html_code(block):
    pass

def text_to_children(text):
    pass

def paragraph_to_html_node(block):
    pass

def heading_to_html_node(block):
    pass

def code_to_html_node(block):
    pass

def ol_to_html_node(block):
    pass

def ul_to_html_node(block):
    pass

def quote_to_html_node(block):
    pass
