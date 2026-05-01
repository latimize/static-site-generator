import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes


class TestInlineMarkDown(unittest.TestCase):
    def test_split_nodes_wrong_syntax(self):
        old_nodes = [TextNode("This is **bold text", TextType.TEXT)]
        with self.assertRaises(Exception):
            split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
            
    
    def test_split_nodes_bold(self):
        old_nodes = [TextNode("This is **bold text**", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                         [TextNode("This is ", TextType.TEXT),
                          TextNode("bold text", TextType.BOLD)  
                          ])

    def test_split_nodes_italic(self):
        old_nodes = [TextNode("This is text with _italic words_ inside", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)
        self.assertEqual(new_nodes, 
                         [TextNode("This is text with ", TextType.TEXT),
                          TextNode("italic words", TextType.ITALIC), 
                          TextNode(" inside", TextType.TEXT)  
                          ])
    
    def test_split_nodes_code(self):
        old_nodes = [TextNode("This is text with a `code block` inside it.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                         [TextNode("This is text with a ", TextType.TEXT),
                          TextNode("code block", TextType.CODE), 
                          TextNode(" inside it.", TextType.TEXT)  
                          ])
        
    def test_split_nodes_multiple_bold(self):
        old_nodes = [TextNode("This is **text** with two **bold** words", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
                         [TextNode("This is ", TextType.TEXT),
                          TextNode("text", TextType.BOLD), 
                          TextNode(" with two ", TextType.TEXT), 
                          TextNode("bold", TextType.BOLD), 
                          TextNode(" words", TextType.TEXT)  
                          ])
    
    def test_split_nodes_text(self):
        old_nodes = [TextNode("This is just plain text", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                         [TextNode("This is just plain text", TextType.TEXT)  
                          ])
        
    def test_split_nodes_multiple_delimiters(self):
        old_nodes = [TextNode("This is a text with **bold words**, _italic words_, and a `block of code`.", TextType.TEXT)]
        new_nodes = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        new_nodes = split_nodes_delimiter(new_nodes, "`", TextType.CODE)
        self.assertEqual(new_nodes, 
                         [TextNode("This is a text with ", TextType.TEXT), 
                         TextNode("bold words", TextType.BOLD), 
                         TextNode(", ", TextType.TEXT), 
                         TextNode("italic words", TextType.ITALIC), 
                         TextNode(", and a ", TextType.TEXT), 
                         TextNode("block of code", TextType.CODE), 
                         TextNode(".", TextType.TEXT)]
                         )
    
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
        "This is text with an [link](https://i.imgur.com/zjjcJKZ.png)"
    )
        self.assertListEqual([("link", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_split_images(self):
        node = TextNode(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode(
                "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
            ),
        ],
        new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
        "This is text with a [link](https://www.boot.dev) and [another link](https://www.google.com)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "another link", TextType.LINK, "https://www.google.com"
            ),
        ],
        new_nodes,
        )
    
    def test_split_no_images(self):
        node = TextNode(
        "This is text with no image at all",TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("This is text with no image at all", TextType.TEXT),
        ],
        new_nodes,
        )
    
    def test_split_no_links(self):
        node = TextNode(
        "This is text with no links at all",TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("This is text with no links at all", TextType.TEXT),
        ],
        new_nodes,
        )
    
    def test_split_only_image(self):
        node = TextNode(
        "![image](https://i.imgur.com/zjjcJKZ.png)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
        [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ],
        new_nodes
        )
    
    def test_split_only_link(self):
        node = TextNode(
        "[link](https://www.boot.dev)",
        TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
        [
            TextNode("link", TextType.LINK, "https://www.boot.dev")
        ],
        new_nodes
        )

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], nodes)
    
    def test_text_to_textnodes_only_text(self):
        text = "This is just text without anything special"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is just text without anything special", TextType.TEXT)
        ], nodes)

    def test_text_to_textnodes_only_image(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ], nodes)

    def test_text_to_textnodes_only_link(self):
        text = "[link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], nodes)

    def test_text_to_textnodes_italic_first(self):
        text = "This is _italic text_ with a **bold** word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertEqual([
            TextNode("This is ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ], nodes)


if __name__ == "__main__":
    unittest.main()