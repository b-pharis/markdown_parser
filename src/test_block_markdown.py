import unittest
from block_markdown import markdown_to_blocks, block_to_block_type, BlockType

class TestMarkdowntoBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph

    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line

    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

class TestBlockTypeIdentification(unittest.TestCase):
    
    def test_heading(self):
        # Test valid headings
        self.assertEqual(block_to_block_type("# Heading 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Heading 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Heading 6"), BlockType.HEADING)
        
        # Test invalid headings
        self.assertEqual(block_to_block_type("####### Too many"), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type("#No space"), BlockType.PARAGRAPH)
    
    def test_code_block(self):
        self.assertEqual(block_to_block_type("```\ncode here\n```"), BlockType.CODE)
        self.assertEqual(block_to_block_type("```python\ndef func():\n    pass\n```"), BlockType.CODE)
        
        # Test invalid code block
        self.assertEqual(block_to_block_type("```\nunclosed code block"), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()