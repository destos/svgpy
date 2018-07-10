#!/usr/bin/env python3


import logging
import os
import sys
import tempfile
import unittest
from pathlib import Path

from lxml import etree

sys.path.extend(['.', '..'])

from svgpy.dom import Comment, Element, Node
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

        parser = etree.XMLParser()
        root = parser.makeelement('svg')
        self.assertNotIsInstance(root, Node)
        self.assertRaises(TypeError, lambda: doc.append_child(root))

        root = doc.create_element('svg')
        self.assertIsInstance(root, Node)
        self.assertIsNone(root.owner_document)
        doc.append_child(root)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)

        comment = doc.create_comment(' Test ')
        self.assertIsNone(comment.owner_document)
        doc.append_child(comment)
        self.assertEqual(doc, comment.owner_document)

        title = doc.create_element('title')
        self.assertIsNone(title.owner_document)
        self.assertRaises(ValueError, lambda: comment.append_child(title))
        doc.append_child(title)
        self.assertEqual(doc, title.owner_document)

        defs = doc.create_element('defs')
        self.assertIsNone(defs.owner_document)
        doc.append_child(defs)
        self.assertEqual(doc, defs.owner_document)

        style = doc.create_element('style')
        self.assertIsNone(style.owner_document)
        defs.append_child(style)
        self.assertEqual(doc, style.owner_document)

        self.assertTrue(style in defs)
        self.assertTrue(style not in doc.document_element)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!-- Test -->' \
            '<title/><defs><style/></defs></svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        appended = doc.append_child(style)
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(style, appended)
        self.assertTrue(style not in defs)
        self.assertTrue(style in doc.document_element)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!-- Test -->' \
            '<title/><defs/><style/></svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        link = parser.makeelement('link')
        self.assertNotIsInstance(link, Node)
        self.assertRaises(TypeError, lambda: root.append_child(link))

        link = doc.create_element('link')
        self.assertIsInstance(link, Node)
        self.assertIsNone(link.owner_document)
        root.append_child(link)
        self.assertEqual(doc, link.owner_document)

    def test_document_create_element(self):
        doc = window.document

        data = 'Comment'
        comment = doc.create_comment(data)
        self.assertIsInstance(comment, Comment)
        self.assertEqual(8, Node.COMMENT_NODE)
        self.assertEqual(8, comment.node_type)
        self.assertIsNone(comment.owner_document)
        self.assertEqual('#comment', comment.node_name)
        self.assertEqual(data, comment.data)
        self.assertEqual(data, comment.node_value)
        self.assertEqual(data, comment.text_content)

        root = doc.create_element(
            'svg',
            attrib={
               'viewBox': '0 0 200 300',
            })
        self.assertIsInstance(root, SVGSVGElement)
        self.assertEqual(1, Node.ELEMENT_NODE)
        self.assertEqual(1, root.node_type)
        self.assertIsNone(root.owner_document)
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
        self.assertEqual('html:video', video.node_name)
        self.assertEqual('html:video', video.tag_name)
        self.assertEqual('video', video.local_name)
        self.assertEqual('100', video.get_attribute('width'))
        self.assertEqual('150', video.get_attribute('height'))

    def test_document_get_elements(self):
        doc = window.document
        doc.write(SVG_CUBIC01)
        for it in doc.document_element.iter():
            self.assertIsInstance(it, Node)
            self.assertEqual(doc, it.owner_document)

        elements = doc.get_elements_by_class_name('EndPoint')
        self.assertEqual(3, len(elements))

        elements = doc.get_elements_by_class_name('AutoCtlPoint')
        self.assertEqual(1, len(elements))

        elements = doc.get_elements_by_class_name('EndPoint AutoCtlPoint')
        self.assertEqual(0, len(elements))

        elements = doc.get_elements_by_tag_name('rect')
        self.assertEqual(1, len(elements))
        self.assertEqual('Border', elements[0].class_name)

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
        self.assertRaises(ValueError,
                          lambda: doc.get_elements_by_class_name('test'))
        self.assertRaises(ValueError,
                          lambda: doc.get_elements_by_tag_name('svg'))
        self.assertRaises(ValueError,
                          lambda: doc.get_elements_by_tag_name_ns(
                              Element.SVG_NAMESPACE_URI,
                              'svg'))
        self.assertIsNone(doc.get_root_node())

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
        self.assertRaises(ValueError,
                          lambda: doc.get_elements_by_class_name('test'))
        self.assertRaises(ValueError,
                          lambda: doc.get_elements_by_tag_name('svg'))
        self.assertRaises(ValueError,
                          lambda: doc.get_elements_by_tag_name_ns(
                              Element.SVG_NAMESPACE_URI,
                              'svg'))
        self.assertIsNone(doc.get_root_node())

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
        self.assertEqual(expected, root.tostring().decode())

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
        self.assertEqual(expected, root.tostring().decode())

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
        self.assertEqual(expected, root.tostring().decode())

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
        doc.append_child(video)
        source = doc.create_element_ns(Element.XHTML_NAMESPACE_URI, 'source')
        video.append_child(source)
        expected = \
            '<svg xmlns:html="http://www.w3.org/1999/xhtml"' \
            ' xmlns="http://www.w3.org/2000/svg">' \
            '<html:video><html:source/></html:video></svg>'
        self.assertEqual(expected, root.tostring().decode())

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
        self.assertIsNone(doc.document_element)
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
        self.assertEqual(window.document.implementation,
                         doc.implementation)
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
        self.assertIsNone(root.owner_document)
        doc.insert_before(root, None)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)

        defs = doc.create_element('defs')
        self.assertIsNone(defs.owner_document)
        doc.insert_before(defs, None)
        self.assertEqual(doc, defs.owner_document)
        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<defs/></svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        title = doc.create_element('title')
        self.assertIsNone(title.owner_document)
        doc.insert_before(title, defs)
        self.assertEqual(doc, title.owner_document)

        style = doc.create_element('style')
        self.assertIsNone(style.owner_document)
        doc.insert_before(style, None)
        self.assertEqual(doc, style.owner_document)

        comment = doc.create_comment(' Test ')
        self.assertIsNone(comment.owner_document)
        doc.insert_before(comment, title)
        self.assertEqual(doc, comment.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!-- Test -->' \
            '<title/><defs/><style/></svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        g = doc.create_element('g')
        path = doc.create_element('path')
        g.append_child(path)
        self.assertIsNone(g.owner_document)
        self.assertIsNone(path.owner_document)

        doc.insert_before(g, None)
        self.assertEqual(doc, g.owner_document)
        self.assertEqual(doc, path.owner_document)

        rect = doc.create_element('rect')
        self.assertRaises(ValueError, lambda: doc.insert_before(rect, path))
        self.assertIsNone(rect.owner_document)
        self.assertEqual(doc, path.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!-- Test -->' \
            '<title/><defs/><style/><g><path/></g></svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

        link = parser.makeelement('link')
        self.assertNotIsInstance(link, Node)
        self.assertRaises(TypeError, lambda: root.insert_before(link, style))

        link = doc.create_element('link')
        self.assertIsInstance(link, Node)
        self.assertIsNone(link.owner_document)
        root.insert_before(link, style)
        self.assertEqual(doc, link.owner_document)

        expected = \
            '<svg xmlns="http://www.w3.org/2000/svg">' \
            '<!-- Test -->' \
            '<title/><defs/><link/><style/><g><path/></g></svg>'
        self.assertEqual(expected, doc.document_element.tostring().decode())

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

    def test_document_remove_child(self):
        impl = SVGDOMImplementation()

        doc = impl.create_document(Element.SVG_NAMESPACE_URI)
        self.assertIsNone(doc.owner_document)
        self.assertIsNone(doc.document_element)

        root = doc.create_element('svg')
        self.assertIsNone(root.owner_document)
        self.assertRaises(ValueError, lambda: doc.remove_child(root))

        doc.append_child(root)
        self.assertEqual(root, doc.document_element)
        self.assertEqual(doc, root.owner_document)

        title = doc.create_element('title')
        doc.append_child(title)

        defs = doc.create_element('defs')
        doc.append_child(defs)

        style = doc.create_element('style')
        defs.append_child(style)

        self.assertEqual(2, len(doc.document_element))
        self.assertTrue(style in defs)
        self.assertTrue(style not in doc.document_element)
        self.assertRaises(ValueError, lambda: doc.remove_child(style))

        doc.append_child(style)
        self.assertEqual(3, len(doc.document_element))
        self.assertTrue(style not in defs)
        self.assertTrue(style in doc.document_element)

        self.assertEqual(doc, style.owner_document)
        removed = doc.remove_child(style)
        self.assertIsNone(style.owner_document)
        self.assertEqual(style, removed)
        self.assertEqual('style', removed.local_name)
        self.assertEqual(2, len(doc.document_element))
        self.assertTrue(style not in defs)
        self.assertTrue(style not in doc.document_element)

        doc.remove_child(title)
        self.assertIsNone(title.owner_document)
        doc.remove_child(defs)
        self.assertIsNone(defs.owner_document)
        self.assertEqual(0, len(doc.document_element))
        root = doc.document_element
        self.assertRaises(ValueError, lambda: doc.remove_child(root))

    def test_document_replace_child(self):
        impl = SVGDOMImplementation()
        doc = impl.create_document(Element.SVG_NAMESPACE_URI, 'svg')
        self.assertIsNone(doc.owner_document)
        root = doc.document_element
        self.assertEqual(doc, root.owner_document)

        title = doc.create_element('title')
        doc.append_child(title)

        defs = doc.create_element('defs')
        doc.append_child(defs)

        children = doc.document_element.getchildren()
        self.assertEqual([title, defs], children)
        self.assertTrue(title in root)
        self.assertTrue(defs in root)

        style = doc.create_element('style')
        self.assertIsNone(style.owner_document)
        replaced = doc.replace_child(style, title)
        self.assertEqual(style, replaced)
        children = doc.document_element.getchildren()
        self.assertEqual([style, defs], children)
        self.assertIsNone(title.owner_document)
        self.assertEqual(doc, defs.owner_document)
        self.assertEqual(doc, style.owner_document)
        self.assertTrue(style in root)
        self.assertTrue(title not in root)
        self.assertTrue(defs in root)

        self.assertRaises(ValueError, lambda: doc.replace_child(style, title))

        parser = etree.XMLParser()
        link = parser.makeelement('link')
        self.assertNotIsInstance(link, Node)
        self.assertRaises(TypeError, lambda: doc.replace_child(link, style))

    def test_document_write(self):
        svg = '''
        <?xml version="1.0" standalone="no"?>
        <svg width="5cm" height="4cm"
          xmlns="http://www.w3.org/2000/svg">
          <title>Sample</title>
          <desc>SVG</desc>
        </svg>
        '''
        doc = window.document
        self.assertIsNone(doc.document_element)

        doc.write(svg.strip())
        root = doc.document_element
        for it in root.iter():
            self.assertIsInstance(it, Node)
            self.assertEqual(doc, it.owner_document, msg=it)
        self.assertIsNotNone(root)
        self.assertIsInstance(root, SVGSVGElement)
        self.assertEqual(doc, root.owner_document)
        self.assertEqual('5cm', root.get_attribute('width'))
        self.assertEqual('4cm', root.get_attribute('height'))

        children = root.getchildren()
        self.assertEqual(2, len(children))
        self.assertEqual('title', children[0].node_name)
        self.assertEqual('desc', children[1].node_name)

        svg = '''
        <g>
          <circle r="10"/>
        </g>
        '''
        doc.write(svg.strip())
        for it in root.iter():
            self.assertIsInstance(it, Node)
            self.assertEqual(doc, it.owner_document, msg=it)
        children = root.getchildren()
        self.assertEqual(3, len(children))
        self.assertEqual('title', children[0].node_name)
        self.assertEqual('desc', children[1].node_name)
        self.assertEqual('g', children[2].node_name)


if __name__ == '__main__':
    unittest.main()
