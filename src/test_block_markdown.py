import unittest
from block_markdown import BlockType, block_to_block_type, markdown_to_blocks


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_blocks(self):
        test = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        res = markdown_to_blocks(test)
        eq = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertEqual(res, eq)

    def test_block_type_heading(self):
        valid = "# This is a heading"
        invalid = "####### This is not a heading"
        res_valid = block_to_block_type(valid)
        res_invalid = block_to_block_type(invalid)
        self.assertEqual(res_valid, BlockType.HEADING)
        self.assertEqual(res_invalid, BlockType.PARAGRAPH)

    def test_block_type_code(self):
        valid = "```This is a code block```"
        invalid = "``This is not a code block``"
        res_valid = block_to_block_type(valid)
        res_invalid = block_to_block_type(invalid)
        self.assertEqual(res_valid, BlockType.CODE)
        self.assertEqual(res_invalid, BlockType.PARAGRAPH)

    def test_block_type_quote(self):
        valid = ">This is a quote.\n>This is still a quote.\n>Yep, looks like a quote to me!"
        invalid = ">This could be a quote;\nAlas, it is not.\n>How unfortunate."
        res_valid = block_to_block_type(valid)
        res_invalid = block_to_block_type(invalid)
        self.assertEqual(res_valid, BlockType.QUOTE)
        self.assertEqual(res_invalid, BlockType.PARAGRAPH)

    def test_block_type_unordered_list(self):
        valid = "- This is a list\n- It isn't ordered\n- It works just fine."
        invalid = "* This could've been a list.\nAlas, it is not.\n-A tragedy."
        res_valid = block_to_block_type(valid)
        res_invalid = block_to_block_type(invalid)
        self.assertEqual(res_valid, BlockType.UNORDERED_LIST)
        self.assertEqual(res_invalid, BlockType.PARAGRAPH)

    def test_block_type_ordered_list(self):
        valid = "1.In a world filled with\n2. misery and uncertainty\n3. it is a great comfort"
        invalid = "3. To know that\n4. In the end\n5. There is a light in the darkness."
        res_valid = block_to_block_type(valid)
        res_invalid = block_to_block_type(invalid)
        self.assertEqual(res_valid, BlockType.ORDERED_LIST)
        self.assertEqual(res_invalid, BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()
