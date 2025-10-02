import os
from converter import markdown_to_html_node
from splitter import extract_title


def generate_page(from_path: str, template_path: str, dest_path: str):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        html_template = f.read()
    html_node = markdown_to_html_node(markdown)
    title = extract_title(markdown)
    html = html_node.to_html()
    page = html_template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, 'w') as f:
        f.write(page)


def generate_page_recursive(dir_path_content: str, template_path: str, dest_dir_path: str):
    for item in os.listdir(dir_path_content):
        item_path = os.path.join(dir_path_content, item)
        if os.path.isfile(item_path):
            item = item.replace(".md", ".html")
            dest_path = os.path.join(dest_dir_path, item)
            generate_page(item_path, template_path, dest_path)
        else:
            dest_path = os.path.join(dest_dir_path, item)
            generate_page_recursive(item_path, template_path, dest_path)
