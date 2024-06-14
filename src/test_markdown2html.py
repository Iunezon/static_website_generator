import unittest

from htmlnode import *
from textnode import *

class TestHTMLNode(unittest.TestCase):

    def test_markdown_to_html_node_1(self):
        markdown = """
1. This is a list
2. with items"""
        print(repr(markdown_to_html_node(markdown)))




if __name__ == "__main__":
    unittest.main()