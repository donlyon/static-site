import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_repr(self):
        node = LeafNode("p", "This is a leaf node")
        self.assertEqual(repr(node), "<p>This is a leaf node</p>")

    def test_to_html(self):
        node = LeafNode("p", "This is a leaf node")
        self.assertEqual(node.to_html(), "<p>This is a leaf node</p>")

    def test_to_html_notag(self):
        node = LeafNode(None, "This is a leaf node")
        self.assertEqual(node.to_html(), "This is a leaf node")

    def test_to_html_novalue(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()
