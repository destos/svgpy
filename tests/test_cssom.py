#!/usr/bin/env python3


import logging
import os
import sys
import tempfile
import unittest

sys.path.extend(['.', '..'])

from svgpy import SVGParser, window
from svgpy.css import CSS, CSSFontFaceRule, CSSFontFeatureValuesRule, \
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

    def test_css_escape(self):
        text = '\0\0'
        result = CSS.escape(text)
        expected = '\ufffd\ufffd'
        self.assertEqual(expected, result)

        text = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f" \
               "\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e" \
               "\x1f\x7f"
        result = CSS.escape(text)
        expected = "\\1 \\2 \\3 \\4 \\5 \\6 \\7 \\8 \\9 \\a \\b \\c \\d \\e " \
                   "\\f \\10 \\11 \\12 \\13 \\14 \\15 \\16 \\17 \\18 \\19 " \
                   "\\1a \\1b \\1c \\1d \\1e \\1f \\7f "
        self.assertEqual(expected, result)

        text = '00'
        result = CSS.escape(text)
        expected = '\\30 0'
        self.assertEqual(expected, result)

        text = '-'
        result = CSS.escape(text)
        expected = '\\-'
        self.assertEqual(expected, result)

        text = '--'
        result = CSS.escape(text)
        expected = '--'
        self.assertEqual(expected, result)

        text = '-0'
        result = CSS.escape(text)
        expected = '-\\30 '
        self.assertEqual(expected, result)

        text = '-00'
        result = CSS.escape(text)
        expected = '-\\30 0'
        self.assertEqual(expected, result)

        text = '_0'
        result = CSS.escape(text)
        expected = '_0'
        self.assertEqual(expected, result)

        text = ' !"#$%&\'()*+,-./09:;<=>?@AZ[\\]^_`az{|}~'
        result = CSS.escape(text)
        expected = "\\ \\!\\\"\\#\\$\\%\\&\\'\\(\\)\\*\\+\\,-\\.\\/09" \
                   "\\:\\;\\<\\=\\>\\?\\@AZ\\[\\\\\\]\\^_\\`az\\{\\|\\}\\~"
        self.assertEqual(expected, result)

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
        expected = "local(Gentium Bold), " \
                   "local(Gentium-Bold), " \
                   "url(\"GentiumBold.woff\")"
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

    def test_css_style_declaration01(self):
        style = CSSStyleDeclaration()
        self.assertEqual(0, style.length)
        self.assertEqual(0, len(style))

        style.set_property('display', 'none', 'important')
        self.assertEqual(1, style.length)
        self.assertEqual(1, len(style))
        self.assertEqual('none', style.get_property_value('display'))
        self.assertEqual('important', style.get_property_priority('display'))
        self.assertEqual('none', style['display'])
        self.assertEqual('display', style.item(0))

        style.set_property('display', 'inline', 'unknown')
        self.assertEqual('none', style.get_property_value('display'))
        self.assertEqual('important', style.get_property_priority('display'))

        style.set_property('display', 'inline', '')
        self.assertEqual('inline', style.get_property_value('display'))
        self.assertEqual('', style.get_property_priority('display'))

        style.set_property('display', 'block', 'IMPORTANT')
        self.assertEqual('block', style.get_property_value('display'))
        self.assertEqual('important', style.get_property_priority('display'))

        style['display'] = 'none'
        self.assertEqual('none', style.get_property_value('display'))
        self.assertEqual('important', style.get_property_priority('display'))

        style.set_property('display', '')
        self.assertEqual(0, style.length)
        self.assertEqual(0, len(style))

        style['display'] = 'none'
        self.assertEqual(1, style.length)
        self.assertEqual(1, len(style))
        self.assertEqual('none', style.get_property_value('display'))
        self.assertEqual('', style.get_property_priority('display'))

        style.remove_property('display')
        self.assertEqual(0, style.length)
        self.assertEqual(0, len(style))

        style.set_property('display', 'inline')
        self.assertEqual(1, style.length)
        self.assertEqual(1, len(style))
        self.assertEqual('inline', style.get_property_value('display'))
        self.assertEqual('', style.get_property_priority('display'))
        del style['display']
        self.assertEqual(0, style.length)
        self.assertEqual(0, len(style))

    def test_css_style_declaration02(self):
        style = CSSStyleDeclaration()
        self.assertEqual(0, style.length)
        self.assertEqual(0, len(style))

        # font: 12pt/14pt sans-serif;
        style.set_property('font', '12pt/14pt sans-serif')

        result = style.get_property_value('font')
        self.assertEqual('12pt/14pt sans-serif', result)
        result = style.get_property_priority('font')
        self.assertEqual(0, len(result))

        result = style.get_property_value('font-size')
        self.assertEqual('12pt', result)
        result = style.get_property_priority('font-size')
        self.assertEqual(0, len(result))

        result = style.get_property_value('line-height')
        self.assertEqual('14pt', result)
        result = style.get_property_priority('line-height')
        self.assertEqual(0, len(result))

        result = style.get_property_value('font-family')
        self.assertEqual('sans-serif', result)
        result = style.get_property_priority('font-family')
        self.assertEqual(0, len(result))

        # font-size: 12pt !important;
        # line-height: 14pt;
        # font-family: sans-serif;
        style.set_property('font-size', '12pt', 'important')

        result = style.get_property_value('font')
        self.assertEqual(0, len(result))
        result = style.get_property_priority('font')
        self.assertEqual(0, len(result))

        result = style.get_property_value('font-size')
        self.assertEqual('12pt', result)
        result = style.get_property_priority('font-size')
        self.assertEqual('important', result)

        result = style.get_property_value('line-height')
        self.assertEqual('14pt', result)
        result = style.get_property_priority('line-height')
        self.assertEqual(0, len(result))

        result = style.get_property_value('font-family')
        self.assertEqual('sans-serif', result)
        result = style.get_property_priority('font-family')
        self.assertEqual(0, len(result))

        # font-size: 12pt !important;
        # line-height: 14pt !important;
        # font-family: sans-serif !important;
        style.set_property('line-height', '14pt', 'important')
        style.set_property('font-family', 'sans-serif', 'important')
        style.set_property('font-stretch', 'normal', 'important')
        style.set_property('font-style', 'normal', 'important')
        style.set_property('font-variant', 'normal', 'important')
        style.set_property('font-weight', 'normal', 'important')

        result = style.get_property_value('font')
        self.assertEqual('12pt/14pt sans-serif', result)
        result = style.get_property_priority('font')
        self.assertEqual('important', result)

        result = style.get_property_value('font-size')
        self.assertEqual('12pt', result)
        result = style.get_property_priority('font-size')
        self.assertEqual('important', result)

        result = style.get_property_value('line-height')
        self.assertEqual('14pt', result)
        result = style.get_property_priority('line-height')
        self.assertEqual('important', result)

        result = style.get_property_value('font-family')
        self.assertEqual('sans-serif', result)
        result = style.get_property_priority('font-family')
        self.assertEqual('important', result)

    def test_css_style_declaration_inline01(self):
        parser = SVGParser()
        rect = parser.create_element_ns('http://www.w3.org/2000/svg', 'rect')
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

        rect.style.set_property('fill', '')
        rect.style.set_property('stroke', '')
        rect.style.set_property('stroke', '')  # no error
        self.assertEqual(0, rect.style.length)
        self.assertEqual(0, len(rect.attributes))

    def test_css_style_declaration_inline02(self):
        parser = SVGParser()
        rect = parser.create_element_ns('http://www.w3.org/2000/svg', 'rect')
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
        rect.style['stroke'] = ''
        self.assertEqual(1, rect.style.length)
        self.assertEqual(1, len(rect.attributes))
        rect.style['stroke-width'] = ''
        self.assertEqual(0, len(rect.attributes))
        self.assertEqual(0, rect.style.length)

        rect.style.set_property('fill', 'white', 'IMPORTANT')
        value = rect.style['fill']
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('white', value)
        self.assertEqual('', priority)  # ignored

        rect.style['fill'] = 'black'  # value without priority
        value = rect.style['fill']
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('black', value)
        self.assertEqual('', priority)  # ignored

        rect.style.remove_property('fill')
        rect.style.set_property('fill', 'none')
        value = rect.style['fill']
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('none', value)
        self.assertEqual('', priority)  # ignored

        rect.style.set_property('fill', 'blue', 'Important')
        value = rect.style.get_property_value('fill')
        priority = rect.style.get_property_priority('fill')
        self.assertEqual('blue', value)
        self.assertEqual('', priority)  # ignored

    def test_css_style_declaration_inline_font01(self):
        # [css-fonts-4] EXAMPLE 12 (1)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            '12pt/14pt sans-serif')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual('font: 12pt/14pt sans-serif;',
                         root.attributes['style'].value)
        self.assertEqual('12pt/14pt sans-serif', root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('12pt', root.style['font-size'])
        self.assertEqual('14pt', root.style['line-height'])
        self.assertEqual('sans-serif', root.style['font-family'])
        # self.assertEqual('none', root.style['font-size-adjust'])
        # self.assertEqual('auto', root.style['font-kerning'])
        # self.assertEqual('normal', root.style['font-feature-settings'])
        # self.assertEqual('normal', root.style['font-language-override'])
        # self.assertEqual('0', root.style['font-min-size'])
        # self.assertEqual('infinity', root.style['font-max-size'])
        # self.assertEqual('auto', root.style['font-optical-sizing'])
        # self.assertEqual('normal', root.style['font-variation-settings'])
        # self.assertEqual('normal', root.style['font-palette'])

        result = root.style.remove_property('font-style')
        self.assertEqual('normal', result)
        self.assertEqual("font-family: sans-serif; "
                         "font-size: 12pt; "
                         "font-stretch: normal; "
                         "font-variant: normal; "
                         "font-weight: normal; "
                         "line-height: 14pt;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font'])
        self.assertEqual('', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('12pt', root.style['font-size'])
        self.assertEqual('14pt', root.style['line-height'])
        self.assertEqual('sans-serif', root.style['font-family'])

    def test_css_style_declaration_inline_font02(self):
        # [css-fonts-4] EXAMPLE 12 (2)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            '80% sans-serif')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual('font: 80% sans-serif;',
                         root.attributes['style'].value)
        self.assertEqual('80% sans-serif', root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('80%', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('sans-serif', root.style['font-family'])
        # self.assertEqual('none', root.style['font-size-adjust'])
        # self.assertEqual('auto', root.style['font-kerning'])
        # self.assertEqual('normal', root.style['font-feature-settings'])
        # self.assertEqual('normal', root.style['font-language-override'])
        # self.assertEqual('0', root.style['font-min-size'])
        # self.assertEqual('infinity', root.style['font-max-size'])
        # self.assertEqual('auto', root.style['font-optical-sizing'])
        # self.assertEqual('normal', root.style['font-variation-settings'])
        # self.assertEqual('normal', root.style['font-palette'])

    def test_css_style_declaration_inline_font03(self):
        # [css-fonts-4] EXAMPLE 12 (3)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            'x-large/110% "new century schoolbook", serif')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual('font: x-large/110% "new century schoolbook", serif;',
                         root.attributes['style'].value)
        self.assertEqual('x-large/110% "new century schoolbook", serif',
                         root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('x-large', root.style['font-size'])
        self.assertEqual('110%', root.style['line-height'])
        self.assertEqual('"new century schoolbook", serif',
                         root.style['font-family'])
        # self.assertEqual('none', root.style['font-size-adjust'])
        # self.assertEqual('auto', root.style['font-kerning'])
        # self.assertEqual('normal', root.style['font-feature-settings'])
        # self.assertEqual('normal', root.style['font-language-override'])
        # self.assertEqual('0', root.style['font-min-size'])
        # self.assertEqual('infinity', root.style['font-max-size'])
        # self.assertEqual('auto', root.style['font-optical-sizing'])
        # self.assertEqual('normal', root.style['font-variation-settings'])
        # self.assertEqual('normal', root.style['font-palette'])

    def test_css_style_declaration_inline_font04(self):
        # [css-fonts-4] EXAMPLE 12 (4)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            'bold italic large Palatino, serif')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual('font: italic bold large Palatino, serif;',
                         root.attributes['style'].value)
        self.assertEqual('italic bold large Palatino, serif',
                         root.style['font'])
        self.assertEqual('italic', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('bold', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('large', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('Palatino, serif', root.style['font-family'])
        # self.assertEqual('none', root.style['font-size-adjust'])
        # self.assertEqual('auto', root.style['font-kerning'])
        # self.assertEqual('normal', root.style['font-feature-settings'])
        # self.assertEqual('normal', root.style['font-language-override'])
        # self.assertEqual('0', root.style['font-min-size'])
        # self.assertEqual('infinity', root.style['font-max-size'])
        # self.assertEqual('auto', root.style['font-optical-sizing'])
        # self.assertEqual('normal', root.style['font-variation-settings'])
        # self.assertEqual('normal', root.style['font-palette'])

        result = root.style.remove_property('font-size')
        self.assertEqual('large', result)
        self.assertEqual("font-family: Palatino, serif; "
                         "font-stretch: normal; "
                         "font-style: italic; "
                         "font-variant: normal; "
                         "font-weight: bold; "
                         "line-height: normal;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font'])
        self.assertEqual('italic', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('bold', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('Palatino, serif', root.style['font-family'])

    def test_css_style_declaration_inline_font05(self):
        # [css-fonts-4] EXAMPLE 12 (5)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            'normal small-caps 120%/120% fantasy')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual('font: small-caps 120%/120% fantasy;',
                         root.attributes['style'].value)
        self.assertEqual('small-caps 120%/120% fantasy',
                         root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('fantasy', root.style['font-family'])
        # self.assertEqual('none', root.style['font-size-adjust'])
        # self.assertEqual('auto', root.style['font-kerning'])
        # self.assertEqual('normal', root.style['font-feature-settings'])
        # self.assertEqual('normal', root.style['font-language-override'])
        # self.assertEqual('0', root.style['font-min-size'])
        # self.assertEqual('infinity', root.style['font-max-size'])
        # self.assertEqual('auto', root.style['font-optical-sizing'])
        # self.assertEqual('normal', root.style['font-variation-settings'])
        # self.assertEqual('normal', root.style['font-palette'])

        result = root.style.remove_property('font-family')
        self.assertEqual('fantasy', result)
        self.assertEqual("font-size: 120%; "
                         "font-stretch: normal; "
                         "font-style: normal; "
                         "font-variant: small-caps; "
                         "font-weight: normal; "
                         "line-height: 120%;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('', root.style['font-family'])

    def test_css_style_declaration_inline_font06(self):
        # [css-fonts-4] EXAMPLE 12 (5)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            'normal small-caps 120%/120% fantasy')
        self.assertEqual(1, len(root.attributes))

        root.style.set_property('font-stretch', '75%')  # [css-font-4]
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font-family: fantasy; "
                         "font-size: 120%; "
                         "font-stretch: 75%; "
                         "font-style: normal; "
                         "font-variant: small-caps; "
                         "font-weight: normal; "
                         "line-height: 120%;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('75%', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('fantasy', root.style['font-family'])

        root.style.set_property('font-stretch', 'condensed')  # [css-font-3]
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font: "
                         "small-caps "
                         "condensed "
                         "120%/120% "
                         "fantasy;",
                         root.attributes['style'].value)
        self.assertEqual('small-caps condensed 120%/120% fantasy',
                         root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('condensed', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('fantasy', root.style['font-family'])

        root.style.set_property('font-variant-ligatures',
                                'no-common-ligatures')  # [css-font-3]
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font-family: fantasy; "
                         "font-size: 120%; "
                         "font-stretch: condensed; "
                         "font-style: normal; "
                         "font-variant: no-common-ligatures small-caps; "
                         "font-weight: normal; "
                         "line-height: 120%;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('no-common-ligatures small-caps',
                         root.style['font-variant'])
        self.assertEqual('no-common-ligatures',
                         root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('condensed', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('fantasy', root.style['font-family'])

        root.style.set_property('font-variant', 'normal')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font: "
                         "condensed "
                         "120%/120% "
                         "fantasy;",
                         root.attributes['style'].value)
        self.assertEqual('condensed 120%/120% fantasy',
                         root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('condensed', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('fantasy', root.style['font-family'])

        root.style.set_property('font', 'monospace')
        root.style.set_property('font-weight', '200')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font: "
                         "200 "
                         "monospace;",
                         root.attributes['style'].value)
        self.assertEqual('200 monospace',
                         root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('200', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('medium', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('monospace', root.style['font-family'])

        root.style.set_property('font-variant-caps', 'all-small-caps')
        root.style.set_property('font-variant-east-asian', 'ruby')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font-family: monospace; "
                         "font-size: medium; "
                         "font-stretch: normal; "
                         "font-style: normal; "
                         "font-variant: all-small-caps ruby; "
                         "font-weight: 200; "
                         "line-height: normal;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('all-small-caps ruby',
                         root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('all-small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('ruby', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('200', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('medium', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('monospace', root.style['font-family'])

        root.style.set_property('font-variant', 'normal')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font: "
                         "200 "
                         "monospace;",
                         root.attributes['style'].value)
        self.assertEqual('200 monospace',
                         root.style['font'])
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('200', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('medium', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('monospace', root.style['font-family'])

    def test_css_style_declaration_inline_font07(self):
        # [css-fonts-4] EXAMPLE 12 (7)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property(
            'font',
            'condensed oblique 25deg 753 12pt "Helvetica Neue", serif')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual("font: "
                         "oblique 25deg "
                         "753 "
                         "condensed "
                         "12pt "
                         "\"Helvetica Neue\", serif;",
                         root.attributes['style'].value)
        self.assertEqual("oblique 25deg "
                         "753 "
                         "condensed "
                         "12pt "
                         "\"Helvetica Neue\", serif",
                         root.style['font'])
        self.assertEqual('oblique 25deg', root.style['font-style'])
        self.assertEqual('normal', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])
        self.assertEqual('753', root.style['font-weight'])
        self.assertEqual('condensed', root.style['font-stretch'])
        self.assertEqual('12pt', root.style['font-size'])
        self.assertEqual('normal', root.style['line-height'])
        self.assertEqual('"Helvetica Neue", serif', root.style['font-family'])

    def test_css_style_declaration_inline_font08(self):
        # [css-fonts-4] EXAMPLE 12 (5)
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property(
            'font',
            'normal small-caps 120%/120% fantasy')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual('font: small-caps 120%/120% fantasy;',
                         root.attributes['style'].value)
        self.assertEqual('small-caps 120%/120% fantasy',
                         root.style['font'])

        result = root.style.remove_property('font-variant')
        self.assertEqual('small-caps', result)
        self.assertEqual("font-family: fantasy; "
                         "font-size: 120%; "
                         "font-stretch: normal; "
                         "font-style: normal; "
                         "font-weight: normal; "
                         "line-height: 120%;",
                         root.attributes['style'].value)
        self.assertEqual('normal', root.style['font-style'])
        self.assertEqual('', root.style['font-variant'])
        self.assertEqual('', root.style['font-variant-ligatures'])
        self.assertEqual('', root.style['font-variant-caps'])
        self.assertEqual('', root.style['font-variant-alternates'])
        self.assertEqual('', root.style['font-variant-numeric'])
        self.assertEqual('', root.style['font-variant-east-asian'])
        self.assertEqual('', root.style['font-variant-position'])
        self.assertEqual('normal', root.style['font-weight'])
        self.assertEqual('normal', root.style['font-stretch'])
        self.assertEqual('120%', root.style['font-size'])
        self.assertEqual('120%', root.style['line-height'])
        self.assertEqual('fantasy', root.style['font-family'])

    def test_css_style_declaration_inline_font_synthesis(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, root.attributes.length)

        root.style.set_property('font-synthesis', 'invalid-value')
        self.assertEqual(0, root.style.length)
        self.assertEqual(0, root.attributes.length)

        root.style.set_property('font-synthesis', 'none')
        self.assertEqual("font-synthesis: none;",
                         root.attributes['style'].value)
        self.assertEqual('none', root.style['font-synthesis'])
        self.assertEqual('none', root.style['font-synthesis-weight'])
        self.assertEqual('none', root.style['font-synthesis-style'])

        root.style.remove_property('font-synthesis-weight')
        self.assertEqual("font-synthesis-style: none;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['font-synthesis'])
        self.assertEqual('', root.style['font-synthesis-weight'])
        self.assertEqual('none', root.style['font-synthesis-style'])

        root.style.set_property('font-synthesis-weight', 'auto')
        self.assertEqual("font-synthesis: weight;",
                         root.attributes['style'].value)
        self.assertEqual('weight', root.style['font-synthesis'])
        self.assertEqual('auto', root.style['font-synthesis-weight'])
        self.assertEqual('none', root.style['font-synthesis-style'])

        root.style.set_property('font-synthesis-style', 'auto')
        self.assertEqual("font-synthesis: weight style;",
                         root.attributes['style'].value)
        self.assertEqual('weight style', root.style['font-synthesis'])
        self.assertEqual('auto', root.style['font-synthesis-weight'])
        self.assertEqual('auto', root.style['font-synthesis-style'])

        root.style.set_property('font-synthesis-weight', 'none')
        self.assertEqual("font-synthesis: style;",
                         root.attributes['style'].value)
        self.assertEqual('style', root.style['font-synthesis'])
        self.assertEqual('none', root.style['font-synthesis-weight'])
        self.assertEqual('auto', root.style['font-synthesis-style'])

        root.style.remove_property('font-synthesis')
        self.assertEqual(0, root.style.length)
        self.assertEqual(0, root.attributes.length)

    def test_css_style_declaration_inline_font_variant01(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property(
            'font-variant',
            'small-caps')
        self.assertEqual("font-variant: small-caps;",
                         root.attributes['style'].value)
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])

    def test_css_style_declaration_inline_font_variant02(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        root.style.set_property('font', 'small-caps sans-serif')
        self.assertEqual("font: small-caps sans-serif;",
                         root.attributes['style'].value)
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])

        root.style.set_property('font-variant', 'all-small-caps')
        self.assertEqual("font-family: sans-serif; "
                         "font-size: medium; "
                         "font-stretch: normal; "
                         "font-style: normal; "
                         "font-variant: all-small-caps; "
                         "font-weight: normal; "
                         "line-height: normal;",
                         root.attributes['style'].value)
        self.assertEqual('all-small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('all-small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])

        result = root.style.remove_property('font-variant')
        self.assertEqual("font-family: sans-serif; "
                         "font-size: medium; "
                         "font-stretch: normal; "
                         "font-style: normal; "
                         "font-weight: normal; "
                         "line-height: normal;",
                         root.attributes['style'].value)
        self.assertEqual('all-small-caps', result)
        self.assertEqual('', root.style['font-variant'])
        self.assertEqual('', root.style['font-variant-ligatures'])
        self.assertEqual('', root.style['font-variant-caps'])
        self.assertEqual('', root.style['font-variant-alternates'])
        self.assertEqual('', root.style['font-variant-numeric'])
        self.assertEqual('', root.style['font-variant-east-asian'])
        self.assertEqual('', root.style['font-variant-position'])

        root.style.set_property('font-variant', 'no-common-ligatures')
        self.assertEqual("font-family: sans-serif; "
                         "font-size: medium; "
                         "font-stretch: normal; "
                         "font-style: normal; "
                         "font-variant: no-common-ligatures; "
                         "font-weight: normal; "
                         "line-height: normal;",
                         root.attributes['style'].value)
        self.assertEqual('all-small-caps', result)
        self.assertEqual('no-common-ligatures', root.style['font-variant'])
        self.assertEqual('no-common-ligatures',
                         root.style['font-variant-ligatures'])
        self.assertEqual('normal', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])

        root.style.set_property('font-variant', 'small-caps')
        self.assertEqual("font: small-caps sans-serif;",
                         root.attributes['style'].value)
        self.assertEqual('small-caps', root.style['font-variant'])
        self.assertEqual('normal', root.style['font-variant-ligatures'])
        self.assertEqual('small-caps', root.style['font-variant-caps'])
        self.assertEqual('normal', root.style['font-variant-alternates'])
        self.assertEqual('normal', root.style['font-variant-numeric'])
        self.assertEqual('normal', root.style['font-variant-east-asian'])
        self.assertEqual('normal', root.style['font-variant-position'])

        result = root.style.remove_property('font')
        self.assertEqual(0, root.attributes.length)
        self.assertEqual("small-caps sans-serif", result)
        self.assertEqual('', root.style['font-variant'])
        self.assertEqual('', root.style['font-variant-ligatures'])
        self.assertEqual('', root.style['font-variant-caps'])
        self.assertEqual('', root.style['font-variant-alternates'])
        self.assertEqual('', root.style['font-variant-numeric'])
        self.assertEqual('', root.style['font-variant-east-asian'])
        self.assertEqual('', root.style['font-variant-position'])

    def test_css_style_declaration_inline_overflow01(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property('overflow', 'clip')
        self.assertEqual("overflow: clip;",
                         root.attributes['style'].value)
        self.assertEqual('clip', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('clip', root.style['overflow-y'])

        result = root.style.remove_property('overflow-y')
        self.assertEqual('clip', result)
        self.assertEqual("overflow: clip;",
                         root.attributes['style'].value)
        self.assertEqual('clip', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('clip', root.style['overflow-y'])

    def test_css_style_declaration_inline_overflow02(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property('overflow', 'clip')
        self.assertEqual("overflow: clip;",
                         root.attributes['style'].value)
        self.assertEqual('clip', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('clip', root.style['overflow-y'])

        result = root.style.remove_property('overflow-x')
        self.assertEqual('clip', result)
        self.assertEqual("overflow-y: clip;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['overflow'])
        self.assertEqual('', root.style['overflow-x'])
        self.assertEqual('clip', root.style['overflow-y'])

    def test_css_style_declaration_inline_overflow03(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property('overflow', 'clip auto')
        self.assertEqual("overflow: clip auto;",
                         root.attributes['style'].value)
        self.assertEqual('clip auto', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('auto', root.style['overflow-y'])

        result = root.style.remove_property('overflow-y')
        self.assertEqual('auto', result)
        self.assertEqual("overflow: clip;",
                         root.attributes['style'].value)
        self.assertEqual('clip', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('clip', root.style['overflow-y'])

    def test_css_style_declaration_inline_overflow04(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property('overflow', 'clip auto')
        self.assertEqual("overflow: clip auto;",
                         root.attributes['style'].value)
        self.assertEqual('clip auto', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('auto', root.style['overflow-y'])

        result = root.style.remove_property('overflow-x')
        self.assertEqual('clip', result)
        self.assertEqual("overflow-y: auto;",
                         root.attributes['style'].value)
        self.assertEqual('', root.style['overflow'])
        self.assertEqual('', root.style['overflow-x'])
        self.assertEqual('auto', root.style['overflow-y'])

    def test_css_style_declaration_inline_overflow05(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, len(root.style))

        root.style.set_property('overflow', 'clip auto')
        self.assertEqual("overflow: clip auto;",
                         root.attributes['style'].value)
        self.assertEqual('clip auto', root.style['overflow'])
        self.assertEqual('clip', root.style['overflow-x'])
        self.assertEqual('auto', root.style['overflow-y'])

        result = root.style.remove_property('overflow')
        self.assertEqual('clip auto', result)
        self.assertEqual(0, root.attributes.length)
        self.assertEqual('', root.style['overflow'])
        self.assertEqual('', root.style['overflow-x'])
        self.assertEqual('', root.style['overflow-y'])

        root.style.set_property('overflow-x', 'auto')
        self.assertEqual("overflow: auto;",
                         root.attributes['style'].value)
        self.assertEqual('auto', root.style['overflow'])
        self.assertEqual('auto', root.style['overflow-x'])
        self.assertEqual('auto', root.style['overflow-y'])

    def test_css_style_declaration_inline_text_decoration01(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg', 'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, root.attributes.length)

        root.style.set_property('text-decoration', 'initial')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration: initial;",
                         root.attributes['style'].value)
        self.assertEqual('initial', root.style['text-decoration-line'])
        self.assertEqual('initial', root.style['text-decoration-style'])
        self.assertEqual('initial', root.style['text-decoration-color'])

        root.style.set_property('text-decoration-line', 'inherit')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration-color: initial; "
                         "text-decoration-line: inherit; "
                         "text-decoration-style: initial;",
                         root.attributes['style'].value)
        self.assertEqual('inherit', root.style['text-decoration-line'])
        self.assertEqual('initial', root.style['text-decoration-style'])
        self.assertEqual('initial', root.style['text-decoration-color'])

        root.style.set_property('text-decoration-color', 'currentColor')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration-color: currentcolor; "
                         "text-decoration-line: inherit; "
                         "text-decoration-style: initial;",
                         root.attributes['style'].value)
        self.assertEqual('inherit', root.style['text-decoration-line'])
        self.assertEqual('initial', root.style['text-decoration-style'])
        self.assertEqual('currentcolor', root.style['text-decoration-color'])

        root.style.set_property('text-decoration-line', 'none')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration: none currentcolor;",
                         root.attributes['style'].value)
        self.assertEqual('none', root.style['text-decoration-line'])
        self.assertEqual('initial', root.style['text-decoration-style'])
        self.assertEqual('currentcolor', root.style['text-decoration-color'])

        root.style.set_property('text-decoration-style', '')
        self.assertEqual(2, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration-color: currentcolor; "
                         "text-decoration-line: none;",
                         root.attributes['style'].value)
        self.assertEqual('none', root.style['text-decoration-line'])
        self.assertEqual('currentcolor', root.style['text-decoration-color'])

        root.style.set_property('text-decoration-style', 'solid')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration: none solid currentcolor;",
                         root.attributes['style'].value)
        self.assertEqual('none', root.style['text-decoration-line'])
        self.assertEqual('solid', root.style['text-decoration-style'])
        self.assertEqual('currentcolor', root.style['text-decoration-color'])

    def test_css_style_declaration_inline_text_decoration02(self):
        parser = SVGParser()
        root = parser.create_element_ns('http://www.w3.org/2000/svg',
                                        'svg')

        self.assertEqual(0, root.style.length)
        self.assertEqual(0, root.attributes.length)

        root.style.set_property('text-decoration', 'navy dotted underline')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration: underline dotted navy;",
                         root.attributes['style'].value)
        self.assertEqual('underline', root.style['text-decoration-line'])
        self.assertEqual('dotted', root.style['text-decoration-style'])
        self.assertEqual('navy', root.style['text-decoration-color'])

        root.style.set_property('text-decoration-color', 'TRANSPARENT')
        self.assertEqual(3, root.style.length)
        self.assertEqual(1, root.attributes.length)
        self.assertEqual("text-decoration: underline dotted transparent;",
                         root.attributes['style'].value)
        self.assertEqual('underline', root.style['text-decoration-line'])
        self.assertEqual('dotted', root.style['text-decoration-style'])
        self.assertEqual('transparent', root.style['text-decoration-color'])

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

        style.set_property('transform-origin', 'center', 'important')
        value = style.get_property_value('transform-origin')
        priority = style.get_property_priority('transform-origin')
        self.assertEqual('center', value)
        self.assertEqual('important', priority)

        style['transform-origin'] = '50 50'
        value = style.get_property_value('transform-origin')
        priority = style.get_property_priority('transform-origin')
        self.assertEqual('50 50', value)
        self.assertEqual('important', priority)

        style['transform-origin'] = ''  # remove
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

        style.set_property('display', '')  # remove
        self.assertEqual(0, style.length)

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

        ml.append_medium('screen, print')
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

        ml.delete_medium('screen, print and (color)')
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

        ml.insert(0, 'screen')
        self.assertEqual('screen', ml.item(0))
        self.assertEqual('print and (color)', ml.item(1))

        ml.media_text = ''
        self.assertEqual(0, ml.length)
        self.assertEqual(0, len(ml))

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
