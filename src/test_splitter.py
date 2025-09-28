import unittest
from splitter import (
    InvalidMarkdownError,
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
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
