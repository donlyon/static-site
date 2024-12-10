from enum import Enum
from leafnode import LeafNode
from parentnode import ParentNode
import re

class TextType(Enum):
    NORMAL = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.NORMAL:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("Invalid text type")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.NORMAL:
            sub_nodes = node.text.split(delimiter)
            # check for unmatched delimiters
            if len(sub_nodes)% 2 == 0:
                raise ValueError("Unmatched delimiters")
            for s in range(len(sub_nodes)):
                sub_node = sub_nodes[s]
                if sub_node and s%2 == 0:
                    new_nodes.append(TextNode(sub_node, node.text_type))
                elif sub_node:
                    new_nodes.append(TextNode(sub_node, text_type))
        else:
            new_nodes.append(node)
    return new_nodes

def extract_markdown_images(text):
    result = []
    matches = re.finditer(r"!\[(.*?)\]\((.*?)\)", text)
    #matches = re.finditer(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        result.append(match.group(1,2))
    return result

def extract_markdown_links(text):
    result = []
    matches = re.finditer(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    for match in matches:
        result.append(match.group(1,2))
    return result

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.NORMAL:
            images = extract_markdown_images(node.text)
            if len(images) == 0:
                new_nodes.append(node)
                continue
            current_split = node.text
            for i in range(len(images)):
                image = images[i]
                split_nodes = current_split.split(f"![{image[0]}]({image[1]})", 1)
                if len(split_nodes) != 2:
                    raise ValueError("Unmatched image")
                if split_nodes[0]:
                    new_nodes.append(TextNode(split_nodes[0], node.text_type))
                new_nodes.append(TextNode(image[0], TextType.IMAGE, image[1]))
                if i == len(images) - 1 and split_nodes[1]:
                    new_nodes.append(TextNode(split_nodes[1], node.text_type))
                current_split = split_nodes[1]
        else:
            new_nodes.append(node)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if isinstance(node, TextNode) and node.text_type == TextType.NORMAL:
            links = extract_markdown_links(node.text)
            if len(links) == 0:
                new_nodes.append(node)
                continue
            current_split = node.text
            for i in range(len(links)):
                link = links[i]
                split_nodes = current_split.split(f"[{link[0]}]({link[1]})", 1)
                if len(split_nodes) != 2:
                    raise ValueError("Unmatched link")
                if split_nodes[0]:
                    new_nodes.append(TextNode(split_nodes[0], node.text_type))
                new_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
                if i == len(link) - 1 and split_nodes[1]:
                    new_nodes.append(TextNode(split_nodes[1], node.text_type))
                current_split = split_nodes[1]
        else:
            new_nodes.append(node)
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = list(filter(lambda x: x != "", map(str.strip, markdown.split("\n\n"))))
    
    return blocks

def block_to_block_type(text):
    if text.startswith("#"):
        return "heading"
    elif text.startswith("```") and text.endswith("```"):
        return "code"
    elif text.startswith(">"):
        lines = text.split("\n")
        for line in lines:
            if not line.startswith(">"):
                return "paragraph"
        return "quote"
    elif text.startswith("- ") or text.startswith("* "):
        lines = text.split("\n")
        for line in lines:
            if not (line.startswith("- ") or line.startswith("* ")):
                return "paragraph"
        return "unordered_list"
    elif re.match(r"\d+\. ", text):
        lines = text.split("\n")
        line_number = 1
        for line in lines:
            if not re.match(r"\d+\. ", line) or int(line.split(".")[0]) != line_number:
                return "paragraph"
            line_number += 1
        return "ordered_list"
    else:
        return "paragraph"

def text_to_children(text):
    nodes = text_to_textnodes(text)
    result = []
    for node in nodes:
        result.append(text_node_to_html_node(node))
    return result

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == "heading":
            level = len(block.split(" ")[0])
            html_nodes.append(ParentNode(f"h{level}", text_to_children(block[level:].strip()), None))
        elif block_type == "code":
            html_nodes.append(LeafNode("pre", block[3:-3].strip()))
        elif block_type == "quote":
            html_nodes.append(ParentNode("blockquote", text_to_children(block[1:].strip()), None))
        elif block_type == "unordered_list":
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                child_nodes.append(ParentNode("li", text_to_children(line[2:].strip()), None))
            html_nodes.append(ParentNode("ul", child_nodes, None))
        elif block_type == "ordered_list":
            lines = block.split("\n")
            child_nodes = []
            for line in lines:
                child_nodes.append(ParentNode("li", text_to_children(line.split(".", 1)[1].strip()), None))
            html_nodes.append(ParentNode("ol", child_nodes, None))
        elif block_type == "paragraph":
            html_nodes.append(ParentNode("p", text_to_children(block), None))
    return ParentNode("div", html_nodes, None)

