import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_to_html(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        #self.assertEqual(node.to_html(), '<a href="https://www.google.com">Google</a>')
        self.assertRaises(NotImplementedError, node.to_html)

    def test_props_to_html(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com"')

    def test_str(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        self.assertEqual(str(node), '<a href="https://www.google.com">Google</a>')
    def test_repr(self):
        node = HTMLNode("a", "Google", None, {"href": "https://www.google.com"})
        self.assertEqual(repr(node), '<a href="https://www.google.com">Google</a>')

if __name__ == "__main__":
    unittest.main()
