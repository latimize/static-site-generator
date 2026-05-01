import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            result.append(node)
        else:
            if delimiter in node.text:
                node_parts = node.text.split(delimiter)
                if len(node_parts) % 2 == 0:
                    raise Exception("Invalid MarkDown Syntax")
                for i in range(len(node_parts)):
                    if i % 2 == 0:
                        if node_parts[i] != "":
                            new_node = TextNode(node_parts[i], TextType.TEXT)
                            result.append(new_node)
                    else:
                        new_node = TextNode(node_parts[i], text_type)
                        result.append(new_node)
            else:
                result.append(node)
    return result        

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    result = []
    for node in old_nodes:
        matches = extract_markdown_images(node.text)
        if matches == []:
            result.append(node)
        else:
            remaining_text = node.text
            for match in matches:
                (alt_text, url) = match
                sections = remaining_text.split(f"![{alt_text}]({url})", 1)
                if sections[0] != "":
                    new_node = TextNode(sections[0], TextType.TEXT)
                    result.append(new_node)
                image_node = TextNode(alt_text, TextType.IMAGE, url)
                result.append(image_node)
                remaining_text = sections[1]
            if remaining_text != "":
                last_node = TextNode(remaining_text, TextType.TEXT)
                result.append(last_node)
    return result

def split_nodes_link(old_nodes):
    result = []
    for node in old_nodes:
        matches = extract_markdown_links(node.text)
        if matches == []:
            result.append(node)
        else:
            remaining_text = node.text
            for match in matches:
                (text, url) = match
                sections = remaining_text.split(f"[{text}]({url})", 1)
                if sections[0] != "":
                    new_node = TextNode(sections[0], TextType.TEXT)
                    result.append(new_node)
                link_node = TextNode(text, TextType.LINK, url)
                result.append(link_node)
                remaining_text = sections[1]
            if remaining_text != "":
                last_node = TextNode(remaining_text, TextType.TEXT)
                result.append(last_node)
    return result

def text_to_textnodes(text):
    node = [TextNode(text, TextType.TEXT)]
    new_node_bold = split_nodes_delimiter(node, "**", TextType.BOLD)
    new_node_italic = split_nodes_delimiter(new_node_bold, "_", TextType.ITALIC)
    new_node_code = split_nodes_delimiter(new_node_italic, "`", TextType.CODE)
    new_node_image = split_nodes_image(new_node_code)
    new_node_final = split_nodes_link(new_node_image)
    return new_node_final

