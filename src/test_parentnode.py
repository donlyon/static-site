import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        child = LeafNode("li", "Google", {"href": "https://www.google.com"})
        children = [child]
        node = ParentNode("ol", children)
        self.assertEqual(node.to_html(), '<ol><li href="https://www.google.com">Google</li></ol>')

    def test_to_html_multi_children(self):
        child = LeafNode("li", "Google", {"href": "https://www.google.com"})
        child2 = LeafNode("li", "Meta", {"href": "https://www.meta.com"})
        children = [child, child2]
        node = ParentNode("ol", children)
        self.assertEqual(node.to_html(), '<ol><li href="https://www.google.com">Google</li><li href="https://www.meta.com">Meta</li></ol>')

    def test_to_html_no_children(self):
        node = ParentNode("ol", None)
        self.assertRaises(ValueError, node.to_html)

if __name__ == "__main__":
    unittest.main()
