from textnode import *

text_types = [
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image
]

types_tag_map = {
    "text": None,
    "bold": "b",
    "italic": "i",
    "code": "code",
    "link": "a",
    "image": "img",
    "list": "li"
}

blocktypes_blocktag_map = {
    block_type_paragraph: "p",
    block_type_code: "code",
    block_type_quote: "blockquote",
    block_type_ul: "ul",
    block_type_ol: "ol",
}

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag                  # html tag
        self.value = value              # text inside tags
        self.children = children        # HTMLNodes that are children of this node
        self.props = props              # a dictionary attrbutes: tags
    
    def to_html(self):
        raise NotImplementedError()
    
    def props_to_html(self):
        if self.props:
            conv = ""
            for k, v in self.props.items():
                conv += f"{k}=\"{v}\" "
            return conv.strip()
        raise Exception("No props provided")
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
    
    def __eq__(self, other):
        return (
            self.tag == other.tag 
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
            )

class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value is None:
            raise ValueError("Leaf does not have a value!")
        if self.tag is None:
            return self.value
        else: 
            if self.tag in "p h1 h2 h3 b i code li".split():
                return f"<{self.tag}>{self.value}</{self.tag}>"
            elif self.tag == "a":
                if self.props is None:
                    raise ValueError("Website link not reported in href!")
                for k, v in self.props.items():
                    return f"<a {k}={v}>{self.value}</a>"
            elif self.tag == "img":
                if self.props is None:
                    raise ValueError("Picture link not reported in src!")
                return f"<img src={self.props['src']} alt={self.value}>"
            elif "list" in self.tag or self.tag == "ul" or self.tag == "ol":
                l = ""
                for item in self.value.split("\n"):
                    item = " ".join(item.split()[1:])
                    l += f"<li>{item}</li>\n"
                return f"<{self.tag}>\n{l}</{self.tag}>"
            elif self.tag == "blockquote":
                return f"<blockquote>\n\t{self.value}\n</blockquote>"
        raise ValueError(f"Unrecognized inserted tag: {self.tag}")

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)
    
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Tag not provided!")
        if self.children is None:
            raise ValueError("Parent node without children!")
        s = f"<{self.tag}>"
        for child in self.children:
            s += child.to_html()
        return f"{s}</{self.tag}>"
    
def text_node_to_html_node(text_node):

    if text_node.text_type not in text_types:
        raise Exception(f"Text type {text_node.text_type} not recognized")
    
    node_tag = types_tag_map[text_node.text_type]

    if node_tag == "img":
        prop_dic = {"src": text_node.url}
    elif node_tag == "a":
        prop_dic = {"href": text_node.url}
    else:    
        prop_dic = None

    node = LeafNode(
        tag = node_tag,
        value = text_node.text,
        props = prop_dic
        )
    
    return node

def markdown_to_html_node(markdown):

    div = ParentNode("div", [])
    blocks = markdown_to_blocks(markdown)

    for block in blocks:
        block_type = block_to_block_type(block)

        if block_type == block_type_heading:
            tag = "h"+str(block[:7].count("#"))
            block = block.strip("#").strip()
        else:
            tag = blocktypes_blocktag_map[block_type]
            if block_type == block_type_code:
                block = block.strip("```").strip("\n")
            elif block_type == block_type_quote:
                new_block = ""
                for line in block.split("\n"):
                    new_block += line.strip(">").strip() + "\n"
                block = new_block.strip("\n")
                
        if block_type in [block_type_ol, block_type_ul]:
            block_node = LeafNode(tag, block, block_type)
        else:
            block_node = ParentNode(tag, [])
            parts = text_to_textnodes(block)
            
            for part in parts:
                node = text_node_to_html_node(part)
                block_node.children.append(node)
        
        div.children.append(block_node)

    return div

    