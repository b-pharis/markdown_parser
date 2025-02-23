import re
from textnode import *

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            text = node.text
            delimiter_index = text.find(delimiter)
            if delimiter_index == -1:
                # No delimiter found, keep node as-is
                new_nodes.append(node)
            else:
                # Find closing delimiter
                closing_index = text.find(delimiter, delimiter_index + len(delimiter))
                if closing_index == -1:
                    raise Exception("Closing delimiter not found")
                before = text[:delimiter_index]
                middle = text[delimiter_index + len(delimiter):closing_index]
                after = text[closing_index + len(delimiter):]
                
                # Create new nodes with the correct types
                if before:
                    new_nodes.append(TextNode(before, TextType.TEXT))
                if middle:
                    new_nodes.append(TextNode(middle, text_type))
                if after:
                    new_nodes.append(TextNode(after, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        links = extract_markdown_links(node.text)
        if not links:
            new_nodes.append(node)
            continue

        text = node.text
        for link_text, url in links:
            # Split around the markdown link pattern
            parts = text.split(f"[{link_text}]({url})", 1)
            
            # If there's text before the link, create a text node
            if parts[0]:
                new_nodes.append(TextNode(parts[0], TextType.TEXT))
                
            # Create the link node
            new_nodes.append(TextNode(link_text, TextType.LINK, url))
            
            # The remaining text becomes our new text to process
            text = parts[1]

            if text:
                new_nodes.append(TextNode(text, TextType.TEXT))

    return new_nodes
        
def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
            continue
        original_text = old_node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
       
def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)