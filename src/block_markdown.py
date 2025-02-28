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

'''def markdown_to_HTML_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_types = []
    nodes = []
    #iterate over each block and assign the type of block it is
    for item in blocks:
        block_types.append(block_to_block_type(item))
    
    zipped_blocks = zip(blocks, block_types)
    for block, type in zipped_blocks:
        if type == BlockType.HEADING:
            head_parts = block.split(" ", 1)
            number_headings = len(head_parts[0])
            if len(head_parts) == 1:  # No content after the # symbols
                head_parts.append("")  # Default to an empty string
            if number_headings >= 1 and number_headings <= 6 and head_parts[1]:
                nodes.append(HTMLNode(f"<h{number_headings}>", head_parts[1]))

        if type == BlockType.CODE:
            code_parts = block.split("```", 1)
            if len(code_parts) > 1:
                # Extract and clean the code content
                code_text = code_parts[1].strip()  # Remove leading/trailing newlines or spaces
                
                # Create the nested structure: <pre> -> <code>
                code_node = HTMLNode("<code>", code_text)  # Inner node
                pre_node = HTMLNode("<pre>", children=[code_node])  # Outer node
                
                # Add the <pre> node to the list
                nodes.append(pre_node)

        if type == BlockType.QUOTE:
            # Remove the leading '>' and any whitespace
            quote_text = block.lstrip("> ").strip()
            
            # Create the <blockquote> node
            quote_node = HTMLNode("<blockquote>", quote_text)
            
            # Append quote_node to the list of nodes
            nodes.append(quote_node)

        if type == BlockType.UNORDERED_LIST:
            # Split the block into separate lines
            u_list_line = block.splitlines()

            # Create an empty list to hold child <li> nodes
            li_nodes = []

            
            for line in u_list_line:
                # Strip the "-" marker and leading/trailing whitespaces
                line_text = line.strip("- ").strip()

                # Add the cleaned text into an <li> node
                li_nodes.append(HTMLNode("<li>", line_text))

            # Wrap all <li> nodes insides a <ul> node
            ul_nodes = HTMLNode("<ul>", children=li_nodes)

            # Add the <ul> node to the list of nodes
            nodes.append(ul_nodes)

        if type == BlockType.ORDERED_LIST:
            # Split the block into separate lines
            o_list_lines = block.splitlines()

            # Create an empty list to hold child <li>
            li_nodes = []

            for line in o_list_lines:
                # Split at the first occurrence of ". " to remove the numbering
                if ". " in line:
                    line_text = line.split(". ", 1)[1].strip()
                else:
                    # Handle edge cases: lines without numbering
                    line_text = line.strip()

                # Add the cleaned text into an <li> node
                li_nodes.append(HTMLNode("<li>", line_text))

            ol_nodes = HTMLNode("<ol>", children=li_nodes)

            nodes.append(ol_nodes)

                # Wrap all nodes in a parent <div>
        parent_node = HTMLNode("<div>", children=nodes)

        # Return the parent <div> node
        return parent_node'''





