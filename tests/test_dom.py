#!/usr/bin/env python3

import sys
import unittest
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
        # Attr.append_child()
        parser = SVGParser()
        node = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        attr = parser.create_attribute('fill')
        self.assertRaises(ValueError, lambda: attr.append_child(node))

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
        # Attr.insert_before()
        parser = SVGParser()
        node = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        attr = parser.create_attribute('fill')
        self.assertRaises(ValueError, lambda: attr.insert_before(node, None))

    def test_attr_remove_child(self):
        # Attr.remove_child()
        parser = SVGParser()
        node = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        attr = parser.create_attribute('fill')
        self.assertRaises(ValueError, lambda: attr.remove_child(node))

    def test_attr_replace_child(self):
        # Attr.replace_child()
        parser = SVGParser()
        node = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        attr = parser.create_attribute('fill')
        self.assertRaises(ValueError, lambda: attr.replace_child(node, None))

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
        # Comment.addnext()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        self.assertIsNone(c1.owner_document)
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        self.assertIsNone(group.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        c0 = doc.create_comment('#0')
        root.append(c0)

        c0.addnext(c1)
        self.assertEqual(doc, c1.owner_document)

        c0.addnext(group)
        self.assertEqual(doc, group.owner_document)

    def test_comment_addprevious(self):
        # Comment.addprevious()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        self.assertIsNone(c1.owner_document)
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        self.assertIsNone(group.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        c0 = doc.create_comment('#0')
        root.append(c0)

        c0.addprevious(c1)
        self.assertEqual(doc, c1.owner_document)

        c0.addprevious(group)
        self.assertEqual(doc, group.owner_document)

    def test_comment_append_child(self):
        # Comment.append_child()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        c2 = parser.create_comment('#2')

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)

        doc.append(c1)
        self.assertRaises(ValueError,
                          lambda: c1.append_child(c2))

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
        # Comment.extend()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        c2 = parser.create_comment('#2')
        c3 = parser.create_comment('#3')
        self.assertIsNone(c1.owner_document)
        self.assertIsNone(c2.owner_document)
        self.assertIsNone(c3.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        c0 = doc.create_comment('#0')
        root.append(c0)
        c0.extend([c1, c2, c3])  # no effect, no error
        self.assertEqual(doc, c1.owner_document)
        self.assertEqual(doc, c2.owner_document)
        self.assertEqual(doc, c3.owner_document)

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
        # Comment.remove()
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        c0 = doc.create_comment('#0')
        root.append(c0)

        self.assertRaises(ValueError,
                          lambda: c0.remove(root))

    def test_comment_replace(self):
        # Comment.replace()
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        c0 = doc.create_comment('#0')
        root.append(c0)
        c1 = doc.create_comment('#1')
        c2 = doc.create_comment('#2')

        self.assertRaises(ValueError,
                          lambda: c0.replace(c1, c2))

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
        # Element.addnext()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        self.assertIsNone(c1.owner_document)
        style = parser.create_element_ns('http://www.w3.org/2000/svg', 'style')
        self.assertIsNone(style.owner_document)
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'group')
        path = parser.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertIsNone(group.owner_document)
        self.assertIsNone(path.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        title = doc.create_element_ns('http://www.w3.org/2000/svg', 'title')
        root.append(title)
        desc = doc.create_element_ns('http://www.w3.org/2000/svg', 'desc')
        root.append(desc)

        title.addnext(c1)
        self.assertEqual(doc, c1.owner_document)

        desc.addnext(style)
        self.assertEqual(doc, style.owner_document)

        # <svg>
        #   <title/>
        #   <!--#1-->
        #   <desc/>
        #   <style/>
        #   <group><path/></group>
        # </svg>
        style.addnext(group)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

        nodes = [e for e in root]
        self.assertEqual([title, c1, desc, style, group], nodes)

    def test_element_addprevious(self):
        # Element.addprevious()
        parser = SVGParser()
        p1 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="1.css"')
        self.assertIsNone(p1.owner_document)
        c1 = parser.create_comment('#1')
        self.assertIsNone(c1.owner_document)
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'group')
        path = parser.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertIsNone(group.owner_document)
        self.assertIsNone(path.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        rect = doc.create_element_ns('http://www.w3.org/2000/svg', 'rect')
        root.append(rect)

        root.addprevious(p1)
        self.assertEqual(doc, p1.owner_document)

        rect.addprevious(group)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

        # <?xml-stylesheet href="1.css"?>
        # <svg>
        #   <!--#1-->
        #   <group><path/></group>
        #   <rect/>
        # </svg>
        group.addprevious(c1)
        self.assertEqual(doc, c1.owner_document)
        # print(doc.tostring())

    def test_element_append(self):
        # Element.append()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'group')
        path = parser.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertIsNone(c1.owner_document)
        self.assertIsNone(group.owner_document)
        self.assertIsNone(path.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)

        root.append(c1)
        self.assertEqual(doc, c1.owner_document)

        # <svg>
        #   <!--#1-->
        #   <group><path/></group>
        # </svg>
        root.append(group)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)
        # print(doc.tostring())

    def test_element_append_child(self):
        # Element.append_child()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'group')
        self.assertIsNone(c1.owner_document)
        self.assertIsNone(group.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)

        node = root.append_child(c1)
        self.assertEqual(c1, node)
        self.assertEqual(doc, c1.owner_document)

        node = root.append_child(group)
        self.assertEqual(group, node)
        self.assertEqual(doc, group.owner_document)

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
        # Element.extend()
        parser = SVGParser()
        desc = parser.create_element_ns('http://www.w3.org/2000/svg', 'desc')
        comment = parser.create_comment('comment')
        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'group')
        path = parser.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertIsNone(desc.owner_document)
        self.assertIsNone(comment.owner_document)
        self.assertIsNone(group.owner_document)
        self.assertIsNone(path.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertEqual(doc, root.owner_document)
        doc.append(root)

        root.extend([desc, comment, group])
        self.assertEqual(doc, desc.owner_document)
        self.assertEqual(doc, comment.owner_document)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)
        # print(doc.tostring())

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
        # Element.insert()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        style = parser.create_element_ns('http://www.w3.org/2000/svg', 'style')
        self.assertIsNone(c1.owner_document)
        self.assertIsNone(style.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'group')
        root.append(group)

        root.insert(0, style)
        self.assertEqual(doc, style.owner_document)

        root.insert(0, c1)
        self.assertEqual(doc, c1.owner_document)

    def test_element_insert_before(self):
        # Element.insert_before()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        style = parser.create_element_ns('http://www.w3.org/2000/svg', 'style')
        self.assertIsNone(c1.owner_document)
        self.assertIsNone(style.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'group')
        root.append(group)

        node = root.insert_before(style, group)
        self.assertEqual(style, node)
        self.assertEqual(doc, style.owner_document)

        node = root.insert_before(c1, style)
        self.assertEqual(c1, node)
        self.assertEqual(doc, c1.owner_document)

        children = [e for e in root]
        self.assertEqual([c1, style, group], children)
        # print(doc.tostring())

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

    def test_element_remove(self):
        # Element.remove()
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'group')
        root.append(group)
        path = doc.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertTrue(group in root)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

        root.remove(group)
        self.assertFalse(group in root)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

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
        # Element.remove_child()
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'group')
        root.append(group)
        path = doc.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertTrue(group in root)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

        node = root.remove_child(group)
        self.assertEqual(group, node)
        self.assertTrue(group not in root)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

    def test_element_replace(self):
        # Element.replace()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        self.assertIsNone(c1.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'group')
        root.append(group)
        path = doc.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertTrue(group in root)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

        root.replace(group, c1)
        self.assertTrue(c1 in root)
        self.assertTrue(group not in root)
        self.assertEqual(doc, c1.owner_document)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

    def test_element_replace_child(self):
        # Element.replace_child()
        parser = SVGParser()
        c1 = parser.create_comment('#1')
        self.assertIsNone(c1.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        group = doc.create_element_ns('http://www.w3.org/2000/svg', 'group')
        root.append(group)
        path = doc.create_element_ns('http://www.w3.org/2000/svg', 'path')
        group.append(path)
        self.assertTrue(group in root)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

        node = root.replace_child(c1, group)
        self.assertEqual(c1, node)
        self.assertTrue(c1 in root)
        self.assertTrue(group not in root)
        self.assertEqual(doc, c1.owner_document)
        self.assertEqual(doc, group.owner_document)
        self.assertEqual(doc, path.owner_document)

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

        def _set_value(d, k, v):
            d[k] = v

        self.assertRaises(TypeError,
                          lambda: _set_value(attributes, 'stroke-width', 1))

        attr = Attr(None, 'color', 'blue')  # name not matched
        self.assertRaises(ValueError,
                          lambda: _set_value(attributes, 'fill', attr))

        group = parser.create_element_ns('http://www.w3.org/2000/svg', 'g')
        attr = Attr(None,
                    'fill',
                    owner_element=group)  # element already in use
        self.assertRaises(ValueError,
                          lambda: _set_value(attributes, 'fill', attr))
        self.assertEqual(group, attr.owner_element)

        self.assertRaises(KeyError,
                          lambda: attributes['background'])

        self.assertRaises(KeyError,
                          lambda: attributes.pop('background'))

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

    def test_pi_addnext(self):
        # ProcessingInstruction.addnext()
        parser = SVGParser()
        p1 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="1.css"')
        self.assertIsNone(p1.owner_document)
        c1 = parser.create_comment('c1')
        self.assertIsNone(c1.owner_document)

        # <?xml-stylesheet href="0.css"?>
        # <svg>
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        p0 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="0.css"')
        doc.insert_before(p0, root)

        # <?xml-stylesheet href="0.css"?>
        # <?xml-stylesheet href="1.css"?>
        # <svg>
        p0.addnext(p1)
        self.assertEqual(doc, p1.owner_document)

        # <?xml-stylesheet href="0.css"?>
        # <?xml-stylesheet href="1.css"?>
        # <!--c1-->
        # <svg>
        p1.addnext(c1)
        self.assertEqual(doc, c1.owner_document)

    def test_pi_addprevious(self):
        # ProcessingInstruction.addprevious()
        parser = SVGParser()
        p0 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="0.css"')
        self.assertIsNone(p0.owner_document)
        p1 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="1.css"')
        self.assertIsNone(p1.owner_document)

        # <?xml-stylesheet href="1.css"?>
        # <svg>
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        doc.insert_before(p1, root)
        self.assertEqual(doc, p1.owner_document)

        # <?xml-stylesheet href="0.css"?>
        # <?xml-stylesheet href="1.css"?>
        # <svg>
        p1.addprevious(p0)
        self.assertEqual(doc, p0.owner_document)

    def test_pi_append_child(self):
        # ProcessingInstruction.append_child()
        parser = SVGParser()
        p1 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="1.css"')

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        p0 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="0.css"')
        doc.insert_before(p0, root)
        # print(doc.tostring())

        self.assertRaises(ValueError,
                          lambda: p0.append_child(p1))

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
        # ProcessingInstruction.extend()
        parser = SVGParser()
        p1 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="1.css"')
        p2 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="2.css"')
        p3 = parser.create_processing_instruction('xml-stylesheet',
                                                  'href="3.css"')
        self.assertIsNone(p1.owner_document)
        self.assertIsNone(p2.owner_document)
        self.assertIsNone(p3.owner_document)

        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        p0 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="0.css"')
        doc.insert_before(p0, root)
        p0.extend([p1, p2, p3])  # no effect, no error
        self.assertEqual(doc, p1.owner_document)
        self.assertEqual(doc, p2.owner_document)
        self.assertEqual(doc, p3.owner_document)
        # print(doc.tostring())

    def test_pi_remove(self):
        # ProcessingInstruction.remove()
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        p0 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="0.css"')
        doc.insert_before(p0, root)

        self.assertRaises(ValueError,
                          lambda: p0.remove(root))

    def test_pi_replace(self):
        # ProcessingInstruction.replace()
        doc = window.document
        root = doc.create_element_ns('http://www.w3.org/2000/svg', 'svg')
        doc.append(root)
        p0 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="0.css"')
        doc.insert_before(p0, root)
        p1 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="1.css"')
        p2 = doc.create_processing_instruction('xml-stylesheet',
                                               'href="2.css"')

        self.assertRaises(ValueError,
                          lambda: p0.replace(p1, p2))


if __name__ == '__main__':
    unittest.main()
