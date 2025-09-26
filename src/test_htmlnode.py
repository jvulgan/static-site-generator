import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_none(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_single(self):
        node = HTMLNode(props={"href": "https://www.google.com"})
        expected = ' href="https://www.google.com"'
        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank",})
        expected = ' href="https://www.google.com" target="_blank"'
        self.assertEqual(node.props_to_html(), expected)
