import re 

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_code = "code"
text_type_link = "link"
text_type_image = "image"

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_ul = "unordered_list"
block_type_ol = "ordered_list"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url
    
    def __eq__(self, tn2):
        return (
            self.text == tn2.text and  \
            self.text_type == tn2.text_type and \
            self.url == tn2.url
            )
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"
    
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    nodes_list = []
    for node in old_nodes:
        if node.text_type == text_type_text:
            if node.text.count(delimiter)%2 != 0:
                raise ValueError(f"{delimiter} miss opening or closing!")
            parts = node.text.split(delimiter)
            for i, part in enumerate(parts):
                if part != "":
                    if i % 2 == 0:
                        nodes_list.append(TextNode(part, "text"))
                    else:
                        nodes_list.append(TextNode(part, text_type))
        else:
            nodes_list.append(node)
    return nodes_list

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"(?<!\!)\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    nodes_list = []

    for node in old_nodes:
        images = extract_markdown_images(node.text)
        remaining_text = node.text

        for image_tup in images:
            before_image, remaining_text = remaining_text.split(f"![{image_tup[0]}]({image_tup[1]})", 1)
            if before_image:
                nodes_list.append(TextNode(before_image, text_type_text))
            nodes_list.append(TextNode(image_tup[0], text_type_image, image_tup[1]))

        if remaining_text and remaining_text.strip():
            nodes_list.append(TextNode(remaining_text, text_type_text))

    return nodes_list

def split_nodes_link(old_nodes):
    nodes_list = []

    for node in old_nodes:
        links = extract_markdown_links(node.text)
        remaining_text = node.text
        
        for link_tup in links:
            before_link, remaining_text = remaining_text.split(f"[{link_tup[0]}]({link_tup[1]})", 1)
            if before_link:
                nodes_list.append(TextNode(before_link, text_type_text))
            nodes_list.append(TextNode(link_tup[0], text_type_link, link_tup[1]))

        if remaining_text and remaining_text.strip():
            nodes_list.append(TextNode(remaining_text, text_type_text))
            
    return nodes_list

def find_first_tag(string):
    tags = ["**", "*", "`", "![", "["]
    min_tag = ""
    tag_index = len(string)
    for tag in tags:
        index = string.find(tag)
        if 0 <= index < tag_index:
            min_tag = tag
            tag_index = index
    return min_tag, tag_index

def text_to_textnodes(text):
    nodes = []
    position = 0

    while position < len(text):
        remaining_text = text[position:]
        tag, tag_index = find_first_tag(remaining_text)

        if tag == "":
            nodes.append(TextNode(remaining_text, text_type_text))
            break

        if tag_index > 0:
            nodes.append(TextNode(remaining_text[:tag_index], text_type_text))

        if tag == "**":  # Bold
            end_index = remaining_text.find("**", tag_index + 2)
            if end_index == -1:
                end_index = len(remaining_text)
            content = remaining_text[tag_index + 2:end_index]
            nodes.append(TextNode(content, text_type_bold))
            position += (end_index + 2)

        elif tag == "*":  # Italic
            end_index = remaining_text.find("*", tag_index + 1)
            if end_index == -1:
                end_index = len(remaining_text)
            content = remaining_text[tag_index + 1:end_index]
            nodes.append(TextNode(content, text_type_italic))
            position += (end_index + 1)

        elif tag == "`":  # Code
            end_index = remaining_text.find("`", tag_index + 1)
            if end_index == -1:
                end_index = len(remaining_text)
            content = remaining_text[tag_index + 1:end_index]
            nodes.append(TextNode(content, text_type_code))
            position += (end_index + 1)

        elif tag == "![":  # Image
            end_alt_text_index = remaining_text.find("]", tag_index + 2)
            start_url_index = remaining_text.find("(", end_alt_text_index)
            end_url_index = remaining_text.find(")", start_url_index)
            if end_alt_text_index == -1 or start_url_index == -1 or end_url_index == -1:
                end_index = len(remaining_text)
            else:
                alt_text = remaining_text[tag_index + 2:end_alt_text_index]
                url = remaining_text[start_url_index + 1:end_url_index]
                nodes.append(TextNode(alt_text, text_type_image, url))
                position += (end_url_index + 1)

        elif tag == "[":  # Link
            end_link_text_index = remaining_text.find("]", tag_index + 1)
            start_url_index = remaining_text.find("(", end_link_text_index)
            end_url_index = remaining_text.find(")", start_url_index)
            if end_link_text_index == -1 or start_url_index == -1 or end_url_index == -1:
                end_index = len(remaining_text)
            else:
                link_text = remaining_text[tag_index + 1:end_link_text_index]
                url = remaining_text[start_url_index + 1:end_url_index]
                nodes.append(TextNode(link_text, text_type_link, url))
                position += (end_url_index + 1)

    return nodes

def markdown_to_blocks(markdown):
    return [x.strip("\n").strip() for x in markdown.split("\n\n") if x.strip("\n").strip()]

def check_lines_start(block, start):
    if start == "num. ":
        for line in block.splitlines():
            if not (line.split(".")[0].isdigit() and line.startswith(line.split(".")[0] + ". ")):
                return False
    else:
        for line in block.splitlines():
            if not line.startswith(start):
                return False  
    return True

def block_to_block_type(block):
    if block.startswith ("#") and "# " in block.replace(u'\xa0', ' '):
        return block_type_heading
    elif block.startswith("```") and block.endswith("```"):
        return block_type_code
    elif check_lines_start(block, ">"):
        return block_type_quote
    elif check_lines_start(block, "* "):
        return block_type_ul
    elif check_lines_start(block, "num. "):
        return block_type_ol
    return block_type_paragraph
        
