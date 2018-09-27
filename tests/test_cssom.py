#!/usr/bin/env python3


import logging
import os
import sys
import tempfile
import unittest

sys.path.extend(['.', '..'])

from svgpy import SVGParser, window
from svgpy.css import CSSFontFaceRule, CSSFontFeatureValuesRule, \
    CSSImportRule, CSSMediaRule, CSSNamespaceRule, CSSParser, CSSRule, \
    CSSStyleDeclaration, CSSStyleRule, CSSStyleSheet, MediaList, StyleSheet

# LOGGING_LEVEL = logging.DEBUG
LOGGING_LEVEL = logging.WARNING

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


class CSSOMTestCase(unittest.TestCase):
    """Important: Run the following command before this test.;
    'cd tests && python3 -m http.server 8000'
    """

    def setUp(self):
        logging_level = int(os.getenv('LOGGING_LEVEL', str(LOGGING_LEVEL)))
        filename = os.path.join(tempfile.gettempdir(),
                                '{}.log'.format(__name__))
        fmt = '%(asctime)s|%(levelname)s|%(name)s|%(funcName)s|%(message)s'
        logging.basicConfig(level=logging_level,
                            filename=filename,
                            format=fmt)
        window.location = 'about:blank'

    def test_css_font_face_rule(self):
        stylesheet = '''
        /* bold face of Gentium */
        @font-face {
            font-family: MyGentium;
            src: local(Gentium Bold),    /* full font name */
            local(Gentium-Bold),    /* Postscript name */
            url(GentiumBold.woff);  /* otherwise, download it */
            font-weight: bold;
        }
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(1, len(rules))
        rule = rules[0]
        self.assertIsInstance(rule, CSSFontFaceRule)
        self.assertEqual(CSSRule.FONT_FACE_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        style = rule.style
        self.assertIsInstance(style, CSSStyleDeclaration)
        self.assertEqual(3, style.length)
        self.assertEqual('MyGentium', style.get_property_value('font-family'))
        self.assertEqual('', style.get_property_priority('font-family'))
        expected = \
            'local(Gentium Bold), local(Gentium-Bold), url(GentiumBold.woff)'
        self.assertEqual(expected, style.get_property_value('src'))
        self.assertEqual('', style.get_property_priority('src'))
        self.assertEqual('bold', style.get_property_value('font-weight'))
        self.assertEqual('', style.get_property_priority('font-weight'))

    def test_css_font_feature_values_rule(self):
        stylesheet = '''
        @font-feature-values Bongo {
          @annotation { boxed: 1; circled: 4; }
          @character-variant { alpha-2: 1 2; }   /* implies cv01 = 2 */
          @character-variant { beta-3: 2 3; }    /* implies cv02 = 3 */
          @character-variant { gamma: 12; }      /* implies cv12 = 1 */
          @ornaments { fleurons: 2; }
          @styleset { double-W: 14; sharp-terminals: 16 1; }
          @stylistic { salt: 2; }
          @swash { ornate: 1; }
          @swash { double-loops: 1; }
        }
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(1, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSFontFeatureValuesRule)
        self.assertEqual(CSSRule.FONT_FEATURE_VALUES_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertEqual('Bongo', rule.font_family)
        self.assertEqual(2, len(rule.annotation))
        self.assertEqual([1], rule.annotation['boxed'])
        self.assertEqual([4], rule.annotation['circled'])
        self.assertEqual(3, len(rule.character_variant))
        self.assertEqual([1, 2], rule.character_variant['alpha-2'])
        self.assertEqual([2, 3], rule.character_variant['beta-3'])
        self.assertEqual([12], rule.character_variant['gamma'])
        self.assertEqual(1, len(rule.ornaments))
        self.assertEqual([2], rule.ornaments['fleurons'])
        self.assertEqual(2, len(rule.styleset))
        self.assertEqual([14], rule.styleset['double-W'])
        self.assertEqual([16, 1], rule.styleset['sharp-terminals'])
        self.assertEqual(1, len(rule.stylistic))
        self.assertEqual([2], rule.stylistic['salt'])
        self.assertEqual(2, len(rule.swash))
        self.assertEqual([1], rule.swash['ornate'])
        self.assertEqual([1], rule.swash['double-loops'])

    def test_css_import_rule01(self):
        # download css style sheet
        # logging.getLogger(__name__).propagate = False
        stylesheet = '''
        @import url("print.css") print;
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(1, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSImportRule)
        self.assertEqual(CSSRule.IMPORT_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertIsNotNone(rule.href)
        self.assertEqual(1, rule.media.length)
        self.assertEqual('print', rule.media.item(0))
        sheet = rule.style_sheet
        self.assertIsInstance(sheet, CSSStyleSheet)
        self.assertEqual(rule, sheet.owner_rule)
        self.assertEqual(0, len(sheet.css_rules))

        stylesheet = '''
        @import url(svg/style8.css);
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(1, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSImportRule)
        self.assertEqual(CSSRule.IMPORT_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertIsNotNone(rule.href)
        # self.assertEqual('http://localhost:8000/svg/style8.css', rule.href)
        self.assertEqual(0, rule.media.length)

        sheet = rule.style_sheet
        self.assertIsInstance(sheet, CSSStyleSheet)
        self.assertEqual(rule, sheet.owner_rule)
        self.assertEqual(15, len(sheet.css_rules),
                         msg='http server may not be working.')

        rule = sheet.css_rules[14]
        self.assertEqual(CSSRule.STYLE_RULE, rule.type)
        self.assertEqual('#inner-petals .segment:hover > .segment-edge',
                         rule.selector_text)
        style = rule.style
        self.assertEqual(1, style.length)
        self.assertEqual('green', style['stroke'])
        self.assertEqual('', style.get_property_priority('stroke'))

    def test_css_import_rule02(self):
        # local css style sheet
        stylesheet = '''
        @import "print.css" print;
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(1, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSImportRule)
        self.assertEqual(CSSRule.IMPORT_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertIsNotNone(rule.href)
        self.assertEqual(1, rule.media.length)
        self.assertEqual('print', rule.media.item(0))
        sheet = rule.style_sheet
        self.assertIsInstance(sheet, CSSStyleSheet)
        self.assertEqual(rule, sheet.owner_rule)
        self.assertEqual(0, len(sheet.css_rules))

        stylesheet = '''
        @import "svg/style8.css";
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(1, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSImportRule)
        self.assertEqual(CSSRule.IMPORT_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertIsNotNone(rule.href)
        self.assertEqual(0, rule.media.length)

        sheet = rule.style_sheet
        self.assertIsInstance(sheet, CSSStyleSheet)
        self.assertEqual(rule, sheet.owner_rule)
        self.assertEqual(15, len(sheet.css_rules))

        rule = sheet.css_rules[14]
        self.assertEqual(CSSRule.STYLE_RULE, rule.type)
        self.assertEqual('#inner-petals .segment:hover > .segment-edge',
                         rule.selector_text)
        style = rule.style
        self.assertEqual(1, style.length)
        self.assertEqual('green', style['stroke'])
        self.assertEqual('', style.get_property_priority('stroke'))

    def test_css_media_rule(self):
        stylesheet = '''
        @media print { /* rule (1) */
          /* hide navigation controls when printing */
          #navigation { display: none }
          @media (max-width: 12cm) { /* rule (2) */
            /* keep notes in flow when printing to narrow pages */
            .note { float: none }
          }
        }
        @media screen and (min-width: 35em),
               print and (min-width: 40em) {
          #section_navigation { float: left; width: 10em; }
        }
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(2, len(rules))

        # '@media print {...}'
        rule = rules[0]
        self.assertIsInstance(rule, CSSMediaRule)
        self.assertEqual(CSSRule.MEDIA_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertEqual(1, rule.media.length)
        self.assertEqual('print', rule.media.item(0))
        self.assertEqual('print', rule.condition_text)
        self.assertEqual(2, len(rule.css_rules))

        # '#navigation {...}'
        style_rule = rule.css_rules[0]
        self.assertEqual(CSSRule.STYLE_RULE, style_rule.type)
        self.assertEqual(rule, style_rule.parent_rule)
        self.assertIsNone(style_rule.parent_style_sheet)
        self.assertEqual('#navigation',
                         style_rule.selector_text)
        style = style_rule.style
        self.assertEqual(1, style.length)
        self.assertEqual('none', style['display'])
        self.assertEqual('', style.get_property_priority('display'))

        # '@media (max-width: 12cm) {...}'
        media_rule = rule.css_rules[1]
        self.assertEqual(CSSRule.MEDIA_RULE, media_rule.type)
        self.assertEqual(rule, media_rule.parent_rule)
        self.assertIsNone(media_rule.parent_style_sheet)
        self.assertEqual(1, media_rule.media.length)
        self.assertEqual('(max-width: 12cm)', media_rule.media.item(0))
        self.assertEqual('(max-width: 12cm)', media_rule.condition_text)
        self.assertEqual(1, len(media_rule.css_rules))

        # '.note {...}'
        style_rule = media_rule.css_rules[0]
        self.assertEqual(CSSRule.STYLE_RULE, style_rule.type)
        self.assertEqual(media_rule, style_rule.parent_rule)
        self.assertIsNone(style_rule.parent_style_sheet)
        self.assertEqual('.note',
                         style_rule.selector_text)
        style = style_rule.style
        self.assertEqual(1, style.length)
        self.assertEqual('none', style['float'])
        self.assertEqual('', style.get_property_priority('float'))

        # '@media screen and (min-width: 35em), print and (min-width: 40em)
        # {...}'
        rule = rules[1]
        self.assertIsInstance(rule, CSSMediaRule)
        self.assertIsInstance(rule, CSSMediaRule)
        self.assertEqual(CSSRule.MEDIA_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertEqual(2, rule.media.length)
        self.assertEqual('screen and (min-width: 35em)',
                         rule.media.item(0))
        self.assertEqual('print and (min-width: 40em)',
                         rule.media.item(1))
        self.assertEqual(
            "screen and (min-width: 35em), print and (min-width: 40em)",
            rule.condition_text)
        self.assertEqual(1, len(rule.css_rules))

        # '#section_navigation {...}'
        style_rule = rule.css_rules[0]
        self.assertEqual(CSSRule.STYLE_RULE, style_rule.type)
        self.assertEqual(rule, style_rule.parent_rule)
        self.assertIsNone(style_rule.parent_style_sheet)
        self.assertEqual('#section_navigation',
                         style_rule.selector_text)
        style = style_rule.style
        self.assertEqual(2, style.length)
        self.assertEqual('left', style['float'])
        self.assertEqual('', style.get_property_priority('float'))
        self.assertEqual('10em', style['width'])
        self.assertEqual('', style.get_property_priority('width'))

    def test_css_namespace_rule(self):
        stylesheet = '''
        @namespace url(http://www.w3.org/2000/svg);
        @namespace xml url(http://www.w3.org/XML/1998/namespace);
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(2, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSNamespaceRule)
        self.assertEqual(CSSRule.NAMESPACE_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertEqual('', rule.prefix)
        self.assertEqual('http://www.w3.org/2000/svg',
                         rule.namespace_uri)

        rule = rules[1]
        self.assertIsInstance(rule, CSSNamespaceRule)
        self.assertEqual(CSSRule.NAMESPACE_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        self.assertEqual('xml', rule.prefix)
        self.assertEqual('http://www.w3.org/XML/1998/namespace',
                         rule.namespace_uri)

    def test_css_style_rule(self):
        stylesheet = '''
        *:not(svg),
        *:not(foreignObject) > svg {
          transform-origin: 0 0;
        }
        :host(use) > symbol {
          display: inline !important;
        }
        '''
        rules = CSSParser.fromstring(stylesheet)
        self.assertEqual(2, len(rules))

        rule = rules[0]
        self.assertIsInstance(rule, CSSStyleRule)
        self.assertEqual(CSSRule.STYLE_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        expected = '*:not(svg), *:not(foreignObject) > svg'
        self.assertEqual(expected, rule.selector_text)
        style = rule.style
        self.assertIsInstance(style, CSSStyleDeclaration)
        self.assertEqual(1, style.length)
        self.assertEqual('0 0',
                         style.get_property_value('transform-origin'))
        self.assertEqual('',
                         style.get_property_priority('transform-origin'))

        value = style['transform-origin']
        priority = style.get_property_priority('transform-origin')
        self.assertEqual('0 0', value)
        self.assertEqual('', priority)

        style['transform-origin'] = 'center', 'important'
        value = style.get_property_value('transform-origin')
        priority = style.get_property_priority('transform-origin')
        self.assertEqual('center', value)
        self.assertEqual('important', priority)

        style['transform-origin'] = '50 50'
        value = style.get_property_value('transform-origin')
        priority = style.get_property_priority('transform-origin')
        self.assertEqual('50 50', value)
        self.assertEqual('important', priority)

        style['transform-origin'] = None  # remove
        self.assertEqual(0, style.length)

        rule = rules[1]
        self.assertIsInstance(rule, CSSStyleRule)
        self.assertEqual(CSSRule.STYLE_RULE, rule.type)
        self.assertIsNone(rule.parent_rule)
        self.assertIsNone(rule.parent_style_sheet)
        expected = ':host(use) > symbol'
        self.assertEqual(expected, rule.selector_text)
        style = rule.style
        self.assertIsInstance(style, CSSStyleDeclaration)
        self.assertEqual(1, style.length)
        self.assertEqual('inline',
                         style.get_property_value('display'))
        self.assertEqual('important',
                         style.get_property_priority('display'))

        value = style['display']
        priority = style.get_property_priority('display')
        self.assertEqual('inline', value)
        self.assertEqual('important', priority)

        style.set_property('display', None)  # remove
        self.assertEqual(0, style.length)

    def test_inline_style01(self):
        parser = SVGParser()
        rect = parser.create_element('rect')
        self.assertIsInstance(rect.style, CSSStyleDeclaration)
        self.assertIsNone(rect.style.parent_rule)
        self.assertEqual(0, rect.style.length)
        self.assertEqual(0, len(rect.attributes))

        rect.style.set_property('fill', 'red')
        rect.style.set_property('stroke', 'blue')
        rect.style.set_property('stroke-width', '5')
        self.assertEqual(3, rect.style.length)
        self.assertEqual('red',
                         rect.style.get_property_value('fill'))
        self.assertEqual('blue',
                         rect.style.get_property_value('stroke'))
        self.assertEqual('5',
                         rect.style.get_property_value('stroke-width'))
        self.assertEqual(1, len(rect.attributes))
        expected = 'fill: red; stroke-width: 5; stroke: blue;'
        self.assertEqual(expected, rect.get('style'))

        rect.style.remove_property('stroke-width')
        self.assertEqual(2, rect.style.length)
        self.assertEqual(1, len(rect.attributes))
        expected = 'fill: red; stroke: blue;'
        self.assertEqual(expected, rect.get('style'))

        rect.style.set_property('fill', None)
        rect.style.set_property('stroke', '')
        rect.style.set_property('stroke', '')  # no error
        self.assertEqual(0, rect.style.length)
        self.assertEqual(0, len(rect.attributes))

    def test_inline_style02(self):
        parser = SVGParser()
        rect = parser.create_element('rect')
        rect.style.update({
            'fill': 'red',
            'stroke': 'blue',
            'stroke-width': '5',
        })
        self.assertIsInstance(rect.style, CSSStyleDeclaration)
        self.assertIsNone(rect.style.parent_rule)
        self.assertEqual(3, rect.style.length)
        self.assertEqual('red',
                         rect.style.get_property_value('fill'))
        self.assertEqual('blue',
                         rect.style.get_property_value('stroke'))
        self.assertEqual('5',
                         rect.style.get_property_value('stroke-width'))
        self.assertEqual(1, len(rect.attributes))
        expected = 'fill: red; stroke-width: 5; stroke: blue;'
        self.assertEqual(expected, rect.get('style'))

        rect.style.update({'fill': 'white'})
        self.assertEqual('white',
                         rect.style.get_property_value('fill'))

        self.assertEqual(3, rect.style.length)
        self.assertEqual(1, len(rect.attributes))
        del rect.style['fill']
        self.assertEqual(2, rect.style.length)
        self.assertEqual(1, len(rect.attributes))
        rect.style['stroke'] = None
        self.assertEqual(1, rect.style.length)
        self.assertEqual(1, len(rect.attributes))
        rect.style['stroke-width'] = ''
        self.assertEqual(0, len(rect.attributes))
        self.assertEqual(0, rect.style.length)

        rect.style['fill'] = 'white', 'IMPORTANT'  # value with priority
        value = rect.style['fill']
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('white', value)
        self.assertEqual('important', priority)

        rect.style['fill'] = 'black'  # value without priority
        value = rect.style['fill']
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('black', value)
        self.assertEqual('important', priority)

        rect.style.remove_property('fill')
        rect.style.set_property('fill', 'none')
        value = rect.style['fill']
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('none', value)
        self.assertEqual('', priority)

        rect.style.set_property('fill', 'blue', 'Important')
        value = rect.style.get_property_value('fill')
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('blue', value)
        self.assertEqual('important', priority)

    def test_link_style_sheet_link(self):
        # HTMLLinkElement#sheet
        doc = window.document
        root = doc.create_element('svg')
        doc.append_child(root)
        link = doc.create_element('link')

        sheet = link.sheet
        self.assertIsNone(sheet)

        # alternative style sheet
        link.attributes.update({
            'rel': 'stylesheet alternate',
            'href': 'style.css',
        })
        sheet = link.sheet
        self.assertIsNone(sheet)

        # internal link
        link.attributes.update({
            'rel': 'stylesheet',
            'href': '#style.css',
        })
        sheet = link.sheet
        self.assertIsNone(sheet)

        # non-associated window
        link.attributes.update({
            'rel': 'stylesheet',
            'href': 'style.css',
            'media': 'print',
        })
        sheet = link.sheet
        self.assertIsNone(sheet)

        # unmatched media
        root.append_child(link)
        sheet = link.sheet
        self.assertIsNone(sheet)

        # file not found
        link.attributes.update({
            'rel': 'stylesheet',
            'href': 'style.css',
            'title': 'Default',
            'media': 'screen, print and (color)',
        })
        sheet = link.sheet
        self.assertEqual('text/css', sheet.type)
        self.assertEqual('style.css', sheet.href)
        self.assertEqual(link, sheet.owner_node)
        self.assertIsNone(sheet.parent_style_sheet)
        self.assertEqual('Default', sheet.title)
        self.assertEqual('screen, print and (color)', sheet.media.media_text)
        self.assertTrue(not sheet.disabled)
        self.assertIsNone(sheet.owner_rule)
        self.assertEqual(0, len(sheet.css_rules))

        # normal pattern
        link.attributes.update({
            'rel': 'stylesheet',
            'href': 'svg/style8.css',
            'title': 'Default',
            'media': 'screen, print and (color)',
        })
        sheet = link.sheet
        self.assertEqual('text/css', sheet.type)
        self.assertEqual('svg/style8.css', sheet.href)
        self.assertEqual(link, sheet.owner_node)
        self.assertIsNone(sheet.parent_style_sheet)
        self.assertEqual('Default', sheet.title)
        self.assertEqual('screen, print and (color)', sheet.media.media_text)
        self.assertTrue(not sheet.disabled)
        self.assertIsNone(sheet.owner_rule)
        self.assertEqual(15, len(sheet.css_rules))

    def test_link_style_sheet_style(self):
        # HTMLStyleElement#sheet
        doc = window.document
        root = doc.create_element('svg')
        doc.append_child(root)
        style = doc.create_element('style')

        # empty style
        sheet = style.sheet
        self.assertIsNone(sheet)

        # unexpected type
        style.attributes.update({
            'type': 'text/xhtml',
        })
        sheet = style.sheet
        self.assertIsNone(sheet)

        # non-associated window
        style.text = '@import url(style.css);'
        style.attributes.update({
            'type': 'text/css',
            'media': 'print',
        })
        sheet = style.sheet
        self.assertIsNone(sheet)

        # unmatched media
        root.append_child(style)
        sheet = style.sheet
        self.assertIsNone(sheet)

        # file not found
        style.attributes.update({
            'type': 'text/css',
            'title': 'Default',
            'media': 'screen, print and (color)',
        })
        sheet = style.sheet
        self.assertEqual('text/css', sheet.type)
        self.assertIsNone(sheet.href)
        self.assertEqual(style, sheet.owner_node)
        self.assertIsNone(sheet.parent_style_sheet)
        self.assertEqual('Default', sheet.title)
        self.assertEqual('screen, print and (color)', sheet.media.media_text)
        self.assertTrue(not sheet.disabled)
        self.assertIsNone(sheet.owner_rule)
        self.assertEqual(1, len(sheet.css_rules))
        css_rule = sheet.css_rules[0]
        self.assertEqual(CSSRule.IMPORT_RULE, css_rule.type)
        self.assertEqual(sheet, css_rule.parent_style_sheet)
        sheet = css_rule.style_sheet
        self.assertEqual(css_rule, sheet.owner_rule)
        self.assertEqual(0, len(sheet.css_rules))

        # normal pattern
        style.text = '@import url(svg/style8.css);'
        sheet = style.sheet
        self.assertEqual('text/css', sheet.type)
        self.assertIsNone(sheet.href)
        self.assertEqual(style, sheet.owner_node)
        self.assertIsNone(sheet.parent_style_sheet)
        self.assertEqual('Default', sheet.title)
        self.assertEqual('screen, print and (color)', sheet.media.media_text)
        self.assertTrue(not sheet.disabled)
        self.assertIsNone(sheet.owner_rule)
        self.assertEqual(1, len(sheet.css_rules))
        css_rule = sheet.css_rules[0]
        self.assertEqual(CSSRule.IMPORT_RULE, css_rule.type)
        self.assertEqual(sheet, css_rule.parent_style_sheet)
        sheet = css_rule.style_sheet
        self.assertEqual(css_rule, sheet.owner_rule)
        self.assertEqual(15, len(sheet.css_rules))

    def test_media_list(self):
        ml = MediaList()
        self.assertEqual(0, ml.length)
        self.assertEqual(0, len(ml))

        ml.append_medium(' screen ')
        ml.append_medium(' print ')
        self.assertEqual(2, ml.length)
        self.assertEqual(2, len(ml))
        self.assertEqual('screen', ml.item(0))
        self.assertEqual('print', ml.item(1))
        self.assertEqual('screen', ml[0])
        self.assertEqual('print', ml[1])

        expected = 'screen, print'
        self.assertEqual(expected, ml.media_text)

        ml.media_text = ''' screen,
        print and (color) '''
        self.assertEqual(2, ml.length)
        self.assertEqual(2, len(ml))
        self.assertEqual('screen', ml.item(0))
        self.assertEqual('print and (color)', ml.item(1))

        ml.delete_medium(' screen ')
        self.assertEqual(1, ml.length)
        self.assertEqual(1, len(ml))
        expected = 'print and (color)'
        self.assertEqual(expected, ml.media_text)

        self.assertRaises(ValueError, lambda: ml.delete_medium('print'))

    def test_style_sheet(self):
        sheet = StyleSheet()
        self.assertEqual('text/css', sheet.type)
        self.assertIsNone(sheet.href)
        self.assertIsNone(sheet.owner_node)
        self.assertIsNone(sheet.parent_style_sheet)
        self.assertIsNone(sheet.title)
        self.assertIsInstance(sheet.media, MediaList)
        self.assertEqual(0, sheet.media.length)
        self.assertTrue(not sheet.disabled)

        sheet2 = StyleSheet(
            type_='text/css',
            href="style.css",
            owner_node=self,
            parent_style_sheet=sheet,
            title='Default',
            media='print and (color)',
            disabled=True
        )
        self.assertEqual('text/css', sheet2.type)
        self.assertEqual('style.css', sheet2.href)
        self.assertEqual(self, sheet2.owner_node)
        self.assertEqual(sheet, sheet2.parent_style_sheet)
        self.assertEqual('Default', sheet2.title)
        self.assertEqual('print and (color)', sheet2.media.media_text)
        self.assertTrue(sheet2.disabled)


if __name__ == '__main__':
    unittest.main()
