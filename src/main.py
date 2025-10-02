import sys
from textnode import TextType, TextNode
from copyfiles import copy_files
from generate_page import generate_page_recursive


def main():
    args = sys.argv
    if len(args) != 2:
        basepath = "/"
    else:
        basepath = args[1]
    copy_files("static", "docs")
    generate_page_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()
