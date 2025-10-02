from textnode import TextType, TextNode
from copyfiles import copy_files
from generate_page import generate_page_recursive


def main():
    copy_files('static', 'public')
    generate_page_recursive("content", "template.html", "public")



if __name__ == "__main__":
    main()
