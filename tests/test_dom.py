#!/usr/bin/env python3

import os
import sys
import unittest
from collections.abc import ItemsView, KeysView, ValuesView
from io import StringIO

sys.path.extend(['.', '..'])

from svgpy import Attr, Comment, DOMTokenList, Element, HTMLElement, \
    NamedNodeMap, Node, SVGElement, SVGParser, formatter, window
from svgpy.dom import DOMStringMap
from svgpy.exception import AbortError, ConstraintError, DataCloneError, \
    DataError, DOMException, EncodingError, HierarchyRequestError, \
    InUseAttributeError, InvalidCharacterError, InvalidModificationError, \
    InvalidNodeTypeError, InvalidStateError, NamespaceError, NetworkError, \
    NoModificationAllowedError, NotAllowedError, NotFoundError, \
    NotReadableError, NotSupportedError, OperationError, QuotaExceededError, \
    ReadOnlyError, SecurityError, TransactionInactiveError, UnknownError, \
    URLMismatchError, VersionError, WrongDocumentError

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

test_level = int(os.getenv('TEST_LEVEL', '0'))


class DOMTestCase(unittest.TestCase):

    def setUp(self):
        formatter.precision = 3
        window.location = 'about:blank'

    def test_attr00(self):
        # Attr()
        namespace = None
        local_name = 'fill'
        qualified_name = local_name
        value = None
        owner_element = None

        self.assertRaises(ValueError,
                          lambda: Attr(namespace, qualified_name, value=value,
                                       owner_element=owner_element))

    def test_attr01(self):
        # Attr()
        namespace = None
        local_name = 'fill'
        qualified_name = local_name
        value = 'none'
        owner_element = None

        attr = Attr(namespace,
                    qualified_name,
                    value=value,
                    owner_element=owner_element)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(Element.ATTRIBUTE_NODE, attr.node_type)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertIsNone(attr.owner_document)
        self.assertIsNone(attr.owner_element)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)

        attr.value = value = 'black'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())

        attr.node_value = value = 'silver'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())

        attr.text_content = value = 'gray'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())

    def test_attr02(self):
        # Attr()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = None
        local_name = 'fill'
        qualified_name = local_name
        value = 'none'
        owner_element = root
        root.set(qualified_name, value)

        # element => attr
        attr = Attr(namespace,
                    qualified_name,
                    value=value,
                    owner_element=owner_element)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(Element.ATTRIBUTE_NODE, attr.node_type)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))
        self.assertIsNone(attr.owner_document)
        self.assertEqual(root, attr.owner_element)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)

        # attr => element
        attr.value = value = 'black'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        attr.node_value = value = 'silver'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        attr.text_content = value = 'gray'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        # element => attr
        value = 'white'
        root.set(qualified_name, value)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

    def test_attr03(self):
        # remove attribute
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = None
        local_name = 'fill'
        qualified_name = local_name
        value = 'none'
        owner_element = root

        attr = Attr(namespace,
                    qualified_name,
                    value=value,
                    owner_element=owner_element)

        root.set(qualified_name, value)
        self.assertEqual(value, attr.value)
        self.assertTrue(qualified_name in root.attrib)
        self.assertEqual(value, root.get(qualified_name))
        attr.value = ''  # remove
        self.assertIsNone(attr.value)
        self.assertEqual('', attr.node_value)
        self.assertEqual('', attr.text_content)
        self.assertEqual('', attr.tostring().decode())
        self.assertTrue(qualified_name not in root.attrib)
        self.assertIsNone(root.get(qualified_name))

        root.set(qualified_name, value)
        self.assertEqual(value, attr.value)
        self.assertTrue(qualified_name in root.attrib)
        self.assertEqual(value, root.get(qualified_name))
        attr.value = None  # remove
        self.assertIsNone(attr.value)
        self.assertEqual('', attr.node_value)
        self.assertEqual('', attr.text_content)
        self.assertEqual('', attr.tostring().decode())
        self.assertTrue(qualified_name not in root.attrib)
        self.assertIsNone(root.get(qualified_name))

    def test_attr04(self):
        # with namespace
        parser = SVGParser()
        namespace = 'http://www.w3.org/1999/xlink'
        prefix = 'xlink'
        local_name = 'href'
        qualified_name = '{{{}}}{}'.format(namespace, local_name)
        value = '#0'
        root = parser.create_element_ns('http://www.w3.org/2000/svg',
                                        'svg',
                                        nsmap={
                                            prefix: namespace,
                                        })
        owner_element = root
        root.set(qualified_name, value)

        # element => attr
        attr = Attr(namespace,
                    qualified_name,
                    value=value,
                    owner_element=owner_element)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(prefix, attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(Element.ATTRIBUTE_NODE, attr.node_type)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))
        self.assertIsNone(attr.owner_document)
        self.assertEqual(root, attr.owner_element)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)

        # attr => element
        attr.value = value = '#1'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        attr.node_value = value = '#2'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        attr.text_content = value = '#3'
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        # element => attr
        value = '#4'
        root.set(qualified_name, value)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))

        # element => attr
        value = '#5'
        attr = Attr(namespace, local_name, value=value, owner_element=root)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(prefix, attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(Element.ATTRIBUTE_NODE, attr.node_type)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))
        self.assertIsNone(attr.owner_document)
        self.assertEqual(root, attr.owner_element)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)

        value = '#6'
        attr = Attr('', qualified_name, value=value, owner_element=root)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(prefix, attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(Element.ATTRIBUTE_NODE, attr.node_type)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))
        self.assertIsNone(attr.owner_document)
        self.assertEqual(root, attr.owner_element)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)

        value = '#7'
        attr = Attr(None, qualified_name, value=value, owner_element=root)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(prefix, attr.prefix)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(qualified_name, attr.node_name)
        self.assertEqual(Element.ATTRIBUTE_NODE, attr.node_type)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, attr.node_value)
        self.assertEqual(value, attr.text_content)
        self.assertEqual(value, attr.tostring().decode())
        self.assertEqual(value, root.get(qualified_name))
        self.assertIsNone(attr.owner_document)
        self.assertEqual(root, attr.owner_element)
        self.assertIsNone(attr.parent_element)
        self.assertIsNone(attr.parent_node)

    def test_attr_append_child(self):
        # Attr
        # Node.append_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_attribute('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.append_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(attr))

        comment = parser.create_comment('foo')
        # parent.append_child(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.append_child(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(doc2))

        element = parser.create_element_ns(svg_ns, 'g')
        # parent.append_child(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.append_child(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(pi))

    def test_attr_child_nodes(self):
        # Node.child_nodes
        # Node.first_child
        # Node.last_child
        # Node.next_sibling
        # Node.previous_sibling
        # Node.has_child_nodes()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr = parser.create_attribute('viewBox')
        attr.value = '0 0 600 400'
        root.set_attribute_node(attr)

        children = attr.child_nodes
        self.assertEqual(0, len(children))
        node = attr.first_child
        self.assertIsNone(node)
        node = attr.last_child
        self.assertIsNone(node)
        node = attr.previous_sibling
        self.assertIsNone(node)
        node = attr.next_sibling
        self.assertIsNone(node)
        self.assertFalse(attr.has_child_nodes())

    def test_attr_get_root_node(self):
        # Attr.get_root_node()
        parser = SVGParser()
        attr = parser.create_attribute('fill')
        self.assertEqual(attr, attr.get_root_node())

    def test_attr_insert_before(self):
        # Attr
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_attribute('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.insert_before(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, None))

        comment = parser.create_comment('foo')
        # parent.insert_before(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.insert_before(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.insert_before(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.insert_before(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(pi, None))

    def test_attr_remove_child(self):
        # Attr
        # Node.remove_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_attribute('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.remove_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(attr))

        comment = parser.create_comment('foo')
        # parent.remove_child(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.remove_child(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.remove_child(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.remove_child(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(pi))

    def test_attr_replace_child(self):
        # Attr
        # Node.replace_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_attribute('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.replace_child(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(attr, None))

        comment = parser.create_comment('foo')
        # parent.replace_child(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.replace_child(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.replace_child(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.replace_child(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(pi, None))

    def test_comment(self):
        parser = SVGParser()
        expected = 'Comment'
        comment = parser.create_comment(expected)
        self.assertIsInstance(comment, Comment)
        self.assertEqual(8, Node.COMMENT_NODE)
        self.assertEqual(8, comment.node_type)
        self.assertEqual('#comment', comment.node_name)
        self.assertEqual(expected, comment.data)
        self.assertEqual(expected, comment.node_value)
        self.assertEqual(expected, comment.text_content)
        expected = '<!--' + expected + '-->'
        self.assertEqual(expected, comment.tostring().decode())

        comment.data = None
        self.assertEqual('', comment.data)
        self.assertEqual('', comment.node_value)
        self.assertEqual('', comment.text_content)
        self.assertEqual('', comment.tostring().decode())

        comment.node_value = expected = 'nodeValue'
        self.assertEqual(expected, comment.data)
        self.assertEqual(expected, comment.node_value)
        self.assertEqual(expected, comment.text_content)
        expected = '<!--' + expected + '-->'
        self.assertEqual(expected, comment.tostring().decode())

        comment.text_content = expected = 'textContent'
        self.assertEqual(expected, comment.data)
        self.assertEqual(expected, comment.node_value)
        self.assertEqual(expected, comment.text_content)
        expected = '<!--' + expected + '-->'
        self.assertEqual(expected, comment.tostring().decode())

    def test_comment_addnext(self):
        # CommentBase.addnext()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_comment('foo-bar')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.addnext(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addnext(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.addnext(comment)
        self.assertEqual([parent, comment], list(root))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.addnext(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addnext(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.addnext(element)
        self.assertEqual([parent, element, comment], list(root))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.addnext(pi)
        self.assertEqual([parent, pi, element, comment], list(root))
        self.assertEqual(doc, pi.owner_document)

    def test_comment_addprevious(self):
        # CommentBase.addprevious()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_comment('foo-bar')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.addprevious(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addprevious(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.addprevious(comment)
        self.assertEqual([comment, parent], list(root))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.addprevious(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addprevious(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.addprevious(element)
        self.assertEqual([comment, element, parent], list(root))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.addprevious(pi)
        self.assertEqual([comment, element, pi, parent], list(root))
        self.assertEqual(doc, pi.owner_document)

    def test_comment_append(self):
        # CommentBase.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.append(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(attr))

        comment = parser.create_comment('foo')
        # parent.append(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.append(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.append(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.append(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(pi))

    def test_comment_append_child(self):
        # Comment
        # Node.append_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.append_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(attr))

        comment = parser.create_comment('foo')
        # parent.append_child(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.append_child(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.append_child(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.append_child(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(pi))

    def test_comment_child_nodes(self):
        # Node.child_nodes
        # Node.first_child
        # Node.last_child
        # Node.next_sibling
        # Node.previous_sibling
        # Node.has_child_nodes()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        start = parser.create_comment('start')
        root.addprevious(start)
        comment = parser.create_comment('comment')
        root.append(comment)
        end = parser.create_comment('end')
        root.addnext(end)

        children = comment.child_nodes
        self.assertEqual(0, len(children))
        node = comment.first_child
        self.assertIsNone(node)
        node = comment.last_child
        self.assertIsNone(node)
        node = comment.previous_sibling
        self.assertIsNone(node)
        node = comment.next_sibling
        self.assertIsNone(node)
        self.assertFalse(comment.has_child_nodes())

        children = start.child_nodes
        self.assertEqual(0, len(children))
        node = start.first_child
        self.assertIsNone(node)
        node = start.last_child
        self.assertIsNone(node)
        node = start.previous_sibling
        self.assertIsNone(node)
        node = start.next_sibling
        self.assertEqual(root, node)
        self.assertFalse(start.has_child_nodes())

        children = end.child_nodes
        self.assertEqual(0, len(children))
        node = end.first_child
        self.assertIsNone(node)
        node = end.last_child
        self.assertIsNone(node)
        node = end.previous_sibling
        self.assertEqual(root, node)
        node = end.next_sibling
        self.assertIsNone(node)
        self.assertFalse(end.has_child_nodes())

    def test_comment_extend(self):
        # CommentBase.extend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

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

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.extend([element])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([element]))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.extend([pi])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([pi]))

    def test_comment_insert(self):
        # CommentBase.insert()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.insert(1, attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, attr))

        comment = parser.create_comment('foo')
        # parent.insert(1, comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, comment))

        doc2 = parser.create_document(svg_ns)
        # parent.insert(1, doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.insert(1, element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.insert(1, pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, pi))

    def test_comment_insert_before(self):
        # Comment
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.insert_before(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, None))

        comment = parser.create_comment('foo')
        # parent.insert_before(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.insert_before(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.insert_before(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.insert_before(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(pi, None))

    def test_comment_next_element_sibling(self):
        # Comment.next_element_sibling
        parser = SVGParser()
        root = parser.create_element('svg')

        desc = parser.create_element('desc')
        root.append(desc)
        comment = parser.create_comment('comment')
        root.append(comment)
        rect = parser.create_element('rect')
        rect.id = 'border'
        root.append(rect)
        path = parser.create_element('path')
        root.append(path)

        e = comment.next_element_sibling
        self.assertEqual(rect, e)

    def test_comment_previous_element_sibling(self):
        # Comment.previous_element_sibling
        parser = SVGParser()
        root = parser.create_element('svg')

        desc = parser.create_element('desc')
        root.append(desc)
        comment = parser.create_comment('comment')
        root.append(comment)
        rect = parser.create_element('rect')
        rect.id = 'border'
        root.append(rect)
        path = parser.create_element('path')
        root.append(path)

        e = comment.previous_element_sibling
        self.assertEqual(desc, e)

    def test_comment_remove(self):
        # CommentBase.remove()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.remove(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(attr))

        comment = parser.create_comment('foo')
        # parent.remove(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.remove(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.remove(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.remove(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(pi))

    def test_comment_remove_child(self):
        # Comment
        # Node.remove_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.remove_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(attr))

        comment = parser.create_comment('foo')
        # parent.remove_child(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.remove_child(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.remove_child(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.remove_child(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(pi))

    def test_comment_replace(self):
        # CommentBase.replace()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.replace(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(attr, None))

        comment = parser.create_comment('foo')
        # parent.replace(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.replace(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.replace(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.replace(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(pi, None))

    def test_comment_replace_child(self):
        # Comment
        # Node.replace_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_comment('foo-bar')

        attr = parser.create_attribute('foo')
        # parent.replace_child(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(attr, None))

        comment = parser.create_comment('foo')
        # parent.replace_child(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.replace_child(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.replace_child(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.replace_child(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(pi, None))

    def test_dom_exception(self):
        e = DOMException()
        self.assertEqual(e.code, 0)
        self.assertEqual('Error', e.name)
        self.assertEqual('', e.message)
        self.assertEqual((), e.args)
        self.assertEqual('', str(e))

        e = DOMException('arg1')
        self.assertEqual(e.code, 0)
        self.assertEqual('Error', e.name)
        self.assertEqual('arg1', e.message)
        self.assertEqual(('arg1',), e.args)
        self.assertEqual('arg1', str(e))

        e = DOMException('arg1',
                         name='TestError')
        self.assertEqual(e.code, 0)
        self.assertEqual('TestError', e.name)
        self.assertEqual('arg1', e.message)
        self.assertEqual(('arg1',), e.args)
        self.assertEqual('arg1', str(e))

        e = DOMException('arg1', 'arg2', 100, None,
                         name='TestError')
        self.assertEqual(e.code, 0)
        self.assertEqual('TestError', e.name)
        self.assertEqual('arg1 arg2 100 None', e.message)
        self.assertEqual(('arg1', 'arg2', 100, None), e.args)
        self.assertEqual("('arg1', 'arg2', 100, None)", str(e))

        e = DOMException(message='test message',
                         name='TestError')
        self.assertEqual(e.code, 0)
        self.assertEqual('TestError', e.name)
        self.assertEqual('test message', e.message)
        self.assertEqual(('test message',), e.args)
        self.assertEqual('test message', str(e))

        e = DOMException('arg1', 'arg2', 100, None,
                         message='test message',
                         name='TestError')
        self.assertEqual(e.code, 0)
        self.assertEqual('TestError', e.name)
        self.assertEqual('test message', e.message)
        self.assertEqual(('arg1', 'arg2', 100, None), e.args)
        self.assertEqual("('arg1', 'arg2', 100, None)", str(e))

        e = DOMException('arg1', name='WrongDocumentError')
        self.assertEqual(e.code, 4)
        self.assertEqual('WrongDocumentError', e.name)
        self.assertEqual('arg1', e.message)
        self.assertEqual(('arg1',), e.args)
        self.assertEqual('arg1', str(e))

        # invalid argument
        self.assertRaises(TypeError,
                          lambda: DOMException(code=100))

        e = WrongDocumentError(message='test message',
                               name='Error')
        self.assertEqual(e.code, 4)
        self.assertEqual('WrongDocumentError', e.name)
        self.assertEqual('test message', e.message)
        self.assertEqual(('test message',), e.args)
        self.assertEqual('test message', str(e))

    def test_dom_exception_abort_error(self):
        try:
            raise AbortError('test message')
        except DOMException as e:
            self.assertEqual(20, e.code)
            self.assertEqual('AbortError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_constraint_error(self):
        try:
            raise ConstraintError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('ConstraintError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_data_clone_error(self):
        try:
            raise DataCloneError('test message')
        except DOMException as e:
            self.assertEqual(25, e.code)
            self.assertEqual('DataCloneError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_data_error(self):
        try:
            raise DataError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('DataError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_encoding_error(self):
        try:
            raise EncodingError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('EncodingError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_hierarchy_request_error(self):
        try:
            raise HierarchyRequestError('test message')
        except DOMException as e:
            self.assertEqual(3, e.code)
            self.assertEqual('HierarchyRequestError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_in_use_attribute_error(self):
        try:
            raise InUseAttributeError('test message')
        except DOMException as e:
            self.assertEqual(10, e.code)
            self.assertEqual('InUseAttributeError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_invalid_character_error(self):
        try:
            raise InvalidCharacterError('test message')
        except DOMException as e:
            self.assertEqual(5, e.code)
            self.assertEqual('InvalidCharacterError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_invalid_modification_error(self):
        try:
            raise InvalidModificationError('test message')
        except DOMException as e:
            self.assertEqual(13, e.code)
            self.assertEqual('InvalidModificationError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_invalid_node_type_error(self):
        try:
            raise InvalidNodeTypeError('test message')
        except DOMException as e:
            self.assertEqual(24, e.code)
            self.assertEqual('InvalidNodeTypeError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_invalid_state_error(self):
        try:
            raise InvalidStateError('test message')
        except DOMException as e:
            self.assertEqual(11, e.code)
            self.assertEqual('InvalidStateError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_namespace_error(self):
        try:
            raise NamespaceError('test message')
        except DOMException as e:
            self.assertEqual(14, e.code)
            self.assertEqual('NamespaceError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_network_error(self):
        try:
            raise NetworkError('test message')
        except DOMException as e:
            self.assertEqual(19, e.code)
            self.assertEqual('NetworkError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_no_modification_allowed_error(self):
        try:
            raise NoModificationAllowedError('test message')
        except DOMException as e:
            self.assertEqual(7, e.code)
            self.assertEqual('NoModificationAllowedError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_not_allowed_error(self):
        try:
            raise NotAllowedError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('NotAllowedError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_not_found_error(self):
        try:
            raise NotFoundError('test message')
        except DOMException as e:
            self.assertEqual(8, e.code)
            self.assertEqual('NotFoundError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_not_readable_error(self):
        try:
            raise NotReadableError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('NotReadableError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_not_supported_error(self):
        try:
            raise NotSupportedError('test message')
        except DOMException as e:
            self.assertEqual(9, e.code)
            self.assertEqual('NotSupportedError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_operation_error(self):
        try:
            raise OperationError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('OperationError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_quota_exceeded_error(self):
        try:
            raise QuotaExceededError('test message')
        except DOMException as e:
            self.assertEqual(22, e.code)
            self.assertEqual('QuotaExceededError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_read_only_error(self):
        try:
            raise ReadOnlyError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('ReadOnlyError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_security_error(self):
        try:
            raise SecurityError('test message')
        except DOMException as e:
            self.assertEqual(18, e.code)
            self.assertEqual('SecurityError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_transaction_inactive_error(self):
        try:
            raise TransactionInactiveError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('TransactionInactiveError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_unknown_error(self):
        try:
            raise UnknownError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('UnknownError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_url_mismatch_error(self):
        try:
            raise URLMismatchError('test message')
        except DOMException as e:
            self.assertEqual(21, e.code)
            self.assertEqual('URLMismatchError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_version_error(self):
        try:
            raise VersionError('test message')
        except DOMException as e:
            self.assertEqual(0, e.code)
            self.assertEqual('VersionError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_exception_wrong_document_error(self):
        try:
            raise WrongDocumentError('test message')
        except DOMException as e:
            self.assertEqual(4, e.code)
            self.assertEqual('WrongDocumentError', e.name)
            self.assertEqual('test message', e.message)
        except Exception as e:
            self.assertTrue(False, msg=repr(e))

    def test_dom_string_map(self):
        # DOMStringMap()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        root.set('viewBox', '0 0 600 400')
        root.set('data-foo', '0')
        root.set('data-foo-bar', '10')
        root.set('data-foo-bar-baz', '100')

        # init
        dataset = DOMStringMap(root, 'data-')
        self.assertEqual(3, len(dataset))
        self.assertEqual('0', dataset['foo'])
        self.assertEqual('10', dataset['fooBar'])
        self.assertEqual('100', dataset['fooBarBaz'])
        # print(dataset.keys(), dataset.values(), dataset.items())

        # update
        dataset['foo'] = 'a'
        dataset['fooBar'] = 'b'
        dataset['fooBarBaz'] = 'c'
        self.assertEqual('a', dataset['foo'])
        self.assertEqual('b', dataset['fooBar'])
        self.assertEqual('c', dataset['fooBarBaz'])
        self.assertEqual('a', root.get('data-foo'))
        self.assertEqual('b', root.get('data-foo-bar'))
        self.assertEqual('c', root.get('data-foo-bar-baz'))

        # append
        dataset['fooBarBazQux'] = 'd'
        self.assertEqual(4, len(dataset))
        self.assertEqual(5, len(root.attrib))
        self.assertEqual('a', dataset['foo'])
        self.assertEqual('b', dataset['fooBar'])
        self.assertEqual('c', dataset['fooBarBaz'])
        self.assertEqual('d', dataset['fooBarBazQux'])
        self.assertEqual('a', root.get('data-foo'))
        self.assertEqual('b', root.get('data-foo-bar'))
        self.assertEqual('c', root.get('data-foo-bar-baz'))
        self.assertEqual('d', root.get('data-foo-bar-baz-qux'))
        self.assertEqual('0 0 600 400', root.get('viewBox'))

        # remove one
        del dataset['fooBarBaz']
        self.assertEqual(3, len(dataset))
        self.assertEqual(4, len(root.attrib))
        self.assertEqual('a', dataset['foo'])
        self.assertEqual('b', dataset['fooBar'])
        self.assertRaises(KeyError, lambda: dataset['fooBarBaz'])
        self.assertEqual('d', dataset['fooBarBazQux'])
        self.assertEqual('a', root.get('data-foo'))
        self.assertEqual('b', root.get('data-foo-bar'))
        self.assertTrue('data-foo-bar-baz' not in root.attrib)
        self.assertEqual('d', root.get('data-foo-bar-baz-qux'))
        self.assertEqual('0 0 600 400', root.get('viewBox'))

        # remove all
        dataset.clear()
        self.assertEqual(0, len(dataset))
        self.assertEqual(1, len(root.attrib))
        self.assertTrue('data-foo' not in root.attrib)
        self.assertTrue('data-foo-bar' not in root.attrib)
        self.assertTrue('data-foo-bar-baz' not in root.attrib)
        self.assertTrue('data-foo-bar-baz-qux' not in root.attrib)
        self.assertEqual('0 0 600 400', root.get('viewBox'))

        # invalid key
        # dataset.get('a-x')
        self.assertRaises(ValueError, lambda: dataset.get('a-x'))

        # valid key
        dataset['a-X'] = 'a-X'  # 'a-X' => 'data-a--x'
        self.assertEqual(1, len(dataset))
        self.assertEqual(2, len(root.attrib))
        self.assertEqual('a-X', dataset['a-X'])
        self.assertEqual('a-X', root.get('data-a--x'))
        self.assertEqual('0 0 600 400', root.get('viewBox'))

        dataset['a--X'] = 'a--X'  # 'a--X' => 'data-a---x'
        self.assertEqual(2, len(dataset))
        self.assertEqual(3, len(root.attrib))
        self.assertEqual('a-X', dataset['a-X'])
        self.assertEqual('a--X', dataset['a--X'])
        self.assertEqual('a-X', root.get('data-a--x'))
        self.assertEqual('a--X', root.get('data-a---x'))
        self.assertEqual('0 0 600 400', root.get('viewBox'))

        dataset[''] = 'x'  # '' => 'data-'
        self.assertEqual(3, len(dataset))
        self.assertEqual(4, len(root.attrib))
        self.assertEqual('a-X', dataset['a-X'])
        self.assertEqual('a--X', dataset['a--X'])
        self.assertEqual('x', dataset[''])
        self.assertEqual('a-X', root.get('data-a--x'))
        self.assertEqual('a--X', root.get('data-a---x'))
        self.assertEqual('x', root.get('data-'))
        self.assertEqual('0 0 600 400', root.get('viewBox'))

    @unittest.skipIf(not (test_level & 0x01),
                     'This test will take some time. Run manually.')
    def test_dom_string_map_validate(self):
        # DOMStringMap()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        # https://www.w3.org/TR/xml/#NT-Name
        # Name ::= NameStartChar (NameChar)*
        test_pattern = (
            # start | end | expected
            (0x00, 0x2c, False),
            (0x2d, 0x2e, True),  # "-", "."
            (0x2f, 0x2f, False),  # "/"
            (0x30, 0x39, True),  # "0" - "9"
            # 0x3a (":") => lxml cause ValueError
            (0x3b, 0x40, False),  # ";<=>?@"
            (0x41, 0x5a, True),  # "A" - "Z"
            (0x5b, 0x5e, False),
            (0x5f, 0x5f, True),  # "_"
            (0x60, 0x60, False),
            (0x61, 0x7a, True),  # "a" - "z"
            (0x7b, 0xb6, False),
            (0xb7, 0xb7, True),  # NameChar
            (0xb8, 0xbf, False),
            (0xc0, 0xd6, True),
            (0xd7, 0xd7, False),
            (0xd8, 0xf6, True),
            (0xf7, 0xf7, False),
            (0x00f8, 0x02ff, True),
            (0x0300, 0x036f, True),  # NameChar
            (0x0370, 0x037d, True),
            (0x037e, 0x037e, False),
            (0x037f, 0x1fff, True),
            (0x2000, 0x200b, False),
            (0x200c, 0x200d, True),
            (0x200e, 0x203e, False),
            (0x203f, 0x2040, True),  # NameChar
            (0x2041, 0x206f, False),
            (0x2070, 0x218f, True),
            (0x2190, 0x2bff, False),
            (0x2c00, 0x2fef, True),
            (0x2ff0, 0x3000, False),
            (0x3001, 0xd7ff, True),
            (0xd800, 0xf8ff, False),
            (0xf900, 0xfdcf, True),
            (0xfdd0, 0xfdef, False),
            (0xfdf0, 0xfffd, True),
            (0xfffe, 0xffff, False),
            # (0x10000, 0xeffff, True),
        )
        for start, end, expected in test_pattern:
            for code in range(start, end + 1):
                name = 'foo{}Bar'.format(chr(code))
                with self.subTest(code=code, name=name, expected=expected):
                    if expected:
                        root.dataset[name] = '1'
                    else:
                        msg = "'{}' (0x{:x})".format(name, code)
                        with self.assertRaises(InvalidCharacterError,
                                               msg=msg):
                            root.dataset[name] = '0'

    def test_dom_string_map_view(self):
        # DOMStringMap()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.attributes['width'] = '600'
        root.attributes['height'] = '400'
        root.dataset['foo'] = '100'
        root.dataset['fooBar'] = '200'
        root.dataset['fooBarBuz'] = '300'
        self.assertEqual(5, root.attributes.length)
        self.assertEqual(3, len(root.dataset))

        view = root.dataset.keys()
        self.assertIsInstance(view, KeysView)

        keys = list(view)
        self.assertEqual(['foo', 'fooBar', 'fooBarBuz'], keys)

        view = root.dataset.values()
        self.assertIsInstance(view, ValuesView)

        values = list(view)
        self.assertEqual(['100', '200', '300'], values)

        view = root.dataset.items()
        self.assertIsInstance(view, ItemsView)

        items = list(view)
        self.assertEqual([('foo', '100'),
                          ('fooBar', '200'),
                          ('fooBarBuz', '300')],
                         items)

    def test_dom_token_list(self):
        # DOMTokenList()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr_name = 'class'

        s = DOMTokenList(root, attr_name)
        self.assertEqual(0, len(s))
        self.assertEqual(0, s.length)
        self.assertEqual('', s.value)

        root.set(attr_name, 'id0 id2 id3')
        s = DOMTokenList(root, attr_name)
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id0 id2 id3', s.value)
        self.assertTrue(s.contains('id0'))
        self.assertFalse(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id2', s.item(1))
        self.assertEqual('id3', s.item(2))

        root.set(attr_name, 'id3 id2 id5')
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id3 id2 id5', s.value)
        self.assertEqual('id3', s[0])
        self.assertEqual('id2', s[1])
        self.assertEqual('id5', s[2])

    def test_dom_token_list_add(self):
        # DOMTokenList.add()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr_name = 'class'

        s = DOMTokenList(root, attr_name)
        self.assertEqual(0, len(s))
        self.assertEqual(0, s.length)
        self.assertEqual('', s.value)

        s.add('id0')
        self.assertEqual(1, len(s))
        self.assertEqual(1, s.length)
        self.assertEqual('id0', s.value)
        self.assertEqual('id0', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertEqual('id0', s.item(0))

        s.add('id1', 'id2')
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id0 id1 id2', s.value)
        self.assertEqual('id0 id1 id2', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))

        s.add('id2')  # already exist
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id0 id1 id2', s.value)
        self.assertEqual('id0 id1 id2', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))

        s.append('id3')
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id0 id1 id2 id3', s.value)
        self.assertEqual('id0 id1 id2 id3', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))
        self.assertEqual('id3', s.item(3))

        s.append('id2')  # already exist
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id0 id1 id2 id3', s.value)
        self.assertEqual('id0 id1 id2 id3', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))
        self.assertEqual('id3', s.item(3))

        self.assertRaises(ValueError, lambda: s.add(''))
        self.assertRaises(ValueError, lambda: s.add('a\tb'))
        self.assertRaises(ValueError, lambda: s.add('a\nb'))
        self.assertRaises(ValueError, lambda: s.add('a\rb'))
        self.assertRaises(ValueError, lambda: s.add('a\fb'))
        self.assertRaises(ValueError, lambda: s.add('a b'))
        self.assertRaises(ValueError, lambda: s.add('a\t\n\r\f b'))

    def test_dom_token_list_insert(self):
        # DOMTokenList.insert()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr_name = 'class'
        root.set(attr_name, 'id0 id2 id5')

        s = DOMTokenList(root, attr_name)
        s.insert(1, 'id1')
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id0 id1 id2 id5', s.value)
        self.assertEqual('id0 id1 id2 id5', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id5'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))
        self.assertEqual('id5', s.item(3))

        s.insert(1, 'id2')
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id0 id1 id2 id5', s.value)
        self.assertEqual('id0 id1 id2 id5', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id5'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))
        self.assertEqual('id5', s.item(3))

        s[3:3] = ['id2', 'id3', 'id4']  # new: 'id3', 'id4'
        self.assertEqual(6, len(s))
        self.assertEqual(6, s.length)
        self.assertEqual('id0 id1 id2 id3 id4 id5', s.value)
        self.assertEqual('id0 id1 id2 id3 id4 id5', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertTrue(s.contains('id4'))
        self.assertTrue(s.contains('id5'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id2', s.item(2))
        self.assertEqual('id3', s.item(3))
        self.assertEqual('id4', s.item(4))
        self.assertEqual('id5', s.item(5))

        self.assertRaises(ValueError, lambda: s.insert(1, ''))
        self.assertRaises(ValueError, lambda: s.insert(1, 'a\tb'))
        self.assertRaises(ValueError, lambda: s.insert(1, 'a\nb'))
        self.assertRaises(ValueError, lambda: s.insert(1, 'a\rb'))
        self.assertRaises(ValueError, lambda: s.insert(1, 'a\fb'))
        self.assertRaises(ValueError, lambda: s.insert(1, 'a b'))
        self.assertRaises(ValueError, lambda: s.insert(1, 'a\t\n\r\f b'))

    def test_dom_token_list_remove(self):
        # DOMTokenList.remove()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr_name = 'class'
        root.set(attr_name, 'id0 id1 id2 id3 id4')

        s = DOMTokenList(root, attr_name)
        s.remove('id1')
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id0 id2 id3 id4', s.value)
        self.assertEqual('id0 id2 id3 id4', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertTrue(s.contains('id4'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id2', s.item(1))
        self.assertEqual('id3', s.item(2))
        self.assertEqual('id4', s.item(3))

        s.remove('id0', 'id3')
        self.assertEqual(2, len(s))
        self.assertEqual(2, s.length)
        self.assertEqual('id2 id4', s.value)
        self.assertEqual('id2 id4', root.get(attr_name))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id4'))
        self.assertEqual('id2', s.item(0))
        self.assertEqual('id4', s.item(1))

        s.remove('xx')  # not exist
        self.assertEqual(2, len(s))
        self.assertEqual(2, s.length)
        self.assertEqual('id2 id4', s.value)
        self.assertEqual('id2 id4', root.get(attr_name))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id4'))
        self.assertEqual('id2', s.item(0))
        self.assertEqual('id4', s.item(1))

        s.remove('id2', 'id4')  # remove attribute
        self.assertEqual(0, len(s))
        self.assertEqual(0, s.length)
        self.assertEqual('', s.value)
        self.assertIsNone(root.get(attr_name))

        root.set(attr_name, 'id3 id5')
        self.assertEqual(2, len(s))
        self.assertEqual(2, s.length)
        self.assertEqual('id3 id5', s.value)
        self.assertEqual('id3', s[0])
        self.assertEqual('id5', s[1])
        self.assertEqual('id3 id5', root.get(attr_name))
        s[1] = ''  # remove token
        self.assertEqual(1, len(s))
        self.assertEqual(1, s.length)
        self.assertEqual('id3', s.value)
        self.assertEqual('id3', s[0])
        self.assertEqual('id3', root.get(attr_name))
        s[0] = ''  # remove token and attribute
        self.assertEqual(0, len(s))
        self.assertEqual(0, s.length)
        self.assertEqual('', s.value)
        self.assertTrue(attr_name not in root.attrib)

    def test_dom_token_list_replace(self):
        # DOMTokenList.replace()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr_name = 'class'
        root.set(attr_name, 'id0 id2 id3')

        s = DOMTokenList(root, attr_name)
        result = s.replace('id2', 'id1')
        self.assertTrue(result)
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id0 id1 id3', s.value)
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id3'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id3', s.item(2))

        result = s.replace('id2', 'id4')  # 'id2': not exist
        self.assertFalse(result)
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id0 id1 id3', s.value)
        self.assertTrue(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id3'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id1', s.item(1))
        self.assertEqual('id3', s.item(2))

    def test_dom_token_list_toggle(self):
        # DOMTokenList.toggle()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        attr_name = 'class'
        root.set(attr_name, 'id0 id2 id3')

        s = DOMTokenList(root, attr_name)
        # token: not exist. force: none => add()
        result = s.toggle('id4')
        self.assertTrue(result)
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id0 id2 id3 id4', s.value)
        self.assertEqual('id0 id2 id3 id4', root.get(attr_name))
        self.assertTrue(s.contains('id0'))
        self.assertFalse(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertTrue(s.contains('id4'))
        self.assertEqual('id0', s.item(0))
        self.assertEqual('id2', s.item(1))
        self.assertEqual('id3', s.item(2))
        self.assertEqual('id4', s.item(3))

        # token: already exist. force: none => remove()
        result = s.toggle('id0')
        self.assertFalse(result)
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id2 id3 id4', s.value)
        self.assertEqual('id2 id3 id4', root.get(attr_name))
        self.assertFalse(s.contains('id0'))
        self.assertFalse(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertTrue(s.contains('id4'))
        self.assertEqual('id2', s.item(0))
        self.assertEqual('id3', s.item(1))
        self.assertEqual('id4', s.item(2))

        # force: True => add()
        result = s.toggle('id1', force=True)
        self.assertTrue(result)
        self.assertEqual(4, len(s))
        self.assertEqual(4, s.length)
        self.assertEqual('id2 id3 id4 id1', s.value)
        self.assertEqual('id2 id3 id4 id1', root.get(attr_name))
        self.assertFalse(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertTrue(s.contains('id4'))
        self.assertEqual('id2', s.item(0))
        self.assertEqual('id3', s.item(1))
        self.assertEqual('id4', s.item(2))
        self.assertEqual('id1', s.item(3))

        # force: False => remove()
        result = s.toggle('id4', False)
        self.assertFalse(result)
        self.assertEqual(3, len(s))
        self.assertEqual(3, s.length)
        self.assertEqual('id2 id3 id1', s.value)
        self.assertEqual('id2 id3 id1', root.get(attr_name))
        self.assertFalse(s.contains('id0'))
        self.assertTrue(s.contains('id1'))
        self.assertTrue(s.contains('id2'))
        self.assertTrue(s.contains('id3'))
        self.assertFalse(s.contains('id4'))
        self.assertEqual('id2', s.item(0))
        self.assertEqual('id3', s.item(1))
        self.assertEqual('id1', s.item(2))

    def test_element(self):
        # Element()
        parser = SVGParser()
        root = parser.create_element_ns(
            'http://www.w3.org/2000/svg',
            'svg',
            attrib={
                'viewBox': '0 0 400 300',
            },
            nsmap={
                'html': 'http://www.w3.org/1999/xhtml',
            })
        video = parser.create_element_ns(
            'http://www.w3.org/1999/xhtml',
            'video',
            attrib={
                'width': '400',
                'height': '300',
            })
        root.append(video)
        self.assertEqual(1, Node.ELEMENT_NODE)

        self.assertIsInstance(root, SVGElement)
        self.assertEqual(Node.ELEMENT_NODE, root.node_type)
        self.assertEqual('svg', root.node_name)
        self.assertEqual('svg', root.tag_name)
        self.assertEqual('svg', root.local_name)
        self.assertIsNone(root.node_value)
        self.assertEqual('http://www.w3.org/2000/svg', root.namespace_uri)
        self.assertIsNone(root.prefix)
        self.assertEqual('0 0 400 300', root.get('viewBox'))

        self.assertIsInstance(video, HTMLElement)
        self.assertEqual(Node.ELEMENT_NODE, video.node_type)
        self.assertEqual('html:video', video.node_name)
        self.assertEqual('html:video', video.tag_name)
        self.assertEqual('video', video.local_name)
        self.assertIsNone(video.node_value)
        self.assertEqual('http://www.w3.org/1999/xhtml', video.namespace_uri)
        self.assertEqual('html', video.prefix)
        self.assertEqual('400', video.get('width'))
        self.assertEqual('300', video.get('height'))

    def test_element_addnext(self):
        # ElementBase.addnext()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.addnext(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addnext(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.addnext(comment)
        self.assertEqual([parent, comment], list(root))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.addnext(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addnext(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.addnext(element)
        self.assertEqual([parent, element, comment], list(root))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.addnext(pi)
        self.assertEqual([parent, pi, element, comment], list(root))
        self.assertEqual(doc, pi.owner_document)

    def test_element_addprevious(self):
        # ElementBase.addprevious()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.addprevious(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addprevious(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.addprevious(comment)
        self.assertEqual([comment, parent], list(root))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.addprevious(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addprevious(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.addprevious(element)
        self.assertEqual([comment, element, parent], list(root))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.addprevious(pi)
        self.assertEqual([comment, element, pi, parent], list(root))
        self.assertEqual(doc, pi.owner_document)

    def test_element_append01(self):
        # ElementBase.append()
        # ParentNode.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.append(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.append(comment)
        self.assertEqual([comment], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.append(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.append(element)
        self.assertEqual([comment, element], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.append(pi)
        self.assertEqual([comment, element, pi], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_append02(self):
        # Element
        # ParentNode.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        root = parser.create_element_ns(svg_ns, 'svg')
        text = parser.create_element_ns(svg_ns, 'text')
        text.text = 'foo '
        root.append(text)

        # "<text>foo </text>"
        text.append('bar ', 'baz ', 'qux')
        # "<text>foo bar baz qux</text>"
        self.assertEqual(0, len(text))
        self.assertEqual('foo bar baz qux', text.text)
        self.assertEqual('foo bar baz qux', text.text_content)

    def test_element_append03(self):
        # Element
        # ParentNode.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        root = parser.create_element_ns(svg_ns, 'svg')
        text = parser.create_element_ns(svg_ns, 'text')
        text.text = 'foo '
        root.append(text)
        tspan = parser.create_element_ns(svg_ns, 'tspan')
        tspan.text = 'baz '

        # "<text>foo </text>"
        text.append('bar ', tspan, 'qux')
        # "<text>foo bar <tspan>baz </tspan>qux</text>"
        self.assertEqual(1, len(text))
        self.assertEqual([tspan], list(text))
        self.assertEqual('foo bar ', text.text)
        self.assertEqual('baz ', tspan.text)
        self.assertEqual('qux', tspan.tail)
        self.assertEqual('foo bar baz qux', text.text_content)

    def test_element_append_child(self):
        # Element
        # Node.append_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('fill')
        # parent.append_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        result = parent.append_child(comment)
        self.assertEqual(comment, result)
        self.assertEqual([comment], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.append_child(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        result = parent.append_child(element)
        self.assertEqual(element, result)
        self.assertEqual([comment, element], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        result = parent.append_child(pi)
        self.assertEqual(pi, result)
        self.assertEqual([comment, element, pi], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_attributes_del(self):
        # NamedNodeMap.__delitem__()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.id = value = 'toc'
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual(value, root.get('id'))
        del root.attributes['id']
        self.assertEqual(0, len(root.attributes))
        self.assertEqual(0, root.attributes.length)
        self.assertIsNone(root.get('id'))

        root.id = value = 'toc'
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual(value, root.get('id'))
        root.attributes['id'] = ''  # remove
        self.assertEqual(0, len(root.attributes))
        self.assertEqual(0, root.attributes.length)
        self.assertIsNone(root.get('id'))

        root.id = value = 'toc'
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual(value, root.get('id'))
        root.attributes['id'] = None  # remove
        self.assertEqual(0, len(root.attributes))
        self.assertEqual(0, root.attributes.length)
        self.assertIsNone(root.get('id'))

    def test_element_attributes_get(self):
        # NamedNodeMap.__getitem__()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        root.id = 'toc'
        root.class_name = 'toc-sidebar'
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(2, root.attributes.length)
        self.assertEqual('toc', root.get('id'))
        self.assertEqual('toc-sidebar', root.get('class'))

        attr = root.attributes['id']
        self.assertIsInstance(attr, Attr)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('id', attr.name)
        self.assertEqual('id', attr.local_name)
        self.assertEqual('toc', attr.value)
        self.assertEqual(root, attr.owner_element)

        attr = root.attributes['class']
        self.assertIsInstance(attr, Attr)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('class', attr.name)
        self.assertEqual('class', attr.local_name)
        self.assertEqual('toc-sidebar', attr.value)
        self.assertEqual(root, attr.owner_element)

        self.assertRaises(KeyError,
                          lambda: root.attributes['style'])

    def test_element_attributes_set(self):
        # NamedNodeMap.__setitem__()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        root.id = 'toc'
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual('toc', root.get('id'))

        root.attributes['id'] = 'toc-nav'  # string
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual('toc-nav', root.get('id'))

        attr = parser.create_attribute('class')
        attr.value = 'toc-sidebar'
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('class', attr.name)
        self.assertEqual('class', attr.local_name)
        self.assertIsNone(attr.owner_element)
        root.attributes['class'] = attr  # Attr
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(2, root.attributes.length)
        self.assertEqual('toc-nav', root.get('id'))
        self.assertEqual('toc-sidebar', root.get('class'))
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('class', attr.name)
        self.assertEqual('class', attr.local_name)
        self.assertEqual(root, attr.owner_element)

    def test_element_attributes_get_named_item(self):
        # NamedNodeMap.get_named_item()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        root.id = 'toc'
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual('toc', root.get('id'))

        attr = root.attributes.get_named_item('id')
        self.assertIsInstance(attr, Attr)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('id', attr.name)
        self.assertEqual('id', attr.local_name)
        self.assertEqual('toc', attr.value)
        self.assertEqual(root, attr.owner_element)

        attr = root.attributes.get_named_item('class')
        self.assertIsNone(attr)

    def test_element_attributes_get_named_item_ns(self):
        # NamedNodeMap.get_named_item_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        qualified_name = '{{{0}}}{1}'.format(namespace, local_name)
        value = 'ja'
        root.set(qualified_name, value)
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual(value, root.get(qualified_name))

        attr = root.attributes.get_named_item_ns(namespace, local_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(root, attr.owner_element)

        attr = root.attributes.get_named_item_ns(namespace, qualified_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(root, attr.owner_element)

        attr = root.attributes.get_named_item_ns('', qualified_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(root, attr.owner_element)

        attr = root.attributes.get_named_item_ns(None, qualified_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(root, attr.owner_element)

    def test_element_attributes_item(self):
        # NamedNodeMap.item()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        root.id = 'toc'
        root.class_name = 'toc-sidebar'
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(2, root.attributes.length)
        self.assertEqual('toc', root.get('id'))
        self.assertEqual('toc-sidebar', root.get('class'))
        keys = list(root.keys())

        for index, name in enumerate(keys):
            with self.subTest(index=index, name=name):
                attr = root.attributes.item(index)
                self.assertIsInstance(attr, Attr)
                self.assertIsNone(attr.namespace_uri)
                self.assertIsNone(attr.prefix)
                self.assertEqual(name, attr.name)
                self.assertEqual(name, attr.local_name)
                self.assertEqual(root.get(name), attr.value)
                self.assertEqual(root, attr.owner_element)

    def test_element_attributes_remove_named_item(self):
        # NamedNodeMap.remove_named_item()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        root.id = 'toc'
        root.class_name = 'toc-sidebar'
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(2, root.attributes.length)

        attr = root.attributes.remove_named_item('id')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertTrue('id' not in root.attrib)
        self.assertTrue('class' in root.attrib)
        self.assertIsInstance(attr, Attr)
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('id', attr.name)
        self.assertEqual('id', attr.local_name)
        self.assertEqual('toc', attr.value)
        self.assertIsNone(attr.owner_element)

        attr.value = 'toc-nav'  # no effect
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertTrue('id' not in root.attrib)
        self.assertTrue('class' in root.attrib)

        self.assertRaises(KeyError,
                          lambda: root.attributes.remove_named_item('id'))

    def test_element_attributes_remove_named_item_ns(self):
        # NamedNodeMap.remove_named_item_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        qualified_name = '{{{0}}}{1}'.format(namespace, local_name)
        value = 'ja'
        root.set(qualified_name, value)
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual(value, root.get(qualified_name))

        attr = root.attributes.remove_named_item_ns(namespace, local_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertIsNone(attr.owner_element)

        self.assertRaises(KeyError,
                          lambda: root.attributes.remove_named_item_ns(
                              namespace, local_name))

    def test_element_attributes_set_named_item(self):
        # NamedNodeMap.set_named_item()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertEqual(0, len(root.attributes))
        self.assertEqual(0, root.attributes.length)

        attr = parser.create_attribute('class')
        attr.value = value = 'toc-sidebar'
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('class', attr.name)
        self.assertEqual('class', attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertIsNone(attr.owner_element)

        root.attributes.set_named_item(attr)
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertEqual(value, root.get('class'))
        self.assertIsNone(attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual('class', attr.name)
        self.assertEqual('class', attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(root, attr.owner_element)

        attr.value = value = 'heading'
        self.assertEqual(value, root.get('class'))

        value = 'issue'
        root.set('class', value)
        self.assertEqual(value, attr.value)

    def test_element_attributes_set_named_item_ns(self):
        # NamedNodeMap.set_named_item()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertEqual(0, len(root.attributes))
        self.assertEqual(0, root.attributes.length)

        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        qualified_name = '{{{0}}}{1}'.format(namespace, local_name)
        value = 'ja'
        attr = parser.create_attribute_ns(namespace, local_name)
        attr.value = value
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertIsNone(attr.owner_element)
        root.attributes.set_named_item_ns(attr)
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, root.attributes.length)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertIsNone(attr.prefix)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(root, attr.owner_element)
        self.assertEqual(value, root.get(qualified_name))

        attr.value = value = 'fr'
        self.assertEqual(value, root.get(qualified_name))

        value = 'es'
        root.set(qualified_name, value)
        self.assertEqual(value, attr.value)

    def test_element_child_nodes(self):
        # Node.child_nodes
        # Node.first_child
        # Node.last_child
        # Node.next_sibling
        # Node.previous_sibling
        # Node.has_child_nodes()
        parser = SVGParser()
        # <?xml-stylesheet ?>
        # <!--start-->
        # <svg xmlns="http://www.w3.org/2000/svg">
        # <!--inner-->
        # <g><path/></g>
        # <text/>
        # </svg>
        # <!--end-->'
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        pi = parser.create_processing_instruction('xml-stylesheet')
        root.addprevious(pi)
        start = parser.create_comment('start')
        root.addprevious(start)
        end = parser.create_comment('end')
        root.addnext(end)
        comment = parser.create_comment('inner')
        root.append(comment)
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        root.append(group)
        path = parser.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        text = parser.create_element_ns('http://www.w3.org/2000/svg', 'text')
        root.append(text)
        # window.document.append(root)
        # print(window.document.tostring())

        children = root.child_nodes
        self.assertEqual([comment, group, text], children)
        node = root.first_child
        self.assertEqual(comment, node)
        node = root.last_child
        self.assertEqual(text, node)
        node = root.previous_sibling
        self.assertEqual(start, node)
        node = root.next_sibling
        self.assertEqual(end, node)
        self.assertTrue(root.has_child_nodes())

        children = group.child_nodes
        self.assertEqual([path], children)
        node = group.first_child
        self.assertEqual(path, node)
        node = group.last_child
        self.assertEqual(path, node)
        node = group.previous_sibling
        self.assertEqual(comment, node)
        node = group.next_sibling
        self.assertEqual(text, node)
        self.assertTrue(group.has_child_nodes())

        children = text.child_nodes
        self.assertEqual(0, len(children))
        node = text.first_child
        self.assertIsNone(node)
        node = text.last_child
        self.assertIsNone(node)
        node = text.previous_sibling
        self.assertEqual(group, node)
        node = text.next_sibling
        self.assertIsNone(node)
        self.assertFalse(text.has_child_nodes())

    def test_element_children(self):
        # ParentNode.children
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        comment = parser.create_comment('comment')
        root.append(comment)
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        root.append(group)
        path = parser.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        text = parser.create_element_ns('http://www.w3.org/2000/svg', 'text')
        root.append(text)

        children = root.children
        self.assertEqual([group, text], children)
        children = group.children
        self.assertEqual([path], children)
        children = text.children
        self.assertEqual(0, len(children))

    def test_element_class_list01(self):
        # Element.class_list
        # Element.class_name
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        self.assertIsNone(root.get('class'))
        self.assertEqual('', root.class_name)
        class_list = root.class_list
        self.assertIsInstance(class_list, DOMTokenList)
        self.assertEqual(0, len(class_list))

        class_list.add('Border')
        self.assertEqual('Border', root.get('class'))
        self.assertEqual('Border', root.class_name)

        class_list.replace('Border', 'Label')
        self.assertEqual('Label', root.get('class'))
        self.assertEqual('Label', root.class_name)

        class_list.toggle('Label')
        self.assertIsNone(root.get('class'))
        self.assertEqual('', root.class_name)

    def test_element_class_list02(self):
        # Element.class_list
        # Element.class_name
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        self.assertIsNone(root.get('class'))
        self.assertEqual('', root.class_name)
        class_list = root.class_list
        self.assertIsInstance(class_list, DOMTokenList)
        self.assertEqual(0, len(class_list))

        root.class_name = 'Border'
        self.assertEqual('Border', root.class_name)
        self.assertEqual('Border', root.get('class'))
        class_list = root.class_list
        self.assertEqual(1, len(class_list))
        self.assertEqual('Border', class_list[0])

    def test_element_class_list03(self):
        # Element.class_list
        # Element.class_name
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        root.class_name = 'Border Label'
        self.assertEqual('Border Label', root.class_name)
        self.assertEqual('Border Label', root.get('class'))
        class_list = root.class_list
        self.assertIsInstance(class_list, DOMTokenList)
        self.assertEqual(2, len(class_list))
        self.assertEqual('Border', class_list[0])
        self.assertEqual('Label', class_list[1])

        rect = root.get_elements_by_tag_name_ns('http://www.w3.org/2000/svg',
                                                'rect')[0]
        self.assertEqual('Border', rect.get('class'))
        self.assertEqual('Border', rect.class_name)
        class_list = rect.class_list
        self.assertEqual(1, len(class_list))
        self.assertEqual('Border', class_list[0])
        class_list.remove('Border')
        self.assertEqual(0, len(class_list))
        self.assertIsNone(rect.get('class'))
        self.assertEqual('', rect.class_name)

    def test_element_dataset(self):
        # HTMLOrSVGElement.dataset
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertIsInstance(root.dataset, DOMStringMap)
        root.attributes['viewBox'] = '0 0 600 400'
        root.dataset['foo'] = 'foo'
        root.dataset['fooBar'] = 'fooBar'
        root.dataset['fooBarBaz'] = 'fooBarBaz'

        self.assertEqual(4, len(root.attrib))
        self.assertEqual(4, len(root.attributes))
        self.assertEqual(3, len(root.dataset))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertEqual('foo', root.get('data-foo'))
        self.assertEqual('fooBar', root.get('data-foo-bar'))
        self.assertEqual('fooBarBaz', root.get('data-foo-bar-baz'))
        self.assertEqual('0 0 600 400', root.attributes['viewBox'].value)
        self.assertEqual('foo', root.attributes['data-foo'].value)
        self.assertEqual('fooBar', root.attributes['data-foo-bar'].value)
        self.assertEqual('fooBarBaz',
                         root.attributes['data-foo-bar-baz'].value)
        self.assertEqual('foo', root.dataset['foo'])
        self.assertEqual('fooBar', root.dataset['fooBar'])
        self.assertEqual('fooBarBaz', root.dataset['fooBarBaz'])

        del root.dataset['fooBarBaz']
        self.assertEqual(3, len(root.attrib))
        self.assertEqual(3, len(root.attributes))
        self.assertEqual(2, len(root.dataset))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertEqual('foo', root.get('data-foo'))
        self.assertEqual('fooBar', root.get('data-foo-bar'))
        self.assertTrue('data-foo-bar-baz' not in root.attrib)
        self.assertEqual('0 0 600 400', root.attributes['viewBox'].value)
        self.assertEqual('foo', root.attributes['data-foo'].value)
        self.assertEqual('fooBar', root.attributes['data-foo-bar'].value)
        self.assertTrue('fooBarBaz' not in root.attributes)
        self.assertEqual('foo', root.dataset['foo'])
        self.assertEqual('fooBar', root.dataset['fooBar'])
        self.assertTrue('fooBarBaz' not in root.dataset)

        del root.attrib['data-foo']
        self.assertEqual(2, len(root.attrib))
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(1, len(root.dataset))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertTrue('data-foo' not in root.attrib)
        self.assertEqual('fooBar', root.get('data-foo-bar'))
        self.assertTrue('data-foo-bar-baz' not in root.attrib)
        self.assertEqual('0 0 600 400', root.attributes['viewBox'].value)
        self.assertTrue('data-foo' not in root.attributes)
        self.assertEqual('fooBar', root.attributes['data-foo-bar'].value)
        self.assertTrue('fooBarBaz' not in root.attributes)
        self.assertTrue('foo' not in root.dataset)
        self.assertEqual('fooBar', root.dataset['fooBar'])
        self.assertTrue('fooBarBaz' not in root.dataset)

        root.set('data-A', 'A')  # invalid name
        self.assertEqual(3, len(root.attrib))
        self.assertEqual(3, len(root.attributes))
        self.assertEqual(1, len(root.dataset))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertTrue('data-foo' not in root.attrib)
        self.assertEqual('fooBar', root.get('data-foo-bar'))
        self.assertTrue('data-foo-bar-baz' not in root.attrib)
        self.assertEqual('A', root.get('data-A'))
        self.assertEqual('0 0 600 400', root.attributes['viewBox'].value)
        self.assertTrue('data-foo' not in root.attributes)
        self.assertEqual('fooBar', root.attributes['data-foo-bar'].value)
        self.assertTrue('fooBarBaz' not in root.attributes)
        self.assertEqual('A', root.attributes['data-A'].value)
        self.assertTrue('foo' not in root.dataset)
        self.assertEqual('fooBar', root.dataset['fooBar'])
        self.assertTrue('fooBarBaz' not in root.dataset)

        root.set('data-a', 'a')  # valid name
        self.assertEqual(4, len(root.attrib))
        self.assertEqual(4, len(root.attributes))
        self.assertEqual(2, len(root.dataset))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertTrue('data-foo' not in root.attrib)
        self.assertEqual('fooBar', root.get('data-foo-bar'))
        self.assertTrue('data-foo-bar-baz' not in root.attrib)
        self.assertEqual('A', root.get('data-A'))
        self.assertEqual('a', root.get('data-a'))
        self.assertEqual('0 0 600 400', root.attributes['viewBox'].value)
        self.assertTrue('data-foo' not in root.attributes)
        self.assertEqual('fooBar', root.attributes['data-foo-bar'].value)
        self.assertTrue('fooBarBaz' not in root.attributes)
        self.assertEqual('A', root.attributes['data-A'].value)
        self.assertEqual('a', root.attributes['data-a'].value)
        self.assertTrue('foo' not in root.dataset)
        self.assertEqual('fooBar', root.dataset['fooBar'])
        self.assertTrue('fooBarBaz' not in root.dataset)
        self.assertEqual('a', root.dataset['a'])
        # print(root.tostring())

    def test_element_extend(self):
        # ElementBase.extend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.extend([attr])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([attr]))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.extend([comment])
        self.assertEqual([comment], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.extend([doc2])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([doc2]))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.extend([element])
        self.assertEqual([comment, element], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.extend([pi])
        self.assertEqual([comment, element, pi], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_get_attribute(self):
        # Element.get_attribute()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.set('viewBox', '0 0 600 400')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        root.set(xml_lang, 'ja')

        value = root.get_attribute('viewBox')
        self.assertEqual('0 0 600 400', value)

        value = root.get_attribute(xml_lang)
        self.assertEqual('ja', value)

        self.assertIsNone(root.get_attribute('x'))
        self.assertIsNone(root.get_attribute('y'))

    def test_element_get_attribute_ns(self):
        # Element.get_attribute_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.set('viewBox', '0 0 600 400')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        root.set(xml_lang, 'ja')

        value = root.get_attribute_ns(None, 'viewBox')
        self.assertEqual('0 0 600 400', value)

        value = root.get_attribute_ns(None, xml_lang)
        self.assertEqual('ja', value)

        value = root.get_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                      xml_lang)
        self.assertEqual('ja', value)

        value = root.get_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                      'lang')
        self.assertEqual('ja', value)

        self.assertIsNone(root.get_attribute_ns(None, 'x'))
        self.assertIsNone(root.get_attribute_ns(None, 'y'))

    def test_element_get_attribute_names(self):
        # Element.get_attribute_names()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        names = root.get_attribute_names()
        self.assertEqual(0, len(names))

        root.set('width', '600')
        root.set('height', '400')
        root.set('viewBox', '0 0 600 400')
        names = root.get_attribute_names()
        self.assertEqual(['height', 'viewBox', 'width'],
                         names)

        root.set('x', '0')
        root.set('y', '0')
        names = root.get_attribute_names()
        self.assertEqual(['height', 'viewBox', 'width', 'x', 'y'],
                         names)

    def test_element_get_attribute_node(self):
        # Element.get_attribute_node()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        src_attr = parser.create_attribute_ns(
            'http://www.w3.org/XML/1998/namespace',
            'lang')
        src_attr.value = 'ja'
        root.attributes.set_named_item_ns(src_attr)

        attr = root.get_attribute_node(xml_lang)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)

        self.assertIsNone(root.get_attribute_node('lang'))

    def test_element_get_attribute_node_ns(self):
        # Element.get_attribute_node_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        src_attr = parser.create_attribute_ns(
            'http://www.w3.org/XML/1998/namespace',
            'lang')
        src_attr.value = 'ja'
        root.attributes.set_named_item_ns(src_attr)

        attr = root.get_attribute_node_ns(None, xml_lang)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)

        attr = root.get_attribute_node_ns(
            'http://www.w3.org/XML/1998/namespace', xml_lang)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)

        attr = root.get_attribute_node_ns(
            'http://www.w3.org/XML/1998/namespace', 'lang')
        self.assertIsInstance(attr, Attr)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)

        self.assertIsNone(root.get_attribute_node_ns(None, 'lang'))

    def test_element_has_attribute(self):
        # Element.has_attribute()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        self.assertFalse(root.has_attribute('viewBox'))

        root.set('viewBox', '0 0 600 400')
        self.assertTrue(root.has_attribute('viewBox'))

        self.assertFalse(root.has_attribute(xml_lang))

        attr = parser.create_attribute_ns(
            'http://www.w3.org/XML/1998/namespace', 'lang')
        attr.value = 'ja'
        root.attributes.set_named_item_ns(attr)
        self.assertTrue(root.has_attribute(xml_lang))

    def test_element_has_attribute_ns(self):
        # Element.has_attribute_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        self.assertFalse(root.has_attribute_ns(None, 'viewBox'))

        root.set('viewBox', '0 0 600 400')
        self.assertTrue(root.has_attribute_ns(None, 'viewBox'))

        self.assertFalse(root.has_attribute_ns(None, xml_lang))
        self.assertFalse(
            root.has_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                  xml_lang))
        self.assertFalse(
            root.has_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                  'lang'))

        attr = parser.create_attribute_ns(
            'http://www.w3.org/XML/1998/namespace', 'lang')
        attr.value = 'ja'
        root.attributes.set_named_item_ns(attr)
        self.assertTrue(root.has_attribute_ns(None, xml_lang))
        self.assertTrue(
            root.has_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                  xml_lang))
        self.assertTrue(
            root.has_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                  'lang'))

    def test_element_has_attributes(self):
        # Element.has_attributes()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertEqual(0, len(root.attrib))
        self.assertFalse(root.has_attributes())

        root.set('width', '600')
        root.set('height', '400')
        self.assertEqual(2, len(root.attrib))
        self.assertTrue(root.has_attributes())

        del root.attrib['width']
        self.assertEqual(1, len(root.attrib))
        self.assertTrue(root.has_attributes())

        del root.attrib['height']
        self.assertEqual(0, len(root.attrib))
        self.assertFalse(root.has_attributes())

    def test_element_id(self):
        # Element.id
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertIsNone(root.get('id'))
        self.assertEqual(0, len(root.id))

        root.id = value = 'toc'
        self.assertEqual(value, root.get('id'))
        self.assertEqual(value, root.id)

        value = 'toc-nav'
        root.set('id', value)
        self.assertEqual(value, root.get('id'))
        self.assertEqual(value, root.id)

    def test_element_namespace_uri(self):
        # Element.namespace_uri
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertEqual('http://www.w3.org/2000/svg', root.namespace_uri)
        self.assertIsNone(root.prefix)

        nsmap = {
            'html': 'http://www.w3.org/1999/xhtml',
        }
        root = parser.create_element_ns('http://www.w3.org/2000/svg',
                                        'svg',
                                        nsmap=nsmap)
        self.assertEqual('http://www.w3.org/2000/svg', root.namespace_uri)
        self.assertIsNone(root.prefix)

        video = parser.create_element_ns('http://www.w3.org/1999/xhtml',
                                         'video',
                                         nsmap=nsmap)
        self.assertEqual('http://www.w3.org/1999/xhtml', video.namespace_uri)
        self.assertEqual('html', video.prefix)

    def test_element_insert(self):
        # ElementBase.insert()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.insert(1, attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.insert(1, comment)
        self.assertEqual([comment], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.insert(1, doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.insert(1, element)
        self.assertEqual([comment, element], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.insert(1, pi)
        self.assertEqual([comment, pi, element], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_insert_before01(self):
        # Element
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        group = parser.create_element_ns(svg_ns, 'g')
        self.assertIsNone(group.owner_document)
        parent.append(group)
        self.assertEqual(doc, group.owner_document)

        attr = parser.create_attribute('foo')
        # parent.insert_before(attr, group)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, group))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        result = parent.insert_before(comment, group)
        self.assertEqual(comment, result)
        self.assertEqual([comment, group], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.insert_before(doc2, group)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, group))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        result = parent.insert_before(element, group)
        self.assertEqual(element, result)
        self.assertEqual([comment, element, group], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        result = parent.insert_before(pi, group)
        self.assertEqual(pi, result)
        self.assertEqual([comment, element, pi, group], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_insert_before02(self):
        # Element
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        group = parser.create_element_ns(svg_ns, 'g')
        self.assertIsNone(group.owner_document)
        parent.append(group)
        self.assertEqual(doc, group.owner_document)

        attr = parser.create_attribute('foo')
        # parent.insert_before(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, None))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.insert_before(comment, None)
        self.assertEqual([group, comment], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.insert_before(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.insert_before(element, None)
        self.assertEqual([group, comment, element], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.insert_before(pi, None)
        self.assertEqual([group, comment, element, pi], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_next_element_sibling(self):
        # Element.next_element_sibling
        parser = SVGParser()
        root = parser.create_element('svg')

        desc = parser.create_element('desc')
        root.append(desc)
        comment = parser.create_comment('comment')
        root.append(comment)
        rect = parser.create_element('rect')
        rect.id = 'border'
        root.append(rect)
        path = parser.create_element('path')
        root.append(path)

        e = root.next_element_sibling
        self.assertIsNone(e)

        e = desc.next_element_sibling
        self.assertEqual(rect, e)

        e = rect.next_element_sibling
        self.assertEqual(path, e)

        e = path.next_element_sibling
        self.assertIsNone(e)

    def test_element_prepend01(self):
        # Element
        # ParentNode.prepend()
        parser = SVGParser()
        svg_ns = 'http://www.w3.org/2000/svg'
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.prepend(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.prepend(comment)
        self.assertEqual(1, len(parent))
        self.assertEqual([comment], list(parent))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.prepend(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.prepend(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.prepend(element)
        self.assertEqual(2, len(parent))
        self.assertEqual([element, comment], list(parent))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.prepend(pi)
        self.assertEqual(3, len(parent))
        self.assertEqual([pi, element, comment], list(parent))
        self.assertEqual(doc, pi.owner_document)

    def test_element_prepend02(self):
        # Element
        # ParentNode.prepend()
        parser = SVGParser()
        svg_ns = 'http://www.w3.org/2000/svg'
        root = parser.create_element_ns(svg_ns, 'svg')
        text = parser.create_element_ns(svg_ns, 'text')
        text.text = 'qux'
        root.prepend(text)

        # "<text>qux</text>"
        text.prepend('foo ', 'bar ', 'baz ')
        # "<text>foo bar baz qux</text>"
        self.assertEqual(0, len(text))
        self.assertEqual('foo bar baz qux', text.text)
        self.assertEqual('foo bar baz qux', text.text_content)

    def test_element_prepend03(self):
        # Element
        # ParentNode.prepend()
        parser = SVGParser()
        svg_ns = 'http://www.w3.org/2000/svg'
        root = parser.create_element_ns(svg_ns, 'svg')
        text = parser.create_element_ns(svg_ns, 'text')
        text.text = 'qux'
        root.prepend(text)
        tspan = parser.create_element_ns(svg_ns, 'tspan')
        tspan.text = 'bar '

        # "<text>qux</text>"
        text.prepend('foo ', tspan, 'baz ')
        # "<text>foo <tspan>bar </tspan>baz qux</text>"
        self.assertEqual([tspan], list(text))
        self.assertEqual('foo ', text.text)
        self.assertEqual('bar ', tspan.text)
        self.assertEqual('baz qux', tspan.tail)
        self.assertEqual('foo bar baz qux', text.text_content)

        tspan1 = parser.create_element_ns(svg_ns, 'tspan')
        tspan1.text = 'quux '
        tspan2 = parser.create_element_ns(svg_ns, 'tspan')
        tspan2.text = 'corge '
        text.prepend(tspan1, tspan2)
        self.assertEqual([tspan1, tspan2, tspan], list(text))
        self.assertEqual('quux corge foo bar baz qux', text.text_content)

    def test_element_previous_element_sibling(self):
        # Element.previous_element_sibling
        parser = SVGParser()
        root = parser.create_element('svg')

        desc = parser.create_element('desc')
        root.append(desc)
        comment = parser.create_comment('comment')
        root.append(comment)
        rect = parser.create_element('rect')
        rect.id = 'border'
        root.append(rect)
        path = parser.create_element('path')
        root.append(path)

        e = root.previous_element_sibling
        self.assertIsNone(e)

        e = desc.previous_element_sibling
        self.assertIsNone(e)

        e = rect.previous_element_sibling
        self.assertEqual(desc, e)

        e = path.previous_element_sibling
        self.assertEqual(rect, e)

    def test_element_remove01(self):
        # ElementBase.remove()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_element_ns(svg_ns, 'svg')

        comment = parser.create_comment('foo')
        parent.append(comment)

        element = parser.create_element_ns(svg_ns, 'svg')
        parent.append(element)
        self.assertEqual([comment, element], list(parent))

        parent.remove(element)
        self.assertEqual([comment], list(parent))

        parent.remove(comment)
        self.assertEqual([], list(parent))

        # parent.remove(comment)
        self.assertRaises(NotFoundError,
                          lambda: parent.remove(comment))

    def test_element_remove02(self):
        # Element
        # ChildNode.remove()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_element_ns(svg_ns, 'svg')

        comment = parser.create_comment('foo')
        parent.append(comment)

        element = parser.create_element_ns(svg_ns, 'svg')
        parent.append(element)
        self.assertEqual([comment, element], list(parent))

        element.remove()
        self.assertEqual([comment], list(parent))

        element.remove()  # non-error
        self.assertEqual([comment], list(parent))

    def test_element_remove_attribute(self):
        # Element.remove_attribute()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        root.set('viewBox', '0 0 600 400')
        attr = parser.create_attribute(xml_lang)
        attr.value = 'ja'
        root.attributes[xml_lang] = attr
        self.assertEqual(2, len(root.attrib))
        self.assertEqual(root, attr.owner_element)

        root.remove_attribute('viewBox')
        self.assertEqual(1, len(root.attrib))
        self.assertTrue(xml_lang in root.attrib)

        root.remove_attribute(xml_lang)
        self.assertEqual(0, len(root.attrib))
        self.assertIsNone(attr.owner_element)

        root.remove_attribute('lang')  # no effect

    def test_element_remove_attribute_node(self):
        # Element.remove_attribute_node()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        root.set('viewBox', '0 0 600 400')
        self.assertTrue('viewBox' in root.attrib)
        src_attr = root.get_attribute_node('viewBox')
        attr = root.remove_attribute_node(src_attr)
        self.assertTrue('viewBox' not in root.attrib)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('0 0 600 400', attr.value)
        self.assertIsNone(attr.owner_element)

        src_attr = parser.create_attribute(xml_lang)
        src_attr.value = 'ja'
        root.attributes[xml_lang] = src_attr
        self.assertTrue(xml_lang in root.attrib)
        attr = root.remove_attribute_node(src_attr)
        self.assertTrue(xml_lang not in root.attrib)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)
        self.assertIsNone(attr.owner_element)

        self.assertRaises(KeyError,
                          lambda: root.remove_attribute_node(attr))

    def test_element_remove_attribute_ns(self):
        # Element.remove_attribute_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        root.set('viewBox', '0 0 600 400')
        attr = parser.create_attribute(xml_lang)
        attr.value = 'ja'
        root.attributes[xml_lang] = attr
        self.assertEqual(2, len(root.attrib))
        self.assertEqual(root, attr.owner_element)

        root.remove_attribute_ns(None, 'viewBox')
        self.assertEqual(1, len(root.attrib))
        self.assertTrue(xml_lang in root.attrib)

        root.remove_attribute_ns(None, xml_lang)
        self.assertEqual(0, len(root.attrib))
        self.assertIsNone(attr.owner_element)

        root.attributes[xml_lang] = attr
        self.assertEqual(1, len(root.attrib))
        self.assertEqual(root, attr.owner_element)
        root.remove_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                 xml_lang)
        self.assertEqual(0, len(root.attrib))
        self.assertIsNone(attr.owner_element)

        root.attributes[xml_lang] = attr
        self.assertEqual(1, len(root.attrib))
        self.assertEqual(root, attr.owner_element)
        root.remove_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                 'lang')
        self.assertEqual(0, len(root.attrib))
        self.assertIsNone(attr.owner_element)

        # no effect
        root.remove_attribute_ns('http://www.w3.org/XML/1998/namespace',
                                 'space')

    def test_element_remove_child(self):
        # Element
        # Node.remove_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        parent = doc.document_element

        comment = parser.create_comment('foo')
        parent.append(comment)

        element = parser.create_element_ns(svg_ns, 'svg')
        parent.append(element)
        self.assertEqual([comment, element], list(parent))

        result = parent.remove_child(element)
        self.assertEqual(element, result)
        self.assertEqual([comment], list(parent))

        result = parent.remove_child(comment)
        self.assertEqual(comment, result)
        self.assertEqual([], list(parent))

        # parent.remove_child(comment)
        self.assertRaises(NotFoundError,
                          lambda: parent.remove_child(comment))

    def test_element_replace(self):
        # ElementBase.replace()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        parent = doc.document_element

        comment = parser.create_comment('foo')
        parent.append(comment)

        style = parser.create_element_ns(svg_ns, 'style')
        parent.append(style)

        text = parser.create_element_ns(svg_ns, 'text')
        parent.append(text)
        self.assertEqual([comment, style, text], list(parent))

        group = parser.create_element_ns(svg_ns, 'g')
        self.assertIsNone(group.owner_document)
        parent.replace(style, group)
        self.assertEqual([comment, group, text], list(parent))
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(doc, group.owner_document)

        # parent.replace(style, group)
        self.assertRaises(NotFoundError,
                          lambda: parent.replace(style, group))

        parent.replace(group, style)
        self.assertEqual([comment, style, text], list(parent))
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(doc, group.owner_document)

    def test_element_replace_child(self):
        # Element
        # Node.replace_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        parent = doc.document_element

        comment = parser.create_comment('foo')
        parent.append(comment)

        style = parser.create_element_ns(svg_ns, 'style')
        parent.append(style)

        text = parser.create_element_ns(svg_ns, 'text')
        parent.append(text)
        self.assertEqual([comment, style, text], list(parent))

        group = parser.create_element_ns(svg_ns, 'g')
        self.assertIsNone(group.owner_document)
        result = parent.replace_child(group, style)
        self.assertEqual(style, result)
        self.assertEqual([comment, group, text], list(parent))
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(doc, group.owner_document)

        # parent.replace_child(group, style)
        self.assertRaises(NotFoundError,
                          lambda: parent.replace_child(group, style))

        result = parent.replace_child(style, group)
        self.assertEqual(group, result)
        self.assertEqual([comment, style, text], list(parent))
        self.assertEqual(doc, style.owner_document)
        self.assertEqual(doc, group.owner_document)

    def test_element_set_attribute(self):
        # Element.set_attribute()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        root.set_attribute('viewBox', '0 0 600 400')
        root.set_attribute(xml_lang, 'ja')
        self.assertEqual(2, len(root.attrib))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertEqual('ja', root.get(xml_lang))

    def test_element_set_attribute_node(self):
        # Element.set_attribute_node()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        src_attr = parser.create_attribute(xml_lang)
        src_attr.value = 'ja'
        attr = root.set_attribute_node(src_attr)
        self.assertEqual('ja', root.get(xml_lang))
        self.assertEqual('ja', src_attr.value)
        self.assertEqual(root, src_attr.owner_element)
        self.assertIsNone(attr)

        new_attr = parser.create_attribute(xml_lang)
        new_attr.value = 'en'
        attr = root.set_attribute_node(new_attr)
        self.assertEqual('en', root.get(xml_lang))
        self.assertEqual('en', new_attr.value)
        self.assertEqual(root, new_attr.owner_element)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)
        self.assertIsNone(attr.owner_element)

    def test_element_set_attribute_node_ns(self):
        # Element.set_attribute_node_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')

        src_attr = parser.create_attribute_ns(
            'http://www.w3.org/XML/1998/namespace',
            'lang')
        src_attr.value = 'ja'
        attr = root.set_attribute_node_ns(src_attr)
        self.assertEqual('ja', root.get(xml_lang))
        self.assertEqual('ja', src_attr.value)
        self.assertEqual(root, src_attr.owner_element)
        self.assertIsNone(attr)

        new_attr = parser.create_attribute_ns(
            'http://www.w3.org/XML/1998/namespace',
            'lang')
        new_attr.value = 'en'
        attr = root.set_attribute_node_ns(new_attr)
        self.assertEqual('en', root.get(xml_lang))
        self.assertEqual('en', new_attr.value)
        self.assertEqual(root, new_attr.owner_element)
        self.assertEqual(id(src_attr), id(attr))
        self.assertEqual('ja', attr.value)
        self.assertIsNone(attr.owner_element)

    def test_element_set_attribute_ns(self):
        # Element.set_attribute_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        root.set_attribute_ns(None, 'viewBox', '0 0 600 400')
        root.set_attribute_ns(None, xml_lang, 'ja')
        self.assertEqual(2, len(root.attrib))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertEqual('ja', root.get(xml_lang))

        root.set_attribute_ns('http://www.w3.org/XML/1998/namespace', xml_lang,
                              'es')
        self.assertEqual(2, len(root.attrib))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertEqual('es', root.get(xml_lang))

        root.set_attribute_ns('http://www.w3.org/XML/1998/namespace', 'lang',
                              'fr')
        self.assertEqual(2, len(root.attrib))
        self.assertEqual('0 0 600 400', root.get('viewBox'))
        self.assertEqual('fr', root.get(xml_lang))

    def test_element_toggle_attribute(self):
        # Element.toggle_attribute()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        xml_lang = '{{{}}}{}'.format('http://www.w3.org/XML/1998/namespace',
                                     'lang')
        self.assertEqual(0, len(root.attrib))

        # not exist, force=None => add
        result = root.toggle_attribute(xml_lang)
        self.assertTrue(xml_lang in root.attrib)
        self.assertTrue(result)
        self.assertEqual('', root.get(xml_lang))

        # exist, force=None => remove
        result = root.toggle_attribute(xml_lang)
        self.assertFalse(xml_lang in root.attrib)
        self.assertFalse(result)

        # not exist, force=True => add
        result = root.toggle_attribute(xml_lang, True)
        self.assertTrue(xml_lang in root.attrib)
        self.assertTrue(result)
        self.assertEqual('', root.get(xml_lang))

        # exist, force=True => do nothing
        root.set(xml_lang, 'ja')
        result = root.toggle_attribute(xml_lang, True)
        self.assertTrue(xml_lang in root.attrib)
        self.assertTrue(result)
        self.assertEqual('ja', root.get(xml_lang))

        # exist, force=False => remove
        result = root.toggle_attribute(xml_lang, False)
        self.assertFalse(xml_lang in root.attrib)
        self.assertFalse(result)

        # not exist, force=False => do nothing
        result = root.toggle_attribute(xml_lang, False)
        self.assertFalse(xml_lang in root.attrib)
        self.assertFalse(result)

    def test_named_node_map(self):
        # NamedNodeMap()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')

        attributes = NamedNodeMap(root)
        self.assertEqual(0, len(attributes))
        self.assertEqual(0, attributes.length)
        self.assertEqual(0, len(root.keys()))

        # fill="none" stroke="black" stroke-width="1"
        fill = 'none'
        stroke = 'black'
        stroke_width = '1'
        attributes['fill'] = fill
        attributes['stroke'] = stroke
        attributes['stroke-width'] = stroke_width
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))
        self.assertEqual(fill, root.get('fill'))
        self.assertEqual(stroke, root.get('stroke'))
        self.assertEqual(stroke_width, root.get('stroke-width'))
        # print(attributes.keys(), attributes.values(), attributes.items())

        attributes = NamedNodeMap(root)
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))
        self.assertEqual(fill, root.get('fill'))
        self.assertEqual(stroke, root.get('stroke'))
        self.assertEqual(stroke_width, root.get('stroke-width'))

        attr = attributes['fill']
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)
        self.assertEqual('fill', attr.name)
        self.assertEqual(fill, attr.value)

        attr = attributes.get('fill', Attr(None, 'fill', ''))
        self.assertIsInstance(attr, Attr)
        self.assertEqual(fill, attr.value)
        self.assertNotEqual('', attr.value)

        attr = attributes.get('background', Attr(None, 'background', ''))
        self.assertIsInstance(attr, Attr)
        self.assertEqual('', attr.value)

        # fill="silver" stroke="black" stroke-width="1"
        fill = 'silver'
        attributes['fill'].value = fill
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))
        self.assertEqual(fill, root.get('fill'))
        self.assertEqual(stroke, root.get('stroke'))
        self.assertEqual(stroke_width, root.get('stroke-width'))

        # fill="white" stroke="black" stroke-width="1"
        fill = 'white'
        attr = Attr(None, 'fill', fill)
        attributes['fill'] = attr
        self.assertEqual(root, attr.owner_element)
        self.assertEqual('fill', attr.name)
        self.assertEqual(fill, attr.value)
        self.assertEqual(fill, root.get('fill'))

        attributes['fill'] = attr  # no effect
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))
        self.assertEqual(root, attr.owner_element)
        self.assertEqual(fill, root.get('fill'))
        self.assertEqual(stroke, root.get('stroke'))
        self.assertEqual(stroke_width, root.get('stroke-width'))

        # fill="none" stroke="red" stroke-width="2"
        fill = 'none'
        stroke = 'red'
        stroke_width = '2'
        attributes.update({
            'fill': fill,
            'stroke': stroke,
            'stroke-width': stroke_width,
        })
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))
        self.assertEqual(fill, root.get('fill'))
        self.assertEqual(stroke, root.get('stroke'))
        self.assertEqual(stroke_width, root.get('stroke-width'))

        with self.assertRaises(TypeError):
            attributes['stroke-width'] = 1

        attr = Attr(None, 'color', 'blue')  # name not matched
        with self.assertRaises(ValueError):
            attributes['fill'] = attr

        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        attr = Attr(None,
                    'fill',
                    owner_element=group)  # element already in use
        with self.assertRaises(InUseAttributeError):
            attributes['fill'] = attr
        self.assertEqual(group, attr.owner_element)

        with self.assertRaises(KeyError):
            _ = attributes['background']

        with self.assertRaises(KeyError):
            _ = attributes.pop('background')

        # remove attributes
        del attributes['fill']
        attributes['stroke'] = ''
        attributes['stroke-width'] = Attr(None, 'stroke-width', '')
        self.assertEqual(0, len(attributes))
        self.assertEqual(0, attributes.length)
        self.assertEqual(0, len(root.keys()))

    def test_named_node_map_get_named_item(self):
        # NamedNodeMap.get_named_item()
        fill = 'white'
        stroke = 'black'
        stroke_width = '1'
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg',
                                        'g',
                                        attrib={
                                            'fill': fill,
                                            'stroke': stroke,
                                            'stroke-width': stroke_width,
                                        })

        attributes = NamedNodeMap(root)
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))

        attr = attributes.get_named_item('fill')
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)
        name = 'fill'
        self.assertEqual(name, attr.name)
        self.assertEqual(fill, attr.value)
        attr.value = fill = 'none'
        self.assertEqual(fill, root.get(name))
        self.assertEqual(fill, attributes[name].value)

        attr = attributes.get_named_item('style')  # not exist
        self.assertIsNone(attr)

        name = 'background'
        background = 'gray'
        root.set(name, background)
        attr = attributes.get_named_item(name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)
        self.assertEqual(name, attr.name)
        self.assertEqual(background, attr.value)

    def test_named_node_map_get_named_item_ns(self):
        # NamedNodeMap.get_named_item_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        name = '{{{}}}{}'.format(namespace, local_name)
        value = 'ja'
        root.set(name, value)

        attributes = NamedNodeMap(root)

        attr = attributes.get_named_item_ns(namespace, local_name)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)
        self.assertEqual(name, attr.name)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(local_name, attr.local_name)
        attr.value = value = 'fr'
        self.assertEqual(value, root.get(name))

        attr = attributes.get_named_item_ns(namespace, 'space')  # not exist
        self.assertIsNone(attr)

    def test_named_node_map_item(self):
        # NamedNodeMap.item()
        fill = 'white'
        stroke = 'black'
        stroke_width = '1'
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg',
                                        'g',
                                        attrib={
                                            'fill': fill,
                                            'stroke': stroke,
                                            'stroke-width': stroke_width,
                                        })

        attributes = NamedNodeMap(root)
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))

        attr = attributes.item(0)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)
        name = attr.name
        value = attr.value
        self.assertEqual(value, root.get(name))
        attr.value = value = 'none'
        self.assertEqual(value, root.get(name))
        self.assertEqual(value, attributes[name].value)

        attr = attributes.item(1)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)

        attr = attributes.item(2)
        self.assertIsInstance(attr, Attr)
        self.assertEqual(root, attr.owner_element)

        attr = attributes.item(3)  # out of range
        self.assertIsNone(attr)

    def test_named_node_map_remove_named_item(self):
        # NamedNodeMap.remove_named_item()
        fill = 'white'
        stroke = 'black'
        stroke_width = '1'
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg',
                                        'g',
                                        attrib={
                                            'fill': fill,
                                            'stroke': stroke,
                                            'stroke-width': stroke_width,
                                        })

        attributes = NamedNodeMap(root)
        self.assertEqual(3, len(attributes))
        self.assertEqual(3, attributes.length)
        self.assertEqual(3, len(root.keys()))

        name = 'stroke'
        attr = attributes.remove_named_item(name)
        self.assertIsInstance(attr, Attr)
        self.assertIsNone(attr.owner_element)
        self.assertEqual(name, attr.name)
        self.assertEqual(stroke, attr.value)
        self.assertEqual(2, len(attributes))
        self.assertEqual(2, attributes.length)
        self.assertEqual(2, len(root.keys()))
        self.assertTrue('fill' in root.attrib)
        self.assertTrue('stroke' not in root.attrib)
        self.assertTrue('stroke-width' in root.attrib)

        # attr = attributes.remove_named_item('background')
        self.assertRaises(KeyError,
                          lambda: attributes.remove_named_item('background'))

    def test_named_node_map_remove_named_item_ns(self):
        # NamedNodeMap.remove_named_item_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        name = '{{{}}}{}'.format(namespace, local_name)
        value = 'ja'
        root.set(name, value)

        attributes = NamedNodeMap(root)
        self.assertEqual(1, len(attributes))
        self.assertEqual(1, attributes.length)
        self.assertEqual(1, len(root.keys()))

        attr = attributes.remove_named_item_ns(namespace, local_name)
        self.assertIsInstance(attr, Attr)
        self.assertIsNone(attr.owner_element)
        self.assertEqual(name, attr.name)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(0, len(attributes))
        self.assertEqual(0, attributes.length)
        self.assertEqual(0, len(root.keys()))

        # attr = attributes.remove_named_item_ns(namespace, 'space')
        self.assertRaises(KeyError,
                          lambda: attributes.remove_named_item_ns(
                              namespace, 'space'))

    def test_named_node_map_set_named_item_ns(self):
        # NamedNodeMap.set_named_item_ns()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        namespace = 'http://www.w3.org/XML/1998/namespace'
        local_name = 'lang'
        qualified_name = '{{{}}}{}'.format(namespace, local_name)
        value = 'ja'

        attributes = NamedNodeMap(root)
        self.assertEqual(0, len(attributes))
        self.assertEqual(0, attributes.length)
        self.assertEqual(0, len(root.keys()))

        attr = Attr(None, qualified_name, value)
        self.assertIsNone(attr.owner_element)
        old = attributes.set_named_item_ns(attr)
        self.assertEqual(root, attr.owner_element)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, root.get(qualified_name))
        self.assertEqual(1, len(attributes))
        self.assertEqual(1, attributes.length)
        self.assertEqual(1, len(root.keys()))
        self.assertIsNone(old)

        old_value = value
        value = 'es'
        attr = Attr(None, qualified_name, value)
        self.assertIsNone(attr.owner_element)
        old = attributes.set_named_item_ns(attr)
        self.assertEqual(root, attr.owner_element)
        self.assertEqual(qualified_name, attr.name)
        self.assertEqual(namespace, attr.namespace_uri)
        self.assertEqual(local_name, attr.local_name)
        self.assertEqual(value, attr.value)
        self.assertEqual(value, root.get(qualified_name))
        self.assertEqual(1, len(attributes))
        self.assertEqual(1, attributes.length)
        self.assertEqual(1, len(root.keys()))
        self.assertIsInstance(old, Attr)
        self.assertIsNone(old.owner_element)
        self.assertEqual(qualified_name, old.name)
        self.assertEqual(namespace, old.namespace_uri)
        self.assertEqual(local_name, old.local_name)
        self.assertEqual(old_value, old.value)

    def test_named_node_map_view(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.attributes['foo'] = '100'
        root.set('foo-bar', '200')
        root.attributes['foo-bar-baz'] = '300'

        view = root.attributes.keys()
        self.assertIsInstance(view, KeysView)

        keys = list(view)
        self.assertEqual(['foo', 'foo-bar', 'foo-bar-baz'], keys)

        view = root.attributes.values()
        self.assertIsInstance(view, ValuesView)

        values = [attr.value for attr in view]
        self.assertEqual(['100', '200', '300'], values)

        view = root.attributes.items()
        self.assertIsInstance(view, ItemsView)

        items = [(name, attr.value) for name, attr in view]
        self.assertEqual(
            [('foo', '100'), ('foo-bar', '200'), ('foo-bar-baz', '300')],
            items)

    def test_pi_addnext(self):
        # PIBase.addnext()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.addnext(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addnext(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.addnext(comment)
        self.assertEqual([parent, comment], list(root))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.addnext(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addnext(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.addnext(element)
        self.assertEqual([parent, element, comment], list(root))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.addnext(pi)
        self.assertEqual([parent, pi, element, comment], list(root))
        self.assertEqual(doc, pi.owner_document)

    def test_pi_addprevious(self):
        # PIBase.addprevious()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        doc = parser.create_svg_document()
        root = doc.document_element
        parent = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(parent.owner_document)
        root.append(parent)
        self.assertEqual(doc, parent.owner_document)

        attr = parser.create_attribute('foo')
        # parent.addprevious(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addprevious(attr))

        comment = parser.create_comment('foo')
        self.assertIsNone(comment.owner_document)
        parent.addprevious(comment)
        self.assertEqual([comment, parent], list(root))
        self.assertEqual(doc, comment.owner_document)

        doc2 = parser.create_document(svg_ns)
        # parent.addprevious(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.addprevious(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        self.assertIsNone(element.owner_document)
        parent.addprevious(element)
        self.assertEqual([comment, element, parent], list(root))
        self.assertEqual(doc, element.owner_document)

        pi = parser.create_processing_instruction('xml-stylesheet')
        self.assertIsNone(pi.owner_document)
        parent.addprevious(pi)
        self.assertEqual([comment, element, pi, parent], list(root))
        self.assertEqual(doc, pi.owner_document)

    def test_pi_append(self):
        # PIBase.append()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.append(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(attr))

        comment = parser.create_comment('foo')
        # parent.append(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(comment))

        doc = parser.create_document(svg_ns)
        # parent.append(doc)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(doc))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.append(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.append(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append(pi))

    def test_pi_append_child(self):
        # ProcessingInstruction
        # Node.append_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.append_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(attr))

        comment = parser.create_comment('foo')
        # parent.append(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(comment))

        doc = parser.create_document(svg_ns)
        # parent.append_child(doc)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(doc))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.append_child(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.append_child(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.append_child(pi))

    def test_pi_child_nodes(self):
        # Node.child_nodes
        # Node.first_child
        # Node.last_child
        # Node.next_sibling
        # Node.previous_sibling
        # Node.has_child_nodes()
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        comment = parser.create_comment('comment')
        root.addprevious(comment)
        pi = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="1.css"')
        comment.addprevious(pi)

        children = pi.child_nodes
        self.assertEqual(0, len(children))
        node = pi.first_child
        self.assertIsNone(node)
        node = pi.last_child
        self.assertIsNone(node)
        node = pi.previous_sibling
        self.assertIsNone(node)
        node = pi.next_sibling
        self.assertEqual(comment, node)
        self.assertFalse(pi.has_child_nodes())

    def test_pi_extend(self):
        # PIBase.extend()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.extend([attr])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([attr]))

        comment = parser.create_comment('foo')
        # parent.extend([comment])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([comment]))

        doc = parser.create_document(svg_ns)
        # parent.extend([doc])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([doc]))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.extend([element])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([element]))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.extend([pi])
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.extend([pi]))

    def test_pi_insert(self):
        # PIBase.insert()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.insert(1, attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, attr))

        comment = parser.create_comment('foo')
        # parent.insert(1, comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, comment))

        doc2 = parser.create_document(svg_ns)
        # parent.insert(1, doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.insert(1, element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.insert(1, pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert(1, pi))

    def test_pi_insert_before(self):
        # ProcessingInstruction
        # Node.insert_before()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.insert_before(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(attr, None))

        comment = parser.create_comment('foo')
        # parent.insert_before(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.insert_before(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.insert_before(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.insert_before(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.insert_before(pi, None))

    def test_pi_remove(self):
        # PIBase.remove()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.remove(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(attr))

        comment = parser.create_comment('foo')
        # parent.remove(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.remove(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.remove(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.remove(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove(pi))

    def test_pi_remove_child(self):
        # ProcessingInstruction
        # Node.remove_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.remove_child(attr)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(attr))

        comment = parser.create_comment('foo')
        # parent.remove_child(comment)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(comment))

        doc2 = parser.create_document(svg_ns)
        # parent.remove_child(doc2)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(doc2))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.remove_child(element)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(element))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.remove_child(pi)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.remove_child(pi))

    def test_pi_replace(self):
        # PIBase.replace()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.replace(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(attr, None))

        comment = parser.create_comment('foo')
        # parent.replace(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.replace(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.replace(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.replace(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace(pi, None))

    def test_pi_replace_child(self):
        # ProcessingInstruction
        # Node.replace_child()
        svg_ns = 'http://www.w3.org/2000/svg'
        parser = SVGParser()
        parent = parser.create_processing_instruction('xml-stylesheet')

        attr = parser.create_attribute('foo')
        # parent.replace_child(attr, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(attr, None))

        comment = parser.create_comment('foo')
        # parent.replace_child(comment, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(comment, None))

        doc2 = parser.create_document(svg_ns)
        # parent.replace_child(doc2, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(doc2, None))

        element = parser.create_element_ns(svg_ns, 'svg')
        # parent.replace_child(element, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(element, None))

        pi = parser.create_processing_instruction('xml-stylesheet')
        # parent.replace_child(pi, None)
        self.assertRaises(HierarchyRequestError,
                          lambda: parent.replace_child(pi, None))


if __name__ == '__main__':
    unittest.main()
