import unittest

from htmlnode import *
from textnode import *


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(),  'href="https://www.google.com" target="_blank"')

    def test_repr(self):
        node = HTMLNode(tag="h1", value="Title", children=None, props=None)
        self.assertEqual(repr(node),  'HTMLNode(h1, Title, None, None)')

    def test_repr_leaf(self):
        node = LeafNode(tag="h1", value="Title", props=None)
        self.assertEqual(repr(node),  'HTMLNode(h1, Title, None, None)')

    def test_h1_leaf(self):
        node = LeafNode(tag="h1", value="Title", props=None)
        self.assertEqual(node.to_html(),  '<h1>Title</h1>')

    def test_p_leaf(self):
        node = LeafNode(tag="p", value="""\nThis is a paragraph\nexample\nlol""", props=None)
        self.assertEqual(node.to_html(),  '<p>\nThis is a paragraph\nexample\nlol</p>')

    def test_link_leaf(self):
        node = LeafNode(tag="a", value="Google", props={'href':'https://www.google.com'})
        self.assertEqual(node.to_html(),  '<a href=https://www.google.com>Google</a>')

    def test_img_leaf(self):
        node = LeafNode(tag="img", value="Picture", props={'src':'/url/to/pic.png'})
        self.assertEqual(node.to_html(),  '<img src=/url/to/pic.png alt=Picture>')

    def test_blockquote_leaf(self):
        node = LeafNode(tag="blockquote", value="Title", props=None)
        self.assertEqual(node.to_html(),  '<blockquote>\n\tTitle\n</blockquote>')

    def test_no_value_leaf(self):
        with self.assertRaises(ValueError):
            LeafNode("p").to_html()
    
    def test_img_leaf_error(self):
        node = LeafNode(tag="img", value="Picture", props=None)
        with self.assertRaises(ValueError):
            LeafNode(node.to_html())

    def test_link_leaf_error(self):
        node = LeafNode(tag="a", value="Google", props=None)
        with self.assertRaises(ValueError):
            LeafNode(node.to_html())
    
    def test_wrong_tag_leaf_error(self):
        node = LeafNode(tag="y", value="Google", props=None)
        with self.assertRaises(ValueError):
            LeafNode(node.to_html())

    def test_parent(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>')
    
    def test_parent_tag_error(self):
        node = ParentNode(children=
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_child_error(self):
        node = ParentNode("p")
        with self.assertRaises(ValueError):
            node.to_html()

    def test_parent_nest(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        self.assertEqual(node.to_html(), '<p><b>Bold text</b><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>')

    def test_textnode2htmlnode(self):
        node = LeafNode(tag="a", value="Google", props={'href':'https://www.google.com'})
        tn = TextNode("Google", text_type_link, "https://www.google.com")
        self.assertEqual(node, text_node_to_html_node(tn))


if __name__ == "__main__":
    unittest.main()