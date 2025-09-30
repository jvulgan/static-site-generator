import unittest
from splitter import (
    InvalidMarkdownError,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
)
from textnode import TextType, TextNode


class TestSplitter(unittest.TestCase):
    def test_split_nodes_delimiter_empty_nodes(self):
        self.assertEqual(split_nodes_delimiter([], "*", TextType.BOLD), [])

    def test_split_nodes_delimiter_only_nontext(self):
        nodes = [
            TextNode("this is bold", TextType.BOLD),
            TextNode("this is italic", TextType.ITALIC),
            TextNode("this is code", TextType.CODE),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.BOLD), nodes)

    def test_split_nodes_delimiter_no_closing_delimiter(self):
        with self.assertRaises(InvalidMarkdownError):
            split_nodes_delimiter(
                [TextNode("bold only starts *here", TextType.TEXT)], "*", TextType.BOLD
            )

    def test_split_nodes_delimiter_code(self):
        node = TextNode("text `code` text", TextType.TEXT)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("text **bold** text", TextType.TEXT)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("bold", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "**", TextType.CODE), expected)

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("text *italic* text", TextType.TEXT)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("italic", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "*", TextType.CODE), expected)

    def test_split_nodes_delimiter_multiple_match(self):
        node = TextNode("text `code` `another code` text", TextType.TEXT)
        expected = [
            TextNode("text ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" ", TextType.TEXT),
            TextNode("another code", TextType.CODE),
            TextNode(" text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_split_nodes_delimiter_multiple_with_empty_strings(self):
        node = TextNode("`code` text `another`", TextType.TEXT)
        expected = [
            TextNode("code", TextType.CODE),
            TextNode(" text ", TextType.TEXT),
            TextNode("another", TextType.CODE),
        ]
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), expected)

    def test_extract_markdown_images_single(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_nothing(self):
        matches = extract_markdown_images("no links here")
        self.assertEqual([], matches)

    def test_extract_markdown_images_multiple(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("rick roll", "https://i.imgur.com/aKaOqIh.gif"),
                ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg"),
            ],
            matches,
        )

    def test_extract_markdown_links_single(self):
        matches = extract_markdown_links(
            "This is text with a [single link](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual(
            [("single link", "https://i.imgur.com/zjjcJKZ.png")], matches
        )

    def test_extract_markdown_links_nothing(self):
        matches = extract_markdown_links("no images here")
        self.assertEqual([], matches)

    def test_extract_markdown_links_multiple(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        matches = extract_markdown_links(text)
        expected = [
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ]

        self.assertListEqual(
            expected,
            matches,
        )

    def test_split_nodes_image_single_image(self):
        text = (
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) inside it"
        )
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" inside it", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_single_image_first(self):
        text = "![image](https://i.imgur.com/zjjcJKZ.png) inside text"
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" inside text", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_single_image_last(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_multiple_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)."
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is text with an ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_no_image(self):
        text = "This is just text."
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is just text.", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_image_no_image_no_text(self):
        text = ""
        nodes = [TextNode(text, TextType.TEXT)]
        expected = []
        self.assertListEqual(split_nodes_image(nodes), expected)

    def test_split_nodes_link_single_link(self):
        text = "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) inside it"
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" inside it", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_single_link_first(self):
        text = "[link](https://i.imgur.com/zjjcJKZ.png) inside text"
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" inside text", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_single_link_last(self):
        text = "This is text with a [link](https://i.imgur.com/zjjcJKZ.png)"
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
        ]
        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_multiple_links(self):
        text = "This is text with a [link](https://i.imgur.com/zjjcJKZ.png) and another [second link](https://i.imgur.com/3elNhQu.png)."
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("second link", TextType.LINK, "https://i.imgur.com/3elNhQu.png"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_no_links(self):
        text = "This is just text."
        nodes = [TextNode(text, TextType.TEXT)]
        expected = [
            TextNode("This is just text.", TextType.TEXT),
        ]
        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_split_nodes_link_no_link_no_text(self):
        text = ""
        nodes = [TextNode(text, TextType.TEXT)]
        expected = []
        self.assertListEqual(split_nodes_link(nodes), expected)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(text_to_textnodes(text), expected)

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_excessive_newlines(self):
        md = """
This is **bolded** paragraph



This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line




- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_single_block(self):
        md = "This is **bolded** paragraph"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
            ],
        )
