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
