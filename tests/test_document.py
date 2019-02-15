#!/usr/bin/env python3


import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path

from lxml import etree

sys.path.extend(['.', '..'])

from svgpy import Attr, Comment, Document, Node, \
    ProcessingInstruction, SVGDOMImplementation, SVGParser, Window, \
    XMLDocument, window
from svgpy.element import HTMLVideoElement, SVGSVGElement
from svgpy.exception import HierarchyRequestError, NotFoundError

# LOGGING_LEVEL = logging.DEBUG
LOGGING_LEVEL = logging.WARNING

SVG_CUBIC01 = '''
<svg width="5cm" height="4cm" viewBox="0 0 500 400"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
    <title>Example cubic01- cubic Bézier commands in path data</title>
    <desc>Picture showing a simple example of path data
        using both a "C" and an "S" command,
        along with annotations showing the control points
        and end points
    </desc>
    <style type="text/css"><![CDATA[
    .Border { fill:none; stroke:blue; stroke-width:1 }
    .Connect { fill:none; stroke:#888888; stroke-width:2 }
    .SamplePath { fill:none; stroke:red; stroke-width:5 }
    .EndPoint { fill:none; stroke:#888888; stroke-width:2 }
    .CtlPoint { fill:#888888; stroke:none }
    .AutoCtlPoint { fill:none; stroke:blue; stroke-width:4 }
    .Label { font-size:22; font-family:Verdana }
    ]]>
    </style>

    <rect class="Border" x="1" y="1" width="498" height="398"/>

    <polyline class="Connect" points="100,200 100,100"/>
    <polyline class="Connect" points="250,100 250,200"/>
    <polyline class="Connect" points="250,200 250,300"/>
    <polyline class="Connect" points="400,300 400,200"/>
    <path class="SamplePath" d="M100,200 C100,100 250,100 250,200
                                       S400,300 400,200" id="path01"/>
    <path d="M100,200 C100,100 250,100 250,200 C250,300 400,300 400,200"
          id="path02" fill="none" stroke="pink" stroke-width="3"
          stroke-dasharray="10 6"/>
    <path d="M100,200 C100,100 250,100 250,200"
          id="path03" fill="none" stroke="blue" stroke-width="3"
          stroke-dasharray="5"/>
    <circle class="EndPoint" cx="100" cy="200" r="10"/>
    <circle class="EndPoint" cx="250" cy="200" r="10"/>
    <circle class="EndPoint" cx="400" cy="200" r="10"/>
    <circle class="CtlPoint" cx="100" cy="100" r="10"/>
    <circle class="CtlPoint" cx="250" cy="100" r="10"/>
    <circle class="CtlPoint" cx="400" cy="300" r="10"/>
    <circle class="AutoCtlPoint" cx="250" cy="300" r="9"/>
    <text class="Label" x="25" y="70">M100,200 C100,100 250,100 250,200</text>
    <text class="Label" x="325" y="350"
          style="text-anchor:middle">S400,300 400,200
    </text>
</svg>
'''

SVG_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100" viewBox="0 0 100 100">
 <g id='gtop' stroke-width="12" stroke="#000">
   <g id="svgstar" transform="translate(50,50)">
     <path id="svgbar" d="M-27-5a7,7,0,1,0,0,10h54a7,7,0,1,0,0-10z"/>
     <use id='use1' xlink:href="#svgbar" transform="rotate(45)"/>
     <use id='use2' xlink:href="#svgbar" transform="rotate(90)"/>
     <use id='use3' xlink:href="#svgbar" transform="rotate(135)"/>
   </g>
 </g>
 <use id="usetop" xlink:href="#svgstar" fill="#FB4"/>
