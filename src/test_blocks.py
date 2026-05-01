import unittest

from blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node, extract_title


class TestBlocks(unittest.TestCase):
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

#----------------------------
# BLOCK_TO_BLOCK_TYPE TESTS
#----------------------------

    def test_markdown_to_blocks_empty(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [],
        )

    def test_block_to_block_type_heading(self):
        md_block = "### This is a H3 heading"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.HEADING)
    
    def test_block_to_block_type_invalid_heading(self):
        md_block = "###No space after heading signs"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md_block = "```\nprint('Hello World')\n```"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md_block = ">first quote line\n> second quote line"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_ol(self):
        md_block = "1. First item\n2. Second item\n3. Third item"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)
    
    def test_block_to_block_type_invalid_ol(self):
        md_block = "1. First item\n3. Third item\n2. Second item"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_ul(self):
        md_block = "- First item\n- Second item\n- Third item"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)
    
    def test_block_to_block_type_invalid_ul(self):
        md_block = "- First item\nSecond item\n- Third item"
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_paragraph(self):
        md_block = "Just a paragraph."
        block_type = block_to_block_type(md_block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

#----------------------------
# MARKDOWN_TO_HTML_NODE TESTS
#----------------------------

    def test_paragraphs(self):
        md = """
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
    )

    def test_codeblock(self):
        md = """
        ```
        This is text that _should_ remain
        the **same** even with inline stuff
        ```
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
    )
        
    def test_quotes(self):
        md = """
> To be or not to be...
>That is the question.
> Or maybe not?

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><blockquote>To be or not to be... That is the question. Or maybe not?</blockquote></div>",
    )
        
    def test_ordered_lists(self):
        md = """
1. First list item
2. Second list item
3. Another list item
4. Item
5. Item
6. Item
7. Item
8. Item
9. Item
10. Item
        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ol><li>First list item</li><li>Second list item</li><li>Another list item</li><li>Item</li><li>Item</li><li>Item</li><li>Item</li><li>Item</li><li>Item</li><li>Item</li></ol></div>",
    )

    def test_unordered_lists(self):
        md = """
- list item
- list item
- list item

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><ul><li>list item</li><li>list item</li><li>list item</li></ul></div>",
    )
        
    def test_headings(self):
        md = """
# Main Title

## Subtitle

Paragraph.

        """

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
        html,
        "<div><h1>Main Title</h1><h2>Subtitle</h2><p>Paragraph.</p></div>",
    )
        
    def test_extract_title(self):
        md = """
# This is the main title

This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here
 """
        title = extract_title(md)
        self.assertEqual(title, "This is the main title")
    
    def test_extract_invalid_title(self):
        md = """
#### This is not a H1 heading

 """
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()