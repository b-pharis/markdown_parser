import re
from enum import Enum

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
