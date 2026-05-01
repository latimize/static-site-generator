import re
from enum import Enum
from htmlnode import HTMLNode, ParentNode
from textnode import TextType, TextNode, text_node_to_html_node
from inline_markdown import text_to_textnodes

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        if block.strip() != "":
            new_blocks.append(block.strip())
    return new_blocks

def block_to_block_type(block):
    lines = block.split("\n")
    if len(lines) == 1 and re.fullmatch(r"#{1,6} .+", lines[0]):
        return BlockType.HEADING
    elif len(lines) > 1 and lines[0].startswith("```") and lines[-1].endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(lines[i].startswith(f"{i + 1}. ") for i in range(len(lines))):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH

def text_to_children(text):
    return list(map(text_node_to_html_node, text_to_textnodes(text)))

def heading_block_to_html_node(block):
    level = len(block.split(" ")[0])
    if 0 < level < 7:
        return ParentNode(f"h{level}", text_to_children(block[level + 1:]))
    else: 
        raise Exception("Invalid heading block")

def paragraph_block_to_html_node(block):
    lines = block.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    new_block = " ".join(lines)
    return ParentNode("p", text_to_children(new_block))

def quote_block_to_html_node(block):
    lines = block.split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].lstrip(">").strip()
    new_block = " ".join(lines)
    return ParentNode("blockquote", text_to_children(new_block))

def unordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        list_nodes.append(ParentNode("li", text_to_children(line[2:])))
    return ParentNode("ul", list_nodes)

def ordered_list_block_to_html_node(block):
    lines = block.split("\n")
    list_nodes = []
    for line in lines:
        list_nodes.append(ParentNode("li", text_to_children(line[line.index(".") + 2:])))
    return ParentNode("ol", list_nodes)

def code_block_to_html_node(block):
    lines = block[4:-3].split("\n")
    for i in range(len(lines)):
        lines[i] = lines[i].strip()
    new_block = "\n".join(lines)
    code_text_node = TextNode(new_block, TextType.TEXT)
    code_html_node = text_node_to_html_node(code_text_node)
    code_node = ParentNode("code", [code_html_node])
    pre_node = ParentNode("pre", [code_node])
    return pre_node

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    result_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.HEADING:
                block_node = heading_block_to_html_node(block)
                result_nodes.append(block_node)
            case BlockType.PARAGRAPH:
                block_node = paragraph_block_to_html_node(block)
                result_nodes.append(block_node)
            case BlockType.QUOTE:
                block_node = quote_block_to_html_node(block)
                result_nodes.append(block_node)
            case BlockType.UNORDERED_LIST:
                block_node = unordered_list_block_to_html_node(block)
                result_nodes.append(block_node)
            case BlockType.ORDERED_LIST:
                block_node = ordered_list_block_to_html_node(block)
                result_nodes.append(block_node)
            case BlockType.CODE:
                block_node = code_block_to_html_node(block)
                result_nodes.append(block_node)
            case _:
                raise Exception("unknown block type")  
    return ParentNode("div", result_nodes)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        if block.startswith("# "):
            return block[2:].strip()   
    raise Exception("Missing H1 header")

