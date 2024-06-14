import unittest

from textnode import *

class TestTextNode(unittest.TestCase):

    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node", text_type_bold)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", text_type_text)
        node2 = TextNode("This is a text node2", text_type_text)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", text_type_italic, "https://www.boot.dev")
        node2 = TextNode(
            "This is a text node", text_type_italic, "https://www.boot.dev"
        )
        self.assertEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", text_type_text, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

    def test_split_nodes_delimiter_1(self):
        node = TextNode("This is `code` example", "text")
        self.assertEqual(
                    split_nodes_delimiter([node], "`", "code"), 
                    [
                        TextNode("This is ", "text"),
                        TextNode("code", "code"),
                        TextNode(" example", "text")
                    ]
                )
        
    def test_split_nodes_delimiter_2(self):
        node = TextNode("This is `code` example `lol`", "text")
        self.assertEqual(
                    split_nodes_delimiter([node], "`", "code"), 
                    [
                        TextNode("This is ", "text"),
                        TextNode("code", "code"),
                        TextNode(" example ", "text"),
                        TextNode("lol", "code")
                    ]
                )
        
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_images(text), 
                         [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")])
    
    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        self.assertEqual(extract_markdown_links(text), [("link", "https://www.example.com"), ("another", "https://www.example.com/another")])
    
    def test_extract_markdown_links2(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_split_image(self):
        node = TextNode(
                    "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                    text_type_text,
                )
        self.assertEqual(split_nodes_image([node]), 
                [
                    TextNode("This is text with an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and another ", text_type_text),
                    TextNode(
                        "second image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"
                    ),
                ]
            )
        
    def test_split_link(self):
        node = TextNode(
                    "This is text with a [link1](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                    text_type_text,
                )
        self.assertEqual(split_nodes_link([node]), 
                [
                    TextNode("This is text with a ", text_type_text),
                    TextNode("link1", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", text_type_text)
                ]
            )

    def test_split_link2(self):
        node = TextNode(
                    "[link1](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
                    text_type_text,
                )
        self.assertEqual(split_nodes_link([node]), 
                [
                    TextNode("link1", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)", text_type_text)
                ]
            )
    
    def test_split_link3(self):
        node = TextNode(
                    "[link1](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                    text_type_text
                )
        self.assertEqual(split_nodes_link([node]), 
                [
                    TextNode("link1", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
                ]
            )
    
    def test_split_link_empty(self):
        node = TextNode(
                    "![IMAGE](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                    text_type_text
                )
        self.assertEqual(split_nodes_link([node]), 
                [
                    TextNode("![IMAGE](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", text_type_text)
                ]
            )
    
    def test_split_image2(self):
        node = TextNode(
                    "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                    text_type_text,
                )
        self.assertEqual(split_nodes_image([node]), 
                [
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png")
                ]
            )
    
    def test_split_image_empty(self):
        node = TextNode(
                    "[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)",
                    text_type_text,
                )
        self.assertEqual(split_nodes_image([node]), 
                [
                    TextNode("[image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png)", text_type_text)
                ]
            )
    
    def test_text2textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), 
                [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_bold),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_italic),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_code),
                    TextNode(" and an ", text_type_text),
                    TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_link, "https://boot.dev"),
                ]
            ) 
        
    def test_text2textnode_2(self):
        text = "This is **text* with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), 
                [
                    TextNode("This is ", text_type_text),
                    TextNode("text* with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)", text_type_bold)
                ]
            )
        
    def test_text2textnode_3(self):
        text = "This is *text* with an `italic` word and a **code block** and an [image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a ![link](https://boot.dev)"
        self.assertEqual(text_to_textnodes(text), 
                [
                    TextNode("This is ", text_type_text),
                    TextNode("text", text_type_italic),
                    TextNode(" with an ", text_type_text),
                    TextNode("italic", text_type_code),
                    TextNode(" word and a ", text_type_text),
                    TextNode("code block", text_type_bold),
                    TextNode(" and an ", text_type_text),
                    TextNode("image", text_type_link, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                    TextNode(" and a ", text_type_text),
                    TextNode("link", text_type_image, "https://boot.dev"),
                ]
            )

    def test_text2textnode_4(self):
        text = "This is text with an italic word and a code block and an image https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png and a link https://boot.dev"
        self.assertEqual(text_to_textnodes(text), 
                [
                    TextNode("This is text with an italic word and a code block and an image https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png and a link https://boot.dev", text_type_text)
                ]
            )

    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        self.assertEqual(markdown_to_blocks(markdown), 
                [
                    "This is **bolded** paragraph",
                    """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
                    """* This is a list
* with items"""
                ]
            )
    
    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

        
This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        self.assertEqual(markdown_to_blocks(markdown), 
                [
                    "This is **bolded** paragraph",
                    """This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line""",
                    """* This is a list
* with items"""
                ]
            )

    def test_block_type(self):
        markdown = """This is **bolded** paragraph
     
This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        blocks = markdown_to_blocks(markdown)
        expected_block_types = ["paragraph", "paragraph", "unordered_list"]
        for i in range(len(blocks)):
            self.assertEqual(block_to_block_type(blocks[i]), expected_block_types[i])

    def test_block_type(self):
        markdown = """## This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
#### This is the same paragraph on a new line

```
code block
```

1. This is a list
2. with items"""
        blocks = markdown_to_blocks(markdown)
        expected_block_types = ["heading", "paragraph", "code", "paragraph"]
        for i in range(len(blocks)):
            self.assertEqual(block_to_block_type(blocks[i]), expected_block_types[i])

if __name__ == "__main__":
    unittest.main()