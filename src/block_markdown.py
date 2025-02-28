import re
from enum import Enum
from htmlnode import *
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    PARAGRAPH = "paragraph"

def block_to_block_type(block):
    # Check for each block type according to the rules
    # For example, to check if it's a heading:
        # Additional checks to confirm it's a valid heading
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    
    lines = block.strip().splitlines()
    if len(lines) >= 2 and lines[0].startswith("```") and lines[-1] == "```":
        return BlockType.CODE
    
    if all(re.match(r'^>', line) for line in block.splitlines()):
        return BlockType.QUOTE
    
    if all(line.startswith("- ") for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    
    lines = block.splitlines()
    is_ordered = True
    expected_number = 1
    
    for line in lines:
        expected_prefix = f"{expected_number}. "
        if not line.startswith(expected_prefix):
            is_ordered = False
            break
        expected_number += 1
    
    if is_ordered and lines:  # Make sure there's at least one line
        return BlockType.ORDERED_LIST
    
    # If none of the specific types match, it's a paragraph
    return BlockType.PARAGRAPH
        

def markdown_to_blocks(markdown):
    split_blocks = markdown.split("\n\n")
    cleaned_blocks = []
    
    for block in split_blocks:
        # Process each line in the block to remove leading/trailing spaces
        lines = block.strip().split("\n")
        cleaned_lines = [line.strip() for line in lines]
        cleaned_block = "\n".join(cleaned_lines)
        
        if cleaned_block:
            cleaned_blocks.append(cleaned_block)
    
    return cleaned_blocks

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
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")


def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)
    return children


def paragraph_to_html_node(block):
    lines = block.split("\n")
    paragraph = " ".join(lines)
    children = text_to_children(paragraph)
    return ParentNode("p", children)


def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)


def code_to_html_node(block):
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3]
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])
    return ParentNode("pre", [code])


def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ol", html_items)


def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:]
        children = text_to_children(text)
        html_items.append(ParentNode("li", children))
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)





