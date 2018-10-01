#!/usr/bin/env python3


import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path

from lxml import etree

sys.path.extend(['.', '..'])

from svgpy import Attr, Comment, Element, Node, ProcessingInstruction
from svgpy.element import HTMLVideoElement, SVGSVGElement
from svgpy.window import Document, SVGDOMImplementation, Window, XMLDocument, \
    window

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

    def test_document_append_child(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document(Element.SVG_NAMESPACE_URI)
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        # parser = etree.XMLParser()
        # root = parser.makeelement('svg')
        # self.assertNotIsInstance(root, Node)
        # self.assertRaises(TypeError, lambda: doc.append_child(root))

        comment = doc.create_comment('start')
        self.assertRaises(TypeError, lambda: doc.append_child(comment))

        root = doc.create_element('svg')
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

        title = doc.create_element('title')
        self.assertEqual(doc, title.owner_document)
        self.assertRaises(ValueError, lambda: comment.append_child(title))
        result = root.append_child(title)
        self.assertEqual(title, result)
        self.assertEqual(doc, title.owner_document)

        defs = doc.create_element('defs')
        self.assertEqual(doc, defs.owner_document)
        result = root.append_child(defs)
        self.assertEqual(defs, result)
        self.assertEqual(doc, defs.owner_document)

        style = doc.create_element('style')
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
        link = doc.create_element('link')
        self.assertIsInstance(link, Node)
        self.assertEqual(doc, link.owner_document)
        result = root.append_child(link)
        self.assertEqual(link, result)
        self.assertEqual(doc, link.owner_document)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<title/><defs/><style/><link/>' \
            '</svg>' \
            '<!--end-->'
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
        root = doc.create_element_ns(Element.SVG_NAMESPACE_URI, 'svg')
        doc.append(root)
        group = doc.create_element_ns(Element.SVG_NAMESPACE_URI, 'g')
        root.append(group)
        path = doc.create_element_ns(Element.SVG_NAMESPACE_URI, 'path')
        group.append(path)
        text = doc.create_element_ns(Element.SVG_NAMESPACE_URI, 'text')
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

        namespace = Element.XML_NAMESPACE_URI
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
            Element.SVG_NAMESPACE_URI,
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
            Element.XHTML_NAMESPACE_URI,
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
                Element.SVG_NAMESPACE_URI,
                'rect')
        self.assertEqual([], elements)

        elements = doc.get_elements_by_tag_name_ns(
                Element.XHTML_NAMESPACE_URI,
                'rect')
        self.assertEqual([], elements)

        doc.write(SVG_CUBIC01)
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
            Element.SVG_NAMESPACE_URI,
            'svg')
        self.assertEqual(1, len(elements))
        self.assertEqual(root, elements[0])

        elements = doc.get_elements_by_tag_name_ns(None, 'rect')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_tag_name_ns('*', 'rect')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_tag_name_ns(
            Element.SVG_NAMESPACE_URI,
            'rect')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_tag_name_ns(
            Element.XHTML_NAMESPACE_URI,
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
                              Element.SVG_NAMESPACE_URI,
                              'svg'))
        self.assertEqual([], doc.get_elements_by_class_name('test'))
        self.assertEqual([], doc.get_elements_by_tag_name('svg'))
        self.assertEqual([], doc.get_elements_by_tag_name_ns(
            Element.SVG_NAMESPACE_URI,
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
                              Element.SVG_NAMESPACE_URI,
                              'svg'))
        self.assertEqual([], doc.get_elements_by_class_name('test'))
        self.assertEqual([], doc.get_elements_by_tag_name('svg'))
        self.assertEqual([], doc.get_elements_by_tag_name_ns(
            Element.SVG_NAMESPACE_URI,
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
        doc = impl.create_document(Element.SVG_NAMESPACE_URI, '')
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
        doc = impl.create_document(Element.SVG_NAMESPACE_URI, 'svg')
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
            nsmap={'html': Element.XHTML_NAMESPACE_URI}
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

        video = doc.create_element_ns(Element.XHTML_NAMESPACE_URI, 'video')
        root.append_child(video)

        source = doc.create_element_ns(Element.XHTML_NAMESPACE_URI, 'source')
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

    def test_document_insert_before(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document(Element.SVG_NAMESPACE_URI)
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        parser = etree.XMLParser()
        root = parser.makeelement('svg')
        self.assertNotIsInstance(root, Node)
        self.assertRaises(TypeError, lambda: doc.insert_before(root, None))

        root = doc.create_element('svg')
        self.assertIsInstance(root, Node)
        self.assertEqual(doc, root.owner_document)
        result = doc.insert_before(root, None)
        self.assertEqual(root, result)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)

        # <defs/>
        defs = doc.create_element('defs')
        self.assertEqual(doc, defs.owner_document)
        result = root.insert_before(defs, None)
        self.assertEqual(defs, result)
        self.assertEqual(doc, defs.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<defs/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        # <title/><defs/>
        title = doc.create_element('title')
        self.assertEqual(doc, title.owner_document)
        result = root.insert_before(title, defs)
        self.assertEqual(title, result)
        self.assertEqual(doc, title.owner_document)

        # <title/><defs/><style/>
        style = doc.create_element('style')
        self.assertEqual(doc, style.owner_document)
        result = root.insert_before(style, None)
        self.assertEqual(style, result)
        self.assertEqual(doc, style.owner_document)

        comment = doc.create_comment('demo')
        self.assertEqual(doc, comment.owner_document)
        result = root.insert_before(comment, title)
        self.assertEqual(comment, result)
        self.assertEqual(doc, comment.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><style/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        g = doc.create_element('g')
        path = doc.create_element('path')
        result = g.append_child(path)
        self.assertEqual(path, result)
        self.assertEqual(doc, g.owner_document)
        self.assertEqual(doc, path.owner_document)

        # <title/><defs/><style/><g><path/></g>
        result = root.insert_before(g, None)
        self.assertEqual(g, result)
        self.assertEqual(doc, g.owner_document)
        self.assertEqual(doc, path.owner_document)

        rect = doc.create_element('rect')
        self.assertRaises(ValueError, lambda: doc.insert_before(rect, path))
        self.assertEqual(doc, rect.owner_document)
        self.assertEqual(doc, path.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><style/><g><path/></g>' \
            '</svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        for it in root.iter():
            self.assertEqual(doc, it.owner_document)

        # link = parser.makeelement('link')
        # self.assertNotIsInstance(link, Node)
        # self.assertRaises(TypeError, lambda: root.insert_before(link, style))

        link = doc.create_element('link')
        self.assertIsInstance(link, Node)
        self.assertEqual(doc, link.owner_document)
        result = root.insert_before(link, style)
        self.assertEqual(link, result)
        self.assertEqual(doc, link.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><link/><style/><g><path/></g>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        pi1 = doc.create_processing_instruction('xml-stylesheet',
                                                'href="1.css"')
        result = doc.insert_before(pi1, root)
        self.assertEqual(pi1, result)
        self.assertEqual(doc, pi1.owner_document)

        pi2 = doc.create_processing_instruction('xml-stylesheet',
                                                'href="2.css"')
        result = doc.insert_before(pi2, root)
        self.assertEqual(pi2, result)
        self.assertEqual(doc, pi2.owner_document)

        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<?xml-stylesheet href="2.css"?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--demo-->' \
            '<title/><defs/><link/><style/><g><path/></g>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

    def test_document_open(self):
        doc = window.document
        self.assertIsNone(doc.document_element)
        self.assertEqual(window, doc.default_view)

        path = os.path.join(here, 'svg/svg.svg')
        src = Path(path).absolute().as_uri()
        doc.location = src
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

        src = 'about:blank'
        doc.location = src
        self.assertEqual(src, doc.location.href)
        self.assertEqual(src, doc.url)
        self.assertEqual(src, doc.document_uri)
        self.assertEqual('null', doc.origin)
        self.assertIsNone(doc.document_element)

    def test_document_prepend(self):
        impl = SVGDOMImplementation()
        doc = impl.create_document(Element.SVG_NAMESPACE_URI)

        parser = etree.XMLParser()
        root = parser.makeelement('svg')
        self.assertNotIsInstance(root, Node)
        self.assertRaises(TypeError, lambda: doc.prepend(root))
        self.assertIsNone(doc.document_element)

        comment = doc.create_comment('demo')
        self.assertRaises(TypeError, lambda: doc.prepend(comment))
        self.assertIsNone(doc.document_element)

        pi = doc.create_processing_instruction('xml-stylesheet',
                                               'href="1.css"')
        self.assertRaises(TypeError, lambda: doc.prepend(pi))
        self.assertIsNone(doc.document_element)

        root = doc.create_element('svg')
        doc.prepend(root)
        self.assertEqual(root, doc.document_element)

        doc.prepend(comment)
        doc.prepend(pi)
        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<!--demo-->' \
            '<svg xmlns="http://www.w3.org/2000/svg"/>'
        self.assertEqual(expected, doc.tostring().decode())

        group = doc.create_element('g')
        style = doc.create_element('style')
        comment2 = doc.create_comment('test')
        root.prepend(group)
        root.prepend(style)
        root.prepend(comment2)
        expected = \
            '<?xml-stylesheet href="1.css"?>' \
            '<!--demo-->' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!--test-->' \
            '<style/>' \
            '<g/>' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())
        for it in root.iter():
            self.assertEqual(doc, it.owner_document)

    def test_document_query_selector_all(self):
        doc = window.document
        doc.write(SVG_SVG)

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

    def test_document_remove_child(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document(Element.SVG_NAMESPACE_URI)
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        root = doc.create_element('svg')
        self.assertEqual(doc, root.owner_document)
        self.assertRaises(ValueError, lambda: doc.remove_child(root))

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
        self.assertRaises(ValueError, lambda: doc.remove_child(style))
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

    def test_document_replace_child(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document(Element.SVG_NAMESPACE_URI, 'svg')
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
        self.assertEqual(pi, result)
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
        self.assertEqual(style, result)
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
        self.assertEqual(comment, result)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual(doc, defs.owner_document)
        expected = \
            '<?xml-stylesheet ?>' \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<style/>' \
            '<!--demo-->' \
            '</svg>'
        self.assertEqual(expected, doc.tostring().decode())

        self.assertRaises(ValueError, lambda: doc.replace_child(defs, style))
        self.assertRaises(ValueError, lambda: root.replace_child(defs, pi))

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

    def test_document_write(self):
        doc = window.document
        root = doc.create_element('svg')
        doc.append(root)

        svg = '''
        <desc>Two groups, each of two rectangles</desc>
        '''
        doc.write(svg.strip())
        self.assertEqual(1, len(root))

        svg = '''
        <g id="group1" fill="red">
          <rect x="1cm" y="1cm" width="1cm" height="1cm"/>
          <rect x="3cm" y="1cm" width="1cm" height="1cm"/>
        </g>
        '''
        doc.write(svg.strip())
        self.assertEqual(2, len(root))

        svg = '''
        <g id="group2" fill="blue">
          <rect x="1cm" y="3cm" width="1cm" height="1cm"/>
          <rect x="3cm" y="3cm" width="1cm" height="1cm"/>
        </g>
        '''
        doc.write(svg.strip())
        self.assertEqual(3, len(root))

        svg = '''
        <!-- Show outline of viewport using 'rect' element -->
        <rect x=".01cm" y=".01cm" width="4.98cm" height="4.98cm"
          fill="none" stroke="blue" stroke-width=".02cm"/>
        '''
        doc.write(svg.strip())
        self.assertEqual(4, len(root))

        for it in root.iter():
            self.assertIsInstance(it, Node)
            self.assertEqual(doc, it.owner_document, msg=it)

        children = root.getchildren()
        self.assertEqual(4, len(children))
        self.assertEqual('desc', children[0].node_name)
        self.assertEqual('g', children[1].node_name)
        self.assertEqual('g', children[2].node_name)
        self.assertEqual('rect', children[3].node_name)

        group = doc.get_element_by_id('group1')
        children = group.getchildren()
        self.assertEqual(2, len(children))
        self.assertEqual('rect', children[0].node_name)
        self.assertEqual('rect', children[1].node_name)


if __name__ == '__main__':
    unittest.main()
