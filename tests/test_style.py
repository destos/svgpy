#!/usr/bin/env python3


import os
import sys
import unittest
from io import StringIO
from urllib.parse import unquote

sys.path.extend(['.', '..'])

from svgpy import Font, SVGParser, window
from svgpy.css import CSSRule
from svgpy.style import get_css_rules, get_css_rules_from_svg_document, \
    get_css_rules_from_xml_stylesheet, get_css_style
from svgpy.utils import get_content_type, load

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


# doc8.svg and style8.css comes from MDN.
# See https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/SVG_and_CSS
class StyleTestCase(unittest.TestCase):
    """Important: Run the following command before this test.;
    'cd tests && python3 -m http.server 8000'
    """

    def setUp(self):
        window.media = 'screen'
        window.inner_width = 1280
        window.inner_height = 720

    def test_get_css_rules_from_svg_document01(self):
        # 'link' and 'style' elements
        svg = '''
        <svg width="5cm" height="4cm" viewBox="0 0 500 400"
             xmlns="http://www.w3.org/2000/svg">
          <link rel="stylesheet" href="svg/style8.css"/>
          <style type="text/css"><![CDATA[
            .Border { fill:none; stroke:blue; stroke-width:1 }
            .Connect { fill:none; stroke:#888888; stroke-width:2 }
            .SamplePath { fill:none; stroke:red; stroke-width:5 }
            .EndPoint { fill:none; stroke:#888888; stroke-width:2 }
            .CtlPoint { fill:#888888; stroke:none }
            .AutoCtlPoint { fill:none; stroke:blue; stroke-width:4 }
            .Label { font-size:22; font-family:Verdana }
          ]]></style>
          <style>
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
          </style>
          <rect class="Border" x="1" y="1" width="498" height="398" id="rect01" />
          <polyline class="Connect" points="100,200 100,100" id="polyline01" />
          <path class="SamplePath" d="M100,200 C100,100 250,100 250,200
                                               S400,300 400,200" id="path01" />
          <circle class="EndPoint" cx="100" cy="200" r="10" id="circle01" />
          <text class="Label" x="25" y="70" id="text01">
            M100,200 C100,100 250,100 250,200</text>
        </svg>
        '''
        parser = SVGParser()
        tree = parser.parse(StringIO(svg))
        root = tree.getroot()
        css_rules = get_css_rules_from_svg_document(root)
        self.assertEqual(15 + 7 + 2, len(css_rules))

        css_rule = css_rules[0]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('svg', css_rule.selector_text)

        css_rule = css_rules[14]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('#inner-petals .segment:hover > .segment-edge',
                         css_rule.selector_text)

        css_rule = css_rules[15]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('.Border', css_rule.selector_text)

        css_rule = css_rules[21]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('.Label', css_rule.selector_text)

        css_rule = css_rules[22]
        self.assertEqual(CSSRule.MEDIA_RULE, css_rule.type)
        self.assertEqual('print', css_rule.media.media_text)

        css_rule = css_rules[23]
        self.assertEqual(CSSRule.MEDIA_RULE, css_rule.type)
        self.assertEqual(
            'screen and (min-width: 35em), print and (min-width: 40em)',
            css_rule.media.media_text
        )

    def test_get_css_rules_from_svg_document02(self):
        # 'link' element
        # See also: svg/style8.css
        parser = SVGParser()
        root = parser.make_element('svg')
        link = root.make_sub_element('link')
        link.attributes.update({
            'rel': 'stylesheet',
            'href': 'svg/style8.css',
            'type': 'text/css',
        })
        css_rules = get_css_rules_from_svg_document(root)
        self.assertEqual(15, len(css_rules))

    def test_get_css_rules_from_svg_document03(self):
        # 'link' element
        # See also: svg/style8.css
        parser = SVGParser()
        root = parser.make_element('svg')
        link = root.make_sub_element('link')
        link.attributes.update({
            'rel': 'stylesheet',
            'href': 'http://localhost:8000/svg/style8.css',
            'type': 'text/css',
        })
        css_rules = get_css_rules_from_svg_document(root)
        self.assertEqual(15, len(css_rules),
                         msg='http server may not be working.')

    def test_get_css_rules_from_svg_document04(self):
        # 'style' element
        # See also: svg/style8.css
        parser = SVGParser()
        root = parser.make_element('svg')
        style = root.make_sub_element('style')
        style.text = '@import url(svg/style8.css);'
        css_rules = get_css_rules_from_svg_document(root)
        self.assertEqual(1, len(css_rules))

        css_rule = css_rules[0]
        self.assertEqual(CSSRule.IMPORT_RULE, css_rule.type)
        css_stylesheet = css_rule.style_sheet
        self.assertEqual(15, len(css_stylesheet.css_rules),
                         msg='http server may not be working.')

    def test_get_css_rules_from_xml_stylesheet01(self):
        # xml-stylesheet
        # See also: svg/doc8.svg and svg/style8.css
        parser = SVGParser()
        tree = parser.parse(here + '/svg/doc8.svg')
        root = tree.getroot()
        # read svg/style8.css
        css_rules = get_css_rules_from_xml_stylesheet(root)
        self.assertEqual(15, len(css_rules))

        css_rule = css_rules[0]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('svg', css_rule.selector_text)

        css_rule = css_rules[14]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('#inner-petals .segment:hover > .segment-edge',
                         css_rule.selector_text)

    def test_get_css_rules_from_xml_stylesheet02(self):
        # xml-stylesheet
        svg = '''<?xml version="1.0" standalone="no"?>
        <?xml-stylesheet type="text/css" href="svg/style8.css" title="default"?>
        <?xml-stylesheet type="text/css" href="svg/ny1.css" title="extras"?>
        <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN"
          "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
        
        <svg width="600px" height="600px" viewBox="-300 -300 600 600"
          xmlns="http://www.w3.org/2000/svg">
        </svg>
        '''
        parser = SVGParser()
        tree = parser.parse(StringIO(svg))
        root = tree.getroot()
        css_rules = get_css_rules_from_xml_stylesheet(root)
        self.assertEqual(15 + 7, len(css_rules))

        css_rule = css_rules[0]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('svg', css_rule.selector_text)

        css_rule = css_rules[14]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('#inner-petals .segment:hover > .segment-edge',
                         css_rule.selector_text)

        css_rule = css_rules[15]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('text', css_rule.selector_text)

        css_rule = css_rules[21]
        self.assertEqual(CSSRule.STYLE_RULE, css_rule.type)
        self.assertEqual('.tick', css_rule.selector_text)

    def test_get_css_style01(self):
        # 'style' element
        # See also: svg/style8.css
        parser = SVGParser()
        root = parser.make_element('svg')
        style = root.make_sub_element('style')
        style.text = '@import url(svg/style8.css);'
        text = root.make_sub_element('text')
        text.id = 'heading'

        css_rules = get_css_rules(text)
        css_style, css_style_important = get_css_style(text, css_rules)
        self.assertEqual('24px', css_style.get('font-size'),
                         msg='http server may not be working.')
        self.assertEqual('bold', css_style.get('font-weight'))
        self.assertEqual(0, len(css_style_important))

        css_style = text.get_computed_style()
        self.assertEqual(24, css_style.get('font-size'))
        self.assertEqual(700, css_style.get('font-weight'))

    def test_get_css_style02(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        style = root.make_sub_element('style')
        style.text = '''
@media (min-height: 680px) and (orientation: landscape) {
    #heading {
        font-size: 24px;
        font-weight: bold;
    }
    #caption {
        font-size: 12px;
    }
}
        '''
        text = root.make_sub_element('text')
        text.id = 'heading'

        root.attributes.update({
            'width': '1280',
            'height': '679',
            'viewBox': '0 0 1280 679',
        })
        css_rules = get_css_rules(text)
        css_style, css_style_important = get_css_style(text, css_rules)
        self.assertIsNone(css_style.get('font-size'))
        self.assertIsNone(css_style.get('font-weight'))
        self.assertEqual(0, len(css_style_important))

        css_style = text.get_computed_style()
        self.assertEqual(Font.default_font_size, css_style.get('font-size'))
        self.assertEqual(Font.default_font_weight, css_style.get('font-weight'))

        root.attributes.update({
            'width': '1280',
            'height': '680',
            'viewBox': '0 0 1280 680',
        })
        css_rules = get_css_rules(text)
        css_style, css_style_important = get_css_style(text, css_rules)
        self.assertEqual('24px', css_style.get('font-size'))
        self.assertEqual('bold', css_style.get('font-weight'))
        self.assertEqual(0, len(css_style_important))

        css_style = text.get_computed_style()
        self.assertEqual(24, css_style.get('font-size'))
        self.assertEqual(700, css_style.get('font-weight'))

        # SVG-UA stylesheet
        css_rules = get_css_rules(style)
        css_style, css_style_important = get_css_style(style, css_rules)
        self.assertEqual('none', css_style.get('display'))
        self.assertEqual('none', css_style_important.get('display'))

        css_style = style.get_computed_style()
        self.assertEqual('none', css_style.get('display'))

    def test_get_css_style03(self):
        parser = SVGParser()
        svg = '''
<svg width="5cm" height="4cm" viewBox="0 0 500 400"
     xmlns="http://www.w3.org/2000/svg">
  <style type="text/css"><![CDATA[
    .Border { fill:none; stroke:blue; stroke-width:1 }
    .Connect { fill:none; stroke:#888888; stroke-width:2 }
    .SamplePath { fill:none; stroke:red; stroke-width:5 }
    .EndPoint { fill:none; stroke:#888888; stroke-width:2 }
    .CtlPoint { fill:#888888; stroke:none }
    .AutoCtlPoint { fill:none; stroke:blue; stroke-width:4 }
    .Label { font-size:22; font-family:Verdana }
  ]]></style>
  <rect class="Border" x="1" y="1" width="498" height="398" id="rect01" />
  <polyline class="Connect" points="100,200 100,100" id="polyline01" />
  <path class="SamplePath" d="M100,200 C100,100 250,100 250,200
                                       S400,300 400,200" id="path01" />
  <circle class="EndPoint" cx="100" cy="200" r="10" id="circle01" />
  <text class="Label" x="25" y="70" id="text01">
    M100,200 C100,100 250,100 250,200</text>
</svg>
        '''
        root = parser.fromstring(svg)

        rect = root.get_element_by_id('rect01')
        css_style = rect.get_computed_style()
        self.assertEqual('none', css_style.get('fill'))
        self.assertEqual('blue', css_style.get('stroke'))
        self.assertEqual(1, css_style.get('stroke-width'))

        path = root.get_element_by_id('path01')
        css_style = path.get_computed_style()
        self.assertEqual('none', css_style.get('fill'))
        self.assertEqual('red', css_style.get('stroke'))
        self.assertEqual(5, css_style.get('stroke-width'))

        text = root.get_element_by_id('text01')
        css_style = text.get_computed_style()
        self.assertEqual(['Verdana'], css_style.get('font-family'))
        self.assertEqual(22, css_style.get('font-size'))

    def test_get_css_style04(self):
        parser = SVGParser()
        svg = '''
<svg width="5cm" height="4cm" viewBox="0 0 500 400"
     xmlns="http://www.w3.org/2000/svg">
  <style type="text/css">
    @import url(svg/style8.css);
    @media screen { /* rule (1) */
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
    .Border { fill:none; stroke:blue; stroke-width:1 }
    .Connect { fill:none; stroke:#888888; stroke-width:2 }
    .SamplePath { fill:none; stroke:red; stroke-width:5 }
    .EndPoint { fill:none; stroke:#888888; stroke-width:2 }
    .CtlPoint { fill:#888888; stroke:none }
    .AutoCtlPoint { fill:none; stroke:blue; stroke-width:4 }
    .Label { font-size:22; font-family:Verdana }
  </style>
  <text id="heading" x="-280" y="-270">
    SVG demonstration</text>
  <rect class="Border" x="1" y="1" width="498" height="398" id="rect01" />
  <polyline class="Connect" points="100,200 100,100" id="polyline01" />
  <path class="SamplePath" d="M100,200 C100,100 250,100 250,200
                                       S400,300 400,200" id="path01" />
  <circle class="EndPoint" cx="100" cy="200" r="10" id="circle01" />
  <text class="Label" x="25" y="70" id="text01">
    M100,200 C100,100 250,100 250,200</text>
</svg>
        '''
        root = parser.fromstring(svg)
        rect = root.get_element_by_id('rect01')
        css_rules = get_css_rules(rect)
        css_style, css_style_important = get_css_style(rect, css_rules)
        self.assertEqual(4, len(css_style))
        self.assertEqual(0, len(css_style_important))

        css_style = rect.get_computed_style()
        self.assertEqual('none', css_style.get('fill'))
        self.assertEqual('blue', css_style.get('stroke'))
        self.assertEqual(1, css_style.get('stroke-width'))

        text = root.get_element_by_id('heading')
        css_style = text.get_computed_style()
        self.assertEqual(24, css_style.get('font-size'),
                         msg='http server may not be working.')
        self.assertEqual(700, css_style.get('font-weight'))

    def test_load_data01(self):
        href = 'data:,Hello%2C%20World!'
        data, headers = load(href)
        content_type = get_content_type(headers)
        self.assertEqual('text/plain', content_type[None])
        self.assertEqual('US-ASCII', content_type.get('charset'))
        encoding = content_type.get('charset', 'utf-8')
        if isinstance(data, bytes):
            text = data.decode(encoding)
        else:
            text = data
        text = unquote(text)
        expected = 'Hello, World!'
        self.assertEqual(expected, text)

    def test_load_data02(self):
        href = 'data:text/plain;base64,SGVsbG8sIFdvcmxkIQ%3D%3D'
        data, headers = load(href)
        content_type = get_content_type(headers)
        self.assertEqual('text/plain', content_type[None])
        self.assertIsNone(content_type.get('charset'))
        encoding = content_type.get('charset', 'utf-8')
        if isinstance(data, bytes):
            text = data.decode(encoding)
        else:
            text = data
        text = unquote(text)
        expected = 'Hello, World!'
        self.assertEqual(expected, text)

    def test_load_data03(self):
        # see RFC 2937
        href = '''data:image/gif;base64,R0lGODdhMAAwAPAAAAAAAP///ywAAAAAMAAw
AAAC8IyPqcvt3wCcDkiLc7C0qwyGHhSWpjQu5yqmCYsapyuvUUlvONmOZtfzgFz
ByTB10QgxOR0TqBQejhRNzOfkVJ+5YiUqrXF5Y5lKh/DeuNcP5yLWGsEbtLiOSp
a/TPg7JpJHxyendzWTBfX0cxOnKPjgBzi4diinWGdkF8kjdfnycQZXZeYGejmJl
ZeGl9i2icVqaNVailT6F5iJ90m6mvuTS4OK05M0vDk0Q4XUtwvKOzrcd3iq9uis
F81M1OIcR7lEewwcLp7tuNNkM3uNna3F2JQFo97Vriy/Xl4/f1cf5VWzXyym7PH
hhx4dbgYKAAA7'''
        data, headers = load(href)
        content_type = get_content_type(headers)
        self.assertEqual('image/gif', content_type[None])
        self.assertIsNone(content_type.get('charset'))
        self.assertIsInstance(data, bytes)
        self.assertEqual(273, len(data))


if __name__ == '__main__':
    unittest.main()
