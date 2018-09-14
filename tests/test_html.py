#!/usr/bin/env python3

import logging
import os
import sys
import tempfile
import unittest

sys.path.extend(['.', '..'])

from svgpy import DOMTokenList, Element, window
from svgpy.css import CSSStyleSheet
from svgpy.element import HTMLLinkElement

# LOGGING_LEVEL = logging.DEBUG
LOGGING_LEVEL = logging.WARNING

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


class HTMLTestCase(unittest.TestCase):
    def setUp(self):
        logging_level = int(os.getenv('LOGGING_LEVEL', str(LOGGING_LEVEL)))
        filename = os.path.join(tempfile.gettempdir(),
                                '{}.log'.format(__name__))
        fmt = '%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(message)s'
        logging.basicConfig(level=logging_level,
                            filename=filename,
                            format=fmt)
        window.location = 'about:blank'

    def test_link(self):
        document = window.document
        root = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'svg')
        document.append(root)

        link = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'link')
        self.assertIsInstance(link, HTMLLinkElement)
        root.append(link)

        href = ''
        # cross_origin = ''
        rel = ''
        as_ = ''
        media = ''
        integrity = ''
        hreflang = ''
        type_ = ''
        referrer_policy = ''
        title = ''
        self.assertEqual(href, link.href)
        self.assertIsNone(link.cross_origin)
        self.assertEqual(rel, link.rel)
        self.assertEqual(as_, link.as_)
        rel_list = link.rel_list
        self.assertIsInstance(rel_list, DOMTokenList)
        self.assertEqual(0, len(rel_list))
        self.assertEqual(media, link.media)
        self.assertEqual(integrity, link.integrity)
        self.assertEqual(hreflang, link.hreflang)
        self.assertEqual(type_, link.type)
        sizes = link.sizes
        self.assertIsInstance(sizes, DOMTokenList)
        self.assertEqual(0, len(sizes))
        self.assertEqual(referrer_policy, link.referrer_policy)
        sheet = link.sheet
        self.assertIsNone(sheet)
        self.assertEqual(title, link.title)

        href = 'svg/ny1.css'
        link.href = href
        cross_origin = 'anonymous'
        link.cross_origin = cross_origin
        rel = 'preload'
        link.rel = rel
        as_ = 'style'
        link.as_ = as_
        media = 'screen'
        link.media = media
        integrity = '[base64-encoded hash]'
        link.integrity = integrity
        hreflang = 'en'
        link.hreflang = hreflang
        type_ = 'text/css'
        link.type = type_
        referrer_policy = 'no-referrer'
        link.referrer_policy = referrer_policy
        title = 'test'
        link.title = title
        self.assertEqual(href, link.href)
        self.assertEqual(href, link.get('href'))
        self.assertEqual(cross_origin, link.cross_origin)
        self.assertEqual(cross_origin, link.get('crossorigin'))
        self.assertEqual(rel, link.rel)
        self.assertEqual(rel, link.get('rel'))
        self.assertEqual(as_, link.as_)
        self.assertEqual(as_, link.get('as'))
        self.assertEqual(media, link.media)
        self.assertEqual(media, link.get('media'))
        self.assertEqual(integrity, link.integrity)
        self.assertEqual(integrity, link.get('integrity'))
        self.assertEqual(hreflang, link.hreflang)
        self.assertEqual(hreflang, link.get('hreflang'))
        self.assertEqual(type_, link.type)
        self.assertEqual(type_, link.get('type'))
        self.assertEqual(referrer_policy, link.referrer_policy)
        self.assertEqual(referrer_policy, link.get('referrerpolicy'))
        sheet = link.sheet
        self.assertIsInstance(sheet, CSSStyleSheet)
        self.assertTrue(len(sheet.css_rules) > 0)
        self.assertEqual(title, link.title)
        self.assertEqual(title, link.get('title'))

    def test_link_rel_list(self):
        document = window.document
        link = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'link')
        rel = 'alternate stylesheet'
        link.set('rel', rel)
        self.assertEqual(rel, link.rel)
        self.assertEqual(rel, link.get('rel'))

        rel_list = link.rel_list
        self.assertIsInstance(rel_list, DOMTokenList)
        self.assertEqual(2, len(rel_list))
        self.assertEqual('alternate', rel_list[0])
        self.assertEqual('stylesheet', rel_list[1])

        rel_list.remove('alternate')
        self.assertEqual(1, len(rel_list))
        self.assertEqual('stylesheet', rel_list[0])
        rel = 'stylesheet'
        self.assertEqual(rel, rel_list.value)
        self.assertEqual(rel, link.rel)
        self.assertEqual(rel, link.get('rel'))

    def test_link_sizes(self):
        document = window.document
        link = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'link')
        sizes = '32x32 64x64'
        link.set('sizes', sizes)
        self.assertEqual(sizes, link.get('sizes'))

        size_list = link.sizes
        self.assertIsInstance(size_list, DOMTokenList)
        self.assertEqual(2, len(size_list))
        self.assertEqual('32x32', size_list[0])
        self.assertEqual('64x64', size_list[1])

        size_list.add('128x128')
        self.assertEqual(3, len(size_list))
        self.assertEqual('32x32', size_list[0])
        self.assertEqual('64x64', size_list[1])
        self.assertEqual('128x128', size_list[2])
        sizes = '32x32 64x64 128x128'
        self.assertEqual(sizes, size_list.value)
        self.assertEqual(sizes, link.get('sizes'))


if __name__ == '__main__':
    unittest.main()
