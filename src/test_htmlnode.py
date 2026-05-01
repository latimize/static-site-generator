import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode()
        node2 = HTMLNode(None, None, None, {})
        node3 = HTMLNode("a", "click here", None, {"href": "https://www.boot.dev"})
        self.assertEqual(node.props_to_html(), "")
        self.assertEqual(node2.props_to_html(), "")
        self.assertEqual(node3.props_to_html(), ' href="https://www.boot.dev"')

    def test_repr(self):
        node = HTMLNode("a", "click here", None, {"href": "https://www.boot.dev"})
        self.assertEqual(str(node), "HTMLNode(a, click here, None, {'href': 'https://www.boot.dev'})")

    def test_props_to_html_multiple_kvps(self):
        node = HTMLNode("a", "click here", None, {"href": "https://www.boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.boot.dev" target="_blank"')

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click Here!", {"href": "https://www.boot.dev"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev">Click Here!</a>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
    )
        
    def test_to_html_parent_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()
    
    def test_to_html_parent_without_child(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_mutliple_children(self):
        child_node_1 = LeafNode("span", "child")
        child_node_2 = LeafNode("em", "second child")
        child_node_3 = LeafNode("b", "third child")
        parent_node = ParentNode("div", [child_node_1, child_node_2, child_node_3])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><em>second child</em><b>third child</b></div>")

if __name__ == "__main__":
    unittest.main()