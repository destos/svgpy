#!/usr/bin/env python3


import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy.utils import CaseInsensitiveMapping


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


if __name__ == '__main__':
    unittest.main()
