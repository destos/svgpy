#!/usr/bin/env python3


import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import SVGParser
from svgpy.exception import InvalidCharacterError, NamespaceError
from svgpy.utils import CaseInsensitiveMapping, QualifiedName


class UtilsTestCase(unittest.TestCase):
    def test_case_insensitive_mapping(self):
        # CaseInsensitiveMapping()
        d = CaseInsensitiveMapping()
        self.assertEqual(0, len(d))

        key = 'Content-Type'
        value = 'image/svg+xml'
        d[key] = value
        self.assertEqual(1, len(d))
        self.assertEqual(value, d[key.upper()])
        self.assertEqual(value, d[key.lower()])
        self.assertTrue(key in d)
        self.assertTrue(key.upper() in d)
        self.assertTrue(key.lower() in d)
        # print(d.keys(), d.values(), d.items())

        del d[key]
        self.assertEqual(0, len(d))

        d = CaseInsensitiveMapping({key: value})
        self.assertEqual(1, len(d))
        self.assertEqual(value, d[key.upper()])
        self.assertEqual(value, d[key.lower()])
        self.assertTrue(key in d)
        self.assertTrue(key.upper() in d)
        self.assertTrue(key.lower() in d)

        del d[key.upper()]
        self.assertEqual(0, len(d))

        key = 'Connection'
        value = 'keep-alive'
        d = CaseInsensitiveMapping(Connection=value)
        self.assertEqual(1, len(d))
        self.assertEqual(value, d[key.upper()])
        self.assertEqual(value, d[key.lower()])
        self.assertTrue(key in d)
        self.assertTrue(key.upper() in d)
        self.assertTrue(key.lower() in d)

        del d[key.lower()]
        self.assertEqual(0, len(d))

        key = None  # non-string
        value = 'http://www.w3.org/2000/svg'
        d = CaseInsensitiveMapping([(key, value)])
        self.assertEqual(1, len(d))
        self.assertEqual(value, d[key])
        self.assertTrue(key in d)

        del d[key]
        self.assertEqual(0, len(d))

    def test_qualified_name01(self):
        # QualifiedName()
        svg_namespace = 'http://www.w3.org/2000/svg'
        xml_namespace = 'http://www.w3.org/XML/1998/namespace'

        q_name = QualifiedName(None, 'lang')
        self.assertIsNone(q_name.namespace_uri)
        self.assertEqual('lang', q_name.name)
        self.assertEqual('lang', q_name.local_name)

        q_name = QualifiedName('', 'lang')
        self.assertIsNone(q_name.namespace_uri)
        self.assertEqual('lang', q_name.name)
        self.assertEqual('lang', q_name.local_name)

        qualified_name = '{{{}}}{}'.format(xml_namespace, 'lang')
        q_name = QualifiedName(xml_namespace, 'lang')
        self.assertEqual(xml_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('lang', q_name.local_name)

        qualified_name = '{{{}}}{}'.format(xml_namespace, 'lang')
        q_name = QualifiedName(None, qualified_name)
        self.assertEqual(xml_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('lang', q_name.local_name)

        qualified_name = '{{{}}}{}'.format(xml_namespace, 'lang')
        q_name = QualifiedName('', qualified_name)
        self.assertEqual(xml_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('lang', q_name.local_name)

        qualified_name = '{{{}}}{}'.format(xml_namespace, 'lang')
        q_name = QualifiedName(xml_namespace, qualified_name)
        self.assertEqual(xml_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('lang', q_name.local_name)

    def test_qualified_name02(self):
        # QualifiedName()

        # Invalid character
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName(None, 'lang\t'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName(None, 'lang\n'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName(None, 'lang\f'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName(None, 'lang\r'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName(None, 'lang '))

        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName('\t', 'lang'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName('\n', 'lang'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName('\f', 'lang'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName('\r', 'lang'))
        self.assertRaises(InvalidCharacterError,
                          lambda: QualifiedName(' ', 'lang'))

    def test_qualified_name03(self):
        # QualifiedName()
        svg_namespace = 'http://www.w3.org/2000/svg'
        xml_namespace = 'http://www.w3.org/XML/1998/namespace'

        # Missing namespace
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, '{}lang'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(xml_namespace, '{}lang'))

        # Missing local name
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, ''))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(xml_namespace, ''))
        qualified_name = '{{{}}}{}'.format(xml_namespace, '')
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, qualified_name))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(xml_namespace, qualified_name))

        # Namespace did not match
        qualified_name = '{{{}}}{}'.format(xml_namespace, 'lang')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName(svg_namespace, qualified_name))

    def test_qualified_name04(self):
        # QualifiedName()
        svg_namespace = 'http://www.w3.org/2000/svg'
        xml_namespace = 'http://www.w3.org/XML/1998/namespace'
        xmlns_namespace = 'http://www.w3.org/2000/xmlns/'

        q_name = QualifiedName(xml_namespace, 'xml:lang')
        qualified_name = '{{{}}}{}'.format(xml_namespace, 'lang')
        self.assertEqual(xml_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('lang', q_name.local_name)

        # prefix is empty string
        # q_name = QualifiedName(xml_namespace, ':lang')
        self.assertRaises(ValueError,
                          lambda: QualifiedName(xml_namespace, ':lang'))

        # prefix is non-null and namespace is null
        # q_name = QualifiedName('', 'xml:lang')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName('', 'xml:lang'))
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName(None, 'xml:lang'))

        # prefix is "xml" and namespace is not the XML namespace
        # q_name = QualifiedName(svg_namespace, 'xml:lang')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName(svg_namespace, 'xml:lang'))

        q_name = QualifiedName(xmlns_namespace, 'xmlns:foo')
        qualified_name = '{{{}}}{}'.format(xmlns_namespace, 'foo')
        self.assertEqual(xmlns_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('foo', q_name.local_name)

        # prefix is "xmlns" and namespace is not the XMLNS namespace
        # q_name = QualifiedName(xml_namespace, 'xmlns:foo')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName(xml_namespace, 'xmlns:foo'))

        # namespace is the XMLNS namespace and neither qualifiedName nor
        # prefix is "xmlns"
        # q_name = QualifiedName(xmlns_namespace, 'xml:lang')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName(xmlns_namespace, 'xml:lang'))

    def test_qualified_name05(self):
        # QualifiedName()
        svg_namespace = 'http://www.w3.org/2000/svg'
        custom_namespace = 'http://www.example.com/'
        custom_prefix = 'custom'
        parser = SVGParser()
        root = parser.create_element_ns(
            svg_namespace,
            'root',
            nsmap={
                custom_prefix: custom_namespace,
            })

        qualified_name = '{{{}}}{}'.format(custom_namespace, 'foo')
        q_name = QualifiedName(custom_namespace, 'foo')
        self.assertEqual(custom_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('foo', q_name.local_name)

        q_name = QualifiedName(custom_namespace, qualified_name)
        self.assertEqual(custom_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('foo', q_name.local_name)

        # q_name = QualifiedName('', custom_prefix + ':foo')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName('',
                                                custom_prefix + ':foo'))

        # q_name = QualifiedName(custom_namespace,
        #                        custom_prefix + ':foo')
        self.assertRaises(NamespaceError,
                          lambda: QualifiedName(custom_namespace,
                                                custom_prefix + ':foo'))

        q_name = QualifiedName(custom_namespace,
                               custom_prefix + ':foo',
                               nsmap=root.nsmap)
        self.assertEqual(custom_namespace, q_name.namespace_uri)
        self.assertEqual(qualified_name, q_name.name)
        self.assertEqual('foo', q_name.local_name)


if __name__ == '__main__':
    unittest.main()
