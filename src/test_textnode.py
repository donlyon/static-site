import unittest

from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, markdown_to_blocks,block_to_block_type,markdown_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne_type(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_ne_text(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(repr(node), "TextNode(This is a text node, TextType.BOLD, None)")

    def test_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "http://example.com")
        self.assertEqual(str(node), "TextNode(This is a text node, TextType.BOLD, http://example.com)")

    def test_str_empty(self):
        node = TextNode("", TextType.BOLD)
        self.assertEqual(str(node), "TextNode(, TextType.BOLD, None)")

    def test_str_none(self):
        node = TextNode(None, TextType.BOLD)
        self.assertEqual(str(node), "TextNode(None, TextType.BOLD, None)")

class TestTextNodeToHTMLNode(unittest.TestCase):

    def test_normal(self):
        node = TextNode("This is a text node", TextType.NORMAL)
        html_node = text_node_to_html_node(node)
        self.assertEqual(str(html_node), "<None>This is a text node</None>")
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(str(html_node), "<b>This is a text node</b>")
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a text node")

    def test_italic(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(str(html_node), "<i>This is a text node</i>")
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is a text node")

    def test_code(self):
        node = TextNode("This is a text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(str(html_node), "<code>This is a text node</code>")
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a text node", TextType.LINK, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(str(html_node), '<a href="http://example.com">This is a text node</a>')
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {"href": "http://example.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "http://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(str(html_node), '<img src="http://example.com" alt="This is an image node"></img>')
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "http://example.com", "alt": "This is an image node"})

    #def test_invalid(self):
    #    node = TextNode("This is a text node", TextType(99))
    #    self.assertRaises(ValueError, text_node_to_html_node, node)

class TestTextNodeSplitNodes(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        nodes = [
            TextNode("This is text with a `code block` word", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)

    def test_split_nodes_delimiter_code_and_bold(self):
        nodes = [
            TextNode("This is text with a `code block` word and **bold** word", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        new_nodes = split_nodes_delimiter(new_nodes, "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word and ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "bold")
        self.assertEqual(new_nodes[3].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[4].text, " word")
        self.assertEqual(new_nodes[4].text_type, TextType.NORMAL)

        # check for multiple occurences of same delimiter
    def test_split_nodes_delimiter_code_twice(self):
        nodes = [
            TextNode("This is text with a `code block` and another `code block`", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 4)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " and another ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "code block")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

    def test_split_nodes_delimiter_code_at_end(self):
        nodes = [
            TextNode("This is text with a `code block`", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)

    def test_split_nodes_delimiter_code_at_beginning(self):
        nodes = [
            TextNode("`code block` This is text with a", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "code block")
        self.assertEqual(new_nodes[0].text_type, TextType.CODE)
        self.assertEqual(new_nodes[1].text, " This is text with a")
        self.assertEqual(new_nodes[1].text_type, TextType.NORMAL)

    def test_split_nodes_delimiter_bold_and_italic(self):
        nodes = [
            TextNode("This is text with **bold** and *italic* words", TextType.NORMAL),
        ]
        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[0].text, "This is text with ")
        self.assertEqual(new_nodes[0].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[1].text, "bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)
        self.assertEqual(new_nodes[2].text, " and ")
        self.assertEqual(new_nodes[2].text_type, TextType.NORMAL)
        self.assertEqual(new_nodes[3].text, "italic")
        self.assertEqual(new_nodes[3].text_type, TextType.ITALIC)
        self.assertEqual(new_nodes[4].text, " words")
        self.assertEqual(new_nodes[4].text_type, TextType.NORMAL)

    def test_split_nodes_unmatched_delimiter_code(self):
        nodes = [
            TextNode("This is text with a `code block word", TextType.NORMAL),
        ]
        self.assertRaises(ValueError, split_nodes_delimiter, nodes, "`", TextType.CODE)

class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is a text with ![an image](http://example.com/image.jpg) and ![another image](http://example.com/another.jpg)"
        md_images = extract_markdown_images(text)
        self.assertListEqual(md_images, 
                             [
                                 ("an image", "http://example.com/image.jpg"), 
                                 ("another image", "http://example.com/another.jpg")
                              ])

    def test_extract_markdown_links(self):
        text = "This is a text with [a link](http://example.com/image.jpg) and [another link](http://example.com/another.jpg)"
        md_links = extract_markdown_links(text)
        self.assertListEqual(md_links, 
                             [
                                 ("a link", "http://example.com/image.jpg"), 
                                 ("another link", "http://example.com/another.jpg")
                              ])

class TestSplitNodesLinkAndImage(unittest.TestCase):
    def test_split_nodes_image(self):
        node = TextNode(
            "This is text with an image ![to boot dev](https://www.boot.dev/image.jpg) and ![to youtube](https://www.youtube.com/image.jpg)", 
            TextType.NORMAL,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with an image ", TextType.NORMAL),
            TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev/image.jpg"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/image.jpg"),
        ])

    def test_split_nodes_link(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com)", 
            TextType.NORMAL,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [
            TextNode("This is text with a link ", TextType.NORMAL),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.NORMAL),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
        ])

class TestSplitNodesAll(unittest.TestCase):
    def test_split_nodes_all(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [TextNode(text, TextType.NORMAL)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_image(nodes)
        nodes = split_nodes_link(nodes)
        #self.assertEqual(len(nodes), 10)
        self.assertListEqual(
            nodes,
            [
                TextNode("This is ", TextType.NORMAL),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.NORMAL),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.NORMAL),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.NORMAL),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.NORMAL),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

class TestSplitBlocks(unittest.TestCase):
    def test_split_blocks(self):
        text = "This is a paragraph.\n\nThis is another paragraph."
        blocks = markdown_to_blocks(text)
        self.assertEqual(len(blocks), 2)
        self.assertEqual(blocks[0], "This is a paragraph.")
        self.assertEqual(blocks[1], "This is another paragraph.")

class TestBlockTyping(unittest.TestCase):
    def test_header(self):
        block = "# This is a header"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_header_multi(self):
        block = "## This is a header"
        self.assertEqual(block_to_block_type(block), "heading")

    def test_code(self):
        block = "```    This is a code block\nline 2 of code block\nline 3 of code block\n```"
        self.assertEqual(block_to_block_type(block), "code")

    def test_code_unmatched(self):
        block = "```    This is a code block\nline 2 of code block\nline 3 of code block"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_quote(self):
        block = "> This is a quote\n> This is another quote"
        self.assertEqual(block_to_block_type(block), "quote")

    def test_quote_multi(self):
        block = "> This is a quote\nThis is not a quote"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_unordered_list(self):
        block = "- This is a list item\n- This is another list item"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_unordered_list_asterisk(self):
        block = "* This is a list item\n* This is another list item"
        self.assertEqual(block_to_block_type(block), "unordered_list")

    def test_unordered_list_multi(self):
        block = "- This is a list item\nThis is not a list item"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"
        self.assertEqual(block_to_block_type(block), "ordered_list")

    def test_ordered_list_multi(self):
        block = "1. This is a list item\nThis is not a list item"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_ordered_list_out_of_order(self):
        block = "1. This is a list item\n3. This is another list item"
        self.assertEqual(block_to_block_type(block), "paragraph")

    def test_paragraph(self):
        block = "This is a paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")

class TestMarkdownToHTML(unittest.TestCase):
    def test_header1(self):
        markdown = "# This is a header"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h1>This is a header</h1></div>")

    def test_header_2(self):
        markdown = "## This is a header"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h2>This is a header</h2></div>")

    def test_header_with_children(self):
        markdown = "# This *is* a **bold header**"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><h1>This <i>is</i> a <b>bold header</b></h1></div>")

    def test_code(self):
        markdown = "```This is a code block\nline 2 of code block\nline 3 of code block\n```"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(str(html_node.children[0]), "<pre>This is a code block\nline 2 of code block\nline 3 of code block</pre>")

    def test_quote(self):
        markdown = "> This is a quote"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><blockquote>This is a quote</blockquote></div>")

    def test_unordered_list(self):
        markdown = "- This is a list item\n- This is another list item"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.to_html(), "<div><ul><li>This is a list item</li><li>This is another list item</li></ul></div>")

    def test_ordered_list(self):
        markdown = "1. This is a list item\n2. This is another list item"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 1)
        self.assertEqual(html_node.to_html(), "<div><ol><li>This is a list item</li><li>This is another list item</li></ol></div>")

    def test_paragraph(self):
        markdown = "This is a paragraph"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(html_node.to_html(), "<div><p>This is a paragraph</p></div>")

    def test_mixed(self):
        markdown = "# Header\n\nThis is a paragraph\n\n- This is a list item\n- This is another list item"
        html_node = markdown_to_html_node(markdown)
        self.assertEqual(len(html_node.children), 3)
        self.assertEqual(html_node.to_html(), "<div><h1>Header</h1><p>This is a paragraph</p><ul><li>This is a list item</li><li>This is another list item</li></ul></div>")


if __name__ == "__main__":
    unittest.main()
