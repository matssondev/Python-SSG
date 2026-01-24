from src.htmlnode import HTMLNode, LeafNode, ParentNode
from src.textnode import TextNode, TextType, text_node_to_html
from src.inline_markdown import text_to_textnode
from src.markdown_blocks import markdown_to_blocks, block_to_block_type, BlockType



def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        html_node = block_to_html_node(block)

def block_to_html_node(block):
    pass

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