</svg>
'''

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


class DocumentTestCase(unittest.TestCase):

    def setUp(self):
        logging_level = int(os.getenv('LOGGING_LEVEL', str(LOGGING_LEVEL)))
        filename = os.path.join(tempfile.gettempdir(),
                                '{}.log'.format(__name__))
        fmt = '%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(message)s'
        logging.basicConfig(level=logging_level,
                            filename=filename,
                            format=fmt)
        window.location = 'about:blank'

    def test_document_append01(self):
        # Document
        # ParentNode.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = doc = parser.create_document(svg_ns)
        self.assertIsNone(doc.document_element)

        # 1st attempt
        attr = parser.create_attribute('foo')
        # parent.append(attr)
        self.assertRaises(HierarchyRequestError, lambda: parent.append(attr))

        comment = parser.create_comment('foo')
        # parent.append(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.append(doc2)
        self.assertRaises(HierarchyRequestError, lambda: parent.append(doc2))

        pi = parser.create_processing_instruction('foo-bar')
        # parent.append(pi)
        self.assertRaises(HierarchyRequestError, lambda: parent.append(pi))

        # '<svg/>'
        root = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(root.owner_document)
        parent.append(root)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual([root], list(doc))

        # 2nd attempt
        # parent.append(attr)
        self.assertRaises(HierarchyRequestError, lambda: parent.append(attr))

        # '<svg/><!--foo-->'
        self.assertIsNone(comment.owner_document)
        parent.append(comment)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual([root, comment], list(doc))

        # parent.append(doc2)
        self.assertRaises(HierarchyRequestError, lambda: parent.append(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.append(element)
        self.assertRaises(TypeError, lambda: parent.append(element))

        # '<svg/><!--foo--><?foo-bar ?>'
        self.assertIsNone(pi.owner_document)
        parent.append(pi)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([root, comment, pi], list(doc))

    def test_document_append02(self):
        # Document
        # ParentNode.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_document(svg_ns)

        args = 'foo', 'bar', 'baz'
        # parent.append(*args)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(*args))

        element = parser.create_element_ns(svg_ns, 'svg')
        args = element, 'foo', 'bar', 'baz'
        # parent.append(*args)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(*args))

    def test_document_append03(self):
        # Document
        # ParentNode.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = doc = parser.create_document(svg_ns)
        self.assertIsNone(doc.document_element)

        root = parser.create_element_ns(svg_ns, 'svg')
        comment = parser.create_comment('foo')
        pi = parser.create_processing_instruction('foo-bar')
        self.assertIsNone(root.owner_document)
        self.assertIsNone(comment.owner_document)
        self.assertIsNone(pi.owner_document)

        # '<svg/><!--foo--><?foo-bar ?>'
        parent.append(root, comment, pi)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([root, comment, pi], list(doc))

    def test_document_append_child(self):
        svg_ns = 'http://www.w3.org/2000/svg'
        impl = SVGDOMImplementation()

        doc = impl.create_document(svg_ns)
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        # parser = etree.XMLParser()
        # root = parser.makeelement('svg')
        # self.assertNotIsInstance(root, Node)
        # self.assertRaises(TypeError, lambda: doc.append_child(root))

        attr = doc.create_attribute('foo')
        # parent.insert_before(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.append_child(attr))

        comment = doc.create_comment('start')
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.append_child(comment))

        root = doc.create_element_ns(svg_ns, 'svg')
        self.assertIsInstance(root, Node)
        self.assertEqual(doc, root.owner_document)
        result = doc.append_child(root)
        self.assertEqual(root, result)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)

        comment = doc.create_comment('end')
        self.assertEqual(doc, comment.owner_document)
        result = doc.append_child(comment)
        self.assertEqual(comment, result)
        self.assertEqual(doc, comment.owner_document)

        title = doc.create_element_ns(svg_ns, 'title')
        self.assertEqual(doc, title.owner_document)
        self.assertRaises(HierarchyRequestError,
                          lambda: comment.append_child(title))
        result = root.append_child(title)
        self.assertEqual(title, result)
        self.assertEqual(doc, title.owner_document)

        defs = doc.create_element_ns(svg_ns, 'defs')
        self.assertEqual(doc, defs.owner_document)
        result = root.append_child(defs)
        self.assertEqual(defs, result)
        self.assertEqual(doc, defs.owner_document)

        style = doc.create_element_ns(svg_ns, 'style')
        self.assertEqual(doc, style.owner_document)
        result = defs.append_child(style)
        self.assertEqual(style, result)
        self.assertEqual(doc, style.owner_document)

        # <title/><defs><style/></defs>
        self.assertTrue(style in defs)
        self.assertTrue(style not in doc.document_element)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs><style/></defs>' \
            '</svg>' \
            '<!--end-->'
        self.assertEqual(expected, doc.tostring().decode())

        # <title/><defs/><style/>
        result = root.append_child(style)
        self.assertEqual(style, result)
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(style, result)
        self.assertTrue(style not in defs)
        self.assertTrue(style in doc.document_element)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs/><style/>' \
            '</svg>' \
            '<!--end-->'
        self.assertEqual(expected, doc.tostring().decode())

        # link = parser.makeelement('link')
        # self.assertNotIsInstance(link, Node)
        # self.assertRaises(TypeError, lambda: root.append_child(link))

        # <title/><defs/><style/><link/>
        link = doc.create_element_ns(svg_ns, 'link')
        self.assertIsInstance(link, Node)
        self.assertEqual(doc, link.owner_document)
        result = root.append_child(link)
        self.assertEqual(link, result)
        self.assertEqual(doc, link.owner_document)

        pi = doc.create_processing_instruction('foo-bar')
        self.assertEqual(doc, pi.owner_document)
        result = doc.append_child(pi)
        self.assertEqual(pi, result)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([root, comment, pi], list(doc))

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs/><style/><link/>' \
            '</svg>' \
            '<!--end-->' \
            '<?foo-bar ?>'
        self.assertEqual(expected, doc.tostring().decode())

        removed = doc.remove_child(root)
        self.assertEqual(root, removed)
        self.assertIsNone(doc.document_element)
        added = doc.append_child(removed)
        self.assertEqual(removed, added)
        self.assertEqual(root, doc.document_element)

    def test_document_child_nodes(self):
        # Node.child_nodes
        # Node.first_child
        # Node.last_child
        # Node.next_sibling
        # Node.previous_sibling
        # Node.has_child_nodes()
        doc = window.document

        children = doc.child_nodes
        self.assertEqual(0, len(children))
        node = doc.first_child
        self.assertIsNone(node)
        node = doc.last_child
        self.assertIsNone(node)
        node = doc.previous_sibling
        self.assertIsNone(node)
        node = doc.next_sibling
        self.assertIsNone(node)
        self.assertFalse(doc.has_child_nodes())

        # <?xml-stylesheet ?>
        # <!--comment-->
        # <svg>
        # <g><path/></g>
        # <text/>
        # </svg>
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'g')
        root.append(group)
        path = doc.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        text = doc.create_element_ns('http://www.w3.org/2000/svg', 'text')
        root.append(text)
        comment = doc.create_comment('comment')
        doc.insert_before(comment, root)
        pi = doc.create_processing_instruction('xml-stylesheet')
        doc.insert_before(pi, comment)

        children = doc.child_nodes
        self.assertEqual([pi, comment, root], children)
        node = doc.first_child
        self.assertEqual(pi, node)
        node = doc.last_child
        self.assertEqual(root, node)
        node = doc.previous_sibling
        self.assertIsNone(node)
        node = doc.next_sibling
        self.assertIsNone(node)
        self.assertTrue(doc.has_child_nodes())

    def test_document_children(self):
        doc = window.document

        children = doc.children
        self.assertEqual(0, len(children))
        self.assertEqual(0, doc.child_element_count)
        self.assertIsNone(doc.first_element_child)
        self.assertIsNone(doc.last_element_child)

        pi = doc.create_processing_instruction('xml-stylesheet')
        comment = doc.create_comment('demo')
        root = doc.create_element('svg')

        # pi.addnext(root)  # TypeError
        # pi.addnext(comment)

        # comment.addprevious(pi)
        # comment.addnext(root)  # TypeError

        root.addprevious(pi)
        root.addprevious(comment)

        doc.append_child(root)

        comment2 = doc.create_comment('sample')
        root.append_child(comment2)
        style = doc.create_element('style')
        root.append_child(style)
        group = doc.create_element('g')
        root.append_child(group)
        path = doc.create_element('path')
        group.append_child(path)

        comment3 = doc.create_comment('end')
        doc.append_child(comment3)

        # print(doc.tostring(pretty_print=True).decode())
        # <?xml-stylesheet ?>
        # <!--demo-->
        # <svg xmlns="http://www.w3.org/2000/svg">
        #   <!--sample-->
        #   <style/>
        #   <g>
        #     <path/>
        #   </g>
        # </svg>
        # <!--end-->

        self.assertEqual(1, doc.child_element_count)
        children = doc.children
        self.assertEqual(1, len(children))
        self.assertEqual([root], children)
        self.assertEqual(root, doc.first_element_child)
        self.assertEqual(root, doc.last_element_child)

        self.assertEqual([comment2, style, group], list(root))
        self.assertEqual(2, root.child_element_count)
        children = root.children
        self.assertEqual(2, len(children))
        self.assertEqual([style, group], children)
        self.assertEqual(style, root.first_element_child)
        self.assertEqual(group, root.last_element_child)

    def test_document_create_attribute(self):
        doc = window.document

        name = 'id'
        attr = doc.create_attribute(name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(2, attr.node_type)
        self.assertEqual(name, attr.node_name)
        self.assertEqual('', attr.node_value)
        self.assertEqual(doc, attr.owner_document)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)
        self.assertEqual('', attr.text_content)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(name, attr.local_name)
        self.assertEqual(name, attr.name)
        self.assertEqual('', attr.value)
        self.assertIsNone(attr.owner_element)

        value = 'id01'
        attr.value = value
        self.assertEqual(2, attr.node_type)
        self.assertEqual(name, attr.node_name)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(doc, attr.owner_document)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)
        self.assertEqual(value, attr.text_content)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(name, attr.local_name)
        self.assertEqual(name, attr.name)
        self.assertEqual(value, attr.value)
        self.assertIsNone(attr.owner_element)

    def test_document_create_attribute_ns(self):
        doc = window.document

        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        qualified_name = '{{{}}}{}'.format(namespace, local_name)
        attr = doc.create_attribute_ns(namespace, local_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(2, attr.node_type)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual('', attr.node_value)
        self.assertEqual(doc, attr.owner_document)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)
        self.assertEqual('', attr.text_content)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual('', attr.value)
        self.assertIsNone(attr.owner_element)

        attr = doc.create_attribute_ns('', qualified_name)
        self.assertEqual(2, attr.node_type)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual('', attr.node_value)
        self.assertEqual(doc, attr.owner_document)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)
        self.assertEqual('', attr.text_content)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual('', attr.value)
        self.assertIsNone(attr.owner_element)

        attr = doc.create_attribute_ns(None, qualified_name)
        self.assertEqual(2, attr.node_type)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual('', attr.node_value)
        self.assertEqual(doc, attr.owner_document)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)
        self.assertEqual('', attr.text_content)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual('', attr.value)
        self.assertIsNone(attr.owner_element)

        value = 'ja'
        attr.value = value
        self.assertEqual(2, attr.node_type)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(doc, attr.owner_document)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(value, attr.value)
        self.assertIsNone(attr.owner_element)

    def test_document_create_comment(self):
        doc = window.document

        data = 'Comment'
        comment = doc.create_comment(data)
        self.assertIsInstance(comment, Comment)
        self.assertEqual(8, Node.COMMENT_NODE)
        self.assertEqual(8, comment.node_type)
        self.assertEqual(doc, comment.owner_document)
        self.assertIsNone(comment.parent_element)
        self.assertIsNone(comment.parent_node)
        self.assertEqual('#comment', comment.node_name)
        self.assertEqual(data, comment.data)
        self.assertEqual(data, comment.node_value)
        self.assertEqual(data, comment.text_content)

    def test_document_create_element(self):
        doc = window.document

        root = doc.create_element(
            'svg',
            attrib={
               'viewBox': '0 0 200 300',
            })
        self.assertIsInstance(root, SVGSVGElement)
        self.assertEqual(1, Node.ELEMENT_NODE)
        self.assertEqual(1, root.node_type)
        self.assertEqual(doc, root.owner_document)
        self.assertIsNone(root.parent_element)
        self.assertIsNone(root.parent_node)
        self.assertEqual('svg', root.node_name)
        self.assertEqual('svg', root.tag_name)
        self.assertEqual('svg', root.local_name)
        self.assertEqual('0 0 200 300', root.get_attribute('viewBox'))

    def test_document_create_element_ns(self):
        doc = window.document

        root = doc.create_element_ns(
            'http://www.w3.org/2000/svg',
            'svg',
            attrib={
               'viewBox': '0 0 200 300',
            })
        self.assertIsInstance(root, SVGSVGElement)
        self.assertEqual(1, Node.ELEMENT_NODE)
        self.assertEqual(1, root.node_type)
        self.assertEqual(doc, root.owner_document)
        self.assertIsNone(root.parent_element)
        self.assertIsNone(root.parent_node)
        self.assertEqual('svg', root.node_name)
        self.assertEqual('svg', root.tag_name)
        self.assertEqual('svg', root.local_name)
        self.assertEqual('0 0 200 300', root.get_attribute('viewBox'))

        video = doc.create_element_ns(
            'http://www.w3.org/1999/xhtml',
            'video',
            attrib={
                'width': '100',
                'height': '150',
            })
        self.assertIsInstance(video, HTMLVideoElement)
        self.assertEqual(1, video.node_type)
        self.assertEqual(doc, video.owner_document)
        self.assertIsNone(video.parent_element)
        self.assertIsNone(video.parent_node)
        self.assertEqual('html:video', video.node_name)
        self.assertEqual('html:video', video.tag_name)
        self.assertEqual('video', video.local_name)
        self.assertEqual('100', video.get_attribute('width'))
        self.assertEqual('150', video.get_attribute('height'))

    def test_document_create_processing_instruction(self):
        doc = window.document

        target = 'xml-stylesheet'
        pi = doc.create_processing_instruction(target)
        self.assertIsInstance(pi, ProcessingInstruction)
        self.assertEqual(7, pi.node_type)
        self.assertEqual(target, pi.node_name)
        self.assertEqual('', pi.node_value)
        self.assertEqual(doc, pi.owner_document)
        self.assertIsNone(pi.parent_element)
        self.assertIsNone(pi.parent_node)
        self.assertEqual('', pi.text_content)
        self.assertEqual('', pi.data)
        self.assertEqual(target, pi.target)

        data = 'href="style.css" type="text/css"'
        pi = doc.create_processing_instruction(target, data)
        self.assertIsInstance(pi, ProcessingInstruction)
        self.assertEqual(7, pi.node_type)
        self.assertEqual(target, pi.node_name)
        self.assertEqual(data, pi.node_value)
        self.assertEqual(doc, pi.owner_document)
        self.assertIsNone(pi.parent_element)
        self.assertIsNone(pi.parent_node)
        self.assertEqual(data, pi.text_content)
        self.assertEqual(data, pi.data)
        self.assertEqual(target, pi.target)
        self.assertEqual('style.css', pi.get('href'))
        self.assertEqual('text/css', pi.get('type'))

    def test_document_extend(self):
        # Document.extend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = doc = parser.create_document(svg_ns)
        self.assertIsNone(doc.document_element)

        attr = parser.create_attribute('foo')
        # parent.extend([attr])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([attr]))

        comment = parser.create_comment('foo')
        # parent.extend([comment])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([comment]))

        doc2 = parser.create_document(svg_ns)
        # parent.extend([doc2])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([doc2]))

        pi = parser.create_processing_instruction('foo-bar')
        # parent.extend([pi])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([pi]))

        # '<svg/>'
        root = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(root.owner_document)
        parent.extend([root])
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual([root], list(doc))

        # parent.extend([attr])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([attr]))

        # '<svg/><!--foo-->'
        parent.extend([comment])
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual([root, comment], list(doc))

        # parent.extend([doc2])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([doc2]))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.append(element)
        self.assertRaises(TypeError,
                          lambda: parent.extend([element]))

        # '<svg/><!--foo--><?foo-bar ?>'
        parent.extend([pi])
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([root, comment, pi], list(doc))

        pi1 = parser.create_processing_instruction('foo-bar')
        pi2 = parser.create_processing_instruction('foo-bar')
        self.assertIsNone(pi1.owner_document)
        self.assertIsNone(pi2.owner_document)
        parent.extend([pi1, pi2])
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([root, comment, pi, pi1, pi2], list(doc))

    def test_document_get_elements(self):
        doc = window.document

        element = doc.get_element_by_id('path01')
        self.assertEqual(None, element)

        elements = doc.get_elements_by_class_name('EndPoint')
        self.assertEqual([], elements)

        elements = doc.get_elements_by_tag_name('rect')
        self.assertEqual([], elements)

        elements = doc.get_elements_by_tag_name_ns(None, 'rect')
        self.assertEqual([], elements)

        elements = doc.get_elements_by_tag_name_ns('*', 'rect')
        self.assertEqual([], elements)

        elements = doc.get_elements_by_tag_name_ns(
                'http://www.w3.org/2000/svg',
                'rect')
        self.assertEqual([], elements)

        elements = doc.get_elements_by_tag_name_ns(
                'http://www.w3.org/1999/xhtml',
                'rect')
        self.assertEqual([], elements)

        parser = doc.implementation.parser
        root = parser.fromstring(SVG_CUBIC01)
        doc.append(root)
        for it in doc.document_element.iter():
            self.assertIsInstance(it, Node)
            self.assertEqual(doc, it.owner_document)

        root = doc.document_element
        root.id = 'root'
        root.class_name = 'Root'

        # Document.get_element_by_id()
        element = doc.get_element_by_id('root')
        self.assertIsNotNone(element)
        self.assertEqual(root, element)

        element = doc.get_element_by_id('path01')
        self.assertIsNotNone(element)
        self.assertEqual('path', element.local_name)
        self.assertEqual('path01', element.id)

        element = doc.get_element_by_id('path04')
        self.assertIsNone(element)

        # Document.get_elements_by_class_name()
        elements = doc.get_elements_by_class_name('Root')
        self.assertEqual(1, len(elements))
        self.assertEqual(root, elements[0])

        elements = doc.get_elements_by_class_name('EndPoint')
        self.assertEqual(3, len(elements))

        elements = doc.get_elements_by_class_name('AutoCtlPoint')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_class_name('EndPoint AutoCtlPoint')
        self.assertEqual(0, len(elements))

        # Document.get_elements_by_tag_name()
        elements = doc.get_elements_by_tag_name('svg')
        self.assertEqual(1, len(elements))
        self.assertEqual(root, elements[0])

        elements = doc.get_elements_by_tag_name('rect')
        self.assertEqual(1, len(elements))
        self.assertEqual('Border', elements[0].class_name)

        # Document.get_elements_by_tag_name_ns()
        elements = doc.get_elements_by_tag_name_ns(
            None,
            'svg')
        self.assertEqual(1, len(elements))
        self.assertEqual(root, elements[0])

        elements = doc.get_elements_by_tag_name_ns(
            '*',
            'svg')
        self.assertEqual(1, len(elements))
        self.assertEqual(root, elements[0])

        elements = doc.get_elements_by_tag_name_ns(
            'http://www.w3.org/2000/svg',
            'svg')
        self.assertEqual(1, len(elements))
        self.assertEqual(root, elements[0])

        elements = doc.get_elements_by_tag_name_ns(None, 'rect')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_tag_name_ns('*', 'rect')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_tag_name_ns(
            'http://www.w3.org/2000/svg',
            'rect')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_tag_name_ns(
            'http://www.w3.org/1999/xhtml',
            'rect')
        self.assertEqual(0, len(elements))

    def test_document_init01(self):
        # Window: window
        # Document: Document()
        doc = Document()
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('application/xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertIsNone(doc.implementation)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)
        self.assertEqual('about:blank', doc.location.href)
        self.assertRaises(ValueError,
                          lambda: doc.create_comment('test'))
        self.assertRaises(ValueError,
                          lambda: doc.create_element('svg'))
        self.assertRaises(ValueError,
                          lambda: doc.create_element_ns(
                              'http://www.w3.org/2000/svg',
                              'svg'))
        self.assertEqual([], doc.get_elements_by_class_name('test'))
        self.assertEqual([], doc.get_elements_by_tag_name('svg'))
        self.assertEqual([], doc.get_elements_by_tag_name_ns(
            'http://www.w3.org/2000/svg',
            'svg'))
        self.assertEqual(doc, doc.get_root_node())

    def test_document_init02(self):
        # Window: window
        # Document: XMLDocument()
        doc = XMLDocument()
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('application/xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertIsNone(doc.implementation)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)
        self.assertEqual('about:blank', doc.location.href)
        self.assertRaises(ValueError,
                          lambda: doc.create_comment('test'))
        self.assertRaises(ValueError,
                          lambda: doc.create_element('svg'))
        self.assertRaises(ValueError,
                          lambda: doc.create_element_ns(
                              'http://www.w3.org/2000/svg',
                              'svg'))
        self.assertEqual([], doc.get_elements_by_class_name('test'))
        self.assertEqual([], doc.get_elements_by_tag_name('svg'))
        self.assertEqual([], doc.get_elements_by_tag_name_ns(
            'http://www.w3.org/2000/svg',
            'svg'))
        self.assertEqual(doc, doc.get_root_node())

    def test_document_init03(self):
        # Window: window
        # Document: SVGDOMImplementation.create_document()
        impl = SVGDOMImplementation()
        doc = impl.create_document(None, '')
        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('application/xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertEqual(impl, doc.implementation)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)
        self.assertEqual('about:blank', doc.location.href)

        root = doc.create_element('svg')
        self.assertIsInstance(root, SVGSVGElement)
        doc.append_child(root)
        self.assertEqual(root, doc.document_element)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg"/>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_init04(self):
        # Window: window
        # Document: SVGDOMImplementation.create_document()
        impl = SVGDOMImplementation()
        doc = impl.create_document('http://www.w3.org/2000/svg', '')
        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('image/svg+xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertEqual(impl, doc.implementation)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)
        self.assertEqual('about:blank', doc.location.href)

        root = doc.create_element('svg')
        self.assertIsInstance(root, SVGSVGElement)
        doc.append_child(root)
        self.assertEqual(root, doc.document_element)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg"/>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_init05(self):
        # Window: window
        # Document: SVGDOMImplementation.create_document()
        impl = SVGDOMImplementation()
        doc = impl.create_document('http://www.w3.org/2000/svg', 'svg')
        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('image/svg+xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertEqual(impl, doc.implementation)
        self.assertIsNotNone(doc.document_element)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)

        root = doc.document_element
        self.assertIsInstance(root, SVGSVGElement)
        self.assertEqual(0, len(root.keys()))
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg"/>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_init06(self):
        # Window: window
        # Document: SVGDOMImplementation.create_svg_document()
        impl = SVGDOMImplementation()
        doc = impl.create_svg_document(
            nsmap={'html': 'http://www.w3.org/1999/xhtml'}
        )
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('image/svg+xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertEqual(impl, doc.implementation)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertEqual('about:blank', doc.location.href)

        root = doc.document_element
        self.assertIsInstance(root, SVGSVGElement)
        self.assertEqual(0, len(root.keys()))

        video = doc.create_element_ns('http://www.w3.org/1999/xhtml', 'video')
        root.append_child(video)

        source = doc.create_element_ns('http://www.w3.org/1999/xhtml',
                                       'source')
        video.append_child(source)

        expected = \
            '<svg xmlns:html="http://www.w3.org/1999/xhtml"' \
            ' xmlns="http://www.w3.org/2000/svg">' \
            '<html:video><html:source/></html:video>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_init07(self):
        # Window: Window()
        # Document: Window().document
        win = Window(SVGDOMImplementation())
        doc = win.document
        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('image/svg+xml', doc.content_type)
        self.assertNotEqual(window, doc.default_view)
        self.assertEqual(win, doc.default_view)
        self.assertNotEqual(window.document.implementation,
                            doc.implementation)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNotNone(doc.document_element)
        self.assertIsInstance(doc.document_element, SVGSVGElement)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)
        self.assertEqual('about:blank', doc.location.href)

    def test_document_init08(self):
        # Window: window
        # Document: window.document
        doc = window.document
        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(9, Node.DOCUMENT_NODE)
        self.assertEqual(9, doc.node_type)
        self.assertEqual('#document', doc.node_name)
        self.assertIsNone(doc.node_value)
        self.assertIsNone(doc.text_content)
        self.assertEqual('image/svg+xml', doc.content_type)
        self.assertEqual(window, doc.default_view)
        self.assertEqual('about:blank', doc.url)
        self.assertEqual('about:blank', doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)
        self.assertIsNone(doc.parent_element)
        self.assertIsNone(doc.parent_node)
        self.assertEqual('about:blank', doc.location.href)

    def test_document_insert(self):
        svg_ns = 'http://www.w3.org/2000/svg'
        impl = SVGDOMImplementation()
        doc = impl.create_document('http://www.w3.org/2000/svg')
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.insert(0, root)
        self.assertEqual(root, doc.document_element)
        self.assertEqual([root], list(doc))

        attr = doc.create_attribute('foo')
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.insert(0, attr))

        pi = doc.create_processing_instruction('xml-stylesheet')
        doc.prepend(pi)
        self.assertEqual([pi, root], doc.child_nodes)
        self.assertEqual([pi, root], list(doc))

        comment = doc.create_comment('demo')
        doc.insert(1, comment)
        self.assertEqual([pi, comment, root], doc.child_nodes)
        self.assertEqual([pi, comment, root], list(doc))

        comment2 = doc.create_comment('comment2')
        doc.insert(-1, comment2)
        self.assertEqual([pi, comment, comment2, root], doc.child_nodes)
        self.assertEqual([pi, comment, comment2, root], list(doc))

        doc2 = doc.implementation.create_document(svg_ns)
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.insert(0, doc2))

        element = doc.create_element_ns(svg_ns, 'svg')
        self.assertRaises(TypeError,
                          lambda: doc.insert(0, element))

    def test_document_insert_before01(self):
        # Document
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = doc = parser.create_document(svg_ns)
        self.assertIsNone(doc.document_element)

        # 1st attempt
        attr = parser.create_attribute('foo')
        # result = parent.insert_before(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, None))

        comment = parser.create_comment('foo')
        # result = parent.insert_before(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(comment, None))

        doc2 = parser.create_document(svg_ns)
        # result = parent.insert_before(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # result = parent.insert_before(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(pi, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        result = parent.insert_before(element, None)
        self.assertEqual(element, result)
        self.assertEqual(doc, element.owner_document)
        self.assertEqual(element, doc.document_element)
        root = doc.document_element
        self.assertEqual([root], list(doc))

        # 2nd attempt
        attr = parser.create_attribute('foo')
        # result = parent.insert_before(attr, root)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, root))

        # comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        result = parent.insert_before(comment, root)
        self.assertEqual(comment, result)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual([comment, root], list(doc))

        # doc2 = parser.create_document(svg_ns)
        # parent.insert_before(doc2, comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, comment))

        element = parser.create_element_ns(svg_ns, 'svg')
        # result = parent.insert_before(element, comment)
        self.assertRaises(TypeError,
                          lambda: parent.insert_before(element, comment))

        # pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        result = parent.insert_before(pi, comment)
        self.assertEqual(pi, result)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([pi, comment, root], list(doc))

    def test_document_insert_before02(self):
        # Document
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        impl = SVGDOMImplementation()

        doc = impl.create_document(svg_ns)
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        # parser = etree.XMLParser()
        # root = parser.makeelement('svg')
        # self.assertNotIsInstance(root, Node)
        # self.assertRaises(TypeError, lambda: doc.insert_before(root, None))

        # '<svg/>'
        root = doc.create_element_ns(svg_ns, 'svg')
        self.assertIsInstance(root, Node)
        self.assertEqual(doc, root.owner_document)
        result = doc.insert_before(root, None)
        self.assertEqual(root, result)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual([root], list(doc))

        root2 = doc.create_element_ns(svg_ns, 'svg')
        comment = doc.create_comment('demo')
        # doc.insert_before(comment, root2)
        self.assertRaises(NotFoundError,
                          lambda: doc.insert_before(comment, root2))

        # '<svg><defs/></svg>'
        defs = doc.create_element_ns(svg_ns, 'defs')
        self.assertEqual(doc, defs.owner_document)
        result = root.insert_before(defs, None)
        self.assertEqual(defs, result)
        self.assertEqual(doc, defs.owner_document)
        self.assertEqual([root], list(doc))

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # '<svg><title/><defs/></svg>'
        title = doc.create_element_ns(svg_ns, 'title')
        self.assertEqual(doc, title.owner_document)
        result = root.insert_before(title, defs)
        self.assertEqual(title, result)
        self.assertEqual(doc, title.owner_document)
        self.assertEqual([root], list(doc))

        # '<svg><title/><defs/><style/></svg>'
        style = doc.create_element_ns(svg_ns, 'style')
        self.assertEqual(doc, style.owner_document)
        result = root.insert_before(style, None)
        self.assertEqual(style, result)
        self.assertEqual(doc, style.owner_document)
        self.assertEqual([root], list(doc))

        # '<svg><!--demo--><title/><defs/><style/></svg>'
        comment = doc.create_comment('demo')
        self.assertEqual(doc, comment.owner_document)
        result = root.insert_before(comment, title)
        self.assertEqual(comment, result)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual([root], list(doc))

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><style/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        g = doc.create_element_ns(svg_ns, 'g')
        path = doc.create_element_ns(svg_ns, 'path')
        result = g.append_child(path)
        self.assertEqual(path, result)
        self.assertEqual(doc, g.owner_document)
        self.assertEqual(doc, path.owner_document)
        self.assertEqual([root], list(doc))

        # '<svg>
        #  <!--demo-->
        #  <title/><defs/><style/><g><path/></g>
        #  </svg>'
        result = root.insert_before(g, None)
        self.assertEqual(g, result)
        self.assertEqual(doc, g.owner_document)
        self.assertEqual(doc, path.owner_document)
        self.assertEqual([root], list(doc))

        rect = doc.create_element_ns(svg_ns, 'rect')
        self.assertRaises(NotFoundError,
                          lambda: doc.insert_before(rect, path))
        self.assertEqual(doc, rect.owner_document)
        self.assertEqual(doc, path.owner_document)
        self.assertEqual([root], list(doc))

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><style/><g><path/></g>' \
            '</svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        for it in root.iter():
            with self.subTest(it=it,
                              it_owner_document=it.owner_document,
                              expected=doc):
                self.assertEqual(doc, it.owner_document)

        # link = parser.makeelement('link')
        # self.assertNotIsInstance(link, Node)
        # self.assertRaises(TypeError, lambda: root.insert_before(link, style))

        # '<svg>
        #  <!--demo-->
        #  <title/><defs/><link/><style/><g><path/></g>
        #  </svg>'
        link = doc.create_element_ns(svg_ns, 'link')
        self.assertIsInstance(link, Node)
        self.assertEqual(doc, link.owner_document)
        result = root.insert_before(link, style)
        self.assertEqual(link, result)
        self.assertEqual(doc, link.owner_document)
        self.assertEqual([root], list(doc))

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><link/><style/><g><path/></g>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # '<?xml-stylesheet href="1.css"?>
        #  <svg>
        #  <!--demo-->
        #  <title/><defs/><link/><style/><g><path/></g>
        #  </svg>'
        pi1 = doc.create_processing_instruction('xml-stylesheet',
                                                'href="1.css"')
        result = doc.insert_before(pi1, root)
        self.assertEqual(pi1, result)
        self.assertEqual(doc, pi1.owner_document)
        self.assertEqual([pi1, root], list(doc))

        # '<?xml-stylesheet href="1.css"?>
        #  <?xml-stylesheet href="2.css"?>
        #  <svg>
        #  <!--demo-->
        #  <title/><defs/><link/><style/><g><path/></g>
        #  </svg>'
        pi2 = doc.create_processing_instruction('xml-stylesheet',
                                                'href="2.css"')
        result = doc.insert_before(pi2, root)
        self.assertEqual(pi2, result)
        self.assertEqual(doc, pi2.owner_document)
        self.assertEqual([pi1, pi2, root], list(doc))

        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<?xml-stylesheet href="2.css"?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><link/><style/><g><path/></g>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_iter(self):
        doc = window.document
        parser = doc.implementation.parser
        root = parser.fromstring(SVG_SVG)
        doc.append(root)
        comment = doc.create_comment('demo')
        doc.prepend(comment)
        pi = doc.create_processing_instruction('xml-stylesheet')
        doc.prepend(pi)
        children = [node for node in doc]
        self.assertEqual(3, len(children))
        self.assertEqual([pi, comment, doc.document_element], children)

        children = [node for node in doc.iter()]
        self.assertEqual(10, len(children))
        self.assertEqual(pi, children[0])
        self.assertEqual(comment, children[1])
        self.assertEqual(doc.document_element, children[2])
        self.assertEqual('svg', children[2].tag_name)
        self.assertEqual('g', children[3].tag_name)
        self.assertEqual('gtop', children[3].id)
        self.assertEqual('g', children[4].tag_name)
        self.assertEqual('svgstar', children[4].id)
        self.assertEqual('path', children[5].tag_name)
        self.assertEqual('svgbar', children[5].id)
        self.assertEqual('use', children[6].tag_name)
        self.assertEqual('use1', children[6].id)
        self.assertEqual('use', children[7].tag_name)
        self.assertEqual('use2', children[7].id)
        self.assertEqual('use', children[8].tag_name)
        self.assertEqual('use3', children[8].id)
        self.assertEqual('use', children[9].tag_name)
        self.assertEqual('usetop', children[9].id)

        children = [node for node in doc.iter(tag='{*}use')]
        self.assertEqual(4, len(children))
        self.assertEqual('use', children[0].tag_name)
        self.assertEqual('use1', children[0].id)
        self.assertEqual('use', children[1].tag_name)
        self.assertEqual('use2', children[1].id)
        self.assertEqual('use', children[2].tag_name)
        self.assertEqual('use3', children[2].id)
        self.assertEqual('use', children[3].tag_name)
        self.assertEqual('usetop', children[3].id)

        children = [node for node in doc.iter(tag=('{*}svg', '{*}g'))]
        self.assertEqual(3, len(children))
        self.assertEqual('svg', children[0].tag_name)
        self.assertEqual('g', children[1].tag_name)
        self.assertEqual('gtop', children[1].id)
        self.assertEqual('g', children[2].tag_name)
        self.assertEqual('svgstar', children[2].id)

    def test_document_location_assign(self):
        doc = window.document
        self.assertIsNone(doc.document_element)
        self.assertEqual(window, doc.default_view)

        path = os.path.join(here, 'svg/svg.svg')
        src = Path(path).absolute().as_uri()
        doc.location.assign(src)
        self.assertEqual(src, doc.location.href)
        self.assertEqual(src, doc.url)
        self.assertEqual(src, doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNotNone(doc.document_element)
        nodes = [x for x in doc.document_element.iter()]
        self.assertEqual(8, len(nodes))
        for it in nodes:
            self.assertIsInstance(it, Node)
            self.assertEqual(doc, it.owner_document)
        self.assertEqual('svg', nodes[0].tag_name)
        self.assertEqual('g', nodes[1].tag_name)
        self.assertEqual('gtop', nodes[1].id)
        self.assertEqual('g', nodes[2].tag_name)
        self.assertEqual('svgstar', nodes[2].id)
        self.assertEqual('path', nodes[3].tag_name)
        self.assertEqual('svgbar', nodes[3].id)
        self.assertEqual('use', nodes[4].tag_name)
        self.assertEqual('use1', nodes[4].id)
        self.assertEqual('use', nodes[5].tag_name)
        self.assertEqual('use2', nodes[5].id)
        self.assertEqual('use', nodes[6].tag_name)
        self.assertEqual('use3', nodes[6].id)
        self.assertEqual('use', nodes[7].tag_name)
        self.assertEqual('usetop', nodes[7].id)

        src = 'about:blank'
        doc.location = src
        self.assertEqual(src, doc.location.href)
        self.assertEqual(src, doc.url)
        self.assertEqual(src, doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)

    def test_document_prepend01(self):
        # Document
        # ParentNode.prepend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = doc = parser.create_document(svg_ns)
        self.assertIsNone(doc.document_element)

        # 1st attempt
        attr = parser.create_attribute('foo')
        # parent.prepend(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(attr))

        comment = parser.create_comment('foo')
        # parent.prepend(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.prepend(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(doc2))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.prepend(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(pi))

        # '<svg/>'
        root = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(root.owner_document)
        parent.prepend(root)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual([root], list(doc))

        # 2nd attempt
        # attr = parser.create_attribute('foo')
        # parent.prepend(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(attr))

        # '<!--foo--><svg/>'
        # comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.prepend(comment)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual([comment, root], list(doc))

        # doc2 = parser.create_document(svg_ns)
        # parent.prepend(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.prepend(element)
        self.assertRaises(TypeError,
                          lambda: parent.prepend(element))

        # '<?xml-stylesheet ?><!--foo--><svg/>'
        # pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.prepend(pi)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([pi, comment, root], list(doc))

        expected = \
            '<?xml-stylesheet ?>' \
            '<!--foo-->' \
            '<svg xmlns="http://www.w3.org/2000/svg"/>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_prepend02(self):
        # Document
        # ParentNode.prepend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_document(svg_ns)

        args = 'foo', 'bar', 'baz'
        # parent.prepend(*args)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(*args))

        element = parser.create_element_ns(svg_ns, 'svg')
        args = element, 'foo', 'bar', 'baz'
        # parent.prepend(*args)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(*args))

    def test_document_prepend03(self):
        # Document
        # ParentNode.prepend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = doc = parser.create_document(svg_ns)
        self.assertIsNone(doc.document_element)

        root = parser.create_element_ns(svg_ns, 'svg')
        comment = parser.create_comment('foo')
        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(root.owner_document)
        self.assertIsNone(comment.owner_document)
        self.assertIsNone(pi.owner_document)

        # element node must be insert first
        args = pi, comment, root
        # parent.append(*args)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(*args))

        # '<svg/>'
        parent.prepend(root)  # insert a node as the root element
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual([root], list(doc))

        # '<?xml-stylesheet ?><!--foo--><svg/>'
        parent.prepend(*args)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual([pi, comment, root], list(doc))

        pi1 = parser.create_processing_instruction('xml-stylesheet')
        pi2 = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi1.owner_document)
        self.assertIsNone(pi2.owner_document)
        parent.prepend(pi1, pi2)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, pi1.owner_document)
        self.assertEqual(doc, pi2.owner_document)
        self.assertEqual([pi1, pi2, pi, comment, root], list(doc))

    def test_document_query_selector_all(self):
        doc = window.document
        parser = doc.implementation.parser
        root = parser.fromstring(SVG_SVG)
        doc.append(root)

        sub_root = doc.create_element('svg', {'id': 'svg2'})
        root = doc.document_element
        root.append(sub_root)
        # print(doc.tostring(pretty_print=True).decode())

        selectors = 'rect, svg|rect'
        elements = doc.query_selector_all(selectors)
        # print((selectors, elements))
        self.assertEqual(0, len(elements))

        element = doc.query_selector(selectors)
        self.assertIsNone(element)

        selectors = 'svg, svg|svg'
        elements = doc.query_selector_all(selectors)
        # print((selectors, elements))
        self.assertEqual(2, len(elements))
        self.assertTrue(root in elements)
        self.assertTrue(sub_root in elements)

        element = doc.query_selector(selectors)
        self.assertEqual(root, element)

        selectors = 'svg:not(:root), svg|svg:not(:root)'
        elements = doc.query_selector_all(selectors)
        # print((selectors, elements))
        self.assertEqual(1, len(elements))
        self.assertTrue(sub_root in elements)

        element = doc.query_selector(selectors)
        self.assertEqual(sub_root, element)

        selectors = '*[xlink|href]'
        elements = doc.query_selector_all(selectors)
        # print((selectors, elements))
        self.assertEqual(4, len(elements))
        ids = [e.id for e in elements]
        self.assertEqual('use1', ids[0])
        self.assertEqual('use2', ids[1])
        self.assertEqual('use3', ids[2])
        self.assertEqual('usetop', ids[3])

        element = doc.query_selector(selectors)
        self.assertEqual('use1', element.id)

    def test_document_remove(self):
        # Document.remove()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_document(svg_ns, 'svg')

        attr = doc.create_attribute('foo')
        comment = doc.create_comment('foo')
        root = doc.document_element
        pi = doc.create_processing_instruction('foo-bar')
        doc.prepend(pi, comment)
        self.assertEqual([pi, comment, root], list(doc))

        # doc.remove(attr)
        self.assertRaises(NotFoundError, lambda: doc.remove(attr))

        doc.remove(comment)
        self.assertEqual([pi, root], list(doc))

        # doc.remove(doc)
        self.assertRaises(NotFoundError, lambda: doc.remove(doc))

        doc.remove(pi)
        self.assertEqual([root], list(doc))

        doc.remove(root)
        self.assertEqual([], list(doc))
        self.assertEqual(0, len(doc))
        self.assertIsNone(doc.document_element)

        # remove again
        # doc.remove(root)
        self.assertRaises(NotFoundError, lambda: doc.remove(root))

    def test_document_remove_child(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document('http://www.w3.org/2000/svg')
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        root = doc.create_element('svg')
        self.assertEqual(doc, root.owner_document)
        self.assertRaises(NotFoundError, lambda: doc.remove_child(root))

        # <svg/>
        doc.append_child(root)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)

        # <svg>
        # <title/>
        # </svg>
        title = doc.create_element('title')
        root.append_child(title)

        # <svg>
        # <title/>
        # <defs/>
        # </svg>
        defs = doc.create_element('defs')
        root.append_child(defs)

        # <svg>
        # <title/>
        # <defs><style/></defs>
        # </svg>
        style = doc.create_element('style')
        defs.append_child(style)

        # <!--demo-->
        # <svg>
        # <title/>
        # <defs><style/></defs>
        # </svg>
        comment = doc.create_comment('demo')
        doc.prepend(comment)

        # <?xml-stylesheet href="1.css"?>
        # <!--demo-->
        # <svg>
        # <title/>
        # <defs><style/></defs>
        # </svg>
        pi1 = doc.create_processing_instruction('xml-stylesheet',
                                                'href="1.css"')
        doc.insert_before(pi1, comment)

        # <?xml-stylesheet href="1.css"?>
        # <?xml-stylesheet href="2.css"?>
        # <!--demo-->
        # <svg>
        # <title/>
        # <defs><style/></defs>
        # </svg>
        pi2 = doc.create_processing_instruction('xml-stylesheet',
                                                'href="2.css"')
        doc.insert_before(pi2, comment)

        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<?xml-stylesheet href="2.css"?>' \
            '<!--demo-->' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs><style/></defs>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        self.assertEqual(2, len(doc.document_element))
        self.assertTrue(style in defs)
        self.assertTrue(style not in doc.document_element)
        self.assertRaises(NotFoundError,
                          lambda: doc.remove_child(style))
        self.assertEqual(doc, style.owner_document)

        # remove <style> element
        removed = defs.remove_child(style)
        self.assertEqual(style, removed)
        self.assertEqual(doc, style.owner_document)
        self.assertEqual('style', removed.local_name)
        self.assertEqual(2, len(doc.document_element))
        self.assertTrue(style not in defs)
        self.assertTrue(style not in doc.document_element)

        # remove a comment node
        removed = doc.remove_child(comment)
        self.assertEqual(comment, removed)
        self.assertEqual(doc, comment.owner_document)

        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<?xml-stylesheet href="2.css"?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # remove a processing instruction node
        removed = doc.remove_child(pi2)
        self.assertEqual(pi2, removed)
        self.assertEqual(doc, pi2.owner_document)

        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # remove a root node
        removed = doc.remove_child(root)
        self.assertEqual(root, removed)
        self.assertEqual(doc, root.owner_document)
        self.assertIsNone(doc.document_element)

    def test_document_replace(self):
        # Document.replace()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_document(svg_ns, 'svg')
        root = doc.document_element
        comment = doc.create_comment('1')
        pi = doc.create_processing_instruction('foo-bar')
        comment2 = doc.create_comment('2')

        doc.prepend(pi, comment)
        doc.append(comment2)
        self.assertEqual([pi, comment, root, comment2], list(doc))

        # replace child node with Attr node
        attr = doc.create_attribute('foo')
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(pi, attr))

        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(comment, attr))

        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(root, attr))

        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(comment2, attr))

        # replace child node with Comment node
        comment3 = doc.create_comment('3')
        self.assertRaises(NotFoundError,
                          lambda: doc.replace(attr, comment3))

        doc.replace(pi, comment3)
        self.assertEqual([comment3, comment, root, comment2], list(doc))

        doc.replace(comment2, comment)
        self.assertEqual([comment3, root, comment], list(doc))

        # remove(root) + append(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(root, comment))

        doc.append(root)  # [comment3, root, comment]
        doc.prepend(pi)
        self.assertEqual([pi, comment3, root, comment], list(doc))

        # replace child node with Document node
        doc2 = doc.implementation.create_document(svg_ns, 'svg')
        self.assertRaises(NotFoundError,
                          lambda: doc.replace(attr, doc2))

        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(pi, doc2))

        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(comment, doc2))

        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(root, doc2))

        # replace child node with Element node
        element = doc.create_element_ns(svg_ns, 'svg')
        self.assertRaises(NotFoundError,
                          lambda: doc.replace(attr, element))

        self.assertRaises(TypeError,
                          lambda: doc.replace(pi, element))

        self.assertRaises(TypeError,
                          lambda: doc.replace(comment, element))

        doc.replace(root, element)
        self.assertEqual([element], list(doc))

        doc.replace(element, root)
        self.assertEqual([pi, comment3, root, comment], list(doc))

        # replace child node with PI node
        pi2 = doc.create_processing_instruction('foo-bar-baz')
        self.assertRaises(NotFoundError,
                          lambda: doc.replace(attr, pi2))

        doc.replace(pi, pi2)
        self.assertEqual([pi2, comment3, root, comment], list(doc))

        doc.replace(comment3, pi)
        self.assertEqual([pi2, pi, root, comment], list(doc))

        doc.remove(pi2)
        self.assertEqual([pi, root, comment], list(doc))
        self.assertRaises(HierarchyRequestError,
                          lambda: doc.replace(root, pi2))
        self.assertEqual(0, len(doc))

    def test_document_replace_child(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document('http://www.w3.org/2000/svg', 'svg')
        self.assertIsNone(doc.owner_document)
        root = doc.document_element
        self.assertEqual(doc, root.owner_document)

        title = doc.create_element('title')
        root.append_child(title)

        defs = doc.create_element('defs')
        root.append_child(defs)

        comment = doc.create_comment('demo')
        doc.insert_before(comment, root)

        expected = \
            '<!--demo-->' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/>' \
            '<defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # <!--demo--> -> <?xml-stylesheet ?>
        pi = doc.create_processing_instruction('xml-stylesheet')
        result = doc.replace_child(pi, comment)
        self.assertEqual(comment, result)
        self.assertEqual(doc, pi.owner_document)
        self.assertEqual(doc, comment.owner_document)
        expected = \
            '<?xml-stylesheet ?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/>' \
            '<defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # <title/> -> <style/>
        style = doc.create_element('style')
        result = root.replace_child(style, title)
        self.assertEqual(title, result)
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(doc, title.owner_document)
        expected = \
            '<?xml-stylesheet ?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<style/>' \
            '<defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # <defs/> -> <!--demo-->
        result = root.replace_child(comment, defs)
        self.assertEqual(defs, result)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual(doc, defs.owner_document)
        expected = \
            '<?xml-stylesheet ?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<style/>' \
            '<!--demo-->' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        self.assertRaises(NotFoundError,
                          lambda: doc.replace_child(defs, style))
        self.assertRaises(NotFoundError,
                          lambda: root.replace_child(defs, pi))

        root2 = doc.create_element('svg')
        doc.replace_child(root2, root)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg"/>'
        self.assertEqual(expected, doc.tostring().decode())
        for it in root.iter():
            self.assertEqual(doc, it.owner_document)
        for it in root2.iter():
            self.assertEqual(doc, it.owner_document)

        # parser = etree.XMLParser()
        # link = parser.makeelement('link')
        # self.assertNotIsInstance(link, Node)
        # self.assertRaises(TypeError, lambda: root.replace_child(link, style))

    def test_parser_create_document(self):
        # SVGParser.create_document()
        parser = SVGParser()
        doc1 = parser.create_document(None)
        self.assertIsInstance(doc1, XMLDocument)
        self.assertEqual(window, doc1.default_view)
        self.assertIsNone(doc1.document_element)
        self.assertNotEqual(window.document.implementation,
                            doc1.implementation)

        doc2 = parser.create_document(
            'http://www.w3.org/2000/svg',
            'svg',
            nsmap={
                'html': 'http://www.w3.org/1999/xhtml',
            })
        self.assertIsInstance(doc2, XMLDocument)
        self.assertEqual(window, doc2.default_view)
        self.assertIsNotNone(doc2.document_element)
        self.assertIsInstance(doc2.document_element, SVGSVGElement)
        self.assertEqual('svg', doc2.document_element.tag_name)
        self.assertNotEqual(window.document.implementation,
                            doc2.implementation)
        self.assertNotEqual(doc1.implementation,
                            doc2.implementation)
        self.assertDictEqual(
            {
                None: 'http://www.w3.org/2000/svg',
                'html': 'http://www.w3.org/1999/xhtml',
            },
            doc2.document_element.nsmap)

    def test_parser_create_svg_document(self):
        # SVGParser.create_svg_document()
        parser = SVGParser()
        doc1 = parser.create_svg_document()
        self.assertIsInstance(doc1, XMLDocument)
        self.assertEqual(window, doc1.default_view)
        self.assertIsNotNone(doc1.document_element)
        self.assertIsInstance(doc1.document_element, SVGSVGElement)
        self.assertEqual('svg', doc1.document_element.tag_name)
        self.assertNotEqual(window.document.implementation,
                            doc1.implementation)
        self.assertDictEqual(
            {
                None: 'http://www.w3.org/2000/svg',
            },
            doc1.document_element.nsmap)

        doc2 = parser.create_svg_document(
            nsmap={
                'html': 'http://www.w3.org/1999/xhtml',
            })
        self.assertIsInstance(doc2, XMLDocument)
        self.assertEqual(window, doc2.default_view)
        self.assertIsNotNone(doc2.document_element)
        self.assertIsInstance(doc2.document_element, SVGSVGElement)
        self.assertEqual('svg', doc2.document_element.tag_name)
        self.assertNotEqual(window.document.implementation,
                            doc2.implementation)
        self.assertNotEqual(doc1.implementation,
                            doc2.implementation)
        self.assertDictEqual(
            {
                None: 'http://www.w3.org/2000/svg',
                'html': 'http://www.w3.org/1999/xhtml',
            },
            doc2.document_element.nsmap)


if __name__ == '__main__':
    unittest.main()
