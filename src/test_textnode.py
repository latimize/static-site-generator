import unittest

from textnode import TextNode, TextType, text_node_to_html_node
from inline_markdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_texttype_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_url_None(self):
        node = TextNode("This is a text node", TextType.BOLD, None)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_url_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://github.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertNotEqual(node, node2)
    
    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is another text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")
    
    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")
    
    def test_code(self):
        node = TextNode("This is code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is code text node")
    
    def test_link(self):
        node = TextNode("This is a link node", TextType.LINK, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://www.boot.dev", "alt": "This is an image node"})

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

if __name__ == "__main__":
    unittest.main()