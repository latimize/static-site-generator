import os
import shutil
from textnode import TextNode
from htmlnode import HTMLNode
from blocks import markdown_to_html_node, extract_title

def reset_directory(dir):
    if os.path.exists(dir):
        shutil.rmtree(dir)

def recursive_copy(source, destination):
    os.mkdir(destination)
    for element in os.listdir(source):
        full_path = os.path.join(source, element)
        if os.path.isfile(full_path):
            shutil.copy(full_path, destination)
        elif os.path.isdir(full_path):
            recursive_copy(full_path, os.path.join(destination, element))
        print(f" * {full_path} -> {os.path.join(destination, element)}")

def copy_static():
    reset_directory("./public")
    recursive_copy("./static", "./public")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        from_content = from_file.read()
    with open(template_path) as template_file:
        template_content = template_file.read()
    html_content = markdown_to_html_node(from_content).to_html()
    page_title = extract_title(from_content)
    full_html_page = template_content.replace("{{ Title }}", page_title).replace("{{ Content }}", html_content)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(full_html_page)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for path in os.listdir(dir_path_content):
        full_path = os.path.join(dir_path_content, path)
        if os.path.isfile(full_path):
            full_dest_path = os.path.join(dest_dir_path, path).replace(".md", ".html")
            generate_page(full_path, template_path, full_dest_path)
        elif os.path.isdir(full_path):
            generate_pages_recursive(full_path, template_path, os.path.join(dest_dir_path, path))

def main():
    copy_static()
    generate_pages_recursive("./content", "template.html", "./public")

main()