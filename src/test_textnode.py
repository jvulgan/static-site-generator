import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_different_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is another text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_different_text_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.LINK)
        self.assertNotEqual(node, node2)

    def test_different_text_link(self):
        node = TextNode("This is a link", TextType.LINK, "https://foo.com")
        node2 = TextNode("This is a link", TextType.LINK, "https://bar.com")
        self.assertNotEqual(node, node2)

    def test_text_node_to_html_node_text(self):
        text_node = TextNode("text", TextType.TEXT)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, None)
        self.assertEqual(result.value, "text")
        self.assertIsNone(result.props)

    def test_text_node_to_html_node_bold(self):
        text_node = TextNode("text", TextType.BOLD)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "b")
        self.assertEqual(result.value, "text")
        self.assertIsNone(result.props)

    def test_text_node_to_html_node_italic(self):
        text_node = TextNode("text", TextType.ITALIC)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "i")
        self.assertEqual(result.value, "text")
        self.assertIsNone(result.props)

    def test_text_node_to_html_node_code(self):
        text_node = TextNode("text", TextType.CODE)
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "code")
        self.assertEqual(result.value, "text")
        self.assertIsNone(result.props)

    def test_text_node_to_html_node_link(self):
        text_node = TextNode("text", TextType.LINK, "https://foo.com")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "a")
        self.assertEqual(result.value, "text")
        self.assertEqual(result.props, {"href": "https://foo.com"})

    def test_text_node_to_html_node_image(self):
        text_node = TextNode("text", TextType.IMAGE, "https://foo.com")
        result = text_node_to_html_node(text_node)
        self.assertEqual(result.tag, "img")
        self.assertEqual(result.value, "")
        self.assertEqual(result.props, {"src": "https://foo.com", "alt": "text"})


if __name__ == "__main__":
    unittest.main()
