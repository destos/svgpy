#!/usr/bin/env python3


import sys
import unittest

sys.path.extend(['.', '..'])

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

    def test_qualified_name(self):
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

        # Invalid character
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, 'lang\t'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, 'lang\n'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, 'lang\f'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, 'lang\r'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(None, 'lang '))

        self.assertRaises(ValueError,
                          lambda: QualifiedName('\t', 'lang'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName('\n', 'lang'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName('\f', 'lang'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName('\r', 'lang'))
        self.assertRaises(ValueError,
                          lambda: QualifiedName(' ', 'lang'))

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
        self.assertRaises(ValueError,
                          lambda: QualifiedName(svg_namespace, qualified_name))


if __name__ == '__main__':
    unittest.main()
