import unittest
from block_functions import BlockType, markdown_to_blocks, block_to_block_type


class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
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

    def test_para_block(self):
        block = "this is a paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_code_block(self):
        block = "```this is a code block\nwith multiple lines```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_not_code_block(self):
        block = "```this is not a code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_also_not_code_block(self):
        block = "````this is also not a code block"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_header_block(self):
        block = "# this is a header"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_not_header_block(self):
        block = "###this is not a header"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block = ">this is a quote\n>with multiple\n>lines"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_not_quote_block(self):
        block = ">this is not a quote\n>with multiple\nlines"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ul_block(self):
        block = "- this is an\n- unordered\n- list"
        self.assertEqual(block_to_block_type(block), BlockType.UL)

    def test_not_ul_block(self):
        block = "- this is not an\n- unordered\n list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_also_not_ul_block(self):
        block = "- this is also not an\n-unordered\n- list"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ol_block(self):
        block = "1. this is an ordered list\n2. with a few \n3. items"
        self.assertEqual(block_to_block_type(block), BlockType.OL)


    def test_not_ol_block(self):
        block = "1. this is not an ordered list\n4. with a few \n3. items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_also_not_ol_block(self):
        block = "1. this is also not an ordered list\n2. with a few \n items"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

if __name__ == "__main__":
    unittest.main()
