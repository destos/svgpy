#!/usr/bin/env python3

import sys
import unittest
from io import StringIO

sys.path.extend(['.', '..'])

from svgpy import Element, Font, Node, PathParser, SVGParser, \
    formatter
from svgpy.core import CSSUtils

SVG_ROTATE_SCALE = '''
<svg width="400px" height="120px" version="1.1"
     xmlns="http://www.w3.org/2000/svg">
    <desc>Example RotateScale - Rotate and scale transforms</desc>
    <g fill="none" stroke="black" stroke-width="3">
        <!-- Draw the axes of the original coordinate system -->
        <line x1="0" y1="1.5" x2="400" y2="1.5"/>
        <line x1="1.5" y1="0" x2="1.5" y2="120"/>
    </g>
    <!-- Establish a new coordinate system whose origin is at (50,30)
         in the initial coord. system and which is rotated by 30 degrees. -->
    <g transform="translate(50,30)" id="g11" class="ctm">
        <g transform="rotate(30)" id="g12" class="ctm">
            <g fill="none" stroke="red" stroke-width="3" id="g13" class="ctm">
                <line x1="0" y1="0" x2="50" y2="0"/>
                <line x1="0" y1="0" x2="0" y2="50"/>
                <path id="path01" d="M0,50 L0,0 50,0" stroke="blue"
                      stroke-dasharray="5"/>
            </g>
            <text x="0" y="0" font-size="20" font-family="Verdana" fill="blue">
                ABC (rotate)
            </text>
        </g>
    </g>
    <!-- Establish a new coordinate system whose origin is at (200,40)
         in the initial coord. system and which is scaled by 1.5. -->
    <g transform="translate(200,40)" id="g21" class="ctm">
        <g transform="scale(1.5)" id="g22" class="ctm">
            <g fill="none" stroke="red" stroke-width="3" id="g23" class="ctm">
                <line x1="0" y1="0" x2="50" y2="0"/>
                <line x1="0" y1="0" x2="0" y2="50"/>
                <path id="path02" d="M0,50 L0,0 50,0" stroke="blue"
                      stroke-dasharray="5"/>
            </g>
            <text x="0" y="0" font-size="20" font-family="Verdana" fill="blue">
                ABC (scale)
            </text>
        </g>
    </g>
</svg>
'''

SVG_RTL_TEXT = '''
<svg xmlns="http://www.w3.org/2000/svg"
     width="100%" height="100%" viewBox="0 0 600 72"
     direction="rtl" xml:lang="fa">

  <title direction="ltr" xml:lang="en">Right-to-left Text</title>
  <desc direction="ltr" xml:lang="en">
    A simple example for using the 'direction' property in documents
    that predominantly use right-to-left languages.
  </desc>

  <text x="600" y="50" text-anchor="start" 
        id="text01" font-family="Vazir"
        font-size="36">داستان SVG 1.1 SE طولا ني است.</text>

  <text x="600" y="50" text-anchor="middle" 
        id="text02" font-family="Vazir" transform="translate(0 60)"
        font-size="36">داستان SVG 1.1 SE طولا ني است.</text>

  <text x="600" y="50" text-anchor="end" 
        id="text03" font-family="Vazir" transform="translate(0 120)"
        font-size="36">داستان SVG 1.1 SE طولا ني است.</text>

</svg>
'''

SVG_TEXT01 = '''
<svg width="100%" height="100%" viewBox="0 0 1000 340"
     id="root" class="text-bbox"
     xmlns="http://www.w3.org/2000/svg">
    <g id="g01" class="text-bbox" font-family="DejaVu Sans, sans-serif"
       font-size="10">
        <g transform="translate(10 30)" font-size="larger">
            <text id="text-larger01" class="text-bbox" x="0" y="0">
                larger
            </text>

            <g transform="translate(0 50)" font-size="larger">
                <text id="text-larger02" class="text-bbox" x="0" y="0">
                    larger
                </text>

                <g transform="translate(0 50)" font-size="larger">
                    <text id="text-larger03" class="text-bbox" x="0" y="0">
                        larger
                    </text>

                    <g transform="translate(0 50)" font-size="larger">
                        <text id="text-larger04" class="text-bbox" x="0" y="0">
                            larger
                        </text>

                        <g transform="translate(0 50)" font-size="larger">
                            <text id="text-larger05" class="text-bbox" x="0"
                                  y="0">
                                larger
                            </text>

                            <g transform="translate(0 50)" font-size="larger">
                                <text id="text-larger06" class="text-bbox"
                                      x="0" y="0">
                                    larger
                                </text>

                                <g transform="translate(0 50)"
                                   font-size="larger">
                                    <text id="text-larger07" class="text-bbox"
                                          x="0" y="0">
                                        larger
                                    </text>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
        </g>
    </g>

    <g id="g02" class="text-bbox" font-family="DejaVu Sans, sans-serif"
       font-size="36"
       transform="translate(150)">
        <g transform="translate(10 30)" font-size="smaller">
            <text id="text-smaller01" class="text-bbox" x="0" y="0">
                smaller
            </text>

            <g transform="translate(0 50)" font-size="smaller">
                <text id="text-smaller02" class="text-bbox" x="0" y="0">
                    smaller
                </text>

                <g transform="translate(0 50)" font-size="smaller">
                    <text id="text-smaller03" class="text-bbox" x="0" y="0">
                        smaller
                    </text>

                    <g transform="translate(0 50)" font-size="smaller">
                        <text id="text-smaller04" class="text-bbox" x="0"
                              y="0">
                            smaller
                        </text>

                        <g transform="translate(0 50)" font-size="smaller">
                            <text id="text-smaller05" class="text-bbox" x="0"
                                  y="0">
                                smaller
                            </text>

                            <g transform="translate(0 50)" font-size="smaller">
                                <text id="text-smaller06" class="text-bbox"
                                      x="0" y="0">
                                    smaller
                                </text>

                                <g transform="translate(0 50)"
                                   font-size="smaller">
                                    <text id="text-smaller07" class="text-bbox"
                                          x="0" y="0">
                                        smaller
                                    </text>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
        </g>
    </g>
</svg>
'''

SVG_TEXT02 = '''
<svg width="100%" height="100%" viewBox="0 0 1000 340"
     id="root" class="text-bbox"
     xmlns="http://www.w3.org/2000/svg">
    <g id="g01" class="text-bbox" font-family="DejaVu Sans, sans-serif"
       font-weight="100">
        <g transform="translate(10 30)" font-weight="bolder">
            <text id="text-bolder01" class="text-bbox" x="0" y="0">
                bolder
            </text>

            <g transform="translate(0 50)" font-weight="bolder">
                <text id="text-bolder02" class="text-bbox" x="0" y="0">
                    bolder
                </text>

                <g transform="translate(0 50)" font-weight="bolder">
                    <text id="text-bolder03" class="text-bbox" x="0" y="0">
                        bolder
                    </text>

                    <g transform="translate(0 50)" font-weight="bolder">
                        <text id="text-bolder04" class="text-bbox" x="0" y="0">
                            bolder
                        </text>

                        <g transform="translate(0 50)" font-weight="bolder">
                            <text id="text-bolder05" class="text-bbox" x="0"
                                  y="0">
                                bolder
                            </text>

                            <g transform="translate(0 50)" font-weight="bolder">
                                <text id="text-bolder06" class="text-bbox"
                                      x="0" y="0">
                                    bolder
                                </text>

                                <g transform="translate(0 50)"
                                   font-weight="bolder">
                                    <text id="text-bolder07" class="text-bbox"
                                          x="0" y="0">
                                        bolder
                                    </text>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
        </g>
    </g>

    <g id="g02" class="text-bbox" font-family="DejaVu Sans, sans-serif"
       font-weight="900"
       transform="translate(150)">
        <g transform="translate(10 30)" font-weight="lighter">
            <text id="text-lighter01" class="text-bbox" x="0" y="0">
                lighter
            </text>

            <g transform="translate(0 50)" font-weight="lighter">
                <text id="text-lighter02" class="text-bbox" x="0" y="0">
                    lighter
                </text>

                <g transform="translate(0 50)" font-weight="lighter">
                    <text id="text-lighter03" class="text-bbox" x="0" y="0">
                        lighter
                    </text>

                    <g transform="translate(0 50)" font-weight="lighter">
                        <text id="text-lighter04" class="text-bbox" x="0"
                              y="0">
                            lighter
                        </text>

                        <g transform="translate(0 50)" font-weight="lighter">
                            <text id="text-lighter05" class="text-bbox" x="0"
                                  y="0">
                                lighter
                            </text>

                            <g transform="translate(0 50)" font-weight="lighter">
                                <text id="text-lighter06" class="text-bbox"
                                      x="0" y="0">
                                    lighter
                                </text>

                                <g transform="translate(0 50)"
                                   font-weight="lighter">
                                    <text id="text-lighter07" class="text-bbox"
                                          x="0" y="0">
                                        lighter
                                    </text>
                                </g>
                            </g>
                        </g>
                    </g>
                </g>
            </g>
        </g>
    </g>
</svg>
'''

SVG_TSPAN01 = '''
<svg width="100%" height="100%" viewBox="0 0 1000 400"
     xmlns="http://www.w3.org/2000/svg">
    <rect width="1000" height="400" stroke="blue" fill="none"/>
    <svg width="10cm" height="3cm" viewBox="0 0 1000 300"
         xmlns="http://www.w3.org/2000/svg">
        <g>
            <text x="250" y="180" id="text01" class="text-bbox"
                  font-family="DejaVu Serif, serif" font-size="64"
                  fill="blue" style="white-space:normal;">
                Hello, out there!
            </text>
        </g>
    </svg>

    <svg y="80" width="10cm" height="3cm" viewBox="0 0 1000 300"
         xmlns="http://www.w3.org/2000/svg">
        <g font-family="DejaVu Serif, serif" font-size="64"
           white-space="normal">
            <text x="160" y="180" fill="blue" id="text02"
                  class="text-bbox" style="white-space:normal;">
                You are
                <tspan font-weight="bold" fill="red" id="tspan0201"
                       class="text-bbox">not
                </tspan>
                a banana.
            </text>
        </g>
    </svg>

    <svg y="160" width="10cm" height="3cm" viewBox="0 0 1000 300"
         xmlns="http://www.w3.org/2000/svg">
        <g font-family="DejaVu Serif, serif" font-size="64"
           white-space="normal">
            <text x="100" y="180" fill="blue" id="text03"
                  class="text-bbox" style="white-space:normal;">
                But you
                <tspan dx="2em" dy="-50" font-weight="bold" fill="red"
                       id="tspan0301" class="text-bbox">
                    are
                </tspan>
                <tspan dy="100" id="tspan0302" class="text-bbox">
                    a peach!
                </tspan>
            </text>
        </g>
    </svg>
</svg>
'''

SVG_TSPAN04 = '''
<svg width="10cm" height="3cm" viewBox="0 0 1000 300"
     xmlns="http://www.w3.org/2000/svg" version="1.1">
    <desc>
        Example tspan04 - The number of rotate values is less than the number of
        characters in the string.
    </desc>
    <text font-family="DejaVu Sans, sans-serif" font-size="55" fill="blue"
          id="text01" class="text-bbox">
    <tspan x="250" y="150" rotate="-30,0,30" id="tspan01" class="text-bbox">
        Hello, out there
    </tspan>
    </text>
    <!-- Show outline of viewport using 'rect' element -->
    <rect x="1" y="1" width="998" height="298"
          fill="none" stroke="blue" stroke-width="2" />
</svg>
'''

SVG_TSPAN05 = '''
<svg width="100%" height="100%" viewBox="0 0 700 120"
  xmlns="http://www.w3.org/2000/svg" version="1.1">
  <desc>
    Example tspan05 - propagation of rotation values to nested tspan elements.
  </desc>
  <text id="parent" font-family="DejaVu Sans, sans-serif" font-size="32" fill="red" x="40" y="40"
    rotate="5,15,25,35,45,55">
    Not

    <tspan id="child1" rotate="-10,-20,-30,-40" fill="orange">
      all characters

      <tspan id="child2" rotate="70,60,50,40,30,20,10" fill="yellow">
        in
        
        <tspan id="child3">
          the
        </tspan>
      </tspan>

      <tspan id="child4" fill="orange" x="40" y="90">
        text
      </tspan>

      have a
    </tspan>

    <tspan id="child5" rotate="-10" fill="blue">
      specified
    </tspan>

    rotation
  </text>

  <!-- Show outline of viewport using 'rect' element -->
  <rect x="1" y="1" width="598" height="118" fill="none"
        stroke="blue" stroke-width="2" />
</svg>
'''

places = 1
delta = 1.5


# Test with: Chrome 64.0 (Linux 64-bit)
class TextTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 6
        Font.default_font_size = 16
        self.maxDiff = None

    def test_font_face01(self):
        from svgpy.freetype import FreeType
        from svgpy import Matrix

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, DejaVu Serif, serif',
            'font-style': 'oblique',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
        })
        text = group.create_sub_element('text')

        font = Font(text)
        face = font.face
        ch = '\u6c34'
        face.load_char(ch, FreeType.FT_LOAD_NO_BITMAP)
        bbox = face.glyph.outline.get_bbox()
        self.assertTrue(bbox.isvalid(), msg=repr(bbox))

        matrix = Matrix()
        matrix.rotate_self(rot_z=45)
        matrix.translate_self(10)
        path_data = PathParser.fromglyph(face, matrix)
        self.assertTrue(len(path_data) > 0)
        normalized = PathParser.normalize(path_data)
        rect = PathParser.get_bbox(normalized)
        self.assertTrue(rect.isvalid(), msg=repr(rect))

    def test_font_prop01(self):
        # 'font' property
        # https://drafts.csswg.org/css-fonts-3/#font-prop
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'Helvetica, Verdana, sans-serif',
            'font-style': 'oblique',
            'font-variant': 'small-caps',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
            'line-height': '1.5',
            'font-size-adjust': '0.5',
            'font-kerning': 'none',
            'font-language-override': 'SRB',
        })
        text = group.create_sub_element('text')

        # font-size/line-height | font-family
        text.attributes.set('font', '12pt/14pt sans-serif')
        style = text.get_computed_style()

        expected = ['sans-serif']
        self.assertEqual(expected, style['font-family'])

        self.assertEqual('normal', style['font-style'])
        self.assertEqual('normal', style['font-variant'])
        self.assertEqual(400, style['font-weight'])
        self.assertEqual('normal', style['font-stretch'])

        # font-size: 12(pt) = 12(pt) * 4 / 3 = 16(px)
        expected = 12 * 4 / 3
        self.assertEqual(expected, style['font-size'])

        # line-height: 14(pt) = 14(pt) * 4 / 3 = 18.6666...(px)
        expected = 14 * 4 / 3
        self.assertEqual(expected, style['line-height'])

        self.assertEqual('none', style['font-size-adjust'])
        self.assertEqual('auto', style['font-kerning'])
        self.assertEqual('normal', style['font-language-override'])

    def test_font_prop02(self):
        # 'font' property
        # https://drafts.csswg.org/css-fonts-3/#font-prop
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'Helvetica, Verdana, sans-serif',
            'font-style': 'oblique',
            'font-variant': 'small-caps',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
            'line-height': '1.5',
            'font-size-adjust': '0.5',
            'font-kerning': 'none',
            'font-language-override': 'SRB',
        })
        text = group.create_sub_element('text')

        text.attributes.set('font', '80% sans-serif')
        style = text.get_computed_style()

        expected = ['sans-serif']
        self.assertEqual(expected, style['font-family'])

        self.assertEqual('normal', style['font-style'])
        self.assertEqual('normal', style['font-variant'], )
        self.assertEqual(400, style['font-weight'])
        self.assertEqual('normal', style['font-stretch'])

        # font-size: 20(px) * 0.8 = 16(px)
        expected = 20 * 0.8
        self.assertEqual(expected, style['font-size'])

        # line-height: 16(px) * 1.2 = 19.2
        expected = 16 * 1.2
        self.assertEqual(expected, style['line-height'])

        self.assertEqual('none', style['font-size-adjust'])
        self.assertEqual('auto', style['font-kerning'])
        self.assertEqual('normal', style['font-language-override'])

    def test_font_prop03(self):
        # 'font' property
        # https://drafts.csswg.org/css-fonts-3/#font-prop
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'Helvetica, Verdana, sans-serif',
            'font-style': 'oblique',
            'font-variant': 'small-caps',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
            'line-height': '1.5',
            'font-size-adjust': '0.5',
            'font-kerning': 'none',
            'font-language-override': 'SRB',
        })
        text = group.create_sub_element('text')

        text.attributes.set('font',
                            'x-large/110% "new century schoolbook", serif')
        style = text.get_computed_style()

        expected = ['new century schoolbook', 'serif']
        self.assertEqual(expected, style['font-family'])

        self.assertEqual('normal', style['font-style'])
        self.assertEqual('normal', style['font-variant'])
        self.assertEqual(400, style['font-weight'])
        self.assertEqual('normal', style['font-stretch'])

        # default font size: 16(px)
        # font-size: x-large = 24(px)
        expected = 24
        self.assertEqual(expected, style['font-size'])

        # line-height: 24(px) * 1.10 = 26.4(px)
        expected = 24 * 1.1
        self.assertEqual(expected, style['line-height'])

        self.assertEqual('none', style['font-size-adjust'])
        self.assertEqual('auto', style['font-kerning'])
        self.assertEqual('normal', style['font-language-override'])

    def test_font_prop04(self):
        # 'font' property
        # https://drafts.csswg.org/css-fonts-3/#font-prop
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'Helvetica, Verdana, sans-serif',
            'font-style': 'oblique',
            'font-variant': 'small-caps',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
            'line-height': '1.5',
            'font-size-adjust': '0.5',
            'font-kerning': 'none',
            'font-language-override': 'SRB',
        })
        text = group.create_sub_element('text')

        text.attributes.set('font', 'bold italic large Palatino, serif')
        style = text.get_computed_style()

        expected = ['Palatino', 'serif']
        self.assertEqual(expected, style['font-family'])

        # font-style: italic
        self.assertEqual('italic', style['font-style'])

        self.assertEqual('normal', style['font-variant'])

        # font-weight: bold = 700
        self.assertEqual(700, style['font-weight'])

        self.assertEqual('normal', style['font-stretch'])

        # default font size: 16(px)
        # font-size: large = 18(px)
        expected = 18
        self.assertEqual(expected, style['font-size'])

        # line-height: 18(px) * 1.2 = 21.6(px)
        expected = 18 * 1.2
        self.assertEqual(expected, style['line-height'])

        self.assertEqual('none', style['font-size-adjust'])
        self.assertEqual('auto', style['font-kerning'])
        self.assertEqual('normal', style['font-language-override'])

    def test_font_prop05(self):
        # 'font' property
        # https://drafts.csswg.org/css-fonts-3/#font-prop
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'Helvetica, Verdana, sans-serif',
            'font-style': 'oblique',
            'font-variant': 'small-caps',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
            'line-height': '1.5',
            'font-size-adjust': '0.5',
            'font-kerning': 'none',
            'font-language-override': 'SRB',
        })
        text = group.create_sub_element('text')

        text.attributes.set('font', 'normal small-caps 120%/120% fantasy')
        style = text.get_computed_style()

        expected = ['fantasy']
        self.assertEqual(expected, style['font-family'])

        self.assertEqual('normal', style['font-style'])
        self.assertEqual('small-caps', style['font-variant'])
        self.assertEqual(400, style['font-weight'])
        self.assertEqual('normal', style['font-stretch'])

        # font-size: 20(px) * 1.2 = 24(px)
        expected = 20 * 1.2
        self.assertEqual(expected, style['font-size'])

        # line-height: 24(px) * 1.2 = 28.8(px)
        expected = 24 * 1.2
        self.assertEqual(expected, style['line-height'])

        self.assertEqual('none', style['font-size-adjust'])
        self.assertEqual('auto', style['font-kerning'])
        self.assertEqual('normal', style['font-language-override'])

    def test_font_prop06(self):
        # 'font' property
        # https://drafts.csswg.org/css-fonts-3/#font-prop
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'Helvetica, Verdana, sans-serif',
            'font-style': 'oblique',
            'font-variant': 'small-caps',
            'font-weight': '800',
            'font-stretch': 'expanded',
            'font-size': '20',
            'line-height': '1.5',
            'font-size-adjust': '0.5',
            'font-kerning': 'none',
            'font-language-override': 'SRB',
        })
        text = group.create_sub_element('text')

        text.attributes.set('font',
                            'condensed oblique 12pt "Helvetica Neue", serif')
        style = text.get_computed_style()

        expected = ['Helvetica Neue', 'serif']
        self.assertEqual(expected, style['font-family'])

        self.assertEqual('oblique', style['font-style'])
        self.assertEqual('normal', style['font-variant'])
        self.assertEqual(400, style['font-weight'])
        self.assertEqual('condensed', style['font-stretch'])

        # font-size: 12(pt) = 12 * 4 / 3 = 16(px)
        expected = 12 * 4 / 3
        self.assertEqual(expected, style['font-size'])

        # line-height: 16(px) * 1.2 = 19.2(px)
        expected = 16 * 1.2
        self.assertEqual(expected, style['line-height'])

        self.assertEqual('none', style['font-size-adjust'])
        self.assertEqual('auto', style['font-kerning'])
        self.assertEqual('normal', style['font-language-override'])
        # text = '100 "new century schoolbook", serif'
        # text = '100 "new century schoolbook",serif'
        # text = '"new century schoolbook", serif'

        # text = '2em "Open Sans", sans-serif'
        # text = 'italic 2em "Open Sans", sans-serif'
        # text = 'italic small-caps bolder 16px/3 cursive'
        # text = 'italic small-caps bolder condensed 16px/3 cursive'
        # text = 'message-box'
        # text = 'icon'

    def test_font_size_prop01(self):
        # 'font-size' property: absolute-size
        # See also: length01.html
        Font.default_font_size = 16
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')

        text.attributes.set('font-size', 'xx-small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'x-small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'small')
        style = text.get_computed_style()
        self.assertEqual(13, style['font-size'])

        text.attributes.set('font-size', 'medium')
        style = text.get_computed_style()
        self.assertEqual(16, style['font-size'])

        text.attributes.set('font-size', 'large')
        style = text.get_computed_style()
        self.assertEqual(18, style['font-size'])

        text.attributes.set('font-size', 'x-large')
        style = text.get_computed_style()
        self.assertEqual(24, style['font-size'])

        text.attributes.set('font-size', 'xx-large')
        style = text.get_computed_style()
        self.assertEqual(32, style['font-size'])

    def test_font_size_prop02(self):
        # 'font-size' property: absolute-size
        # See also: length01.html
        Font.default_font_size = 10
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')

        text.attributes.set('font-size', 'xx-small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'x-small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'medium')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'large')
        style = text.get_computed_style()
        self.assertEqual(11, style['font-size'])

        text.attributes.set('font-size', 'x-large')
        style = text.get_computed_style()
        self.assertEqual(14, style['font-size'])

        text.attributes.set('font-size', 'xx-large')
        style = text.get_computed_style()
        self.assertEqual(18, style['font-size'])

    def test_font_size_prop03(self):
        # 'font-size' property: absolute-size
        # See also: length01.html
        Font.default_font_size = 12
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')

        text.attributes.set('font-size', 'xx-small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'x-small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'small')
        style = text.get_computed_style()
        self.assertEqual(10, style['font-size'])

        text.attributes.set('font-size', 'medium')
        style = text.get_computed_style()
        self.assertEqual(12, style['font-size'])

        text.attributes.set('font-size', 'large')
        style = text.get_computed_style()
        self.assertEqual(14, style['font-size'])

        text.attributes.set('font-size', 'x-large')
        style = text.get_computed_style()
        self.assertEqual(18, style['font-size'])

        text.attributes.set('font-size', 'xx-large')
        style = text.get_computed_style()
        self.assertEqual(24, style['font-size'])

    def test_font_size_prop04(self):
        # 'font-size' property: absolute-size
        # See also: length01.html
        Font.default_font_size = 20
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')

        text.attributes.set('font-size', 'xx-small')
        style = text.get_computed_style()
        self.assertEqual(12, style['font-size'])

        text.attributes.set('font-size', 'x-small')
        style = text.get_computed_style()
        self.assertEqual(15, style['font-size'])

        text.attributes.set('font-size', 'small')
        style = text.get_computed_style()  # 17.7777...
        self.assertAlmostEqual(17.8, style['font-size'], places=places)

        text.attributes.set('font-size', 'medium')
        style = text.get_computed_style()
        self.assertEqual(20, style['font-size'])

        text.attributes.set('font-size', 'large')
        style = text.get_computed_style()
        self.assertEqual(24, style['font-size'])

        text.attributes.set('font-size', 'x-large')
        style = text.get_computed_style()
        self.assertEqual(30, style['font-size'])

        text.attributes.set('font-size', 'xx-large')
        style = text.get_computed_style()
        self.assertEqual(40, style['font-size'])

    def test_font_size_prop05(self):
        # 'font-size' property: absolute-size
        # See also: length01.html
        Font.default_font_size = 24
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')

        text.attributes.set('font-size', 'xx-small')
        style = text.get_computed_style()
        self.assertAlmostEqual(14.4, style['font-size'])

        text.attributes.set('font-size', 'x-small')
        style = text.get_computed_style()
        self.assertEqual(18, style['font-size'])

        text.attributes.set('font-size', 'small')
        style = text.get_computed_style()  # 21.3333...
        self.assertAlmostEqual(21.36, style['font-size'], places=places)

        text.attributes.set('font-size', 'medium')
        style = text.get_computed_style()
        self.assertEqual(24, style['font-size'])

        text.attributes.set('font-size', 'large')
        style = text.get_computed_style()
        self.assertAlmostEqual(28.8, style['font-size'])

        text.attributes.set('font-size', 'x-large')
        style = text.get_computed_style()
        self.assertEqual(36, style['font-size'])

        text.attributes.set('font-size', 'xx-large')
        style = text.get_computed_style()
        self.assertEqual(48, style['font-size'])

    def test_font_size_prop06(self):
        # 'font-size' property: relative-size
        # See also: text01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TEXT01))
        root = tree.getroot()

        # <g font-size="10">
        group = root.get_element_by_id('g01')
        style = group.get_computed_style()
        expected = 10
        self.assertEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger01')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger02')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger03')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger04')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger05')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger06')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="10">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        # <g font-size="larger">
        text = root.get_element_by_id('text-larger07')
        style = text.get_computed_style()
        expected *= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

    def test_font_size_prop07(self):
        # 'font-size' property: relative-size
        # See also: text01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TEXT01))
        root = tree.getroot()

        # <g font-size="36">
        group = root.get_element_by_id('g02')
        style = group.get_computed_style()
        expected = 36
        self.assertEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller01')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller02')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller03')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller04')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller05')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller06')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

        # <g font-size="36">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        # <g font-size="smaller">
        text = root.get_element_by_id('text-smaller07')
        style = text.get_computed_style()
        expected /= 1.2
        self.assertAlmostEqual(expected, style['font-size'])

    def test_font_variant_prop00(self):
        # font-variant: normal
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')

        style = text.get_computed_style()
        self.assertEqual('normal', style['font-variant'])
        self.assertEqual(['normal'], style['font-variant-alternates'])
        self.assertEqual('normal', style['font-variant-caps'])
        self.assertEqual(['normal'], style['font-variant-east-asian'])
        self.assertEqual(['normal'], style['font-variant-ligatures'])
        self.assertEqual(['normal'], style['font-variant-numeric'])
        self.assertEqual('normal', style['font-variant-position'])

    def test_font_variant_prop01(self):
        # font-variant: normal
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-variant': 'normal',
        })

        style = text.get_computed_style()
        self.assertEqual('normal', style['font-variant'])
        self.assertEqual(['normal'], style['font-variant-alternates'])
        self.assertEqual('normal', style['font-variant-caps'])
        self.assertEqual(['normal'], style['font-variant-east-asian'])
        self.assertEqual(['normal'], style['font-variant-ligatures'])
        self.assertEqual(['normal'], style['font-variant-numeric'])
        self.assertEqual('normal', style['font-variant-position'])

    def test_font_variant_prop02(self):
        # font-variant: none
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-variant': 'none',
        })

        style = text.get_computed_style()
        self.assertEqual('none', style['font-variant'])
        self.assertEqual(['normal'], style['font-variant-alternates'])
        self.assertEqual('normal', style['font-variant-caps'])
        self.assertEqual(['normal'], style['font-variant-east-asian'])
        self.assertEqual(['none'], style['font-variant-ligatures'])
        self.assertEqual(['normal'], style['font-variant-numeric'])
        self.assertEqual('normal', style['font-variant-position'])

    def test_font_variant_prop03(self):
        # font-variant: ...
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-variant':
                'common-ligatures discretionary-ligatures historical-ligatures'
                ' contextual historical-forms all-small-caps'
                ' lining-nums proportional-nums diagonal-fractions ordinal'
                ' slashed-zero traditional proportional-width'
                ' ruby super',
        })

        style = text.get_computed_style()
        # self.assertEqual(style['font-variant'], 'none')
        self.assertEqual(['historical-forms'],
                         style['font-variant-alternates'],
                         msg='font-variant-alternates')
        self.assertEqual('all-small-caps',
                         style['font-variant-caps'],
                         msg='font-variant-caps')
        self.assertEqual(['traditional', 'proportional-width', 'ruby'],
                         style['font-variant-east-asian'],
                         msg='font-variant-east-asian')
        self.assertEqual(['common-ligatures', 'discretionary-ligatures',
                          'historical-ligatures', 'contextual'],
                         style['font-variant-ligatures'],
                         msg='font-variant-ligatures')
        self.assertEqual(['lining-nums', 'proportional-nums',
                          'diagonal-fractions', 'ordinal', 'slashed-zero'],
                         style['font-variant-numeric'],
                         msg='font-variant-numeric')
        self.assertEqual('super',
                         style['font-variant-position'],
                         msg='font-variant-position')

    def test_font_variant_prop04(self):
        # font: small-caps 16px serif
        # -> font-variant-caps: small-caps
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-variant-caps': 'all-small-caps',
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font': 'small-caps 16px serif',
        })

        style = text.get_computed_style()
        self.assertEqual('small-caps', style['font-variant'])
        self.assertEqual(['normal'], style['font-variant-alternates'])
        self.assertEqual('small-caps', style['font-variant-caps'])
        self.assertEqual(['normal'], style['font-variant-east-asian'])
        self.assertEqual(['normal'], style['font-variant-ligatures'])
        self.assertEqual(['normal'], style['font-variant-numeric'])
        self.assertEqual('normal', style['font-variant-position'])

    def test_font_variant_prop05(self):
        # font: small-caps 16px serif
        # -> font-variant-caps: small-caps
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font': 'small-caps 16px serif',
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-variant-east-asian': 'jis78 proportional-width',
        })

        style = text.get_computed_style()
        self.assertEqual('small-caps', style['font-variant'])
        self.assertEqual(['normal'], style['font-variant-alternates'])
        self.assertEqual('small-caps', style['font-variant-caps'])
        self.assertEqual(['jis78', 'proportional-width'],
                         style['font-variant-east-asian'])
        self.assertEqual(['normal'], style['font-variant-ligatures'])
        self.assertEqual(['normal'], style['font-variant-numeric'])
        self.assertEqual('normal', style['font-variant-position'])

    def test_font_weight_prop01(self):
        # 'font-weight' property
        # See also: text02.html
        # https://drafts.csswg.org/css-fonts-3/#font-weight-prop
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TEXT02))
        root = tree.getroot()

        # <g font-weight="100">
        group = root.get_element_by_id('g01')
        style = group.get_computed_style()
        self.assertEqual(100, style['font-weight'])

        # <g font-weight="100">
        # <g font-weight="bolder">
        text = root.get_element_by_id('text-bolder01')
        # 100 -> 400
        style = text.get_computed_style()
        self.assertAlmostEqual(400, style['font-weight'])

        # <g font-weight="100">
        # <g font-weight="bolder">
        # <g font-weight="bolder">
        text = root.get_element_by_id('text-bolder02')
        # 100 -> 400 -> 700
        style = text.get_computed_style()
        self.assertAlmostEqual(700, style['font-weight'])

        # <g font-weight="100">
        # <g font-weight="bolder">
        # <g font-weight="bolder">
        # <g font-weight="bolder">
        text = root.get_element_by_id('text-bolder03')
        # 100 -> 400 -> 700 -> 900
        style = text.get_computed_style()
        self.assertAlmostEqual(900, style['font-weight'])

        # <g font-weight="100">
        # <g font-weight="bolder">
        # <g font-weight="bolder">
        # <g font-weight="bolder">
        # <g font-weight="bolder">
        text = root.get_element_by_id('text-bolder04')
        # 100 -> 400 -> 700 -> 900 -> 900
        style = text.get_computed_style()
        self.assertAlmostEqual(900, style['font-weight'])

    def test_font_weight_prop02(self):
        # 'font-weight' property
        # See also: text02.html
        # https://drafts.csswg.org/css-fonts-3/#font-weight-prop
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TEXT02))
        root = tree.getroot()

        # <g font-weight="900">
        group = root.get_element_by_id('g02')
        style = group.get_computed_style()
        self.assertEqual(900, style['font-weight'])

        # <g font-weight="900">
        # <g font-weight="lighter">
        text = root.get_element_by_id('text-lighter01')
        # 900 -> 700
        style = text.get_computed_style()
        self.assertAlmostEqual(700, style['font-weight'])

        # <g font-weight="900">
        # <g font-weight="lighter">
        # <g font-weight="lighter">
        text = root.get_element_by_id('text-lighter02')
        # 900 -> 700 -> 400
        style = text.get_computed_style()
        self.assertAlmostEqual(400, style['font-weight'])

        # <g font-weight="900">
        # <g font-weight="lighter">
        # <g font-weight="lighter">
        # <g font-weight="lighter">
        text = root.get_element_by_id('text-lighter03')
        # 900 -> 700 -> 400 > 100
        style = text.get_computed_style()
        self.assertAlmostEqual(100, style['font-weight'])

        # <g font-weight="900">
        # <g font-weight="lighter">
        # <g font-weight="lighter">
        # <g font-weight="lighter">
        # <g font-weight="lighter">
        text = root.get_element_by_id('text-lighter04')
        # 900 -> 700 -> 400 > 100 > 100
        style = text.get_computed_style()
        self.assertAlmostEqual(100, style['font-weight'])

    def test_get_bbox_tspan01(self):
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()
        text = root.get_element_by_id('text01')

        bbox = text.get_bbox()
        x = 250
        y = 119.813
        width = 538.531
        height = 75.219
        self.assertAlmostEqual(x, bbox.x, delta=delta)
        self.assertAlmostEqual(y, bbox.y, delta=delta)
        self.assertAlmostEqual(width, bbox.width, delta=delta)
        self.assertAlmostEqual(height, bbox.height, delta=delta)

    def test_get_bbox_tspan04(self):
        # See also: tspan04.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN04))
        root = tree.getroot()
        text = root.get_element_by_id('text01')

        bbox = text.get_bbox()
        x = 224.859
        y = 85.781
        width = 473.547
        height = 93.094
        self.assertAlmostEqual(x, bbox.x, delta=delta)
        self.assertAlmostEqual(y, bbox.y, delta=delta)  # 86 vs. 85
        self.assertAlmostEqual(width, bbox.width, delta=delta)
        self.assertAlmostEqual(height, bbox.height, delta=delta)

    def test_get_bbox_tspan05(self):
        # See also: tspan05.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN05))
        root = tree.getroot()
        text = root.get_element_by_id('parent')

        bbox = text.get_bbox()
        x = 20.891
        y = 4.188
        width = 505.563
        height = 106.594
        self.assertAlmostEqual(x, bbox.x, delta=delta)
        self.assertAlmostEqual(y, bbox.y, delta=delta)
        self.assertAlmostEqual(width, bbox.width, delta=delta)
        self.assertAlmostEqual(height, bbox.height, delta=delta)

    def test_get_computed_text_length_tspan04(self):
        # See also: tspan04.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN04))
        root = tree.getroot()
        text = root.get_element_by_id('text01')

        length = text.get_computed_text_length()  # 427.46875
        expected = 428.52801513671875
        self.assertAlmostEqual(expected, length, delta=delta)

    def test_get_computed_text_length_tspan05(self):
        # See also: tspan05.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN05))
        root = tree.getroot()
        text = root.get_element_by_id('parent')

        length = text.get_computed_text_length()  # 866.671875
        expected = 867.9374389648438
        self.assertAlmostEqual(expected, length, delta=delta)

    def test_get_number_of_chars_tspan01(self):
        # SVGTextContentElement#getNumberOfChars()
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text01')

        # chars = text.get_chars()
        # expected = 'Hello, out there!'
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 17
        self.assertEqual(expected, n)

    def test_get_number_of_chars_tspan01_02(self):
        # SVGTextContentElement#getNumberOfChars()
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text02')

        # chars = text.get_chars()
        # expected = 'You are not a banana.'
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 21
        self.assertEqual(expected, n)

    def test_get_number_of_chars_tspan01_02_01(self):
        # SVGTextContentElement#getNumberOfChars()
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('tspan0201')

        # chars = text.get_chars()
        # expected = 'not '
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 4
        self.assertEqual(expected, n)

    def test_get_number_of_chars_tspan01_03(self):
        # SVGTextContentElement#getNumberOfChars()
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text03')

        # chars = text.get_chars()
        # expected = 'But you are a peach!'
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 20
        self.assertEqual(expected, n)

    def test_get_number_of_chars_tspan01_03_01(self):
        # SVGTextContentElement#getNumberOfChars()
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('tspan0301')

        # chars = text.get_chars()
        # expected = 'are '
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 4
        self.assertEqual(expected, n)

    def test_get_number_of_chars_tspan01_03_02(self):
        # SVGTextContentElement#getNumberOfChars()
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('tspan0302')

        # chars = text.get_chars()
        # expected = 'a peach!'
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 8
        self.assertEqual(expected, n)

    def test_get_number_of_chars_tspan05(self):
        # See also: tspan05.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN05))
        root = tree.getroot()

        text = root.get_element_by_id('parent')

        # chars = text.get_chars()
        # expected = 'a peach!'
        # self.assertEqual(expected, chars)

        n = text.get_number_of_chars()
        expected = 56
        self.assertEqual(expected, n)

    def _test_get_path_data00(self):
        parser = SVGParser()
        root = parser.create_element('svg',
                                   nsmap={'xml': Element.XML_NAMESPACE_URI})
        # root = parser.create_element('svg')
        root.attributes.update({
            # '{http://www.w3.org/XML/1998/namespace}lang': 'ja',
            Element.XML_LANG: 'ja',
        })
        group = root.create_sub_element('g')
        group.attributes.update({
            # 'font-family': 'IPAmjMincho, serif',
            'font-family': 'DejaVu Serif, serif',
            'font-size': '18',
            # 'font-weight': 'bold',
            # 'font-style': 'italic'
        })
        text = group.create_sub_element('text')
        # text.text = 'Hello World!'
        # text.text = '春は\n\tあけぼの。'
        text.text = 'office'
        text.attributes.update({
            'x': '10, 20, 30, 40, 50, 60',
            'dx': '110, 120, 130, 140, 150, 160',
            'y': '0',
            'rotate': '0',
            # 'writing-mode': 'vertical-rl',
            'font-kerning': 'auto',
            'style': 'white-space:pre;',
        })
        # x: o(10) ff(20) i(40) c(50) e(60)
        # dx: o(110) ff(120) i(130+140) c(150) e(160)
        print(root.tostring(encoding='unicode'))

        path_data = text.get_path_data()
        # print([PathParser.tostring(path_data)])

    # @unittest.expectedFailure
    def test_get_path_data_tspan01(self):
        # See also: tspan01.html
        # Test with DejaVu font 2.37, FontConfig 2.12.6, and FreeType 2.8
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text01')
        path_data = text.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M253.53,180 L253.53,177 259.47,177 259.47,136 253.53,136" \
            " 253.53,133 271.75,133 271.75,136 265.81,136 265.81,153" \
            " 290,153 290,136 284.06,136 284.06,133 302.28,133 302.28,136" \
            " 296.34,136 296.34,177 302.28,177 302.28,180 284.06,180" \
            " 284.06,177 290,177 290,156 265.81,156 265.81,177 271.75,177" \
            " 271.75,180 253.53,180 M340.5,164 L315.72,164 315.72,164.25" \
            " Q315.72,171.06 318.25,174.53 320.78,178 325.72,178 329.5,178" \
            " 331.92,175.98 334.34,173.97 335.31,170 L339.94,170" \
            " Q338.56,175.48 334.86,178.23 331.16,181 325.12,181" \
            " 317.84,181 313.42,176.2 309,171.42 309,163.48 309,155.61" \
            " 313.34,150.8 317.69,146 324.75,146 332.28,146 336.31,150.61" \
            " 340.34,155.22 340.5,164 M333.72,161 Q333.53,155.05" \
            " 331.27,152.02 329,149 324.75,149 320.78,149 318.5,152.03" \
            " 316.22,155.08 315.72,161 L333.72,161 M356.81,177 L362.25,177" \
            " 362.25,180 345.53,180 345.53,177 351.06,177 351.06,134" \
            " 345.53,134 345.53,131 356.81,131 356.81,177 M377.28,177" \
            " L382.72,177 382.72,180 366,180 366,177 371.53,177 371.53,134" \
            " 366,134 366,131 377.28,131 377.28,177 M403.88,178 Q408.5,178" \
            " 410.86,174.31 413.22,170.64 413.22,163.48 413.22,156.33" \
            " 410.86,152.66 408.5,149 403.88,149 399.25,149 396.89,152.66" \
            " 394.53,156.33 394.53,163.48 394.53,170.64 396.91,174.31" \
            " 399.28,178 403.88,178 M403.88,181 Q396.62,181 392.22,176.2" \
            " 387.81,171.42 387.81,163.48 387.81,155.55 392.2,150.77" \
            " 396.59,146 403.88,146 411.16,146 415.55,150.77 419.94,155.55" \
            " 419.94,163.48 419.94,171.42 415.55,176.2 411.16,181" \
            " 403.88,181 M425.47,186.47 Q428.41,184.28 429.78,181.33" \
            " 431.16,178.38 431.16,174.17 L431.16,173 437.31,173" \
            " Q437.06,178.41 434.8,182.28 432.53,186.16 427.97,189" \
            " L425.47,186.47 M483.09,178 Q487.72,178 490.08,174.31" \
            " 492.44,170.64 492.44,163.48 492.44,156.33 490.08,152.66" \
            " 487.72,149 483.09,149 478.47,149 476.11,152.66 473.75,156.33" \
            " 473.75,163.48 473.75,170.64 476.12,174.31 478.5,178" \
            " 483.09,178 M483.09,181 Q475.84,181 471.44,176.2" \
            " 467.03,171.42 467.03,163.48 467.03,155.55 471.42,150.77" \
            " 475.81,146 483.09,146 490.38,146 494.77,150.77 499.16,155.55" \
            " 499.16,163.48 499.16,171.42 494.77,176.2 490.38,181" \
            " 483.09,181 M525.03,147 L535.78,147 535.78,177 541.22,177" \
            " 541.22,180 530.03,180 530.03,174.39 Q528.44,177.62" \
            " 525.91,179.31 523.38,181 520.03,181 514.5,181 511.89,177.88" \
            " 509.28,174.75 509.28,168.08 L509.28,150 504.09,150" \
            " 504.09,147 515.06,147 515.06,166.27 Q515.06,172.42" \
            " 516.55,174.7 518.03,177 521.84,177 525.84,177 527.94,174.02" \
            " 530.03,171.03 530.03,165.34 L530.03,150 525.03,150" \
            " 525.03,147 M550.5,150 L545.44,150 545.44,147 550.5,147" \
            " 550.5,137 556.28,137 556.28,147 567.09,147 567.09,150" \
            " 556.28,150 556.28,171.03 Q556.28,175.48 557.09,176.73" \
            " 557.91,178 560.09,178 562.34,178 563.38,176.58 564.41,175.17" \
            " 564.47,172 L568.81,172 Q568.56,176.67 566.34,178.83" \
            " 564.12,181 559.59,181 554.62,181 552.56,178.73 550.5,176.47" \
            " 550.5,171.03 L550.5,150 M596.56,150 L591.5,150 591.5,147" \
            " 596.56,147 596.56,137 602.34,137 602.34,147 613.16,147" \
            " 613.16,150 602.34,150 602.34,171.03 Q602.34,175.48" \
            " 603.16,176.73 603.97,178 606.16,178 608.41,178 609.44,176.58" \
            " 610.47,175.17 610.53,172 L614.88,172 Q614.62,176.67" \
            " 612.41,178.83 610.19,181 605.66,181 600.69,181 598.62,178.73" \
            " 596.56,176.47 596.56,171.03 L596.56,150 M618,180 L618,177" \
            " 623.19,177 623.19,134 617.69,134 617.69,131 628.94,131" \
            " 628.94,152.61 Q630.53,149.33 633.08,147.66 635.62,146" \
            " 639,146 644.5,146 647.09,149.12 649.69,152.27 649.69,158.89" \
            " L649.69,177 654.81,177 654.81,180 638.94,180 638.94,177" \
            " 643.91,177 643.91,160.73 Q643.91,154.55 642.42,152.27" \
            " 640.94,150 637.12,150 633.12,150 631.03,152.95 628.94,155.91" \
            " 628.94,161.56 L628.94,177 633.94,177 633.94,180 618,180" \
            " M691.28,164 L666.5,164 666.5,164.25 Q666.5,171.06" \
            " 669.03,174.53 671.56,178 676.5,178 680.28,178 682.7,175.98" \
            " 685.12,173.97 686.09,170 L690.72,170 Q689.34,175.48" \
            " 685.64,178.23 681.94,181 675.91,181 668.62,181 664.2,176.2" \
            " 659.78,171.42 659.78,163.48 659.78,155.61 664.12,150.8" \
            " 668.47,146 675.53,146 683.06,146 687.09,150.61 691.12,155.22" \
            " 691.28,164 M684.5,161 Q684.31,155.05 682.05,152.02" \
            " 679.78,149 675.53,149 671.56,149 669.28,152.03 667,155.08" \
            " 666.5,161 L684.5,161 M725.06,147 L725.06,155 721.75,155" \
            " Q721.59,152.48 720.38,151.23 719.16,150 716.81,150" \
            " 712.56,150 710.3,152.98 708.03,155.98 708.03,161.58" \
            " L708.03,177 714.69,177 714.69,180 697.09,180 697.09,177" \
            " 702.28,177 702.28,150 696.78,150 696.78,147 708.03,147" \
            " 708.03,152.61 Q709.72,149.25 712.38,147.62 715.03,146" \
            " 718.84,146 720.25,146 721.8,146.25 723.34,146.52 725.06,147" \
            " M759.75,164 L734.97,164 734.97,164.25 Q734.97,171.06" \
            " 737.5,174.53 740.03,178 744.97,178 748.75,178 751.17,175.98" \
            " 753.59,173.97 754.56,170 L759.19,170 Q757.81,175.48" \
            " 754.11,178.23 750.41,181 744.38,181 737.09,181 732.67,176.2" \
            " 728.25,171.42 728.25,163.48 728.25,155.61 732.59,150.8" \
            " 736.94,146 744,146 751.53,146 755.56,150.61 759.59,155.22" \
            " 759.75,164 M752.97,161 Q752.78,155.05 750.52,152.02" \
            " 748.25,149 744,149 740.03,149 737.75,152.03 735.47,155.08" \
            " 734.97,161 L752.97,161 M771.66,177.02 Q771.66,175.34" \
            " 772.84,174.17 774.03,173 775.81,173 777.53,173 778.75,174.17" \
            " 779.97,175.34 779.97,177.02 779.97,178.66 778.75,179.83" \
            " 777.53,181 775.81,181 774.03,181 772.84,179.84 771.66,178.69" \
            " 771.66,177.02 M771.78,133 L779.84,133 777.72,159.02" \
            " 777.72,167 773.88,167 773.88,159.02 771.78,133"
        self.assertEqual(expected, d)

    # @unittest.expectedFailure
    def test_get_path_data_tspan01_02(self):
        # See also: tspan01.html
        # Test with DejaVu font 2.37, FontConfig 2.12.6, and FreeType 2.8
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text02')
        path_data = text.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M172.09,180 L172.09,177 178.06,177 178.06,159.8 163.66,136" \
            " 159.28,136 159.28,133 176.62,133 176.62,136 171.19,136" \
            " 182.84,155.34 194.5,136 189.25,136 189.25,133 202.81,133" \
            " 202.81,136 198.41,136 184.38,159.19 184.38,177 190.34,177" \
            " 190.34,180 172.09,180 M215.94,178 Q220.56,178 222.92,174.31" \
            " 225.28,170.64 225.28,163.48 225.28,156.33 222.92,152.66" \
            " 220.56,149 215.94,149 211.31,149 208.95,152.66 206.59,156.33" \
            " 206.59,163.48 206.59,170.64 208.97,174.31 211.34,178" \
            " 215.94,178 M215.94,181 Q208.69,181 204.28,176.2" \
            " 199.88,171.42 199.88,163.48 199.88,155.55 204.27,150.77" \
            " 208.66,146 215.94,146 223.22,146 227.61,150.77 232,155.55" \
            " 232,163.48 232,171.42 227.61,176.2 223.22,181 215.94,181" \
            " M257.88,147 L268.62,147 268.62,177 274.06,177 274.06,180" \
            " 262.88,180 262.88,174.39 Q261.28,177.62 258.75,179.31" \
            " 256.22,181 252.88,181 247.34,181 244.73,177.88 242.12,174.75" \
            " 242.12,168.08 L242.12,150 236.94,150 236.94,147 247.91,147" \
            " 247.91,166.27 Q247.91,172.42 249.39,174.7 250.88,177" \
            " 254.69,177 258.69,177 260.78,174.02 262.88,171.03" \
            " 262.88,165.34 L262.88,150 257.88,150 257.88,147" \
            " M322.25,169.45 L322.25,162 314.84,162 Q310.56,162" \
            " 308.47,163.95 306.38,165.92 306.38,169.98 306.38,173.67" \
            " 308.5,175.83 310.62,178 314.25,178 317.84,178 320.05,175.62" \
            " 322.25,173.27 322.25,169.45 M328,159.06 L328,177 333.12,177" \
            " 333.12,180 322.25,180 322.25,176.7 Q320.34,178.91" \
            " 317.84,179.95 315.34,181 312,181 306.47,181 303.22,178.02" \
            " 299.97,175.05 299.97,169.98 299.97,164.77 303.69,161.88" \
            " 307.41,159 314.19,159 L322.25,159 322.25,157.3" \
            " Q322.25,153.34 319.95,151.17 317.66,149 313.5,149 310.06,149" \
            " 308.03,150.77 306,152.53 305.5,156 L302.53,156 302.53,149" \
            " Q305.53,147.5 308.36,146.75 311.19,146 313.88,146 320.78,146" \
            " 324.39,149.34 328,152.69 328,159.06 M365.53,147 L365.53,155" \
            " 362.22,155 Q362.06,152.48 360.84,151.23 359.62,150" \
            " 357.28,150 353.03,150 350.77,152.98 348.5,155.98" \
            " 348.5,161.58 L348.5,177 355.16,177 355.16,180 337.56,180" \
            " 337.56,177 342.75,177 342.75,150 337.25,150 337.25,147" \
            " 348.5,147 348.5,152.61 Q350.19,149.25 352.84,147.62" \
            " 355.5,146 359.31,146 360.72,146 362.27,146.25 363.81,146.52" \
            " 365.53,147 M400.22,164 L375.44,164 375.44,164.25" \
            " Q375.44,171.06 377.97,174.53 380.5,178 385.44,178 389.22,178" \
            " 391.64,175.98 394.06,173.97 395.03,170 L399.66,170" \
            " Q398.28,175.48 394.58,178.23 390.88,181 384.84,181" \
            " 377.56,181 373.14,176.2 368.72,171.42 368.72,163.48" \
            " 368.72,155.61 373.06,150.8 377.41,146 384.47,146 392,146" \
            " 396.03,150.61 400.06,155.22 400.22,164 M393.44,161" \
            " Q393.25,155.05 390.98,152.02 388.72,149 384.47,149 380.5,149" \
            " 378.22,152.03 375.94,155.08 375.44,161 L393.44,161" \
            " M425.94,180 L425.94,176 430.66,176 430.66,151 425.94,151" \
            " 425.94,147 441.72,147 441.72,151.41 Q443.72,148.53" \
            " 446.28,147.27 448.84,146 452.75,146 458.34,146 461.2,149.23" \
            " 464.06,152.47 464.06,158.77 L464.06,176 468.81,176" \
            " 468.81,180 448.97,180 448.97,176 453,176 453,158.45" \
            " Q453,154.27 451.92,152.62 450.84,151 448.19,151 444.84,151" \
            " 443.28,153.44 441.72,155.88 441.72,161.19 L441.72,176" \
            " 445.78,176 445.78,180 425.94,180 M491.66,177 Q495.16,177" \
            " 496.58,174.09 498,171.2 498,163.48 498,155.77 496.59,152.88" \
            " 495.19,150 491.66,150 488.12,150 486.69,152.91 485.25,155.83" \
            " 485.25,163.48 485.25,171.14 486.69,174.06 488.12,177" \
            " 491.66,177 M491.66,181 Q482.88,181 477.89,176.33" \
            " 472.91,171.67 472.91,163.48 472.91,155.27 477.89,150.62" \
            " 482.88,146 491.66,146 500.47,146 505.44,150.62 510.41,155.27" \
            " 510.41,163.48 510.41,171.67 505.42,176.33 500.44,181" \
            " 491.66,181 M519.31,151 L514.5,151 514.5,147 519.31,147" \
            " 519.31,137 530.38,137 530.38,147 539.59,147 539.59,151" \
            " 530.38,151 530.38,170.09 Q530.38,174.73 531.06,175.86" \
            " 531.75,177 533.56,177 535.56,177 536.53,175.53 537.5,174.06" \
            " 537.56,171 L542.22,171 Q541.94,176.53 539.48,178.77" \
            " 537.03,181 531.03,181 524.19,181 521.75,178.66 519.31,176.33" \
            " 519.31,170.09 L519.31,151 M590.28,169.45 L590.28,162" \
            " 582.88,162 Q578.59,162 576.5,163.95 574.41,165.92" \
            " 574.41,169.98 574.41,173.67 576.53,175.83 578.66,178" \
            " 582.28,178 585.88,178 588.08,175.62 590.28,173.27" \
            " 590.28,169.45 M596.03,159.06 L596.03,177 601.16,177" \
            " 601.16,180 590.28,180 590.28,176.7 Q588.38,178.91" \
            " 585.88,179.95 583.38,181 580.03,181 574.5,181 571.25,178.02" \
            " 568,175.05 568,169.98 568,164.77 571.72,161.88 575.44,159" \
            " 582.22,159 L590.28,159 590.28,157.3 Q590.28,153.34" \
            " 587.98,151.17 585.69,149 581.53,149 578.09,149 576.06,150.77" \
            " 574.03,152.53 573.53,156 L570.56,156 570.56,149" \
            " Q573.56,147.5 576.39,146.75 579.22,146 581.91,146 588.81,146" \
            " 592.42,149.34 596.03,152.69 596.03,159.06 M630.69,177" \
            " L630.69,134 625.16,134 625.16,131 636.44,131 636.44,152.48" \
            " Q638.12,149.16 640.73,147.58 643.34,146 647.19,146" \
            " 653.31,146 657.19,150.83 661.06,155.67 661.06,163.48" \
            " 661.06,171.3 657.19,176.14 653.31,181 647.19,181 643.34,181" \
            " 640.73,179.56 638.12,178.14 636.44,175.14 L636.44,180" \
            " 625.16,180 625.16,177 630.69,177 M636.44,165.44" \
            " Q636.44,171.09 638.73,174.05 641.03,177 645.41,177" \
            " 649.81,177 652.08,173.58 654.34,170.16 654.34,163.48" \
            " 654.34,156.78 652.08,153.39 649.81,150 645.41,150 641.03,150" \
            " 638.73,153.12 636.44,156.27 636.44,162.19 L636.44,165.44" \
            " M689.75,169.45 L689.75,162 682.34,162 Q678.06,162" \
            " 675.97,163.95 673.88,165.92 673.88,169.98 673.88,173.67" \
            " 676,175.83 678.12,178 681.75,178 685.34,178 687.55,175.62" \
            " 689.75,173.27 689.75,169.45 M695.5,159.06 L695.5,177" \
            " 700.62,177 700.62,180 689.75,180 689.75,176.7 Q687.84,178.91" \
            " 685.34,179.95 682.84,181 679.5,181 673.97,181 670.72,178.02" \
            " 667.47,175.05 667.47,169.98 667.47,164.77 671.19,161.88" \
            " 674.91,159 681.69,159 L689.75,159 689.75,157.3" \
            " Q689.75,153.34 687.45,151.17 685.16,149 681,149 677.56,149" \
            " 675.53,150.77 673.5,152.53 673,156 L670.03,156 670.03,149" \
            " Q673.03,147.5 675.86,146.75 678.69,146 681.38,146 688.28,146" \
            " 691.89,149.34 695.5,152.69 695.5,159.06 M705.06,180" \
            " L705.06,177 710.25,177 710.25,150 704.75,150 704.75,147" \
            " 716,147 716,152.61 Q717.59,149.33 720.14,147.66 722.69,146" \
            " 726.06,146 731.56,146 734.16,149.12 736.75,152.27" \
            " 736.75,158.89 L736.75,177 741.88,177 741.88,180 726,180" \
            " 726,177 730.97,177 730.97,160.73 Q730.97,154.58" \
            " 729.47,152.28 727.97,150 724.19,150 720.19,150 718.09,152.95" \
            " 716,155.91 716,161.56 L716,177 721,177 721,180 705.06,180" \
            " M769.12,169.45 L769.12,162 761.72,162 Q757.44,162" \
            " 755.34,163.95 753.25,165.92 753.25,169.98 753.25,173.67" \
            " 755.38,175.83 757.5,178 761.12,178 764.72,178 766.92,175.62" \
            " 769.12,173.27 769.12,169.45 M774.88,159.06 L774.88,177" \
            " 780,177 780,180 769.12,180 769.12,176.7 Q767.22,178.91" \
            " 764.72,179.95 762.22,181 758.88,181 753.34,181 750.09,178.02" \
            " 746.84,175.05 746.84,169.98 746.84,164.77 750.56,161.88" \
            " 754.28,159 761.06,159 L769.12,159 769.12,157.3" \
            " Q769.12,153.34 766.83,151.17 764.53,149 760.38,149" \
            " 756.94,149 754.91,150.77 752.88,152.53 752.38,156" \
            " L749.41,156 749.41,149 Q752.41,147.5 755.23,146.75" \
            " 758.06,146 760.75,146 767.66,146 771.27,149.34 774.88,152.69" \
            " 774.88,159.06 M784.44,180 L784.44,177 789.62,177 789.62,150" \
            " 784.12,150 784.12,147 795.38,147 795.38,152.61" \
            " Q796.97,149.33 799.52,147.66 802.06,146 805.44,146" \
            " 810.94,146 813.53,149.12 816.12,152.27 816.12,158.89" \
            " L816.12,177 821.25,177 821.25,180 805.38,180 805.38,177" \
            " 810.34,177 810.34,160.73 Q810.34,154.58 808.84,152.28" \
            " 807.34,150 803.56,150 799.56,150 797.47,152.95 795.38,155.91" \
            " 795.38,161.56 L795.38,177 800.38,177 800.38,180 784.44,180" \
            " M848.5,169.45 L848.5,162 841.09,162 Q836.81,162" \
            " 834.72,163.95 832.62,165.92 832.62,169.98 832.62,173.67" \
            " 834.75,175.83 836.88,178 840.5,178 844.09,178 846.3,175.62" \
            " 848.5,173.27 848.5,169.45 M854.25,159.06 L854.25,177" \
            " 859.38,177 859.38,180 848.5,180 848.5,176.7 Q846.59,178.91" \
            " 844.09,179.95 841.59,181 838.25,181 832.72,181 829.47,178.02" \
            " 826.22,175.05 826.22,169.98 826.22,164.77 829.94,161.88" \
            " 833.66,159 840.44,159 L848.5,159 848.5,157.3 Q848.5,153.34" \
            " 846.2,151.17 843.91,149 839.75,149 836.31,149 834.28,150.77" \
            " 832.25,152.53 831.75,156 L828.78,156 828.78,149" \
            " Q831.78,147.5 834.61,146.75 837.44,146 840.12,146 847.03,146" \
            " 850.64,149.34 854.25,152.69 854.25,159.06 M867.22,177.02" \
            " Q867.22,175.34 868.41,174.17 869.59,173 871.38,173" \
            " 873.09,173 874.31,174.17 875.53,175.34 875.53,177.02" \
            " 875.53,178.66 874.31,179.83 873.09,181 871.38,181 869.59,181" \
            " 868.41,179.84 867.22,178.69 867.22,177.02"
        self.assertEqual(expected, d)

    # @unittest.expectedFailure
    def test_get_path_data_tspan01_03(self):
        # See also: tspan01.html
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text03')
        path_data = text.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M115.81,177 L125.16,177 Q130.78,177 133.38,174.47" \
            " 135.97,171.95 135.97,166.47 135.97,161 133.39,158.5" \
            " 130.81,156 125.16,156 L115.81,156 115.81,177 M115.81,153" \
            " L123.75,153 Q128.88,153 131.23,150.95 133.59,148.91" \
            " 133.59,144.5 133.59,140.06 131.23,138.03 128.88,136" \
            " 123.75,136 L115.81,136 115.81,153 M103.53,180 L103.53,177" \
            " 109.47,177 109.47,136 103.53,136 103.53,133 126.56,133" \
            " Q133.62,133 137.2,135.91 140.78,138.81 140.78,144.61" \
            " 140.78,148.8 138.3,151.28 135.81,153.77 131.03,154.33" \
            " 136.97,155.08 140.05,158.14 143.12,161.22 143.12,166.39" \
            " 143.12,173.39 138.75,176.69 134.38,180 125.09,180" \
            " L103.53,180 M169.69,147 L180.44,147 180.44,177 185.88,177" \
            " 185.88,180 174.69,180 174.69,174.39 Q173.09,177.62" \
            " 170.56,179.31 168.03,181 164.69,181 159.16,181 156.55,177.88" \
            " 153.94,174.75 153.94,168.08 L153.94,150 148.75,150" \
            " 148.75,147 159.72,147 159.72,166.27 Q159.72,172.42" \
            " 161.2,174.7 162.69,177 166.5,177 170.5,177 172.59,174.02" \
            " 174.69,171.03 174.69,165.34 L174.69,150 169.69,150" \
            " 169.69,147 M195.16,150 L190.09,150 190.09,147 195.16,147" \
            " 195.16,137 200.94,137 200.94,147 211.75,147 211.75,150" \
            " 200.94,150 200.94,171.03 Q200.94,175.48 201.75,176.73" \
            " 202.56,178 204.75,178 207,178 208.03,176.58 209.06,175.17" \
            " 209.12,172 L213.47,172 Q213.22,176.67 211,178.83 208.78,181" \
            " 204.25,181 199.28,181 197.22,178.73 195.16,176.47" \
            " 195.16,171.03 L195.16,150 M248.12,186.19 L250.31,180.62" \
            " 237.91,150 234.12,150 234.12,147 249.41,147 249.41,150" \
            " 244.09,150 253.44,172.94 262.78,150 257.81,150 257.81,147" \
            " 270.28,147 270.28,150 266.56,150 251.34,187.59" \
            " Q249.78,191.28 247.88,192.64 245.97,194 242.5,194 241.03,194" \
            " 239.48,193.73 237.94,193.48 236.38,193 L236.38,187" \
            " 239.31,187 Q239.5,189.14 240.39,190.06 241.28,191 243.16,191" \
            " 244.88,191 245.92,190.03 246.97,189.08 248.12,186.19" \
            " M289.72,178 Q294.34,178 296.7,174.31 299.06,170.64" \
            " 299.06,163.48 299.06,156.33 296.7,152.66 294.34,149" \
            " 289.72,149 285.09,149 282.73,152.66 280.38,156.33" \
            " 280.38,163.48 280.38,170.64 282.75,174.31 285.12,178" \
            " 289.72,178 M289.72,181 Q282.47,181 278.06,176.2" \
            " 273.66,171.42 273.66,163.48 273.66,155.55 278.05,150.77" \
            " 282.44,146 289.72,146 297,146 301.39,150.77 305.78,155.55" \
            " 305.78,163.48 305.78,171.42 301.39,176.2 297,181 289.72,181" \
            " M331.66,147 L342.41,147 342.41,177 347.84,177 347.84,180" \
            " 336.66,180 336.66,174.39 Q335.06,177.62 332.53,179.31" \
            " 330,181 326.66,181 321.12,181 318.52,177.88 315.91,174.75" \
            " 315.91,168.08 L315.91,150 310.72,150 310.72,147 321.69,147" \
            " 321.69,166.27 Q321.69,172.42 323.17,174.7 324.66,177" \
            " 328.47,177 332.47,177 334.56,174.02 336.66,171.03" \
            " 336.66,165.34 L336.66,150 331.66,150 331.66,147" \
            " M533.81,109.44 L533.81,126 538.56,126 538.56,130 522.75,130" \
            " 522.75,126 Q520.56,128.56 517.88,129.78 515.19,131" \
            " 511.75,131 506.66,131 503.92,128.22 501.19,125.45" \
            " 501.19,120.3 501.19,114.64 505.11,111.81 509.03,109" \
            " 516.94,109 L522.75,109 522.75,107.53 Q522.75,103.67" \
            " 520.84,101.83 518.94,100 514.94,100 511.62,100 509.83,101.41" \
            " 508.03,102.81 507.28,106 L503.75,106 503.75,98 Q506.72,97" \
            " 509.91,96.5 513.09,96 516.62,96 525.53,96 529.67,99.23" \
            " 533.81,102.48 533.81,109.44 M522.75,119.75 L522.75,113" \
            " 518.59,113 Q515.5,113 513.84,114.7 512.19,116.42" \
            " 512.19,119.62 512.19,122.83 513.39,124.41 514.59,126" \
            " 517.06,126 519.62,126 521.19,124.28 522.75,122.58" \
            " 522.75,119.75 M574.41,96.59 L574.41,106 570.88,106" \
            " Q570.69,103.47 569.44,102.23 568.19,101 565.81,101" \
            " 562.19,101 560.09,104.12 558,107.27 558,112.81 L558,126" \
            " 564.03,126 564.03,130 542.22,130 542.22,126 546.94,126" \
            " 546.94,101 541.88,101 541.88,97 558,97 558,102.55" \
            " Q559.62,99.22 562.3,97.61 564.97,96 568.84,96 569.81,96" \
            " 571.2,96.16 572.59,96.31 574.41,96.59 M599.41,111" \
            " Q599.41,104.91 598.19,102.45 596.97,100 594.03,100" \
            " 591.19,100 589.95,102.41 588.72,104.83 588.72,110.48" \
            " L588.72,111 599.41,111 M611.56,115 L588.72,115 588.72,115.25" \
            " Q588.72,121.47 590.66,124.23 592.59,127 596.91,127 600.5,127" \
            " 602.72,125.2 604.94,123.41 605.56,120 L610.75,120" \
            " Q609.41,125.67 605.41,128.33 601.41,131 594.22,131" \
            " 585.59,131 580.98,126.45 576.38,121.92 576.38,113.48" \
            " 576.38,105.23 581.09,100.61 585.81,96 594.22,96 602.47,96" \
            " 606.88,100.83 611.28,105.67 611.56,115 M662.22,219.45" \
            " L662.22,212 654.81,212 Q650.53,212 648.44,213.95" \
            " 646.34,215.92 646.34,219.98 646.34,223.67 648.47,225.83" \
            " 650.59,228 654.22,228 657.81,228 660.02,225.62 662.22,223.27" \
            " 662.22,219.45 M667.97,209.06 L667.97,227 673.09,227" \
            " 673.09,230 662.22,230 662.22,226.7 Q660.31,228.91" \
            " 657.81,229.95 655.31,231 651.97,231 646.44,231 643.19,228.02" \
            " 639.94,225.05 639.94,219.98 639.94,214.77 643.66,211.88" \
            " 647.38,209 654.16,209 L662.22,209 662.22,207.3" \
            " Q662.22,203.34 659.92,201.17 657.62,199 653.47,199" \
            " 650.03,199 648,200.77 645.97,202.53 645.47,206 L642.5,206" \
            " 642.5,199 Q645.5,197.5 648.33,196.75 651.16,196 653.84,196" \
            " 660.75,196 664.36,199.34 667.97,202.69 667.97,209.06" \
            " M708.38,211.55 L708.38,214.8 Q708.38,220.77 710.67,223.88" \
            " 712.97,227 717.34,227 721.75,227 724.02,223.58 726.28,220.16" \
            " 726.28,213.48 726.28,206.78 724.02,203.39 721.75,200" \
            " 717.34,200 712.97,200 710.67,202.97 708.38,205.94" \
            " 708.38,211.55 M702.62,200 L697.09,200 697.09,197 708.38,197" \
            " 708.38,201.83 Q710.06,198.84 712.67,197.42 715.28,196" \
            " 719.12,196 725.25,196 729.12,200.83 733,205.67 733,213.48" \
            " 733,221.3 729.12,226.14 725.25,231 719.12,231 715.28,231" \
            " 712.67,229.42 710.06,227.84 708.38,224.52 L708.38,240" \
            " 713.81,240 713.81,243 697.09,243 697.09,240 702.62,240" \
            " 702.62,200 M770.91,214 L746.12,214 746.12,214.25" \
            " Q746.12,221.06 748.66,224.53 751.19,228 756.12,228" \
            " 759.91,228 762.33,225.98 764.75,223.97 765.72,220" \
            " L770.34,220 Q768.97,225.48 765.27,228.23 761.56,231" \
            " 755.53,231 748.25,231 743.83,226.2 739.41,221.42" \
            " 739.41,213.48 739.41,205.61 743.75,200.8 748.09,196" \
            " 755.16,196 762.69,196 766.72,200.61 770.75,205.22 770.91,214" \
            " M764.12,211 Q763.94,205.05 761.67,202.02 759.41,199" \
            " 755.16,199 751.19,199 748.91,202.03 746.62,205.08 746.12,211" \
            " L764.12,211 M799.56,219.45 L799.56,212 792.16,212" \
            " Q787.88,212 785.78,213.95 783.69,215.92 783.69,219.98" \
            " 783.69,223.67 785.81,225.83 787.94,228 791.56,228 795.16,228" \
            " 797.36,225.62 799.56,223.27 799.56,219.45 M805.31,209.06" \
            " L805.31,227 810.44,227 810.44,230 799.56,230 799.56,226.7" \
            " Q797.66,228.91 795.16,229.95 792.66,231 789.31,231" \
            " 783.78,231 780.53,228.02 777.28,225.05 777.28,219.98" \
            " 777.28,214.77 781,211.88 784.72,209 791.5,209 L799.56,209" \
            " 799.56,207.3 Q799.56,203.34 797.27,201.17 794.97,199" \
            " 790.81,199 787.38,199 785.34,200.77 783.31,202.53 782.81,206" \
            " L779.84,206 779.84,199 Q782.84,197.5 785.67,196.75 788.5,196" \
            " 791.19,196 798.09,196 801.7,199.34 805.31,202.69" \
            " 805.31,209.06 M845.16,220 Q843.94,225.38 840.47,228.19" \
            " 837,231 831.5,231 824.25,231 819.84,226.2 815.44,221.42" \
            " 815.44,213.48 815.44,205.52 819.84,200.75 824.25,196" \
            " 831.5,196 834.66,196 837.78,196.73 840.91,197.48 844.06,199" \
            " L844.06,208 840.72,208 Q840.06,203.3 837.86,201.14" \
            " 835.66,199 831.56,199 826.91,199 824.53,202.62 822.16,206.27" \
            " 822.16,213.48 822.16,220.7 824.52,224.34 826.88,228" \
            " 831.56,228 835.28,228 837.5,226 839.72,224.02 840.53,220" \
            " L845.16,220 M850.72,230 L850.72,227 855.91,227 855.91,184" \
            " 850.41,184 850.41,181 861.66,181 861.66,202.61" \
            " Q863.25,199.33 865.8,197.66 868.34,196 871.72,196 877.22,196" \
            " 879.81,199.12 882.41,202.27 882.41,208.89 L882.41,227" \
            " 887.53,227 887.53,230 871.66,230 871.66,227 876.62,227" \
            " 876.62,210.73 Q876.62,204.55 875.14,202.27 873.66,200" \
            " 869.84,200 865.84,200 863.75,202.95 861.66,205.91" \
            " 861.66,211.56 L861.66,227 866.66,227 866.66,230 850.72,230" \
            " M898.03,227.02 Q898.03,225.34 899.22,224.17 900.41,223" \
            " 902.19,223 903.91,223 905.12,224.17 906.34,225.34" \
            " 906.34,227.02 906.34,228.66 905.12,229.83 903.91,231" \
            " 902.19,231 900.41,231 899.22,229.84 898.03,228.69" \
            " 898.03,227.02 M898.16,183 L906.22,183 904.09,209.02" \
            " 904.09,217 900.25,217 900.25,209.02 898.16,183"
        self.assertEqual(expected, d)

    # @unittest.expectedFailure
    def test_get_path_data_tspan04(self):
        # See also: tspan04.html
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN04))
        root = tree.getroot()
        text = root.get_element_by_id('text01')

        path_data = text.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M234.64,112.66 L239.36,109.94 247.36,123.8 264.42,113.94" \
            " 256.42,100.08 261.11,97.38 281.11,132.02 276.42,134.72" \
            " 266.42,117.41 249.36,127.27 259.36,144.58 254.64,147.3" \
            " 234.64,112.66 M322.27,133.5 L322.27,136 299.55,136" \
            " Q299.88,141.38 302.62,144.19 305.38,147 310.28,147" \
            " 313.14,147 315.81,146.25 318.48,145.5 321.11,144 L321.11,149" \
            " Q318.45,149.98 315.66,150.48 312.86,151 310,151 302.8,151" \
            " 298.59,146.75 294.39,142.52 294.39,135.27 294.39,127.78" \
            " 298.38,123.39 302.36,119 309.14,119 315.2,119 318.73,122.89" \
            " 322.27,126.8 322.27,133.5 M317.33,132 Q317.28,127.89" \
            " 315.06,125.44 312.84,123 309.19,123 305.06,123 302.58,125.36" \
            " 300.09,127.73 299.72,132.02 L317.33,132 M350.67,116.22" \
            " L354.95,118.69 333.95,155.06 329.67,152.59 350.67,116.22" \
            " M365.95,116.22 L370.23,118.69 349.23,155.06 344.95,152.59" \
            " 365.95,116.22 M383.83,135.05 Q380.39,133.06 376.78,134.69" \
            " 373.17,136.31 370.39,141.14 367.59,145.97 367.98,149.89" \
            " 368.38,153.83 371.83,155.83 375.25,157.8 378.86,156.16" \
            " 382.47,154.53 385.25,149.72 388.02,144.92 387.62,140.97" \
            " 387.25,137.02 383.83,135.05 M385.83,131.58 Q391.41,134.8" \
            " 392.47,140.3 393.53,145.81 389.78,152.33 386.03,158.81" \
            " 380.72,160.66 375.41,162.52 369.83,159.3 364.22,156.05" \
            " 363.17,150.53 362.12,145.02 365.88,138.53 369.62,132.02" \
            " 374.92,130.17 380.22,128.33 385.83,131.58 M398.48,147.17" \
            " L403.38,150 401.11,153.94 393.06,159.05 390.08,157.31" \
            " 396.22,151.11 398.48,147.17 M452.47,135.05 Q449.03,133.06" \
            " 445.41,134.69 441.8,136.31 439.02,141.14 436.22,145.97" \
            " 436.61,149.89 437,153.83 440.47,155.83 443.88,157.8" \
            " 447.48,156.17 451.09,154.55 453.88,149.72 456.64,144.94" \
            " 456.25,140.97 455.88,137.02 452.47,135.05 M454.47,131.58" \
            " Q460.05,134.8 461.09,140.31 462.16,145.83 458.41,152.33" \
            " 454.66,158.81 449.34,160.66 444.05,162.52 438.47,159.3" \
            " 432.84,156.05 431.8,150.53 430.75,145.02 434.5,138.53" \
            " 438.25,132.03 443.55,130.17 448.84,128.33 454.47,131.58" \
            " M467.77,142.47 L477.06,126.36 481.34,128.83 472.14,144.77" \
            " Q470,148.48 470.36,151.17 470.72,153.88 473.61,155.55" \
            " 477.08,157.55 480.38,156.48 483.69,155.42 485.91,151.58" \
            " L494.61,136.48 498.88,138.95 483.88,164.94 479.61,162.47" \
            " 481.61,159 Q478.78,160.28 476.11,160.16 473.44,160.05" \
            " 470.7,158.47 466.22,155.89 465.47,151.81 464.73,147.73" \
            " 467.77,142.47 M488.34,131.72 L488.34,131.72 M521.11,121.27" \
            " L516.61,129.06 525.42,134.14 523.42,137.59 514.61,132.52" \
            " 506.48,146.59 Q504.66,149.77 505,151.17 505.36,152.58" \
            " 508.02,154.11 L512.42,156.66 510.42,160.11 506.02,157.56" \
            " Q501.06,154.72 500.23,151.81 499.42,148.91 502.19,144.11" \
            " L510.31,130.03 507.17,128.22 509.17,124.77 512.31,126.58" \
            " 516.81,118.78 521.11,121.27 M560.16,121.25 L555.66,129.05" \
            " 564.47,134.14 562.47,137.61 553.66,132.52 545.53,146.58" \
            " Q543.7,149.75 544.05,151.16 544.41,152.58 547.06,154.11" \
            " L551.47,156.66 549.47,160.12 545.06,157.58 Q540.11,154.72" \
            " 539.28,151.81 538.45,148.91 541.23,144.09 L549.36,130.03" \
            " 546.22,128.22 548.22,124.75 551.36,126.56 555.86,118.77" \
            " 560.16,121.25 M588.92,149 L579.64,165.08 575.36,162.61" \
            " 584.56,146.66 Q586.72,142.94 586.34,140.25 585.97,137.58" \
            " 583.09,135.91 579.62,133.91 576.33,134.98 573.05,136.06" \
            " 570.81,139.91 L562.12,154.97 557.83,152.48 578.83,116.11" \
            " 583.12,118.59 575.12,132.45 Q577.91,131.17 580.61,131.3" \
            " 583.33,131.42 586.05,132.98 590.53,135.58 591.25,139.62" \
            " 591.98,143.69 588.92,149 M623.38,151.16 L622.12,153.33" \
            " 602.45,141.97 Q600.05,146.78 601.02,150.58 602,154.39" \
            " 606.25,156.84 608.73,158.28 611.42,158.97 614.11,159.66" \
            " 617.12,159.67 L614.62,164 Q611.83,163.53 609.16,162.56" \
            " 606.48,161.61 604.02,160.17 597.77,156.58 596.23,150.8" \
            " 594.72,145.03 598.34,138.75 602.09,132.27 607.73,130.45" \
            " 613.39,128.66 619.27,132.05 624.52,135.08 625.61,140.22" \
            " 626.72,145.36 623.38,151.16 M619.86,147.39 Q621.86,143.8" \
            " 621.16,140.56 620.47,137.34 617.31,135.52 613.73,133.45" \
            " 610.39,134.27 607.05,135.08 604.59,138.59 L619.86,147.39" \
            " M654.77,138.78 Q654.31,137.91 653.58,137.2 652.84,136.5" \
            " 651.83,135.92 648.2,133.83 644.88,135.11 641.55,136.41" \
            " 638.94,140.92 L630.83,154.97 626.52,152.48 641.52,126.5" \
            " 645.83,128.98 643.83,132.45 Q646.44,131.05 649.22,131.22" \
            " 652,131.41 655.09,133.19 655.53,133.44 656.06,133.75" \
            " 656.59,134.06 657.25,134.44 L654.77,138.78 M678.62,151.16" \
            " L677.38,153.33 657.7,141.97 Q655.3,146.78 656.27,150.58" \
            " 657.25,154.39 661.5,156.84 663.97,158.28 666.66,158.97" \
            " 669.36,159.66 672.38,159.67 L669.88,164 Q667.08,163.53" \
            " 664.41,162.56 661.73,161.61 659.25,160.17 653.02,156.58" \
            " 651.48,150.8 649.97,145.03 653.59,138.75 657.34,132.27" \
            " 662.98,130.45 668.64,128.64 674.52,132.03 679.77,135.06" \
            " 680.86,140.2 681.97,145.36 678.62,151.16 M675.09,147.39" \
            " Q677.11,143.8 676.41,140.56 675.72,137.34 672.55,135.52" \
            " 668.98,133.45 665.64,134.27 662.3,135.08 659.83,138.59" \
            " L675.09,147.39"
        self.assertEqual(expected, d)

    # @unittest.expectedFailure
    def test_get_path_data_tspan05(self):
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN05))
        root = tree.getroot()

        text = root.get_element_by_id('parent')
        path_data = text.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M45.12,17.36 L49.36,17.73 57.98,37.8 59.66,18.64 62.7,18.91" \
            " 60.7,41.81 56.47,41.44 47.84,21.38 46.17,40.53 43.12,40.27" \
            " 45.12,17.36 M77.28,28.05 Q75.05,27.44 73.33,28.64" \
            " 71.62,29.84 70.89,32.53 70.17,35.23 71.05,37.12 71.92,39.02" \
            " 74.17,39.62 76.39,40.22 78.09,39 79.81,37.8 80.53,35.11" \
            " 81.25,32.45 80.38,30.55 79.5,28.64 77.28,28.05 M78.05,25.14" \
            " Q81.67,26.11 83.12,28.97 84.58,31.84 83.48,35.91 82.41,39.97" \
            " 79.7,41.73 77.02,43.5 73.39,42.53 69.77,41.55 68.33,38.67" \
            " 66.89,35.81 67.97,31.75 69.06,27.69 71.73,25.92 74.42,24.16" \
            " 78.05,25.14 M98.55,21.62 L96.44,26.16 101.8,28.66" \
            " 100.53,31.38 95.17,28.88 91.42,36.91 Q90.58,38.72" \
            " 90.86,39.48 91.16,40.25 92.78,41 L95.45,42.25 94.19,44.97" \
            " 91.52,43.72 Q88.5,42.31 87.91,40.58 87.33,38.86 88.8,35.69" \
            " L92.55,27.66 90.64,26.77 91.91,24.05 93.81,24.94 95.92,20.41" \
            " 98.55,21.62 M115.64,30.22 Q112.22,30.81 110.98,31.61" \
            " 109.77,32.42 110,33.8 110.2,34.91 111.3,35.38 112.41,35.86" \
            " 114.12,35.56 116.47,35.14 117.69,33.67 118.91,32.22" \
            " 118.55,30.22 L118.47,29.72 115.64,30.22 M121.02,27.66" \
            " L122.69,37.09 119.86,37.59 119.33,34.64 Q118.62,36.31" \
            " 117.3,37.28 115.98,38.27 113.89,38.64 111.25,39.11" \
            " 109.44,37.95 107.62,36.81 107.2,34.42 106.7,31.66" \
            " 108.39,29.89 110.09,28.12 113.95,27.45 L117.94,26.75" \
            " 117.89,26.48 Q117.58,24.72 116.12,23.98 114.67,23.27" \
            " 112.34,23.67 110.88,23.94 109.52,24.42 108.17,24.92" \
            " 106.95,25.64 L106.44,22.69 Q107.89,21.92 109.31,21.41" \
            " 110.73,20.91 112.12,20.67 115.86,20.02 118.06,21.73" \
            " 120.28,23.47 121.02,27.66 M120.45,16.41 L123.16,15.42" \
            " 131.38,37.98 128.67,38.97 120.45,16.41 M125.33,17.7" \
            " L127.83,16.27 139.83,37.05 137.33,38.48 125.33,17.7" \
            " M154.81,16.94 L156.73,19.25 Q155.5,19.64 154.39,20.23" \
            " 153.28,20.84 152.33,21.66 150.19,23.45 150.02,25.64" \
            " 149.84,27.84 151.67,30.03 153.5,32.2 155.7,32.42" \
            " 157.91,32.64 160.05,30.84 161,30.03 161.78,29.05" \
            " 162.56,28.06 163.17,26.91 L165.09,29.2 Q164.5,30.36" \
            " 163.67,31.38 162.84,32.41 161.73,33.34 158.7,35.88" \
            " 155.36,35.5 152.02,35.14 149.36,31.98 146.67,28.77" \
            " 146.92,25.41 147.17,22.05 150.31,19.42 151.33,18.56" \
            " 152.45,17.94 153.58,17.33 154.81,16.94 M177.94,20.48" \
            " L184.83,28.7 182.62,30.56 175.8,22.42 Q174.39,20.75" \
            " 172.94,20.52 171.5,20.3 170.02,21.55 168.23,23.05" \
            " 168.06,24.92 167.89,26.81 169.36,28.58 L175.81,36.27" \
            " 173.61,38.12 158.19,19.73 160.39,17.88 166.17,24.77" \
            " Q166,22.97 166.59,21.48 167.19,20.02 168.59,18.84" \
            " 170.89,16.91 173.25,17.31 175.62,17.73 177.94,20.48" \
            " M194.92,26.83 Q192.25,29.06 191.59,30.38 190.95,31.7" \
            " 191.84,32.77 192.56,33.62 193.75,33.47 194.95,33.33" \
            " 196.28,32.2 198.11,30.67 198.42,28.8 198.73,26.94" \
            " 197.44,25.38 L197.11,24.98 194.92,26.83 M198.3,21.94" \
            " L204.45,29.27 202.25,31.11 200.31,28.81 Q200.55,30.61" \
            " 199.89,32.11 199.25,33.62 197.62,35 195.56,36.72" \
            " 193.42,36.64 191.28,36.56 189.72,34.7 187.92,32.55" \
            " 188.5,30.17 189.09,27.8 192.09,25.28 L195.17,22.69 195,22.47" \
            " Q193.84,21.11 192.23,21.2 190.62,21.3 188.81,22.81" \
            " 187.66,23.78 186.72,24.89 185.8,26 185.12,27.22" \
            " L183.19,24.92 Q184.08,23.52 185.05,22.38 186.03,21.23" \
            " 187.09,20.33 190.02,17.89 192.78,18.28 195.56,18.67" \
            " 198.3,21.94 M211.7,20.05 Q211.33,20.36 210.89,20.72" \
            " 210.45,21.09 209.92,21.53 208.06,23.09 207.98,25.05" \
            " 207.92,27.02 209.69,29.11 L215.7,36.28 213.48,38.14" \
            " 201.91,24.34 204.12,22.48 206.06,24.78 Q205.77,23.03" \
            " 206.41,21.53 207.05,20.03 208.64,18.69 208.86,18.5" \
            " 209.14,18.27 209.42,18.05 209.75,17.77 L211.7,20.05" \
            " M227.69,26.83 Q225.02,29.08 224.36,30.38 223.7,31.69" \
            " 224.61,32.75 225.33,33.62 226.52,33.47 227.72,33.33" \
            " 229.05,32.22 230.88,30.69 231.19,28.81 231.52,26.95" \
            " 230.2,25.39 L229.88,25 227.69,26.83 M231.06,21.92" \
            " L237.22,29.27 235.02,31.12 233.09,28.83 Q233.31,30.62" \
            " 232.66,32.12 232,33.64 230.38,35 228.33,36.73 226.17,36.64" \
            " 224.03,36.55 222.48,34.7 220.67,32.55 221.27,30.17" \
            " 221.86,27.81 224.86,25.3 L227.95,22.7 227.77,22.48" \
            " Q226.62,21.12 225,21.22 223.38,21.31 221.56,22.83" \
            " 220.42,23.8 219.48,24.89 218.56,26 217.88,27.23" \
            " L215.95,24.94 Q216.83,23.53 217.81,22.39 218.8,21.25" \
            " 219.88,20.34 222.78,17.91 225.55,18.28 228.33,18.67" \
            " 231.06,21.92 M245.06,16.94 L246.98,19.23 Q245.73,19.64" \
            " 244.62,20.23 243.53,20.83 242.58,21.64 240.44,23.44" \
            " 240.27,25.64 240.09,27.84 241.92,30.02 243.75,32.2" \
            " 245.95,32.41 248.16,32.62 250.3,30.83 251.25,30.02" \
            " 252.02,29.03 252.8,28.06 253.42,26.89 L255.34,29.19" \
            " Q254.75,30.36 253.92,31.38 253.09,32.39 251.97,33.31" \
            " 248.95,35.86 245.59,35.48 242.25,35.12 239.59,31.97" \
            " 236.91,28.77 237.16,25.41 237.42,22.05 240.56,19.42" \
            " 241.58,18.56 242.7,17.94 243.83,17.31 245.06,16.94" \
            " M251.33,18.61 L254.53,22.45 259.08,18.64 261.02,20.94" \
            " 256.47,24.75 262.16,31.53 Q263.44,33.06 264.25,33.12" \
            " 265.08,33.19 266.45,32.03 L268.72,30.12 270.66,32.42" \
            " 268.39,34.33 Q265.84,36.47 264.02,36.27 262.2,36.08" \
            " 259.95,33.39 L254.27,26.61 252.64,27.97 250.7,25.67" \
            " 252.33,24.31 249.12,20.47 251.33,18.61 M281.61,20.86" \
            " L282.81,22.3 272.69,30.8 Q274.41,32.55 276.45,32.5" \
            " 278.5,32.45 280.69,30.61 281.95,29.55 282.83,28.16" \
            " 283.7,26.78 284.23,25.03 L286.16,27.33 Q285.61,29.09" \
            " 284.69,30.52 283.77,31.94 282.48,33.02 279.27,35.7" \
            " 275.86,35.45 272.47,35.2 269.86,32.09 267.14,28.86" \
            " 267.33,25.47 267.52,22.09 270.53,19.56 273.23,17.28" \
            " 276.22,17.62 279.2,17.98 281.61,20.86 M278.69,21.86" \
            " Q277.48,20.47 275.8,20.47 274.11,20.47 272.48,21.83" \
            " 270.64,23.38 270.2,25.11 269.78,26.84 270.83,28.45" \
            " L278.69,21.86 M294.3,20.05 Q293.92,20.36 293.48,20.72" \
            " 293.05,21.09 292.53,21.53 290.66,23.09 290.59,25.05" \
            " 290.53,27 292.28,29.09 L298.3,36.27 296.09,38.12" \
            " 284.53,24.33 286.73,22.47 288.66,24.77 Q288.39,23.03" \
            " 289.02,21.53 289.66,20.03 291.25,18.69 291.48,18.5" \
            " 291.75,18.27 292.03,18.03 292.36,17.75 L294.3,20.05" \
            " M306.94,17.86 L308.88,20.16 Q307.61,20.55 306.45,21.2" \
            " 305.3,21.86 304.22,22.77 302.58,24.14 302.11,25.23" \
            " 301.64,26.34 302.34,27.19 302.88,27.83 303.77,27.69" \
            " 304.66,27.56 306.7,26.42 L307.58,25.94 Q310.36,24.47" \
            " 312.09,24.55 313.84,24.64 315.22,26.27 316.77,28.12" \
            " 316.2,30.44 315.64,32.75 313.05,34.92 311.97,35.83" \
            " 310.48,36.42 309,37.03 307.05,37.34 L305.12,35.05" \
            " Q306.98,34.78 308.48,34.17 310,33.56 311.16,32.59" \
            " 312.72,31.28 313.12,30.06 313.55,28.86 312.77,27.94" \
            " 312.06,27.09 311.08,27.14 310.09,27.19 307.69,28.5" \
            " L306.8,28.98 Q304.41,30.3 302.8,30.22 301.19,30.16" \
            " 299.97,28.7 298.48,26.94 299.02,24.84 299.55,22.77" \
            " 302.02,20.69 303.23,19.67 304.47,18.95 305.72,18.23" \
            " 306.94,17.86 M351.8,36.66 L352.78,39.36 335.88,45.52" \
            " 334.89,42.81 351.8,36.66 M357.44,34.61 L358.42,37.31" \
            " 354.67,38.69 353.69,35.98 357.44,34.61 M360.81,49.84" \
            " L351.53,55.2 350.09,52.7 359.3,47.39 Q361.19,46.3" \
            " 361.66,44.91 362.12,43.53 361.16,41.86 359.98,39.84" \
            " 358.14,39.34 356.31,38.86 354.33,40 L345.64,45.02 344.2,42.5" \
            " 359.8,33.5 361.23,36.02 358.64,37.52 Q360.45,37.66" \
            " 361.8,38.48 363.16,39.33 364.06,40.91 365.58,43.52" \
            " 364.75,45.78 363.92,48.05 360.81,49.84 M392.47,26.16" \
            " L389.27,29.98 393.81,33.8 391.88,36.09 387.33,32.28" \
            " 381.64,39.06 Q380.34,40.59 380.42,41.41 380.52,42.22" \
            " 381.89,43.38 L384.16,45.28 382.23,47.58 379.97,45.67" \
            " Q377.42,43.53 377.3,41.7 377.19,39.89 379.44,37.2" \
            " L385.12,30.42 383.5,29.06 385.44,26.77 387.06,28.12" \
            " 390.27,24.3 392.47,26.16 M406.31,39.5 L400.95,48.78" \
            " 398.47,47.34 403.78,38.14 Q404.88,36.25 404.58,34.81" \
            " 404.28,33.39 402.61,32.42 400.59,31.27 398.77,31.75" \
            " 396.94,32.23 395.78,34.22 L390.77,42.91 388.27,41.45" \
            " 400.27,20.67 402.77,22.12 398.27,29.92 Q399.91,29.12" \
            " 401.48,29.17 403.08,29.22 404.66,30.14 407.28,31.64" \
            " 407.69,34.02 408.11,36.39 406.31,39.5 M426.31,36.88" \
            " L425.67,38.64 413.25,34.11 Q412.59,36.47 413.66,38.22" \
            " 414.73,39.98 417.42,40.95 418.97,41.53 420.59,41.58" \
            " 422.22,41.64 424,41.22 L422.98,44.05 Q421.19,44.44" \
            " 419.48,44.36 417.8,44.28 416.22,43.72 412.3,42.28" \
            " 410.81,39.19 409.33,36.11 410.7,32.3 412.16,28.33" \
            " 415.19,26.8 418.22,25.27 421.91,26.62 425.23,27.83" \
            " 426.41,30.59 427.59,33.36 426.31,36.88 M424,34.83" \
            " Q424.59,33.11 423.75,31.64 422.91,30.19 420.91,29.45" \
            " 418.64,28.64 416.92,29.12 415.22,29.62 414.34,31.34" \
            " L424,34.83 M29.7,68.59 L32.92,72.42 37.45,68.61 39.38,70.91" \
            " 34.84,74.72 40.55,81.52 Q41.83,83.05 42.64,83.11 43.45,83.17" \
            " 44.83,82.02 L47.09,80.11 49.02,82.41 46.75,84.31 Q44.2,86.45" \
            " 42.39,86.25 40.58,86.05 38.33,83.38 L32.62,76.58 31,77.94" \
            " 29.08,75.64 30.7,74.28 27.48,70.45 29.7,68.59 M59.97,70.88" \
            " L61.19,72.31 51.06,80.81 Q52.77,82.55 54.81,82.5 56.86,82.45" \
            " 59.05,80.62 60.33,79.55 61.19,78.17 62.06,76.8 62.59,75.05" \
            " L64.52,77.34 Q63.97,79.08 63.05,80.52 62.14,81.95" \
            " 60.86,83.03 57.66,85.72 54.23,85.45 50.83,85.2 48.22,82.08" \
            " 45.5,78.86 45.69,75.47 45.89,72.08 48.91,69.55 51.61,67.28" \
            " 54.58,67.64 57.56,68 59.97,70.88 M57.05,71.86 Q55.86,70.47" \
            " 54.17,70.47 52.48,70.48 50.86,71.84 49.02,73.39 48.58,75.12" \
            " 48.14,76.86 49.22,78.45 L57.05,71.86 M73.55,64.91" \
            " L74.34,75.69 85.38,78.48 82.78,80.66 74.33,78.52 74.97,87.2" \
            " 72.38,89.39 71.52,77.8 61.25,75.23 63.84,73.06 71.52,74.98" \
            " 70.95,67.09 73.55,64.91 M80.28,68.61 L83.5,72.44 88.05,68.62" \
            " 89.97,70.92 85.42,74.73 91.12,81.53 Q92.41,83.06 93.22,83.12" \
            " 94.05,83.19 95.42,82.03 L97.69,80.12 99.62,82.42 97.36,84.33" \
            " Q94.81,86.47 92.98,86.27 91.17,86.06 88.92,83.39" \
            " L83.22,76.59 81.59,77.95 79.67,75.66 81.3,74.3 78.08,70.47" \
            " 80.28,68.61 M119.88,70.5 L126.77,78.7 124.58,80.56" \
            " 117.73,72.42 Q116.33,70.75 114.88,70.53 113.44,70.31" \
            " 111.95,71.56 110.16,73.06 109.98,74.94 109.83,76.83" \
            " 111.31,78.58 L117.77,86.27 115.55,88.12 100.11,69.73" \
            " 102.33,67.88 108.11,74.78 Q107.94,72.97 108.52,71.5" \
            " 109.11,70.03 110.52,68.86 112.83,66.92 115.19,67.33" \
            " 117.56,67.73 119.88,70.5 M136.86,76.83 Q134.19,79.06" \
            " 133.53,80.38 132.88,81.69 133.77,82.75 134.48,83.61" \
            " 135.67,83.47 136.88,83.33 138.2,82.2 140.03,80.67" \
            " 140.34,78.8 140.67,76.94 139.38,75.38 L139.05,74.98" \
            " 136.86,76.83 M140.23,71.92 L146.39,79.27 144.19,81.11" \
            " 142.25,78.81 Q142.48,80.62 141.83,82.12 141.19,83.62" \
            " 139.55,85 137.5,86.72 135.34,86.62 133.2,86.55 131.64,84.69" \
            " 129.83,82.55 130.42,80.17 131.02,77.8 134.02,75.28" \
            " L137.11,72.69 136.94,72.47 Q135.78,71.09 134.16,71.19" \
            " 132.55,71.3 130.73,72.81 129.59,73.77 128.66,74.88" \
            " 127.72,75.98 127.05,77.22 L125.11,74.91 Q126,73.52" \
            " 126.97,72.36 127.95,71.22 129.03,70.31 131.94,67.88" \
            " 134.72,68.27 137.5,68.67 140.23,71.92 M142.38,75.59" \
            " L144.7,73.64 158.59,81.69 153.08,66.61 155.42,64.66" \
            " 161.95,82.66 158.95,85.16 142.38,75.59 M179.56,70.88" \
            " L180.77,72.31 170.64,80.81 Q172.36,82.55 174.41,82.5" \
            " 176.47,82.47 178.66,80.62 179.92,79.56 180.78,78.17" \
            " 181.66,76.8 182.17,75.05 L184.11,77.34 Q183.56,79.09" \
            " 182.64,80.52 181.72,81.95 180.44,83.03 177.23,85.72" \
            " 173.81,85.45 170.41,85.2 167.8,82.09 165.09,78.86" \
            " 165.28,75.47 165.48,72.09 168.5,69.56 171.2,67.28" \
            " 174.17,67.64 177.16,68 179.56,70.88 M176.64,71.88" \
            " Q175.44,70.48 173.75,70.47 172.08,70.47 170.44,71.83" \
            " 168.59,73.38 168.17,75.11 167.75,76.86 168.8,78.45" \
            " L176.64,71.88 M205.27,76.83 Q202.59,79.06 201.94,80.38" \
            " 201.28,81.7 202.17,82.77 202.91,83.62 204.09,83.47" \
            " 205.3,83.33 206.62,82.22 208.45,80.67 208.77,78.8" \
            " 209.09,76.94 207.78,75.38 L207.45,74.98 205.27,76.83" \
            " M208.64,71.94 L214.8,79.27 212.59,81.11 210.67,78.81" \
            " Q210.91,80.62 210.25,82.12 209.59,83.64 207.97,85" \
            " 205.91,86.73 203.75,86.64 201.61,86.56 200.06,84.7" \
            " 198.25,82.55 198.84,80.17 199.44,77.8 202.45,75.28" \
            " L205.53,72.69 205.34,72.47 Q204.2,71.11 202.58,71.2" \
            " 200.95,71.31 199.16,72.83 198,73.78 197.08,74.88" \
            " 196.16,75.98 195.45,77.22 L193.53,74.92 Q194.42,73.52" \
            " 195.39,72.38 196.38,71.23 197.45,70.33 200.36,67.89" \
            " 203.12,68.28 205.91,68.67 208.64,71.94 M242.78,70.78" \
            " L243.31,73.73 Q242.03,73.47 240.69,73.44 239.36,73.42" \
            " 237.97,73.67 235.88,74.05 234.91,74.77 233.95,75.48" \
            " 234.14,76.56 234.28,77.39 235.11,77.72 235.95,78.05" \
            " 238.3,78.09 L239.31,78.11 Q242.44,78.22 243.91,79.16" \
            " 245.38,80.11 245.75,82.2 246.17,84.58 244.52,86.31" \
            " 242.86,88.05 239.55,88.62 238.16,88.88 236.56,88.64" \
            " 234.98,88.42 233.14,87.73 L232.62,84.78 Q234.38,85.48" \
            " 235.98,85.7 237.59,85.92 239.08,85.67 241.08,85.31" \
            " 242.03,84.47 243,83.62 242.8,82.44 242.59,81.34 241.72,80.89" \
            " 240.84,80.44 238.11,80.38 L237.09,80.34 Q234.38,80.3" \
            " 233.02,79.42 231.66,78.56 231.33,76.69 230.92,74.42" \
            " 232.42,72.88 233.94,71.33 237.11,70.78 238.67,70.5" \
            " 240.11,70.5 241.55,70.52 242.78,70.78 M253.66,86.03" \
            " L255.39,95.88 252.53,96.38 248.19,71.75 251.05,71.25" \
            " 251.58,74.2 Q252.2,72.56 253.42,71.58 254.66,70.61" \
            " 256.55,70.28 259.69,69.72 262.08,71.81 264.47,73.92" \
            " 265.17,77.91 265.88,81.89 264.34,84.67 262.81,87.45" \
            " 259.67,88.02 257.78,88.34 256.3,87.84 254.81,87.36" \
            " 253.66,86.03 M262.23,78.42 Q261.75,75.64 260.19,74.3" \
            " 258.64,72.95 256.39,73.36 254.14,73.75 253.12,75.55" \
            " 252.12,77.34 252.61,80.12 253.11,82.89 254.66,84.23" \
            " 256.22,85.58 258.47,85.19 260.72,84.78 261.72,82.98" \
            " 262.73,81.19 262.23,78.42 M284.77,77.14 L285.09,78.98" \
            " 272.08,81.28 Q272.69,83.66 274.48,84.62 276.28,85.61" \
            " 279.09,85.12 280.72,84.83 282.16,84.06 283.61,83.31" \
            " 284.95,82.06 L285.47,85.02 Q284.11,86.25 282.61,87.03" \
            " 281.11,87.81 279.45,88.11 275.33,88.83 272.5,86.89" \
            " 269.67,84.97 268.97,80.97 268.23,76.81 270.09,73.98" \
            " 271.97,71.16 275.84,70.47 279.31,69.86 281.7,71.66" \
            " 284.11,73.45 284.77,77.14 M281.73,76.53 Q281.39,74.75" \
            " 279.94,73.89 278.48,73.05 276.39,73.42 274.02,73.84" \
            " 272.77,75.12 271.53,76.42 271.66,78.33 L281.73,76.53" \
            " M300.89,70.55 L301.41,73.5 Q300.11,73.22 298.86,73.19" \
            " 297.61,73.16 296.38,73.38 293.62,73.86 292.38,75.67" \
            " 291.12,77.5 291.62,80.3 292.11,83.09 293.91,84.38" \
            " 295.7,85.67 298.45,85.19 299.69,84.97 300.86,84.5" \
            " 302.03,84.05 303.14,83.34 L303.67,86.3 Q302.56,87.02" \
            " 301.33,87.47 300.11,87.94 298.69,88.19 294.8,88.88" \
            " 292.06,86.88 289.34,84.89 288.64,80.83 287.91,76.7" \
            " 289.81,73.92 291.72,71.16 295.75,70.44 297.05,70.2" \
            " 298.33,70.22 299.62,70.25 300.89,70.55 M305.89,71.75" \
            " L308.72,71.25 311.84,88.97 309.02,89.47 305.89,71.75" \
            " M304.86,65.83 L307.69,65.33 308.38,69.28 305.55,69.78" \
            " 304.86,65.83 M328.72,69.28 L331.84,87.02 329,87.52" \
            " 326.39,72.73 318.61,74.11 321.22,88.89 318.38,89.39" \
            " 315.77,74.61 313.06,75.09 312.55,72.14 315.25,71.66" \
            " 315.06,70.59 Q314.62,68.12 315.75,66.7 316.88,65.28" \
            " 319.62,64.8 L322.47,64.3 322.98,67.25 320.28,67.72" \
            " Q318.75,68 318.23,68.52 317.72,69.03 317.91,70.12" \
            " L318.09,71.16 328.72,69.28 M324.83,63.88 L327.67,63.38" \
            " 328.36,67.31 325.52,67.81 324.83,63.88 M351.09,77.14" \
            " L351.42,78.98 338.41,81.28 Q339,83.66 340.8,84.64" \
            " 342.59,85.62 345.42,85.12 347.05,84.83 348.48,84.06" \
            " 349.94,83.31 351.27,82.06 L351.78,85.02 Q350.44,86.25" \
            " 348.92,87.03 347.42,87.81 345.78,88.11 341.66,88.83" \
            " 338.83,86.91 336,84.98 335.3,80.98 334.56,76.83 336.42,73.98" \
            " 338.28,71.16 342.16,70.47 345.64,69.86 348.03,71.64" \
            " 350.44,73.44 351.09,77.14 M348.06,76.53 Q347.72,74.75" \
            " 346.25,73.89 344.8,73.05 342.7,73.42 340.33,73.84" \
            " 339.08,75.12 337.84,76.42 337.95,78.33 L348.06,76.53" \
            " M366.48,72.69 L364.92,63.83 367.75,63.33 371.92,86.97" \
            " 369.09,87.47 368.56,84.52 Q367.94,86.16 366.7,87.12" \
            " 365.48,88.11 363.58,88.45 360.45,89 358.06,86.91" \
            " 355.67,84.81 354.97,80.83 354.27,76.84 355.8,74.05" \
            " 357.33,71.27 360.45,70.72 362.36,70.38 363.84,70.86" \
            " 365.33,71.36 366.48,72.69 M357.89,80.31 Q358.38,83.08" \
            " 359.92,84.42 361.48,85.77 363.73,85.38 365.98,84.97" \
            " 367,83.17 368.02,81.38 367.53,78.61 367.03,75.83" \
            " 365.47,74.48 363.91,73.14 361.66,73.55 359.41,73.94" \
            " 358.39,75.73 357.39,77.53 357.89,80.31 M405.17,88.7" \
            " Q404.83,88.36 404.42,87.95 404.02,87.55 403.53,87.06" \
            " 401.81,85.34 399.84,85.44 397.89,85.55 395.97,87.47" \
            " L389.34,94.09 387.31,92.06 400.05,79.33 402.08,81.36" \
            " 399.95,83.48 Q401.67,83.05 403.22,83.55 404.78,84.06" \
            " 406.25,85.53 406.45,85.73 406.7,85.98 406.97,86.25" \
            " 407.28,86.56 L405.17,88.7 M415.62,89.42 Q414.3,87.52" \
            " 412.2,87.34 410.12,87.17 407.83,88.77 405.55,90.38 405,92.39" \
            " 404.45,94.41 405.8,96.31 407.11,98.19 409.19,98.36" \
            " 411.28,98.53 413.56,96.94 415.83,95.36 416.38,93.33" \
            " 416.94,91.3 415.62,89.42 M418.08,87.7 Q420.22,90.77" \
            " 419.48,93.89 418.77,97.02 415.31,99.44 411.88,101.86" \
            " 408.67,101.47 405.47,101.09 403.33,98.03 401.16,94.94" \
            " 401.91,91.81 402.66,88.7 406.09,86.28 409.55,83.86" \
            " 412.72,84.23 415.91,84.61 418.08,87.7 M439.5,81.59" \
            " L435.41,84.47 438.8,89.33 436.34,91.05 432.95,86.19" \
            " 425.7,91.27 Q424.06,92.42 423.92,93.23 423.8,94.05" \
            " 424.83,95.52 L426.52,97.94 424.06,99.66 422.38,97.23" \
            " Q420.45,94.5 420.8,92.7 421.16,90.92 424.03,88.91" \
            " L431.28,83.83 430.08,82.09 432.53,80.38 433.73,82.11" \
            " 437.83,79.23 439.5,81.59 M442.67,94.39 Q440.67,91.53" \
            " 439.42,90.77 438.17,90 437.03,90.8 436.11,91.45 436.14,92.66" \
            " 436.19,93.86 437.19,95.28 438.56,97.23 440.39,97.72" \
            " 442.23,98.2 443.89,97.03 L444.31,96.73 442.67,94.39" \
            " M447.25,98.19 L439.41,103.69 437.77,101.33 440.22,99.61" \
            " Q438.41,99.67 436.95,98.89 435.52,98.11 434.3,96.38" \
            " 432.75,94.17 433.02,92.05 433.3,89.92 435.28,88.53" \
            " 437.59,86.92 439.91,87.7 442.22,88.5 444.47,91.7" \
            " L446.78,95.02 447,94.86 Q448.47,93.83 448.5,92.2" \
            " 448.55,90.58 447.2,88.64 446.33,87.42 445.31,86.41" \
            " 444.3,85.39 443.14,84.59 L445.59,82.88 Q446.91,83.88" \
            " 447.95,84.94 449.02,86.02 449.81,87.17 452,90.28" \
            " 451.36,93.02 450.73,95.75 447.25,98.19 M471.64,81.61" \
            " L467.55,84.47 470.95,89.31 468.48,91.05 465.08,86.2" \
            " 457.83,91.28 Q456.19,92.42 456.05,93.22 455.92,94.03" \
            " 456.95,95.5 L458.66,97.92 456.2,99.64 454.5,97.22" \
            " Q452.59,94.5 452.94,92.7 453.3,90.91 456.17,88.91" \
            " L463.42,83.83 462.22,82.11 464.69,80.38 465.89,82.09" \
            " 469.98,79.23 471.64,81.61 M478.47,82.14 L480.12,84.5" \
            " 465.38,94.83 463.72,92.47 478.47,82.14 M483.38,78.7" \
            " L485.03,81.06 481.75,83.36 480.09,81 483.38,78.7" \
            " M488.78,89.42 Q487.45,87.53 485.38,87.34 483.3,87.16" \
            " 481,88.77 478.72,90.38 478.17,92.38 477.62,94.39 478.95,96.3" \
            " 480.28,98.17 482.36,98.34 484.45,98.53 486.72,96.94" \
            " 488.98,95.36 489.55,93.33 490.11,91.3 488.78,89.42" \
            " M491.23,87.7 Q493.39,90.77 492.66,93.89 491.94,97.02" \
            " 488.47,99.44 485.03,101.84 481.84,101.47 478.66,101.09" \
            " 476.5,98.03 474.34,94.94 475.08,91.81 475.81,88.69" \
            " 479.25,86.28 482.72,83.86 485.89,84.23 489.08,84.61" \
            " 491.23,87.7 M509.33,98.23 L500.55,104.38 498.89,102.02" \
            " 507.59,95.92 Q509.39,94.67 509.72,93.25 510.06,91.84" \
            " 508.95,90.25 507.62,88.34 505.75,88 503.89,87.67" \
            " 502.02,88.98 L493.8,94.73 492.14,92.38 506.89,82.06" \
            " 508.55,84.42 506.08,86.14 Q507.91,86.12 509.31,86.84" \
            " 510.73,87.56 511.78,89.06 513.52,91.53 512.89,93.84" \
            " 512.27,96.17 509.33,98.23"
        self.assertEqual(expected, d)

    def test_get_sub_string_length_tspan01_01(self):
        # See also: tspan01.html
        # Test with DejaVu font 2.37, FontConfig 2.12.6, and FreeType 2.8
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text01')
        nchars = text.get_number_of_chars()
        advances = list()
        for i in range(nchars):
            advances.append(text.get_sub_string_length(i, 1))
        expected = [55.805, 37.870, 20.466, 20.466, 38.526, 20.341, 20.341,
                    38.526, 41.214, 25.716, 20.341, 25.716, 41.214, 37.870,
                    30.590, 37.870, 25.715]
        for i, (e, a) in enumerate(zip(expected, advances)):
            self.assertAlmostEqual(e, a, places=places, msg=i)

    def test_get_sub_string_length_tspan01_02(self):
        # See also: tspan01.html
        # Test with DejaVu font 2.37, FontConfig 2.12.6, and FreeType 2.8
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text02')
        nchars = text.get_number_of_chars()
        advances = list()
        for i in range(nchars):
            advances.append(text.get_sub_string_length(i, 1))
        expected = [36.682, 38.526, 41.214, 20.341, 38.151, 30.590, 37.870,
                    20.341, 46.525, 42.682, 29.559, 22.278, 38.151, 20.341,
                    40.964, 38.151, 41.214, 38.151, 41.214, 38.151, 20.341]
        for i, (e, a) in enumerate(zip(expected, advances)):
            self.assertAlmostEqual(e, a, places=places, msg=i)

    def test_get_sub_string_length_tspan01_03(self):
        # See also: tspan01.html
        # Test with DejaVu font 2.37, FontConfig 2.12.6, and FreeType 2.8
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text03')
        nchars = text.get_number_of_chars()
        advances = list()
        for i in range(nchars):
            advances.append(text.get_sub_string_length(i, 1))
        expected = [47.025, 41.214, 25.716, 20.341, 36.152, 38.526, 41.214,
                    20.341, 41.464, 33.715, 40.714, 22.278, 38.151, 20.341,
                    40.964, 37.870, 38.151, 35.839, 41.214, 25.716]
        for i, (e, a) in enumerate(zip(expected, advances)):
            self.assertAlmostEqual(e, a, places=places, msg=i)

    def test_get_sub_string_length_tspan04(self):
        # See also: tspan04.html
        formatter.precision = 2

        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN04))
        root = tree.getroot()

        text = root.get_element_by_id('text01')
        nchars = text.get_number_of_chars()
        advances = list()
        for i in range(nchars):
            advances.append(text.get_sub_string_length(i, 1))
        expected = [41.318, 33.806, 15.266, 15.266, 33.618, 17.466, 17.466,
                    33.618, 34.825, 21.544, 17.466, 21.544, 34.825, 33.806,
                    21.383, 33.806]
        for i, (e, a) in enumerate(zip(expected, advances)):
            self.assertAlmostEqual(e, a, places=places, msg=i)

    def test_text_content01(self):
        # Node#nodeName
        # Node#nodeType
        # Node#nodeValue
        # Node#textContent
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ROTATE_SCALE))
        root = tree.getroot()

        elements = list()
        elements.append(root)
        for node in root.iterdescendants():
            elements.append(node)

        node = elements.pop(0)
        self.assertEqual('svg', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('desc', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        expected = 'Example RotateScale - Rotate and scale transforms'
        self.assertIsNone(node.node_value)
        self.assertEqual(expected, node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('#comment', node.node_name)
        self.assertEqual(Node.COMMENT_NODE, node.node_type)
        expected = " Draw the axes of the original coordinate system "
        self.assertEqual(expected, node.node_value)
        self.assertEqual(expected, node.text_content)

        node = elements.pop(0)
        self.assertEqual('line', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('line', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('#comment', node.node_name)
        self.assertEqual(Node.COMMENT_NODE, node.node_type)
        expected = """ Establish a new coordinate system whose origin is at (50,30)
         in the initial coord. system and which is rotated by 30 degrees. """
        self.assertEqual(expected, node.node_value)
        self.assertEqual(expected, node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('line', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('line', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('path', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('text', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        expected = """
                ABC (rotate)
            """
        self.assertIsNone(node.node_value)
        self.assertEqual(expected, node.text_content)

        node = elements.pop(0)
        self.assertEqual('#comment', node.node_name)
        self.assertEqual(Node.COMMENT_NODE, node.node_type)
        expected = """ Establish a new coordinate system whose origin is at (200,40)
         in the initial coord. system and which is scaled by 1.5. """
        self.assertEqual(expected, node.node_value)
        self.assertEqual(expected, node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('g', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('line', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('line', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('path', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        self.assertIsNone(node.node_value)
        self.assertIsNone(node.text_content)

        node = elements.pop(0)
        self.assertEqual('text', node.node_name)
        self.assertEqual(Node.ELEMENT_NODE, node.node_type)
        expected = """
                ABC (scale)
            """
        self.assertIsNone(node.node_value)
        self.assertEqual(expected, node.text_content)

    def test_text_content02(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text01')
        expected = """
                Hello, out there!
            """
        self.assertEqual(expected, text.text_content)

    def test_text_content03(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text02')
        expected = """
                You are
                not
                
                a banana.
            """
        self.assertEqual(expected, text.text_content)

    def test_text_content04(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('tspan0201')
        expected = """not
                """
        self.assertEqual(expected, text.text_content)

    def test_text_content05(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text03')
        expected = """
                But you
                
                    are
                
                
                    a peach!
                
            """
        self.assertEqual(expected, text.text_content)

    def test_text_content06(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('tspan0301')
        expected = """
                    are
                """
        self.assertEqual(expected, text.text_content)

    def test_text_content07(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('tspan0302')
        expected = """
                    a peach!
                """
        self.assertEqual(expected, text.text_content)

    def test_text_content08(self):
        # Node#textContent
        # See also: tspan01.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_TSPAN01))
        root = tree.getroot()

        text = root.get_element_by_id('text02')
        self.assertEqual(1, len(text))  # tspan
        self.assertTrue(len(text.attributes) > 0)

        expected = 'Hello World!'
        text.text_content = expected
        self.assertEqual(0, len(text))
        self.assertTrue(len(text.attributes) > 0)
        self.assertEqual(expected, text.text_content)

    def _test_rtl_text01(self):
        # bi-directional text
        formatter.precision = 2
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_RTL_TEXT))
        root = tree.getroot()

        # 'داستان SVG 1.1 SE طولا ني است.'
        text = root.get_element_by_id('text01')

        path_data = text.get_path_data()
        print([PathParser.tostring(path_data)])
        # print(root.tostring(encoding='unicode'))

    def _test_rtl_text02(self):
        # bi-directional text
        formatter.precision = 2
        parser = SVGParser()
        root = parser.create_element('svg')
        root.attributes.update({
            'width': '300',
            'height': '100',
            'viewBox': '0 0 300 100',
        })
        text = root.create_sub_element('text')
        text.attributes.update({
            'x': '250',
            'y': '30',
        })
        text.attributes.set_style({
            'font': '20px Vazir, "DejaVu Sans"',
            'inline-size': '200px',
            'direction': 'rtl',
        })
        text.text = 'هذا النص يلتف في 200 بكسل.'

        path_data = text.get_path_data()
        print([PathParser.tostring(path_data)])
        print(text.get_bbox())

    def _test_rtl_text03(self):
        # http://unicode.org/faq/bidi.html
        formatter.precision = 2
        parser = SVGParser()
        root = parser.create_element('svg')
        root.attributes.update({
            'width': '300',
            'height': '100',
            'viewBox': '0 0 300 100',
        })
        text = root.create_sub_element('text')
        text.attributes.set_ns(Element.XML_NAMESPACE_URI, 'lang', 'ar')
        text.attributes.update({
            'x': '200',
            'y': '50',
            'font-family': 'Vazir, DejaVu Serif, serif',
            'font-size': '24',
            'direction': 'rtl',
        })
        text.text = " ما هو الترميز الموحد يونيكود؟ in Arabic "

        path_data = text.get_path_data()
        print([PathParser.tostring(path_data)])

    def _test_rtl_text04(self):
        # http://unicode.org/faq/bidi.html
        formatter.precision = 2
        parser = SVGParser()
        root = parser.create_element('svg')
        root.attributes.update({
            'width': '300',
            'height': '100',
            'viewBox': '0 0 300 100',
        })
        text = root.create_sub_element('text')
        text.attributes.set_ns(Element.XML_NAMESPACE_URI, 'lang', 'ar')
        text.attributes.update({
            'x': '-150',
            'y': '100',
            'font-family': 'Vazir, DejaVu Serif, serif',
            'font-size': '24',
            'direction': 'ltr',
        })
        text.text = " ما هو الترميز الموحد يونيكود؟ in Arabic "

        path_data = text.get_path_data()
        print([PathParser.tostring(path_data)])

    def _test_text_repositioning_x01(self):
        formatter.precision = 2
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Serif, serif',
            'font-size': '12',
        })
        text = group.create_sub_element('text')
        text.text = 'flip'
        text.attributes.update({
            'x': '10, 20, 30, 40, 50, 60, 70, 80, 90, 100',
            'y': '0',
            'rotate': '0',
        })
        tspan = text.create_sub_element('tspan')
        tspan.text = 'flop'
        # x: fl(10) i(30) p(40) _(50) fl(60) o(80) p(90)

        path_data = text.get_path_data()
        print([PathParser.tostring(path_data)])

    def _test_text_repositioning_x02(self):
        formatter.precision = 2
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Serif, serif',
            'font-size': '18',
        })
        text = group.create_sub_element('text')
        text.text = 'ff'
        text.attributes.update({
            'x': '10, 20, 30, 40, 50, 60',
            'y': '0',
            'rotate': '-20',
        })
        tspan = text.create_sub_element('tspan')
        tspan.text = 'flfflo'
        # x: ff(10) _(30) fl(40) ffl(60)

        path_data = text.get_path_data()
        print([PathParser.tostring(path_data)])

    def _test_text_wrap_vertical(self):
        formatter.precision = 2
        parser = SVGParser()
        root = parser.create_element('svg')
        root.attributes.update({
            Element.XML_LANG: 'ja-Jpan',
            'width': '100',
            'height': '300',
            'viewBox': '0 0 100 300',
        })
        text = root.create_sub_element('text')
        text.attributes.update({
            'x': '62.5',
            'y': '25',
            'inline-size': '200',
        })
        text.attributes.set_style({
            'font': '25px IPAmjMincho',
            'inline-size': '200px',
            'writing-mode': 'vertical-rl',
            # 'font-kerning': 'normal',
            'font-feature-settings': '"swsh" 2',
            'font-variant-caps': 'small-caps',
        })
        text.text = 'テキストは１０文字の後に折り返されます。'

        path_data = text.get_path_data()
        # print([PathParser.tostring(path_data)])

        bbox = text.get_bbox()
        print((bbox.x, bbox.y, bbox.width, bbox.height))

        # style = text.get_computed_style()
        # for key, value in sorted(style.items()):
        #     print((key, value))
        font = Font(text)
        face = font.face
        # face.glyph.render_glyph(0)
        # face.load_char('M')
        bbox = face.bbox
        size = face.size
        glyph = face.glyph
        metrics = face.size.metrics
        x_ratio = metrics.x_ppem / face.units_per_em
        y_ratio = metrics.y_ppem / face.units_per_em
        print(('units_per_em', face.units_per_em))
        print(('size.metrics.x_ppem', size.metrics.x_ppem))
        print(('size.metrics.y_ppem', size.metrics.y_ppem))
        print(('size.metrics.height', size.metrics.height / 64))
        print(('size.metrics.x_scale', size.metrics.x_scale / 0x10000))
        print(('size.metrics.y_scale', size.metrics.y_scale / 0x10000))
        print(('height', face.height * y_ratio))
        print(('glyph.linear_hori_advance', glyph.linear_hori_advance / 0x10000))
        print(('glyph.linear_vert_advance', glyph.linear_vert_advance / 0x10000))
        print(('glyph.metrics.width', glyph.metrics.width / 64))
        print(('glyph.metrics.height', glyph.metrics.height / 64))
        print(('glyph.metrics.hori_bearing_x', glyph.metrics.hori_bearing_x / 64))
        print(('glyph.metrics.hori_bearing_y', glyph.metrics.hori_bearing_y / 64))
        print(('glyph.metrics.vert_bearing_x', glyph.metrics.vert_bearing_x / 64))
        print(('glyph.metrics.vert_bearing_y', glyph.metrics.vert_bearing_y / 64))

    def test_white_space_prop01(self):
        # See also: white-space.html
        # 'white-space' property: normal
        # New lines: Collapse
        # Spaces/Tabs: Collapse
        # Text wrapping: Wrap
        parser = SVGParser()
        text = parser.create_element('text')
        text.text = \
            "\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n&#x20;   ﾊﾝ  ｶｸ\n"
        style = {'white-space': 'normal'}
        out = CSSUtils.normalize_text_content(
            text, text.text, style, first=True, tail=True)
        expected = 'Hello there ＦＵＬＬ ＷＩＤＴＨﾊﾝ ｶｸ'
        self.assertEqual(expected, out)

    def test_white_space_prop02(self):
        # See also: white-space.html
        # 'white-space' property: nowrap
        # New lines: Collapse
        # Spaces/Tabs: Collapse
        # Text wrapping: No wrap
        parser = SVGParser()
        text = parser.create_element('text')
        text.text = \
            "\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n&#x20;   ﾊﾝ  ｶｸ\n"
        style = {'white-space': 'nowrap'}
        out = CSSUtils.normalize_text_content(
            text, text.text, style, first=True, tail=True)
        expected = 'Hello there ＦＵＬＬ ＷＩＤＴＨﾊﾝ ｶｸ'
        self.assertEqual(expected, out)

    def test_white_space_prop03(self):
        # See also: white-space.html
        # 'white-space' property: pre
        # New lines: Preserve
        # Spaces/Tabs: Preserve
        # Text wrapping: No wrap
        parser = SVGParser()
        text = parser.create_element('text')
        text.text = \
            "\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n&#x20;   ﾊﾝ  ｶｸ\n"
        style = {'white-space': 'pre'}
        out = CSSUtils.normalize_text_content(
            text, text.text, style, first=True, tail=True)
        expected = '\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n    ﾊﾝ  ｶｸ\n'
        self.assertEqual(expected, out)

    def test_white_space_prop04(self):
        # See also: white-space.html
        # 'white-space' property: pre-wrap
        # New lines: Preserve
        # Spaces/Tabs: Preserve
        # Text wrapping: Wrap
        parser = SVGParser()
        text = parser.create_element('text')
        text.text = \
            "\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n&#x20;   ﾊﾝ  ｶｸ\n"
        style = {'white-space': 'pre-wrap'}
        out = CSSUtils.normalize_text_content(
            text, text.text, style, first=True, tail=True)
        expected = '\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n    ﾊﾝ  ｶｸ\n'
        self.assertEqual(expected, out)

    def test_white_space_prop05(self):
        # See also: white-space.html
        # 'white-space' property: pre-line
        # New lines: Preserve
        # Spaces/Tabs: Collapse
        # Text wrapping: Wrap
        parser = SVGParser()
        text = parser.create_element('text')
        text.text = \
            "\nHello there\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n&#x20;   ﾊﾝ  ｶｸ\n"
        style = {'white-space': 'pre-line'}
        out = CSSUtils.normalize_text_content(
            text, text.text, style, first=True, tail=True)
        expected = '\nHello there\nＦＵＬＬ ＷＩＤＴＨ\nﾊﾝ ｶｸ\n'
        self.assertEqual(expected, out)

    def test_white_space_prop06(self):
        # See also: white-space.html
        # 'white-space' property: normal
        # New lines: Collapse
        # Spaces/Tabs: Collapse
        # Text wrapping: Wrap
        parser = SVGParser()
        text = parser.create_element('text')
        text.text = \
            "\n\nHello there\n\n\t\tＦＵＬＬ  ＷＩＤＴＨ \n\n&#x20;   ﾊﾝ  ｶｸ\n\n"
        style = {'white-space': 'normal'}
        out = CSSUtils.normalize_text_content(
            text, text.text, style, first=True, tail=True)
        expected = 'Hello there ＦＵＬＬ ＷＩＤＴＨﾊﾝ ｶｸ'
        self.assertEqual(expected, out)


if __name__ == '__main__':
    unittest.main()
