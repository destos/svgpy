#!/usr/bin/env python3

import math
import sys
import unittest
from io import StringIO

sys.path.extend(['.', '..'])

from svgpy.element import HTMLAudioElement, HTMLVideoElement, \
    SVGCircleElement, SVGGElement, SVGPathElement, SVGPolylineElement, \
    SVGRectElement, SVGSVGElement, SVGTextElement
from svgpy import Comment, Element, Font, \
    HTMLElement, \
    Matrix, Node, PathParser, Rect, SVGLength, SVGParser, SVGPathSegment, \
    SVGPathDataSettings, SVGPreserveAspectRatio, SVGZoomAndPan, Window, \
    formatter

SVG_ARCS02 = '''
<svg width="12cm" height="5.25cm" viewBox="0 0 1200 525" version="1.1"
     xmlns="http://www.w3.org/2000/svg"
     xmlns:xlink="http://www.w3.org/1999/xlink">
    <title>Example arcs02 - arc options in paths</title>
    <desc>Pictures showing the result of setting
        large-arc-flag and sweep-flag to the four
        possible combinations of 0 and 1.
    </desc>
    <g font-family="Verdana">
        <defs>
            <g id="baseEllipses" font-size="20">
                <ellipse cx="125" cy="125" rx="100" ry="50"
                         fill="none" stroke="#888888" stroke-width="2"/>
                <ellipse cx="225" cy="75" rx="100" ry="50"
                         fill="none" stroke="#888888" stroke-width="2"/>
                <text x="35" y="70">Arc start</text>
                <text x="225" y="145">Arc end</text>
            </g>
        </defs>
        <rect x="1" y="1" width="1198" height="523"
              fill="none" stroke="blue" stroke-width="1"/>

        <g font-size="30">
            <g transform="translate(0,0)">
                <use xlink:href="#baseEllipses"/>
            </g>
            <g transform="translate(400,0)">
                <text x="50" y="210">large-arc-flag=0</text>
                <text x="50" y="250">sweep-flag=0</text>
                <use xlink:href="#baseEllipses"/>
                <path d="M 125,75 a100,50 0 0,0 100,50"
                      id="path01"
                      fill="none" stroke="red" stroke-width="6"/>
                <path d="M125,75 C125,102.614 169.772,125 225,125"
                      id="path01norm"
                      fill="none" stroke="blue" stroke-width="4" stroke-dasharray="5"/>
            </g>
            <g transform="translate(800,0)">
                <text x="50" y="210">large-arc-flag=0</text>
                <text x="50" y="250">sweep-flag=1</text>
                <use xlink:href="#baseEllipses"/>
                <path d="M 125,75 a100,50 0 0,1 100,50"
                      id="path02"
                      fill="none" stroke="red" stroke-width="6"/>
                <path d="M125,75 C180.228,75 225,97.386 225,125"
                      id="path02norm"
                      fill="none" stroke="blue" stroke-width="4"
                      stroke-dasharray="5"/>
            </g>
            <g transform="translate(400,250)">
                <text x="50" y="210">large-arc-flag=1</text>
                <text x="50" y="250">sweep-flag=0</text>
                <use xlink:href="#baseEllipses"/>
                <path d="M 125,75 a100,50 0 1,0 100,50"
                      id="path03"
                      fill="none" stroke="red" stroke-width="6"/>
                <path d="M125,75 C69.772,75 25,97.386 25,125 25,152.614 69.772,175 125,175 180.228,175 225,152.614 225,125"
                      id="path03norm"
                      fill="none" stroke="blue" stroke-width="4"
                      stroke-dasharray="5"/>
                <circle cx="125" cy="125" r="5" fill="green" stroke="black"
                        id="center3"/>
            </g>
            <g transform="translate(800,250)">
                <text x="50" y="210">large-arc-flag=1</text>
                <text x="50" y="250">sweep-flag=1</text>
                <use xlink:href="#baseEllipses"/>
                <path d="M 125,75 a100,50 0 1,1 100,50"
                      id="path04"
                      fill="none" stroke="red" stroke-width="6"/>
                <path d="M125,75 C125,47.386 169.772,25 225,25 280.228,25 325,47.386 325,75 325,102.614 280.228,125 225,125"
                      id="path04norm"
                      fill="none" stroke="blue" stroke-width="4"
                      stroke-dasharray="5"/>
                <circle cx="125" cy="75" r="5" fill="white" stroke="black"/>
                <circle cx="225" cy="125" r="5" fill="red" stroke="black"/>
                <circle cx="225" cy="75" r="5" fill="green" stroke="black"/>
            </g>
        </g>
    </g>
</svg>
'''

SVG_BBOX01 = '''
<svg xmlns="http://www.w3.org/2000/svg">

  <title>Bounding Box Calculation</title>
  <desc>Examples of elements with different bounding box results based on context.</desc>

  <defs id="defs-1">
     <rect id="rect-1" x="20" y="20" width="40" height="40" fill="blue" />
  </defs>

  <g id="group-1">
    <use id="use-1" href="#rect-1" x="10" y="10" />

    <g id="group-2" display="none">
      <rect id="rect-2" x="10" y="10" width="100" height="100" fill="red" />
    </g>
  </g>
</svg>
'''

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

SVG_PRESERVE_ASPECT_RATIO = '''
<svg width="450px" height="300px" xmlns="http://www.w3.org/2000/svg">

    <desc>Example SVGPreserveAspectRatio - illustrates preserveAspectRatio
        attribute
    </desc>

    <style type="text/css">
    text { font-size: 9; }
    rect { fill: none; stroke: blue; }

    </style>

    <defs>
        <g id="smile">
            <rect x='.5' y='.5' width='29' height='39'
                  style="fill:black;stroke:red"/>
            <circle cx='15' cy='20' r='10' fill='yellow'/>
            <circle cx='12' cy='17' r='1.5' fill='black'/>
            <circle cx='17' cy='17' r='1.5' fill='black'/>
            <path d='M 10 24 A 8 8 0 0 0 20 24' stroke='black'
                  stroke-width='2'/>
        </g>
    </defs>

    <rect x="1" y="1" width="448" height="298"/>

    <text x="10" y="30">SVG to fit</text>
    <g transform="translate(20,40)">
        <use href="#smile"/>
    </g>

    <text x="10" y="110">Viewport 1</text>
    <g id="viewport1" transform="translate(10,120)">
        <rect x='.5' y='.5' width='49' height='29'/>
    </g>

    <text x="10" y="180">Viewport 2</text>
    <g id="viewport2" transform="translate(20,190)">
        <rect x='.5' y='.5' width='29' height='59'/>
    </g>

    <g id="meet-group-1" transform="translate(100, 60)">
        <text x="0" y="-30">--------------- meet ---------------</text>
        <g>
            <text y="-10">xMin*</text>
            <rect x='.5' y='.5' width='49' height='29'/>
            <svg preserveAspectRatio="xMinYMin meet" viewBox="0 0 30 40"
                 width="50" height="30">
                <use id="xMinYMin_meet" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(70,0)">
            <text y="-10">xMid*</text>
            <rect x='.5' y='.5' width='49' height='29'/>
            <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 30 40"
                 width="50" height="30">
                <use id="xMidYMid_meet" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(0,70)">
            <text y="-10">xMax*</text>
            <rect x='.5' y='.5' width='49' height='29'/>
            <svg preserveAspectRatio="xMaxYMax meet" viewBox="0 0 30 40"
                 width="50" height="30">
                <use id="xMaxYMax_meet" href="#smile"/>
            </svg>
        </g>
    </g>

    <g id="meet-group-2" transform="translate(250, 60)">
        <text x="0" y="-30">---------- meet ----------</text>
        <g>
            <text y="-10">*YMin</text>
            <rect x='.5' y='.5' width='29' height='59'/>
            <svg preserveAspectRatio="xMinYMin meet" viewBox="0 0 30 40"
                 width="30" height="60">
                <use id="xMinYMin_meet02" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(50, 0)">
            <text y="-10">*YMid</text>
            <rect x='.5' y='.5' width='29' height='59'/>
            <svg preserveAspectRatio="xMidYMid meet" viewBox="0 0 30 40"
                 width="30" height="60">
                <use id="xMidYMid_meet02" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(100, 0)">
            <text y="-10">*YMax</text>
            <rect x='.5' y='.5' width='29' height='59'/>
            <svg preserveAspectRatio="xMaxYMax meet" viewBox="0 0 30 40"
                 width="30" height="60">
                <use id="xMaxYMax_meet02" href="#smile"/>
            </svg>
        </g>
    </g>

    <g id="slice-group-1" transform="translate(100, 220)">
        <text x="0" y="-30">---------- slice ----------</text>
        <g>
            <text y="-10">xMin*</text>
            <rect x='.5' y='.5' width='29' height='59'/>
            <svg preserveAspectRatio="xMinYMin slice" viewBox="0 0 30 40"
                 width="30" height="60">
                <use id="xMinYMin_slice" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(50,0)">
            <text y="-10">xMid*</text>
            <rect x='.5' y='.5' width='29' height='59'/>
            <svg preserveAspectRatio="xMidYMid slice" viewBox="0 0 30 40"
                 width="30" height="60">
                <use id="xMidYMid_slice" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(100,0)">
            <text y="-10">xMax*</text>
            <rect x='.5' y='.5' width='29' height='59'/>
            <svg preserveAspectRatio="xMaxYMax slice" viewBox="0 0 30 40"
                 width="30" height="60">
                <use id="xMaxYMax_slice" href="#smile"/>
            </svg>
        </g>
    </g>

    <g id="slice-group-2" transform="translate(250, 220)">
        <text x="0" y="-30">--------------- slice ---------------</text>
        <g>
            <text y="-10">*YMin</text>
            <rect x='.5' y='.5' width='49' height='29'/>
            <svg preserveAspectRatio="xMinYMin slice" viewBox="0 0 30 40"
                 width="50" height="30">
                <use id="xMinYMin_slice02" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(70,0)">
            <text y="-10">*YMid</text>
            <rect x='.5' y='.5' width='49' height='29'/>
            <svg preserveAspectRatio="xMidYMid slice" viewBox="0 0 30 40"
                 width="50" height="30">
                <use id="xMidYMid_slice02" href="#smile"/>
            </svg>
        </g>
        <g transform="translate(140,0)">
            <text y="-10">*YMax</text>
            <rect x='.5' y='.5' width='49' height='29'/>
            <svg preserveAspectRatio="xMaxYMax slice" viewBox="0 0 30 40"
                 width="50" height="30">
                <use id="xMaxYMax_slice02" href="#smile"/>
            </svg>
        </g>
    </g>
</svg>
'''

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
    <g transform="translate(50,30)" id="g11">
        <g transform="rotate(30)" id="g12">
            <g fill="none" stroke="red" stroke-width="3" id="g13">
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
    <g transform="translate(200,40)" id="g21">
        <g transform="scale(1.5)" id="g22">
            <g fill="none" stroke="red" stroke-width="3" id="g23">
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

# from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
SVG_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="100" height="100" viewBox="0 0 100 100">
 <g id='gtop' stroke-width="12" stroke="#000">
   <g id="svgstar" transform="translate(50,50)">
     <path id="svgbar" d="M-27-5a7,7,0,1,0,0,10h54a7,7,0,1,0,0-10z"/>
     <use id='use1' xlink:href="#svgbar" transform="rotate(45)"/>
     <use id='use2' xlink:href="#svgbar" transform="rotate(90)"/>
     <use id='use3' xlink:href="#svgbar" transform="rotate(135)"/>
   </g>
 </g>
 <use id="usetop" xlink:href="#svgstar" fill="#FB4"/>
</svg>
'''

SVG_UNITS = '''
<svg width="400px" height="200px" viewBox="0 0 4000 2000"
     xmlns="http://www.w3.org/2000/svg">
    <title>Example Units</title>
    <desc>Illustrates various units options</desc>

    <!-- Frame the picture -->
    <rect x="5" y="5" width="3990" height="1990"
          fill="none" stroke="blue" stroke-width="10"/>

    <g fill="blue" stroke="red" font-family="Verdana" font-size="150">
        <!-- Absolute unit specifiers -->
        <g transform="translate(400,0)">
            <text x="-50" y="300" fill="black" stroke="none">Abs. units:</text>
            <rect x="0" y="400" width="4in" height="2in" stroke-width=".4in"
                  id="rect_abs_01"/>
            <rect x="0" y="750" width="384" height="192" stroke-width="38.4"
                  id="rect_abs_02"/>
            <g transform="scale(2)">
                <rect x="0" y="600" width="4in" height="2in"
                      stroke-width=".4in" id="rect_abs_03"/>
            </g>
        </g>

        <!-- Relative unit specifiers -->
        <g transform="translate(1600,0)">
            <text x="-50" y="300" fill="black" stroke="none">Rel. units:</text>
            <rect x="0" y="400" width="2.5em" height="1.25em"
                  stroke-width=".25em" id="rect_rel_01"/>
            <rect x="0" y="750" width="375" height="187.5"
                  stroke-width="37.5" id="rect_rel_02"/>
            <g transform="scale(2)">
                <rect x="0" y="600" width="2.5em" height="1.25em"
                      stroke-width=".25em" id="rect_rel_03"/>
            </g>
        </g>

        <!-- Percentages -->
        <g transform="translate(2800,0)">
            <text x="-50" y="300" fill="black" stroke="none">Percentages:
            </text>
            <rect x="0" y="400" width="10%" height="10%" stroke-width="1%"
                  id="rect_per_01"/>
            <rect x="0" y="750" width="400" height="200" stroke-width="31.62"
                  id="rect_per_02"/>
            <g transform="scale(2)">
                <rect x="0" y="600" width="10%" height="10%"
                      stroke-width="1%" id="rect_per_03"/>
            </g>
        </g>
    </g>
</svg>
'''

SVG_VIEW_BOX = '''
<svg width="600px" height="200px"
     id="root"
     xmlns="http://www.w3.org/2000/svg">

    <svg width="300px" height="200px"
         x="0" y="0"
         viewBox="0 0 1500 1000" preserveAspectRatio="none"
         id="svg01"
         xmlns="http://www.w3.org/2000/svg">
        <desc>Example ViewBox - uses the viewBox
        attribute to automatically create an initial user coordinate
        system which causes the graphic to scale to fit into the
        viewport no matter what size the viewport is.</desc>

        <!-- This rectangle goes from (0,0) to (1500,1000) in local coordinate system.
             Because of the viewBox attribute above,
             the rectangle will end up filling the entire area
             reserved for the SVG content. -->
        <rect x="0" y="0" width="1500" height="1000"
              fill="yellow" stroke="blue" stroke-width="12" id="rect01" />

        <!-- A large, red triangle -->
        <path fill="red"  d="M 750,100 L 250,900 L 1250,900 z"/>

        <!-- A text string that spans most of the viewport -->
        <text x="100" y="600" font-size="200" font-family="Verdana" >
            Stretch to fit
        </text>
    </svg>

    <svg width="150px" height="200px"
         x="300" y="0"
         viewBox="0 0 1500 1000" preserveAspectRatio="none"
         id="svg02"
         xmlns="http://www.w3.org/2000/svg">
        <desc>Example ViewBox - uses the viewBox
        attribute to automatically create an initial user coordinate
        system which causes the graphic to scale to fit into the
        viewport no matter what size the viewport is.</desc>

        <!-- This rectangle goes from (0,0) to (1500,1000) in local coordinate system.
             Because of the viewBox attribute above,
             the rectangle will end up filling the entire area
             reserved for the SVG content. -->
        <rect x="0" y="0" width="1500" height="1000"
              fill="yellow" stroke="blue" stroke-width="12" id="rect02" />

        <!-- A large, red triangle -->
        <path fill="red"  d="M 750,100 L 250,900 L 1250,900 z"/>

        <!-- A text string that spans most of the viewport -->
        <text x="100" y="600" font-size="200" font-family="Verdana" >
            Stretch to fit
        </text>
    </svg>
</svg>
'''

places = 0
delta = 1


# Test with: Chrome 64.0 (Linux 64-bit)
class BasicShapesTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3
        SVGLength.dpi = 96

    def test_bbox01_01(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('defs-1')
        bbox = element.get_bbox()
        self.assertEqual(bbox, Rect(), msg=element)

    def test_bbox01_02(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('rect-1')
        bbox = element.get_bbox()
        self.assertEqual(bbox, Rect(20, 20, 40, 40), msg=element.id)

    def test_bbox01_03(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('group-1')
        bbox = element.get_bbox()
        self.assertEqual(bbox, Rect(30, 30, 40, 40), msg=element.id)

    def test_bbox01_04(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('use-1')
        bbox = element.get_bbox()
        self.assertEqual(bbox, Rect(30, 30, 40, 40), msg=element.id)

    def test_bbox01_05(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('group-2')
        bbox = element.get_bbox()
        self.assertEqual(bbox, Rect(10, 10, 100, 100), msg=element.id)

    def test_bbox01_06(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('rect-2')
        bbox = element.get_bbox()
        self.assertEqual(bbox, Rect(10, 10, 100, 100), msg=element.id)

    def test_bbox02_01(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root
        bbox = element.get_bbox()
        self.assertAlmostEqual(bbox.x, 11.101, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.y, 11.101, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.width, 77.798, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.height, 77.798, msg=element.id, delta=delta)

    def test_bbox02_02(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('gtop')
        bbox = element.get_bbox()
        self.assertAlmostEqual(bbox.x, 11.101, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.y, 11.101, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.width, 77.798, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.height, 77.798, msg=element.id, delta=delta)

    def test_bbox02_03(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('svgstar')
        bbox = element.get_bbox()
        self.assertAlmostEqual(bbox.x, -38.899, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.y, -38.899, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.width, 77.798, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.height, 77.798, msg=element.id, delta=delta)

    def test_bbox02_04(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('svgbar')
        bbox = element.get_bbox()
        self.assertAlmostEqual(bbox.x, -38.899, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.y, -7, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.width, 77.798, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.height, 14, msg=element.id, delta=delta)

    def test_bbox02_08(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('usetop')
        bbox = element.get_bbox()
        self.assertAlmostEqual(bbox.x, 11.101, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.y, 11.101, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.width, 77.798, msg=element.id, delta=delta)
        self.assertAlmostEqual(bbox.height, 77.798, msg=element.id, delta=delta)

    def test_circle00_length(self):
        # circle: initial value
        parser = SVGParser()
        circle = parser.make_element('circle')

        style = circle.get_computed_style()
        self.assertEqual(style['cx'], 0)
        self.assertEqual(style['cy'], 0)
        self.assertEqual(style['r'], 0)

        path_data = circle.get_path_data()
        self.assertEqual(len(path_data), 0)

        n = circle.get_total_length()
        expected = 0
        self.assertAlmostEqual(n, expected)

    def test_circle01_bbox(self):
        parser = SVGParser()
        circle = parser.make_element('circle')
        circle.attributes.update({
            'cx': '200',
            'cy': '300',
            'r': '100',
        })

        bbox = circle.get_bbox()
        self.assertEqual(bbox.x, 200 - 100)
        self.assertEqual(bbox.y, 300 - 100)
        self.assertEqual(bbox.width, 100 * 2)
        self.assertEqual(bbox.height, 100 * 2)

    def test_circle02_length(self):
        # See also: circle01.html
        parser = SVGParser()
        root = parser.make_element('svg')

        cx = 600
        cy = 200
        r = 100
        circle = root.make_sub_element('circle')
        circle.attributes.update({
            'cx': str(cx),
            'cy': str(cy),
            'r': str(r),
        })

        style = circle.get_computed_style()
        self.assertEqual(style['cx'], cx)
        self.assertEqual(style['cy'], cy)
        self.assertEqual(style['r'], r)

        path_data = circle.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M700,200" \
            " A100,100 0 0 1 600,300" \
            " 100,100 0 0 1 500,200" \
            " 100,100 0 0 1 600,100" \
            " 100,100 0 0 1 700,200 Z"
        self.assertEqual(d, expected, msg=d)

        n = circle.get_total_length()
        expected = 2 * math.pi * r
        self.assertAlmostEqual(n, expected)

    def test_circle02_normalize(self):
        # See also: circle01.html
        parser = SVGParser()
        root = parser.make_element('svg')

        circle = root.make_sub_element('circle')
        circle.attributes.update({
            'cx': '600',
            'cy': '200',
            'r': '100',
        })

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = circle.get_path_data(settings)
        exp = PathParser.tostring(path_data)
        expected = \
            "M700,200" \
            " C700,255.228 655.228,300 600,300 544.772,300" \
            " 500,255.228 500,200 500,144.772 544.772,100" \
            " 600,100 655.228,100 700,144.772 700,200 Z"
        self.assertEqual(exp, expected)

    def test_circle03_length(self):
        # circle: viewport-relative length
        # See also: circle01.html
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'width': '12cm',
            'height': '4cm',
            'viewBox': '0 0 1200 400',
        })

        circle = root.make_sub_element('circle')
        circle.attributes.update({
            'cx': '25%',
            'cy': '50%',
            'r': '10%',
        })

        style = circle.get_computed_style()

        # cx = 1200 * 25% = 300
        expected = 300
        self.assertAlmostEqual(style['cx'], expected)

        # cy = 400 * 50% = 200
        expected = 200
        self.assertAlmostEqual(style['cy'], expected)

        # r = sqrt((width) ** 2 + (height) ** 2) / sqrt(2) * 10%
        #  = sqrt(1200 ** 2 + 400 ** 2) / sqrt(2) * 10%
        #  = 89.44271909999159
        expected = 89.44271909999159
        self.assertAlmostEqual(style['r'], expected, places=places)

        n = circle.get_total_length()
        # 2 * pi * r = 561.9851784832581
        expected = 561.9851784832581
        self.assertAlmostEqual(n, expected, places=places)

    def test_computed_style02(self):
        # See also: Units.html
        # Relative units
        # Default font size: 16px
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_UNITS))
        root = tree.getroot()

        rect = root.get_element_by_id('rect_rel_01')
        style = rect.get_computed_style()
        self.assertEqual(style['font-family'], ['Verdana'], msg=style)
        self.assertEqual(style['font-size'], 150, msg=style)
        self.assertEqual(style['font-weight'], Font.WEIGHT_NORMAL, msg=style)
        self.assertEqual(style['x'], 0, msg=style)
        self.assertEqual(style['y'], 400, msg=style)
        self.assertEqual(style['width'], 375, msg=style)
        self.assertEqual(style['height'], 187.5, msg=style)
        self.assertEqual(style['rx'], 0, msg=style)
        self.assertEqual(style['ry'], 0, msg=style)
        self.assertAlmostEqual(style['stroke-width'], 37.5, msg=style,
                               places=places)

        rect = root.get_element_by_id('rect_rel_03')
        style = rect.get_computed_style()
        self.assertEqual(style['font-family'], ['Verdana'], msg=style)
        self.assertEqual(style['font-size'], 150, msg=style)
        self.assertEqual(style['font-weight'], Font.WEIGHT_NORMAL, msg=style)
        self.assertEqual(style['x'], 0, msg=style)
        self.assertEqual(style['y'], 600, msg=style)
        self.assertEqual(style['width'], 375, msg=style)
        self.assertEqual(style['height'], 187.5, msg=style)
        self.assertEqual(style['rx'], 0, msg=style)
        self.assertEqual(style['ry'], 0, msg=style)
        self.assertAlmostEqual(style['stroke-width'], 37.5, msg=style,
                               places=places)

    def test_computed_style03(self):
        # See also: Units.html
        # Percentages units
        # Default font size: 16px
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_UNITS))
        root = tree.getroot()

        rect = root.get_element_by_id('rect_per_01')
        style = rect.get_computed_style()
        self.assertEqual(style['font-family'], ['Verdana'], msg=style)
        self.assertEqual(style['font-size'], 150, msg=style)
        self.assertEqual(style['font-weight'], Font.WEIGHT_NORMAL, msg=style)
        self.assertEqual(style['x'], 0, msg=style)
        self.assertEqual(style['y'], 400, msg=style)
        self.assertEqual(style['width'], 400, msg=style)
        self.assertEqual(style['height'], 200, msg=style)
        self.assertEqual(style['rx'], 0, msg=style)
        self.assertEqual(style['ry'], 0, msg=style)
        self.assertAlmostEqual(style['stroke-width'], 31.62, msg=style,
                               places=places)

        rect = root.get_element_by_id('rect_per_03')
        style = rect.get_computed_style()
        # print(sorted(style.items()))
        self.assertEqual(style['font-family'], ['Verdana'], msg=style)
        self.assertEqual(style['font-size'], 150, msg=style)
        self.assertEqual(style['font-weight'], Font.WEIGHT_NORMAL, msg=style)
        self.assertEqual(style['x'], 0, msg=style)
        self.assertEqual(style['y'], 600, msg=style)
        self.assertEqual(style['width'], 400, msg=style)
        self.assertEqual(style['height'], 200, msg=style)
        self.assertEqual(style['rx'], 0, msg=style)
        self.assertEqual(style['ry'], 0, msg=style)
        self.assertAlmostEqual(style['stroke-width'], 31.62, msg=style,
                               places=places)

    def test_element_attributes(self):
        parser = SVGParser()
        root = parser.make_element('svg')

        root.attributes.set('width', '20cm')
        root.attributes.set('height', '10cm')
        self.assertEqual(len(root.attributes), 2)
        self.assertEqual(len(root.attrib), 2)
        self.assertTrue('width' in root.attributes)
        self.assertTrue('height' in root.attributes)
        self.assertTrue('x' not in root.attributes)
        self.assertTrue(root.attributes.has('width'))
        self.assertTrue(root.attributes.has('height'))
        self.assertTrue(not root.attributes.has('x'))

        width = root.attributes.pop('width')
        self.assertEqual(len(root.attributes), 1)
        self.assertEqual(len(root.attrib), 1)
        self.assertEqual(width, '20cm')
        self.assertTrue('width' not in root.attributes)
        self.assertTrue('height' in root.attributes)
        self.assertTrue(not root.attributes.has('width'))
        self.assertTrue(root.attributes.has('height'))

        del root.attributes['height']
        self.assertEqual(len(root.attributes), 0)
        self.assertEqual(len(root.attrib), 0)
        self.assertTrue('width' not in root.attributes)
        self.assertTrue('height' not in root.attributes)
        self.assertTrue(not root.attributes.has('width'))
        self.assertTrue(not root.attributes.has('height'))

        root.attributes.set('width', '20cm')
        root.attributes.set('height', '10cm')
        root.attributes.update({
            'width': '15cm',
        })
        width = root.attributes.get('width')
        height = root.attributes.get('height')
        x = root.attributes.get('x')
        self.assertEqual(len(root.attributes), 2)
        self.assertEqual(len(root.attrib), 2)
        self.assertEqual(width, '15cm')
        self.assertEqual(height, '10cm')
        self.assertTrue(x is None)
        self.assertTrue(root.attributes.has('width'))
        self.assertTrue(root.attributes.has('height'))
        self.assertTrue(not root.attributes.has('x'))

        x = root.attributes.get('x', '100')
        self.assertEqual(x, '100')

        self.assertTrue('viewBox' not in root.attributes)

        view_box = root.attributes.setdefault('viewBox', '0 0 200 100')
        self.assertEqual(view_box, '0 0 200 100')

        self.assertTrue('viewBox' in root.attributes)
        self.assertTrue(root.attributes.has('viewBox'))

    def test_element_attributes_ns(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        text = root.make_sub_element('text')

        attributes = text.attributes

        self.assertTrue(not attributes.has_ns(Element.XML_NAMESPACE_URI,
                                              'lang'))
        attributes.set_ns(Element.XML_NAMESPACE_URI, 'lang', 'ja')
        self.assertTrue(attributes.has_ns(Element.XML_NAMESPACE_URI, 'lang'))

        expected = "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
                   "<text xml:lang=\"ja\"/></svg>"
        self.assertEqual(root.tostring().decode(), expected)

        lang = attributes.get('lang')
        self.assertIsNone(lang)
        self.assertTrue(not attributes.has_ns(None, 'lang'))

        lang = attributes.get_ns(Element.XML_NAMESPACE_URI, 'lang')
        expected = 'ja'
        self.assertEqual(lang, expected)

        space = attributes.get_ns(Element.XML_NAMESPACE_URI,
                                  'space')  # deprecated
        self.assertIsNone(space)
        self.assertTrue(not attributes.has_ns(Element.XML_NAMESPACE_URI,
                                              'space'))

        space = attributes.get_ns(Element.XML_NAMESPACE_URI,
                                  'space', 'preserve')
        expected = 'preserve'
        self.assertEqual(space, expected)

        lang = attributes.pop_ns(Element.XML_NAMESPACE_URI, 'lang', 'en')
        expected = 'ja'
        self.assertEqual(lang, expected)
        self.assertTrue(not attributes.has_ns(Element.XML_NAMESPACE_URI,
                                              'lang'))

        expected = "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
                   "<text/></svg>"
        self.assertEqual(root.tostring().decode(), expected)

        lang = attributes.setdefault_ns(Element.XML_NAMESPACE_URI, 'lang', 'en')
        expected = 'en'
        self.assertEqual(lang, expected)
        self.assertTrue(attributes.has_ns(Element.XML_NAMESPACE_URI, 'lang'))

        expected = "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
                   "<text xml:lang=\"en\"/></svg>"
        self.assertEqual(root.tostring().decode(), expected)

    def test_element_style_attribute(self):
        parser = SVGParser()
        root = parser.make_element('svg')

        circle = root.make_sub_element('circle')
        circle.attributes.update({
            'r': '120',
            'cx': '100',
            'cy': '200',
        })
        circle.attributes.set_style({
            'stroke': 'red',
            'stroke-width': '5',
            'stroke-dasharray': '10 5',
        })
        self.assertEqual(len(circle.keys()), 4)
        self.assertEqual(len(circle.attributes), 4)
        self.assertEqual(len(circle.attrib), 4)
        self.assertEqual(circle.attributes.get('r'), '120')
        self.assertEqual(circle.attributes.get('cx'), '100')
        self.assertEqual(circle.attributes.get('cy'), '200')
        self.assertEqual(circle.attributes.get('stroke'), 'red')
        self.assertEqual(circle.attributes.get('stroke-width'), '5')
        self.assertEqual(circle.attributes.get('stroke-dasharray'), '10 5')

        style = circle.attributes.get('style')
        expected = 'stroke-dasharray: 10 5; stroke-width: 5; stroke: red;'
        self.assertEqual(style, expected)
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(circle.attributes.has('style'))
        self.assertTrue(circle.attributes.has('stroke'))
        self.assertTrue(circle.attributes.has('stroke-width'))
        self.assertTrue(circle.attributes.has('stroke-dasharray'))

        d = circle.attributes.get_style()
        self.assertEqual(len(d), 3)
        self.assertEqual(d['stroke'], 'red')
        self.assertEqual(d['stroke-width'], '5')
        self.assertEqual(d['stroke-dasharray'], '10 5')

        sw = circle.attributes.pop('stroke-width')
        self.assertEqual(len(circle.keys()), 4)
        self.assertEqual(sw, '5')
        self.assertEqual(circle.attributes.get('r'), '120')
        self.assertEqual(circle.attributes.get('cx'), '100')
        self.assertEqual(circle.attributes.get('cy'), '200')
        self.assertEqual(circle.attributes.get('stroke'), 'red')
        self.assertEqual(circle.attributes.get('stroke-dasharray'), '10 5')
        self.assertTrue(circle.attributes.get('stroke-width') is None)
        self.assertTrue('stroke-width' not in circle.attributes)
        self.assertTrue('stroke-width' not in circle.attrib)
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(circle.attributes.has('style'))
        self.assertTrue(circle.attributes.has('stroke'))
        self.assertTrue(not circle.attributes.has('stroke-width'))
        self.assertTrue(circle.attributes.has('stroke-dasharray'))

        style = circle.attributes.get('style')
        expected = 'stroke-dasharray: 10 5; stroke: red;'
        self.assertEqual(style, expected)

        d = circle.attributes.get_style()
        self.assertEqual(len(d), 2)
        self.assertEqual(d['stroke'], 'red')
        self.assertEqual(d['stroke-dasharray'], '10 5')

        circle.attributes.update({
            'cx': '500',
            'cy': '800',
            'stroke': 'green',
        })
        self.assertEqual(len(circle.keys()), 4)
        self.assertEqual(circle.attributes.get('r'), '120')
        self.assertEqual(circle.attributes.get('cx'), '500')
        self.assertEqual(circle.attributes.get('cy'), '800')
        self.assertEqual(circle.attributes.get('stroke'), 'green')
        self.assertTrue('stroke' in circle.attributes)
        self.assertTrue('stroke' not in circle.attrib)
        self.assertTrue('stroke' not in circle.keys())
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(circle.attributes.has('style'))
        self.assertTrue(circle.attributes.has('stroke'))
        self.assertTrue(not circle.attributes.has('stroke-width'))
        self.assertTrue(circle.attributes.has('stroke-dasharray'))

        style = circle.attributes.get('style')
        expected = 'stroke-dasharray: 10 5; stroke: green;'
        self.assertEqual(style, expected)

        d = circle.attributes.get_style()
        self.assertEqual(len(d), 2)
        self.assertEqual(d['stroke'], 'green')
        self.assertEqual(d['stroke-dasharray'], '10 5')

        self.assertTrue('fill' not in circle.attributes)
        self.assertTrue('fill' not in circle.attrib)
        d = circle.attributes.get_style()
        d.update({
            'fill': 'none',
        })
        circle.attributes.set_style(d)
        self.assertTrue('fill' in circle.attributes)
        self.assertTrue('fill' not in circle.attrib)
        self.assertEqual(len(circle.keys()), 4)
        self.assertEqual(circle.attributes.get('r'), '120')
        self.assertEqual(circle.attributes.get('cx'), '500')
        self.assertEqual(circle.attributes.get('cy'), '800')
        self.assertEqual(circle.attributes.get('fill'), 'none')
        self.assertEqual(circle.attributes.get('stroke'), 'green')
        self.assertEqual(circle.attributes.get('stroke-dasharray'), '10 5')
        self.assertTrue(circle.attributes.get('stroke-width') is None)
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(circle.attributes.has('style'))
        self.assertTrue(circle.attributes.has('stroke'))
        self.assertTrue(not circle.attributes.has('stroke-width'))
        self.assertTrue(circle.attributes.has('stroke-dasharray'))
        self.assertTrue(circle.attributes.has('fill'))

        style = circle.attributes.get('style')
        expected = 'fill: none; stroke-dasharray: 10 5; stroke: green;'
        self.assertEqual(style, expected)

        circle.attributes.pop('stroke')
        self.assertEqual(len(circle.keys()), 4)

        circle.attributes.pop('stroke')  # remove twice
        self.assertEqual(len(circle.keys()), 4)

        circle.attributes.pop('stroke-width')
        self.assertEqual(len(circle.keys()), 4)

        circle.attributes.pop('stroke-dasharray')
        self.assertEqual(len(circle.keys()), 4)

        style = circle.attributes.get('style')
        expected = 'fill: none;'
        self.assertEqual(style, expected)

        fill = circle.attributes.pop('fill', 'red')
        self.assertEqual(fill, 'none')

        fill = circle.attributes.pop('fill', 'red')  # remove twice
        self.assertEqual(fill, 'red')

        style = circle.attributes.get('style')
        self.assertEqual(len(circle.keys()), 3)
        self.assertEqual(circle.attributes.get('r'), '120')
        self.assertEqual(circle.attributes.get('cx'), '500')
        self.assertEqual(circle.attributes.get('cy'), '800')
        self.assertTrue(style is None)
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(not circle.attributes.has('style'))
        self.assertTrue(not circle.attributes.has('stroke'))
        self.assertTrue(not circle.attributes.has('stroke-width'))
        self.assertTrue(not circle.attributes.has('stroke-dasharray'))
        self.assertTrue(not circle.attributes.has('fill'))

        circle.attributes.update_style({'fill': 'none', 'stroke': 'red'})
        circle.attributes.update_style({'stroke-width': '2'})
        style = circle.attributes.get('style')
        expected = 'fill: none; stroke-width: 2; stroke: red;'
        self.assertEqual(style, expected)
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(circle.attributes.has('style'))
        self.assertTrue(circle.attributes.has('stroke'))
        self.assertTrue(circle.attributes.has('stroke-width'))
        self.assertTrue(not circle.attributes.has('stroke-dasharray'))
        self.assertTrue(circle.attributes.has('fill'))

    def test_element_style_attribute_ns(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        circle = root.make_sub_element('circle')

        value = circle.attributes.get_ns(None, 'fill')
        self.assertIsNone(value)
        self.assertTrue(not circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))

        circle.attributes.set('style', 'fill:red;stroke:blue')
        value = circle.attributes.get_ns(None, 'fill')
        expected = 'red'
        self.assertEqual(value, expected)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        circle.attributes.set_ns(None, 'fill', 'white')
        value = circle.attributes.pop_ns(None, 'fill')
        expected = 'white'
        self.assertEqual(value, expected)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        value = circle.attributes.pop_ns(None, 'fill', 'black')
        expected = 'black'
        self.assertEqual(value, expected)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        value = circle.attributes.setdefault_ns(None, 'stroke', 'black')
        expected = 'blue'
        self.assertEqual(value, expected)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        circle.attributes.update({'stroke': 'white'})
        value = circle.attributes.get_ns(None, 'style')
        expected = 'stroke: white;'
        self.assertEqual(value, expected)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

    def test_element_class_list01(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        class_name = root.class_name
        self.assertIsNone(class_name)

        class_list = root.class_list
        self.assertEqual(class_list, [])

    def test_element_class_list02(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        root.class_name = 'Border'
        class_name = root.class_name
        self.assertEqual(class_name, 'Border')

        class_list = root.class_list
        self.assertEqual(class_list, ['Border'])

    def test_element_class_list03(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        root.class_name = 'Border Label'
        class_name = root.class_name
        self.assertEqual(class_name, 'Border Label')

        class_list = root.class_list
        self.assertEqual(class_list, ['Border', 'Label'])

    def test_element_find_by_class_names01(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        # not match
        elements = root.get_elements_by_class_name('NotExistClass')
        self.assertEqual(len(elements), 0)

        # match
        elements = root.get_elements_by_class_name('Connect')
        self.assertEqual(len(elements), 4)
        self.assertTrue(isinstance(elements[0], SVGPolylineElement))
        self.assertTrue(isinstance(elements[1], SVGPolylineElement))
        self.assertTrue(isinstance(elements[2], SVGPolylineElement))
        self.assertTrue(isinstance(elements[3], SVGPolylineElement))

        # match
        elements = root.get_elements_by_class_name('SamplePath')
        self.assertEqual(len(elements), 1)
        self.assertTrue(isinstance(elements[0], SVGPathElement))

        # not match
        elements = root.get_elements_by_class_name('Connect SamplePath')
        self.assertEqual(len(elements), 0)

    def test_element_find_by_class_names02(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        circle = root.make_sub_element('circle')
        circle.attributes.update({
            'class': 'red',
        })
        ellipse = root.make_sub_element('ellipse')
        ellipse.attributes.update({
            'class': 'red test',  # match
        })
        line = root.make_sub_element('line')
        line.attributes.update({
            'class': 'test',
        })
        polygon = root.make_sub_element('polygon')
        polygon.attributes.update({
            'class': 'test red',  # match
        })
        polyline = root.make_sub_element('polyline')
        polyline.attributes.update({
            'class': 'test dark-red',
        })
        rect = root.make_sub_element('rect')
        rect.attributes.update({
            'class': 'test dark red',  # match
        })

        elements = root.get_elements_by_class_name('red test')
        self.assertEqual(len(elements), 3)
        node_names = [x.node_name for x in elements]
        self.assertTrue('ellipse' in node_names)
        self.assertTrue('polygon' in node_names)
        self.assertTrue('rect' in node_names)

    def test_element_find_by_local_name(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        # tag 'path' -> not found
        elements = root.findall('path')
        self.assertEqual(len(elements), 0)

        # tag '{http://www.w3.org/2000/svg}path' -> found
        name = '{{{}}}{}'.format(Element.SVG_NAMESPACE_URI, 'path')
        elements = root.findall(name)
        self.assertEqual(len(elements), 3)

        # local-name 'path' -> found
        elements = root.get_elements_by_local_name('path')
        self.assertEqual(len(elements), 3)

        elements = root.get_elements_by_local_name(
            'path',
            namespaces={'svg': Element.SVG_NAMESPACE_URI})
        self.assertEqual(len(elements), 3)

    def test_element_find_by_id(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        # not found
        element = root.get_element_by_id('dummy')
        self.assertTrue(element is None)

        # found
        element = root.get_element_by_id('path01')
        self.assertTrue(element is not None)
        self.assertEqual(element.local_name, 'path')

    def test_element_isdisplay(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element(
            'group',
            attrib={'display': 'none'}
        )
        text = group.make_sub_element(
            'text',
            attrib={'display': 'inline'}
        )

        display = root.isdisplay()  # inline
        self.assertEqual(display, True)

        display = group.isdisplay()  # inline > none
        self.assertEqual(display, False)

        display = text.isdisplay()  # inline > none > none
        self.assertEqual(display, False)

    def test_element_iter(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ROTATE_SCALE))
        root = tree.getroot()

        for element in root:
            if element.node_type == Node.COMMENT_NODE:
                self.assertIsInstance(element, Comment)
                self.assertEqual(element.node_name, '#comment')
                self.assertIsNotNone(element.data)
            else:
                self.assertEqual(element.node_type, Node.ELEMENT_NODE)

    def test_element_make_sub_element(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        _ = root.make_sub_element('rect')
        _ = root.make_sub_element('ellipse')
        _ = root.make_sub_element('circle', index=1)
        # rect > circle > ellipse
        expected = \
            "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
            "<rect/><circle/><ellipse/>" \
            "</svg>"
        self.assertEqual(root.tostring().decode(), expected)

    def test_element_make_sub_element_html(self):
        parser = SVGParser()
        nsmap = {
            None: Element.SVG_NAMESPACE_URI,
            'html': Element.XHTML_NAMESPACE_URI
        }
        root = parser.make_element('svg', nsmap=nsmap)
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual(root.tag_name, 'svg')
        self.assertEqual(root.local_name, 'svg')
        self.assertEqual(root.namespace_uri, 'http://www.w3.org/2000/svg')

        video = root.make_sub_element('video')
        self.assertTrue(isinstance(video, HTMLVideoElement))
        self.assertEqual(video.tag_name, 'video')
        self.assertEqual(video.local_name, 'video')
        self.assertEqual(video.namespace_uri, 'http://www.w3.org/2000/svg')

        tag = '{{{}}}{}'.format(Element.XHTML_NAMESPACE_URI, 'audio')
        audio = root.make_sub_element(tag)
        self.assertTrue(isinstance(audio, HTMLAudioElement))
        self.assertEqual(audio.tag, tag)
        self.assertEqual(audio.tag_name, 'html:audio')
        self.assertEqual(audio.local_name, 'audio')
        self.assertEqual(audio.namespace_uri, 'http://www.w3.org/1999/xhtml')

        tag = '{{{}}}{}'.format(Element.XHTML_NAMESPACE_URI, 'source')
        source = audio.make_sub_element_ns(Element.XHTML_NAMESPACE_URI,
                                           'source')
        self.assertTrue(isinstance(source, HTMLElement))
        self.assertEqual(source.tag, tag)
        self.assertEqual(source.tag_name, 'html:source')
        self.assertEqual(source.local_name, 'source')
        self.assertEqual(source.namespace_uri, 'http://www.w3.org/1999/xhtml')

    def test_element_make_sub_element_svg01(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual(root.tag, 'svg')
        self.assertEqual(root.tag_name, 'svg')
        self.assertEqual(root.local_name, 'svg')
        self.assertEqual(root.namespace_uri, 'http://www.w3.org/2000/svg')

        g = root.make_sub_element('g')
        self.assertTrue(isinstance(g, SVGGElement))

        path = g.make_sub_element('path')
        self.assertTrue(isinstance(path, SVGPathElement))

        rect = g.make_sub_element('rect', index=0)
        self.assertTrue(isinstance(rect, SVGRectElement))

        # svg > g > (rect, path)
        expected = \
            "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
            "<g><rect/><path/></g>" \
            "</svg>"
        self.assertEqual(root.tostring(), expected.encode())

    def test_element_make_sub_element_svg02(self):
        parser = SVGParser()
        root = parser.make_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual(root.tag, '{http://www.w3.org/2000/svg}svg')
        self.assertEqual(root.tag_name, 'svg')
        self.assertEqual(root.local_name, 'svg')
        self.assertEqual(root.namespace_uri, 'http://www.w3.org/2000/svg')

        g = root.make_sub_element('g')
        self.assertTrue(isinstance(g, SVGGElement))
        self.assertEqual(g.tag, 'g')
        self.assertEqual(g.tag_name, 'g')
        self.assertEqual(g.local_name, 'g')
        self.assertEqual(g.namespace_uri, 'http://www.w3.org/2000/svg')

        path = g.make_sub_element_ns('http://www.w3.org/2000/svg', 'path')
        self.assertTrue(isinstance(path, SVGPathElement))
        self.assertEqual(path.tag, '{http://www.w3.org/2000/svg}path')
        self.assertEqual(path.tag_name, 'path')
        self.assertEqual(path.local_name, 'path')
        self.assertEqual(path.namespace_uri, 'http://www.w3.org/2000/svg')

        rect = g.make_sub_element_ns(None, 'rect', index=0)
        self.assertTrue(isinstance(rect, SVGRectElement))
        self.assertEqual(rect.tag, 'rect')
        self.assertEqual(rect.tag_name, 'rect')
        self.assertEqual(rect.local_name, 'rect')
        self.assertEqual(rect.namespace_uri, 'http://www.w3.org/2000/svg')

    def test_ellipse01_length(self):
        # ellipse: initial value
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        path_data = ellipse.get_path_data()
        self.assertEqual(len(path_data), 0)

        n = ellipse.get_total_length()
        self.assertEqual(n, 0)

    def test_ellipse02_length(self):
        # ellipse: rx = 0
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '0',
            'cy': '0',
            'rx': '0',
            'ry': '100',
        })

        path_data = ellipse.get_path_data()
        self.assertEqual(len(path_data), 0)

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = ellipse.get_path_data(settings)
        self.assertEqual(len(path_data), 0)

        n = ellipse.get_total_length()
        self.assertEqual(n, 0)

    def test_ellipse03_length(self):
        # ellipse: ry = 0
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '0',
            'cy': '0',
            'rx': '100',
            'ry': '0',
        })

        path_data = ellipse.get_path_data()
        self.assertEqual(len(path_data), 0)

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = ellipse.get_path_data(settings)
        self.assertEqual(len(path_data), 0)

        n = ellipse.get_total_length()
        self.assertEqual(n, 0)

    def test_ellipse04_length(self):
        # ellipse: rx = ry
        # See also: circle01.html
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '600',
            'cy': '200',
            'rx': '100',
            'ry': '100',
        })

        path_data = ellipse.get_path_data()
        d = PathParser.tostring(path_data)
        expected = "M700,200" \
                   " A100,100 0 0 1 600,300" \
                   " 100,100 0 0 1 500,200" \
                   " 100,100 0 0 1 600,100" \
                   " 100,100 0 0 1 700,200 Z"
        self.assertEqual(len(path_data), 6)
        self.assertEqual(d, expected, msg=d)

        n = ellipse.get_total_length()
        expected = 2 * math.pi * 100
        self.assertAlmostEqual(n, expected)

    def test_ellipse04_normalize(self):
        # ellipse: rx = ry
        # See also: circle01.html
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '600',
            'cy': '200',
            'rx': '100',
            'ry': '100',
        })

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = ellipse.get_path_data(settings)
        d = PathParser.tostring(path_data)
        expected = "M700,200" \
                   " C700,255.228 655.228,300 600,300" \
                   " 544.772,300 500,255.228 500,200" \
                   " 500,144.772 544.772,100 600,100" \
                   " 655.228,100 700,144.772 700,200 Z"
        self.assertEqual(d, expected, msg=d)

    def test_ellipse05_length(self):
        # ellipse: rx > ry
        # See also: ellipse01.html
        # id="ellipse1"
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '0',
            'cy': '0',
            'rx': '250',
            'ry': '100',
        })

        # id="path1"
        path_data = ellipse.get_path_data()
        d = PathParser.tostring(path_data)
        expected = "M250,0" \
                   " A250,100 0 0 1 0,100" \
                   " 250,100 0 0 1 -250,0" \
                   " 250,100 0 0 1 0,-100" \
                   " 250,100 0 0 1 250,0 Z"
        self.assertEqual(len(path_data), 6)
        self.assertEqual(d, expected, msg=d)

    def test_ellipse05_normalize(self):
        # ellipse: rx > ry
        # See also: ellipse01.html
        # id="ellipse1"
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '0',
            'cy': '0',
            'rx': '250',
            'ry': '100',
        })

        # id="path1n"
        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = ellipse.get_path_data(settings)
        d = PathParser.tostring(path_data)
        expected = "M250,0" \
                   " C250,55.228 138.071,100 0,100" \
                   " -138.071,100 -250,55.228 -250,0" \
                   " -250,-55.228 -138.071,-100 0,-100" \
                   " 138.071,-100 250,-55.228 250,0 Z"
        self.assertEqual(d, expected, msg=d)

        n = ellipse.get_total_length()
        # expected = 1150.816162109375  # firefox
        expected = 1150.81787109375
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse06_length(self):
        # ellipse: ry > rx
        # See also: ellipse01.html
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        ellipse.attributes.update({
            'cx': '0',
            'cy': '0',
            'rx': '100',
            'ry': '250',
        })

        # id="path2"
        path_data = ellipse.get_path_data()
        d = PathParser.tostring(path_data)
        expected = "M100,0" \
                   " A100,250 0 0 1 0,250" \
                   " 100,250 0 0 1 -100,0" \
                   " 100,250 0 0 1 0,-250" \
                   " 100,250 0 0 1 100,0 Z"
        self.assertEqual(len(path_data), 6)
        self.assertEqual(d, expected, msg=d)

        n = ellipse.get_total_length()
        # expected = 1150.8154296875  # firefox
        expected = 1150.818115234375
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse07_length(self):
        # ellipse: viewport-percentage length
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'width': '1250',
            'height': '400',
        })

        ellipse = root.make_sub_element('ellipse')
        ellipse.attributes.update({
            'cx': '0',
            'cy': '0',
            'rx': '20%',  # 1250 * 0.2 = 250
            'ry': '25%',  # 400 * 0.25 = 100
        })

        style = ellipse.get_computed_style()
        self.assertEqual(style['cx'], 0)
        self.assertEqual(style['cy'], 0)
        self.assertEqual(style['rx'], 250)
        self.assertEqual(style['ry'], 100)

        path_data = ellipse.get_path_data()
        d = PathParser.tostring(path_data)
        expected = "M250,0" \
                   " A250,100 0 0 1 0,100" \
                   " 250,100 0 0 1 -250,0" \
                   " 250,100 0 0 1 0,-100" \
                   " 250,100 0 0 1 250,0 Z"
        self.assertEqual(d, expected, msg=d)

        n = ellipse.get_total_length()
        # expected = 1150.816162109375  # firefox
        expected = 1150.81787109375
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse08_bbox(self):
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')
        ellipse.attributes.update({
            'cx': '200',
            'cy': '300',
            'rx': '100',
            'ry': '200',
        })

        bbox = ellipse.get_bbox()
        self.assertEqual(bbox.x, 200 - 100)
        self.assertEqual(bbox.y, 300 - 200)
        self.assertEqual(bbox.width, 100 * 2)
        self.assertEqual(bbox.height, 200 * 2)

    def test_group_ctm(self):
        # See also: RotateScale.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ROTATE_SCALE))
        root = tree.getroot()

        # no viewBox
        # transform="translate(50,30)"
        g = root.get_element_by_id('g11')
        matrix = g.get_ctm()
        exp = matrix.tostring()
        expected = 'matrix(1 0 0 1 50 30)'
        self.assertEqual(exp, expected)

        # no viewBox
        # transform="translate(50,30)"
        # transform="rotate(30)"
        g = root.get_element_by_id('g12')
        matrix = g.get_ctm()
        exp = matrix.tostring()
        expected = 'matrix(0.866 0.5 -0.5 0.866 50 30)'
        self.assertEqual(exp, expected)

    def test_line01_length(self):
        parser = SVGParser()
        line = parser.make_element('line')

        path_data = line.get_path_data()
        self.assertEqual(len(path_data), 0)

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = line.get_path_data(settings)
        self.assertEqual(len(path_data), 0)

        n = line.get_total_length()
        self.assertEqual(n, 0)

    def test_line02_length(self):
        # horizontal line
        parser = SVGParser()
        line = parser.make_element('line')
        line.attributes.update({
            'x1': '0',
            'y1': '0',
            'x2': '100',
            'y2': '0',
        })

        path_data = line.get_path_data()
        self.assertEqual(len(path_data), 2)

        d = PathParser.tostring(path_data)
        expected = 'M0,0 L100,0'
        self.assertEqual(d, expected)

        n = line.get_total_length()
        expected = 100
        self.assertEqual(n, expected)

    def test_line03_length(self):
        # vertical line
        parser = SVGParser()
        line = parser.make_element('line')
        line.attributes.update({
            'x1': '0',
            'y1': '100',
            'x2': '0',
            'y2': '-100',
        })

        path_data = line.get_path_data()
        self.assertEqual(len(path_data), 2)

        d = PathParser.tostring(path_data)
        expected = 'M0,100 L0,-100'
        self.assertEqual(d, expected)

        n = line.get_total_length()
        expected = 200
        self.assertEqual(n, expected)

    def test_line04_length(self):
        parser = SVGParser()
        line = parser.make_element('line')
        line.attributes.update({
            'x1': '-100',
            'y1': '-100',
            'x2': '100',
            'y2': '100',
        })

        path_data = line.get_path_data()
        self.assertEqual(len(path_data), 2)

        d = PathParser.tostring(path_data)
        expected = 'M-100,-100 L100,100'
        self.assertEqual(d, expected)

        n = line.get_total_length()
        expected = math.sqrt((100 - -100) ** 2 + (100 - -100) ** 2)
        self.assertEqual(n, expected)

    def test_line05_length(self):
        parser = SVGParser()
        line = parser.make_element('line')
        line.attributes.update({
            'x1': '100',
            'y1': '200',
            'x2': '-100',
            'y2': '-200',
        })

        path_data = line.get_path_data()
        self.assertEqual(len(path_data), 2)

        d = PathParser.tostring(path_data)
        expected = 'M100,200 L-100,-200'
        self.assertEqual(d, expected)

        n = line.get_total_length()
        expected = math.sqrt((-100 - 100) ** 2 + (-200 - 200) ** 2)
        self.assertEqual(n, expected)

    def test_line06_bbox(self):
        parser = SVGParser()
        line = parser.make_element('line')
        line.attributes.update({
            'x1': '100',
            'y1': '200',
            'x2': '300',
            'y2': '400',
        })

        bbox = line.get_bbox()
        self.assertEqual(bbox.x, 100)
        self.assertEqual(bbox.y, 200)
        self.assertEqual(bbox.width, 300 - 100)
        self.assertEqual(bbox.height, 400 - 200)

    def test_parser_from_string(self):
        parser = SVGParser()
        root = parser.fromstring(SVG_CUBIC01)
        # <svg>
        #  <title>
        #  <desc>
        #  <style>
        #  <rect>
        #  <polyline> * 4
        #  <path> * 3
        #  <circle> * 7
        #  <text> * 2
        self.assertEqual(len(root), 20)
        self.assertEqual(root.local_name, 'svg')
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual(root[0].local_name, 'title')
        self.assertEqual(root[1].local_name, 'desc')
        self.assertEqual(root[2].local_name, 'style')
        self.assertEqual(root[3].local_name, 'rect')
        self.assertTrue(isinstance(root[3], SVGRectElement))
        self.assertEqual(root[4].local_name, 'polyline')
        self.assertTrue(isinstance(root[4], SVGPolylineElement))
        self.assertEqual(root[5].local_name, 'polyline')
        self.assertTrue(isinstance(root[5], SVGPolylineElement))
        self.assertEqual(root[6].local_name, 'polyline')
        self.assertTrue(isinstance(root[6], SVGPolylineElement))
        self.assertEqual(root[7].local_name, 'polyline')
        self.assertTrue(isinstance(root[7], SVGPolylineElement))
        self.assertEqual(root[8].local_name, 'path')
        self.assertTrue(isinstance(root[8], SVGPathElement))
        # ...
        self.assertTrue(isinstance(root[9], SVGPathElement))
        self.assertTrue(isinstance(root[10], SVGPathElement))
        self.assertTrue(isinstance(root[11], SVGCircleElement))
        self.assertTrue(isinstance(root[12], SVGCircleElement))
        self.assertTrue(isinstance(root[13], SVGCircleElement))
        self.assertTrue(isinstance(root[14], SVGCircleElement))
        self.assertTrue(isinstance(root[15], SVGCircleElement))
        self.assertTrue(isinstance(root[16], SVGCircleElement))
        self.assertTrue(isinstance(root[17], SVGCircleElement))
        self.assertTrue(isinstance(root[18], SVGTextElement))
        self.assertTrue(isinstance(root[19], SVGTextElement))

    def test_parser_parse(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()
        # <svg>
        #  <title>
        #  <desc>
        #  <style>
        #  <rect>
        #  <polyline> * 4
        #  <path> * 3
        #  <circle> * 7
        #  <text> * 2
        self.assertEqual(len(root), 20)
        self.assertEqual(root.local_name, 'svg')
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual(root[0].local_name, 'title')
        self.assertEqual(root[1].local_name, 'desc')
        self.assertEqual(root[2].local_name, 'style')
        self.assertEqual(root[3].local_name, 'rect')
        self.assertTrue(isinstance(root[3], SVGRectElement))
        self.assertEqual(root[4].local_name, 'polyline')
        self.assertTrue(isinstance(root[4], SVGPolylineElement))
        self.assertEqual(root[5].local_name, 'polyline')
        self.assertTrue(isinstance(root[5], SVGPolylineElement))
        self.assertEqual(root[6].local_name, 'polyline')
        self.assertTrue(isinstance(root[6], SVGPolylineElement))
        self.assertEqual(root[7].local_name, 'polyline')
        self.assertTrue(isinstance(root[7], SVGPolylineElement))
        self.assertEqual(root[8].local_name, 'path')
        self.assertTrue(isinstance(root[8], SVGPathElement))
        # ...
        self.assertTrue(isinstance(root[9], SVGPathElement))
        self.assertTrue(isinstance(root[10], SVGPathElement))
        self.assertTrue(isinstance(root[11], SVGCircleElement))
        self.assertTrue(isinstance(root[12], SVGCircleElement))
        self.assertTrue(isinstance(root[13], SVGCircleElement))
        self.assertTrue(isinstance(root[14], SVGCircleElement))
        self.assertTrue(isinstance(root[15], SVGCircleElement))
        self.assertTrue(isinstance(root[16], SVGCircleElement))
        self.assertTrue(isinstance(root[17], SVGCircleElement))
        self.assertTrue(isinstance(root[18], SVGTextElement))
        self.assertTrue(isinstance(root[19], SVGTextElement))

    @unittest.expectedFailure
    def test_path01_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path01')
        # [0.378 0 0 0.378 151.181 0]
        ctm = path.get_ctm()
        exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 151.17708333333331,
        #  0.0009765624999955354]
        expected = 'matrix(0.378 0 0 0.378 151.177 0)'
        self.assertEqual(exp, expected, msg=ctm)

    @unittest.expectedFailure
    def test_path02_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path02')
        # [0.378 0 0 0.378 302.362 0]
        ctm = path.get_ctm()
        exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 302.35416666666663,
        #  0.0009765624999955354]
        expected = 'matrix(0.378 0 0 0.378 302.354 0)'
        self.assertEqual(exp, expected, msg=ctm)

    @unittest.expectedFailure
    def test_path03_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path03')
        # [0.378 0 0 0.378 151.181 94.488]
        ctm = path.get_ctm()
        exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 151.17708333333331,
        #  94.48665364583333]
        expected = 'matrix(0.378 0 0 0.378 151.177 94.487)'
        self.assertEqual(exp, expected, msg=ctm)

    @unittest.expectedFailure
    def test_path04_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path04')
        # [0.378 0 0 0.378 302.362 94.488]
        ctm = path.get_ctm()
        exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 302.35416666666663,
        #  94.48665364583333]
        expected = 'matrix(0.378 0 0 0.378 302.354 94.487)'
        self.assertEqual(exp, expected, msg=ctm)

    def test_path01_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path01')
        n = path.get_total_length()
        expected = 121.12298583984375
        self.assertAlmostEqual(n, expected, delta=delta)

    def test_path02_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path02')
        n = path.get_total_length()
        expected = 121.12297821044922
        self.assertAlmostEqual(n, expected, delta=delta)

    def test_path03_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path03')
        n = path.get_total_length()
        expected = 363.36895751953125
        self.assertAlmostEqual(n, expected, delta=delta)

    def test_path04_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path04')
        n = path.get_total_length()
        expected = 363.3689880371094
        self.assertAlmostEqual(n, expected, delta=delta)

    def test_polygon01_bbox(self):
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        polygon.attributes.update({
            'points': "350,75 379,161 469,161 397,215 423,301 350,250" 
                      " 277,301 303,215 231,161 321,161",
        })

        bbox = polygon.get_bbox()
        self.assertEqual(bbox.x, 231)
        self.assertEqual(bbox.y, 75)
        self.assertEqual(bbox.width, 469 - 231)
        self.assertEqual(bbox.height, 301 - 75)

    def test_polygon02_length(self):
        # See also: polygon01.html
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        points = \
            "350,75 379,161 469,161 397,215 423,301 350,250" \
            " 277,301 303,215 231,161 321,161"
        polygon.attributes.set('points', points)
        pts = polygon.points
        self.assertEqual(len(pts), 10)
        self.assertEqual(pts[0], (350, 75))
        self.assertEqual(pts[1], (379, 161))
        self.assertEqual(pts[2], (469, 161))
        self.assertEqual(pts[3], (397, 215))
        self.assertEqual(pts[4], (423, 301))
        self.assertEqual(pts[5], (350, 250))
        self.assertEqual(pts[6], (277, 301))
        self.assertEqual(pts[7], (303, 215))
        self.assertEqual(pts[8], (231, 161))
        self.assertEqual(pts[9], (321, 161))

        path_data = polygon.get_path_data()
        self.assertEqual(len(path_data), 11)
        self.assertEqual(path_data[0].type, 'M')
        self.assertEqual(path_data[1].type, 'L')
        self.assertEqual(path_data[2].type, 'L')
        self.assertEqual(path_data[3].type, 'L')
        self.assertEqual(path_data[4].type, 'L')
        self.assertEqual(path_data[5].type, 'L')
        self.assertEqual(path_data[6].type, 'L')
        self.assertEqual(path_data[7].type, 'L')
        self.assertEqual(path_data[8].type, 'L')
        self.assertEqual(path_data[9].type, 'L')
        self.assertEqual(path_data[10].type, 'Z')
        self.assertEqual(path_data[0].values, (350, 75))
        self.assertEqual(path_data[1].values, (379, 161))
        self.assertEqual(path_data[2].values, (469, 161))
        self.assertEqual(path_data[3].values, (397, 215))
        self.assertEqual(path_data[4].values, (423, 301))
        self.assertEqual(path_data[5].values, (350, 250))
        self.assertEqual(path_data[6].values, (277, 301))
        self.assertEqual(path_data[7].values, (303, 215))
        self.assertEqual(path_data[8].values, (231, 161))
        self.assertEqual(path_data[9].values, (321, 161))
        self.assertEqual(path_data[10].values, ())

        n = polygon.get_total_length()
        expected = 899.3055419921875
        self.assertAlmostEqual(n, expected, places=places)

    def test_polygon02_normalize(self):
        # See also: polygon01.html
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        points = \
            "350,75 379,161 469,161 397,215 423,301 350,250" \
            " 277,301 303,215 231,161 321,161"
        polygon.attributes.set('points', points)

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = polygon.get_path_data(settings)
        exp = PathParser.tostring(normalized)
        expected = \
            "M350,75 L379,161 469,161 397,215 423,301 350,250 277,301" \
            " 303,215 231,161 321,161 Z"
        self.assertEqual(exp, expected)

    def test_polygon03_length(self):
        # See also: polygon01.html
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        points = \
            "850,75 958,137.5 958,262.5" \
            " 850,325 742,262.6 742,137.5"
        polygon.attributes.set('points', points)
        pts = polygon.points
        self.assertEqual(len(pts), 6)
        self.assertEqual(pts[0], (850, 75))
        self.assertEqual(pts[1], (958, 137.5))
        self.assertEqual(pts[2], (958, 262.5))
        self.assertEqual(pts[3], (850, 325))
        self.assertEqual(pts[4], (742, 262.6))
        self.assertEqual(pts[5], (742, 137.5))

        path_data = polygon.get_path_data()
        self.assertEqual(len(path_data), 7)
        self.assertEqual(path_data[0].type, 'M')
        self.assertEqual(path_data[1].type, 'L')
        self.assertEqual(path_data[2].type, 'L')
        self.assertEqual(path_data[3].type, 'L')
        self.assertEqual(path_data[4].type, 'L')
        self.assertEqual(path_data[5].type, 'L')
        self.assertEqual(path_data[6].type, 'Z')
        self.assertEqual(path_data[0].values, (850, 75))
        self.assertEqual(path_data[1].values, (958, 137.5))
        self.assertEqual(path_data[2].values, (958, 262.5))
        self.assertEqual(path_data[3].values, (850, 325))
        self.assertEqual(path_data[4].values, (742, 262.6))
        self.assertEqual(path_data[5].values, (742, 137.5))
        self.assertEqual(path_data[6].values, ())

        d = PathParser.tostring(path_data)
        expected = \
            "M850,75 L958,137.5 958,262.5 850,325 742,262.6 742,137.5 Z"
        self.assertEqual(d, expected)

        n = polygon.get_total_length()
        expected = 749.1731567382812
        self.assertAlmostEqual(n, expected, places=places)

    def test_polyline01_length(self):
        parser = SVGParser()
        polyline = parser.make_element('polyline')

        style = polyline.get_computed_geometry()
        points = style['points']
        self.assertEqual(len(points), 0)

        n = polyline.get_total_length()
        expected = 0
        self.assertEqual(n, expected)

    def test_polyline02_length(self):
        # See also: polyline01.html
        parser = SVGParser()
        polyline = parser.make_element('polyline')

        pts = \
            "50,375" \
            " 150,375 150,325 250,325 250,375" \
            " 350,375 350,250 450,250 450,375" \
            " 550,375 550,175 650,175 650,375" \
            " 750,375 750,100 850,100 850,375" \
            " 950,375 950,25 1050,25 1050,375" \
            " 1150,375"
        polyline.attributes.set('points', pts)

        points = polyline.points
        self.assertEqual(len(points), 22)
        self.assertEqual(points[0], (50, 375))
        self.assertEqual(points[1], (150, 375))
        self.assertEqual(points[2], (150, 325))
        # ...
        self.assertEqual(points[19], (1050, 25))
        self.assertEqual(points[20], (1050, 375))
        self.assertEqual(points[21], (1150, 375))

        path_data = polyline.get_path_data()
        self.assertEqual(len(path_data), 22)
        self.assertEqual(path_data[0].type, 'M')
        self.assertEqual(path_data[1].type, 'L')
        # ...
        self.assertEqual(path_data[21].type, 'L')

        n = polyline.get_total_length()
        expected = 3100
        self.assertEqual(n, expected)

    def test_polyline02_normalize(self):
        # See also: polyline01.html
        parser = SVGParser()
        polyline = parser.make_element('polyline')
        pts = \
            "50,375" \
            " 150,375 150,325 250,325 250,375" \
            " 350,375 350,250 450,250 450,375" \
            " 550,375 550,175 650,175 650,375" \
            " 750,375 750,100 850,100 850,375" \
            " 950,375 950,25 1050,25 1050,375" \
            " 1150,375"
        polyline.attributes.set('points', pts)

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = polyline.get_path_data(settings)
        exp = PathParser.tostring(normalized)
        expected = \
            "M50,375 L150,375 150,325 250,325 250,375 350,375 350,250" \
            " 450,250 450,375 550,375 550,175 650,175 650,375 750,375" \
            " 750,100 850,100 850,375 950,375 950,25 1050,25 1050,375 1150,375"
        self.assertEqual(exp, expected)

    def test_polyline03_length(self):
        # See also: triangle01.html
        parser = SVGParser()
        polyline = parser.make_element('polyline')
        pts = [(100, 100), (300, 100), (200, 300), (100, 100)]
        polyline.points = pts

        points = polyline.attributes.get('points')
        expected = '100,100 300,100 200,300 100,100'
        self.assertEqual(expected, points)

        n = polyline.get_total_length()
        expected = 647.213623046875
        self.assertAlmostEqual(n, expected, places=places)

    def test_polyline04_bbox(self):
        parser = SVGParser()
        polyline = parser.make_element('polyline')
        polyline.attributes.update({
            'points': "350,75 379,161 469,161 397,215 423,301 350,250" 
                      " 277,301 303,215 231,161 321,161",
        })

        bbox = polyline.get_bbox()
        self.assertEqual(bbox.x, 231)
        self.assertEqual(bbox.y, 75)
        self.assertEqual(bbox.width, 469 - 231)
        self.assertEqual(bbox.height, 301 - 75)

    def test_preserve_aspect_ratio01(self):
        par = SVGPreserveAspectRatio()  # -> xMidYMid meet
        self.assertEqual(par.align, 'xMidYMid')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMidYMid meet')

    def test_preserve_aspect_ratio02(self):
        par = SVGPreserveAspectRatio('slice')  # -> xMidYMid meet
        self.assertEqual(par.align, 'xMidYMid')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMidYMid meet')

    def test_preserve_aspect_ratio03(self):
        par = SVGPreserveAspectRatio('xMidYMin')  # -> xMidYMin meet
        self.assertEqual(par.align, 'xMidYMin')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMidYMin meet')

    def test_preserve_aspect_ratio04(self):
        par = SVGPreserveAspectRatio('xMaxYMin slice')
        self.assertEqual(par.align, 'xMaxYMin')
        self.assertEqual(par.meet_or_slice, 'slice')
        self.assertEqual(par.tostring(), 'xMaxYMin slice')

    def test_preserve_aspect_ratio05(self):
        par = SVGPreserveAspectRatio('XMinYMid slice')
        self.assertEqual(par.align, 'XMinYMid')
        self.assertEqual(par.meet_or_slice, 'slice')
        self.assertEqual(par.tostring(), 'XMinYMid slice')

    def test_preserve_aspect_ratio06(self):
        par = SVGPreserveAspectRatio('xMidYMid')  # -> xMidYMid meet
        self.assertEqual(par.align, 'xMidYMid')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMidYMid meet')

    def test_preserve_aspect_ratio07(self):
        par = SVGPreserveAspectRatio('xMaxYMid')  # -> xMaxYMid meet
        self.assertEqual(par.align, 'xMaxYMid')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMaxYMid meet')

    def test_preserve_aspect_ratio08(self):
        par = SVGPreserveAspectRatio('xMinYMax slice')
        self.assertEqual(par.align, 'xMinYMax')
        self.assertEqual(par.meet_or_slice, 'slice')
        self.assertEqual(par.tostring(), 'xMinYMax slice')

    def test_preserve_aspect_ratio09(self):
        par = SVGPreserveAspectRatio('xMidYMax meet')
        self.assertEqual(par.align, 'xMidYMax')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMidYMax meet')

    def test_preserve_aspect_ratio10(self):
        par = SVGPreserveAspectRatio('xMaxYMax meet')
        self.assertEqual(par.align, 'xMaxYMax')
        self.assertEqual(par.meet_or_slice, 'meet')
        self.assertEqual(par.tostring(), 'xMaxYMax meet')

    def test_preserve_aspect_ratio11(self):
        par = SVGPreserveAspectRatio('none')
        self.assertEqual(par.align, 'none')
        self.assertEqual(par.meet_or_slice, None)
        self.assertEqual(par.tostring(), 'none')

    def test_rect01_bbox(self):
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '0',
            'y': '0',
            'width': '400',
            'height': '200',
            'rx': '50',
            'ry': '25'
        })

        bbox = rect.get_bbox()
        self.assertEqual(bbox.x, 0)
        self.assertEqual(bbox.y, 0)
        self.assertEqual(bbox.width, 400)
        self.assertEqual(bbox.height, 200)

    def test_rect02_bbox(self):
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '.5',
            'y': '.5',
            'width': '29',
            'height': '39',
        })

        bbox = rect.get_bbox()
        self.assertEqual(bbox.x, 0.5)
        self.assertEqual(bbox.y, 0.5)
        self.assertEqual(bbox.width, 29)
        self.assertEqual(bbox.height, 39)

    def test_rect03_length(self):
        # initial value
        # x: 0
        # y: 0
        # width: auto => 0
        # height: auto => 0
        # rx: auto => 0
        # ry: auto => 0
        parser = SVGParser()
        rect = parser.make_element('rect')

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 0)

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = rect.get_path_data(settings)
        self.assertEqual(len(normalized), 0)

        n = rect.get_total_length()
        self.assertEqual(n, 0)

    def test_rect04_length(self):
        # square rectangle
        # x: 20
        # y: 10
        # width: 100
        # height: 120
        # rx: auto => 0
        # ry: auto => 0
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '20',
            'y': '10',
            'width': '100',
            'height': '120',
        })

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 6)
        d = PathParser.tostring(path_data)
        expected = "M20,10 H120 V130 H20 V10 Z"
        self.assertEqual(d, expected)

        n = rect.get_total_length()
        # (100 + 120) * 2 = 440
        self.assertEqual(n, 440)

    def test_rect04_normalize(self):
        # square rectangle
        # x: 20
        # y: 10
        # width: 100
        # height: 120
        # rx: auto => 0
        # ry: auto => 0
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '20',
            'y': '10',
            'width': '100',
            'height': '120',
        })

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = rect.get_path_data(settings)
        exp = PathParser.tostring(normalized)
        expected = 'M20,10 L120,10 120,130 20,130 20,10 Z'
        self.assertEqual(exp, expected)

    def test_rect05_length(self):
        # See also: rect02.html
        # ry = rx
        # x: 100
        # y: 100
        # width: 400
        # height: 200
        # rx: 50
        # ry: auto => 50
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '100',
            'y': '100',
            'width': '400',
            'height': '200',
            'rx': '50',
        })

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 10)
        d = PathParser.tostring(path_data)
        expected = \
            "M150,100" \
            " H450 A50,50 0 0 1 500,150" \
            " V250 A50,50 0 0 1 450,300" \
            " H150 A50,50 0 0 1 100,250" \
            " V150 A50,50 0 0 1 150,100 Z"
        self.assertEqual(d, expected)

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625  # chrome
        self.assertAlmostEqual(n, expected, places=places)

    def test_rect05_normalize(self):
        # See also: rect02.html
        # ry = rx
        # x: 100
        # y: 100
        # width: 400
        # height: 200
        # rx: 50
        # ry: auto => 50
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '100',
            'y': '100',
            'width': '400',
            'height': '200',
            'rx': '50',
        })

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = rect.get_path_data(settings)
        exp = PathParser.tostring(normalized)
        expected = \
            "M150,100" \
            " L450,100 C477.614,100 500,122.386 500,150" \
            " L500,250 C500,277.614 477.614,300 450,300" \
            " L150,300 C122.386,300 100,277.614 100,250" \
            " L100,150 C100,122.386 122.386,100 150,100 Z"
        self.assertEqual(exp, expected)

    def test_rect06_length(self):
        # See also: rect02.html
        # ry < rx
        # x: 0
        # y: 0
        # width: 400
        # height: 200
        # rx: 50
        # ry: 25
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '0',
            'y': '0',
            'width': '400',
            'height': '200',
            'rx': '50',
            'ry': '25'
        })

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 10)
        d = PathParser.tostring(path_data)
        expected = \
            "M50,0 H350 A50,25 0 0 1 400,25" \
            " V175 A50,25 0 0 1 350,200" \
            " H50 A50,25 0 0 1 0,175" \
            " V25 A50,25 0 0 1 50,0 Z"
        self.assertEqual(d, expected)

        n = rect.get_total_length()
        # expected = 1142.2462158203125  # firefox
        expected = 1142.2459716796875  # chrome
        self.assertAlmostEqual(n, expected, places=places)

    def test_rect06_normalize(self):
        # See also: rect02.html
        # ry < rx
        # x: 0
        # y: 0
        # width: 400
        # height: 200
        # rx: 50
        # ry: 25
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '0',
            'y': '0',
            'width': '400',
            'height': '200',
            'rx': '50',
            'ry': '25'
        })

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = rect.get_path_data(settings)
        exp = PathParser.tostring(normalized)
        expected = \
            "M50,0" \
            " L350,0 C377.614,0 400,11.193 400,25" \
            " L400,175 C400,188.807 377.614,200 350,200" \
            " L50,200 C22.386,200 0,188.807 0,175" \
            " L0,25 C0,11.193 22.386,0 50,0 Z"
        self.assertEqual(exp, expected)

    def test_rect07_length(self):
        # See also: rect02.html
        # rx = 'auto', ry = 'auto' -> square corners
        # x: 150
        # y: 150
        # width: 400
        # height: 200
        # rx: auto => 0
        # ry: auto => 0
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '150',
            'y': '150',
            'width': '400',
            'height': '200',
            'rx': 'auto',
            'ry': 'auto'
        })

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 6)
        d = PathParser.tostring(path_data)
        expected = 'M150,150 H550 V350 H150 V150 Z'
        self.assertEqual(d, expected)

        n = rect.get_total_length()
        # (400 + 200) * 2 = 1200
        expected = 1200
        self.assertEqual(n, expected)

    def test_rect08_length(self):
        # rx = length value, ry = 'auto' => ry = rx
        # x: 150
        # y: 150
        # width: 400
        # height: 200
        # rx: 50
        # ry: auto => 50
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '150',
            'y': '150',
            'width': '400',
            'height': '200',
            'rx': '50',
            'ry': 'auto'
        })

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 10)
        d = PathParser.tostring(path_data)
        expected = \
            "M200,150" \
            " H500 A50,50 0 0 1 550,200" \
            " V300 A50,50 0 0 1 500,350" \
            " H200 A50,50 0 0 1 150,300" \
            " V200 A50,50 0 0 1 200,150 Z"
        self.assertEqual(d, expected)

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625  # chrome
        self.assertAlmostEqual(n, expected, places=places)

    def test_rect09_length(self):
        # rx = 'auto', ry = length value => rx = ry
        # x: 150
        # y: 150
        # width: 400
        # height: 200
        # rx: auto => 50
        # ry: 50
        parser = SVGParser()
        rect = parser.make_element('rect')
        rect.attributes.update({
            'x': '150',
            'y': '150',
            'width': '400',
            'height': '200',
            'rx': 'auto',
            'ry': '50'
        })

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 10)
        d = PathParser.tostring(path_data)
        expected = \
            "M200,150" \
            " H500 A50,50 0 0 1 550,200" \
            " V300 A50,50 0 0 1 500,350" \
            " H200 A50,50 0 0 1 150,300" \
            " V200 A50,50 0 0 1 200,150 Z"
        self.assertEqual(d, expected)

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625  # chrome
        self.assertAlmostEqual(n, expected, places=places)

    def test_rect10_length(self):
        # rx = percentage value, ry = 'auto' => ry = rx
        # x: 150
        # y: 150
        # width: 400
        # height: 200
        # rx: 12.5% => 400 * 12.5% = 50
        # ry: auto => 50
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'viewBox': '0 0 400 200'
        })
        rect = root.make_sub_element('rect')
        rect.attributes.update({
            'x': '150',
            'y': '150',
            'width': '400',
            'height': '200',
            'rx': '12.5%',
            'ry': 'auto'
        })

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625
        self.assertAlmostEqual(n, expected, places=places)

        path_data = rect.get_path_data()
        self.assertEqual(len(path_data), 10)
        d = PathParser.tostring(path_data)
        expected = \
            "M200,150" \
            " H500 A50,50 0 0 1 550,200" \
            " V300 A50,50 0 0 1 500,350" \
            " H200 A50,50 0 0 1 150,300" \
            " V200 A50,50 0 0 1 200,150 Z"
        self.assertEqual(d, expected)

    def test_rect11_length(self):
        # x: 150
        # y: 150
        # width: 25(%) => 1600 * 25% = 400(px)
        # height: 50(%) => 400(cm) * 50% = 200(px)
        # rx: 12.5% => 1600 * 12.5% = 200(px)
        # ry: auto => rx => 200(px) => height / 2 => 100(px)
        # => ellipse rx=200 ry=100
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'width': '4cm',
            'height': '3cm',
            'viewBox': '0 0 1600 400',
        })

        rect = root.make_sub_element('rect')
        rect.attributes.update({
            'x': '150',
            'y': '150',
            'width': '25%',
            'height': '50%',
            'rx': '12.5%',
            'ry': 'auto'
        })

        n = rect.get_total_length()
        # arc length: 968.8438541327044183204(px)
        expected = 968.8438541327044183204
        self.assertAlmostEqual(n, expected, places=places)

    def test_svg(self):
        # nested svg
        # percentage-length
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'width': '1200',
            'height': '400',
        })

        child = root.make_sub_element('svg')
        child.attributes.update({
            'width': '40%',
            'height': '50%',
        })

        style = child.get_computed_geometry()

        # FIXME: correct?
        expected = 1200 * 0.4
        self.assertAlmostEqual(style['width'], expected)

        expected = 400 * 0.5
        self.assertAlmostEqual(style['height'], expected)

    def test_svg_current_scale(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'id': 'root',
        })

        child = root.make_sub_element('svg')
        child.attributes.update({
            'id': 'svg01',
        })

        # outermost svg element
        scale = root.current_scale
        expected = 1
        self.assertEqual(scale, expected)

        root.current_scale = 1.5
        scale = root.current_scale
        expected = 1.5
        self.assertEqual(scale, expected)

        # child svg element
        scale = child.current_scale
        expected = 1
        self.assertEqual(scale, expected)

        child.current_scale = 1.5
        scale = child.current_scale
        expected = 1
        self.assertEqual(scale, expected)

    def test_svg_current_translate(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'id': 'root',
        })

        child = root.make_sub_element('svg')
        child.attributes.update({
            'id': 'svg01',
        })

        # outermost svg element
        translate = root.current_translate
        expected = 0, 0
        self.assertEqual(translate, expected)

        root.current_translate = 100, -100
        translate = root.current_translate
        expected = 100, -100
        self.assertEqual(translate, expected)

        # child svg element
        translate = child.current_translate
        expected = 0, 0
        self.assertEqual(translate, expected)

        child.current_translate = 100, -100
        translate = child.current_translate
        expected = 0, 0
        self.assertEqual(translate, expected)

    def test_view_box01(self):
        # See also: ViewBox.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_VIEW_BOX))
        root = tree.getroot()

        # id="root"
        element = root.get_element_by_id('root')
        view_box = element.get_view_box()
        self.assertIsNone(view_box)

        # CTM = [1, 0, 0, 1, 0, 0]
        m = element.get_ctm()
        expected = Matrix()
        self.assertEqual(m, expected)

        # id="svg01"
        element = root.get_element_by_id('svg01')
        view_box = element.get_view_box()
        par = SVGPreserveAspectRatio('none')
        expected = \
            SVGLength(0), SVGLength(0), SVGLength(1500), SVGLength(1000), par
        self.assertEqual(view_box, expected)

        # CTM = [0.2, 0, 0, 0.2, 0, 0]
        m = element.get_ctm()
        expected = Matrix(0.2, 0, 0, 0.2, 0, 0)
        self.assertEqual(m, expected)

        # id="rect01"
        element = root.get_element_by_id('rect01')

        # CTM = [0.2, 0, 0, 0.2, 0, 0]
        m = element.get_ctm()
        expected = Matrix(0.2, 0, 0, 0.2, 0, 0)
        self.assertEqual(m, expected)

        # id="svg02"
        element = root.get_element_by_id('svg02')
        view_box = element.get_view_box()
        par = SVGPreserveAspectRatio('none')
        expected = \
            SVGLength(0), SVGLength(0), SVGLength(1500), SVGLength(1000), par
        self.assertEqual(view_box, expected)

        # CTM = [0.1, 0, 0, 0.2, 300, 0]
        m = element.get_ctm()
        expected = Matrix(0.1, 0, 0, 0.2, 300, 0)
        self.assertEqual(m, expected)

        # id="rect02"
        element = root.get_element_by_id('rect02')

        # CTM = [0.1, 0, 0, 0.2, 300, 0]
        m = element.get_ctm()
        expected = Matrix(0.1, 0, 0, 0.2, 300, 0)
        self.assertEqual(m, expected)

    def test_view_box02(self):
        # See also: ViewBox.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_VIEW_BOX))
        root = tree.getroot()

        # outermost svg element
        element = root.get_element_by_id('root')
        element.attributes.update({
            'transform': 'translate(50 25)',
            'zoomAndPan': 'magnify',
        })
        element.current_scale = 1.2
        element.current_translate = 100, 50

        zap = element.zoom_and_pan
        self.assertEqual(zap, SVGZoomAndPan.ZOOMANDPAN_MAGNIFY)

        # CTM: [1, 0, 0, 1, 0, 0] ->
        # [1.2, 0, 0, 1.2, 100, 50] * [1, 0, 0, 1, 50, 25]
        # = [1.2, 0, 0, 1.2, 160, 80]
        m = element.get_ctm()
        expected = Matrix(1.2, 0, 0, 1.2, 160, 80)
        self.assertEqual(m, expected)

        element.attributes.update({
            'zoomAndPan': 'disable',
        })

        # CTM: [1, 0, 0, 1, 0, 0] -> [1, 0, 0, 1, 50, 25]
        m = element.get_ctm()
        expected = Matrix(1, 0, 0, 1, 50, 25)
        self.assertEqual(m, expected)

        # child svg element
        element = root.get_element_by_id('svg02')
        element.attributes.update({
            'zoomAndPan': 'magnify',
        })
        element.current_scale = 1.2
        element.current_translate = 100, 50

        # CTM: [0.1, 0, 0, 0.2, 300, 0]
        m = element.get_ctm()
        expected = Matrix(0.1, 0, 0, 0.2, 300, 0)
        self.assertEqual(m, expected)

    def test_viewport01_01(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # meet-group-1
        # id="xMinYMin_meet"
        # width="50" height="30"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMinYMin meet"
        element = root.get_element_by_id('xMinYMin_meet')

        vpx, vpy, vpw, vph = element.get_viewport_size()
        expected = SVGLength(0), SVGLength(0), SVGLength(50), SVGLength(30)
        self.assertEqual((vpx, vpy, vpw, vph), expected)

        vbx, vby, vbw, vbh, par = element.get_view_box()
        expected = SVGLength(0), SVGLength(0), SVGLength(30), SVGLength(40)
        self.assertEqual((vbx, vby, vbw, vbh), expected)
        self.assertEqual(par.align, 'xMinYMin')
        self.assertEqual(par.meet_or_slice, 'meet')

        # CTM = [0.75, 0, 0, 0.75, 0, 0]
        m = element.get_ctm()
        expected = Matrix(0.75, 0, 0, 0.75, 0, 0)
        self.assertEqual(m, expected)

    def test_viewport01_02(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # meet-group-1
        # id="xMidYMid_meet"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMidYMid meet"
        # width="50" height="30"
        # CTM = [0.75, 0, 0, 0.75, 13.75, 0]
        element = root.get_element_by_id('xMidYMid_meet')
        m = element.get_ctm()
        expected = Matrix(0.75, 0, 0, 0.75, 13.75, 0)
        self.assertEqual(m, expected)

    def test_viewport01_03(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # meet-group-1
        # id="xMaxYMax_meet"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMaxYMax meet"
        # width="50" height="30"
        # CTM = [0.75, 0, 0, 0.75, 27.5, 0]
        element = root.get_element_by_id('xMaxYMax_meet')
        m = element.get_ctm()
        expected = Matrix(0.75, 0, 0, 0.75, 27.5, 0)
        self.assertEqual(m, expected)

    def test_viewport01_04(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # meet-group-2
        # id="xMinYMin_meet02"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMinYMin meet"
        # width="30" height="60"
        # CTM = [1, 0, 0, 1, 0, 0]
        element = root.get_element_by_id('xMinYMin_meet02')
        m = element.get_ctm()
        expected = Matrix(1, 0, 0, 1, 0, 0)
        self.assertEqual(m, expected)

    def test_viewport01_05(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # meet-group-2
        # id="xMidYMid_meet02"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMidYMid meet"
        # width="30" height="60"
        # CTM = [1, 0, 0, 1, 0, 10]
        element = root.get_element_by_id('xMidYMid_meet02')
        m = element.get_ctm()
        expected = Matrix(1, 0, 0, 1, 0, 10)
        self.assertEqual(m, expected)

    def test_viewport01_06(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # meet-group-2
        # id="xMaxYMax_meet"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMaxYMax meet"
        # width="30" height="60"
        # CTM = [1, 0, 0, 1, 0, 20]
        element = root.get_element_by_id('xMaxYMax_meet02')
        m = element.get_ctm()
        expected = Matrix(1, 0, 0, 1, 0, 20)
        self.assertEqual(m, expected)

    def test_viewport01_07(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # slice-group-1
        # id="xMinYMin_slice"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMinYMin slice"
        # width="30" height="60"
        # CTM = [1.5, 0, 0, 1.5, 0, 0]
        element = root.get_element_by_id('xMinYMin_slice')
        m = element.get_ctm()
        expected = Matrix(1.5, 0, 0, 1.5, 0, 0)
        self.assertEqual(m, expected)

    def test_viewport01_08(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # slice-group-1
        # id="xMidYMid_slice"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMidYMid slice"
        # width="30" height="60"
        # CTM = [1.5, 0, 0, 1.5, -7.5, 0]
        element = root.get_element_by_id('xMidYMid_slice')
        m = element.get_ctm()
        expected = Matrix(1.5, 0, 0, 1.5, -7.5, 0)
        self.assertEqual(m, expected)

    def test_viewport01_09(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # slice-group-1
        # id="xMaxYMax_slice"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMaxYMax slice"
        # width="30" height="60"
        # CTM = [1.5, 0, 0, 1.5, -15, 0]
        element = root.get_element_by_id('xMaxYMax_slice')
        m = element.get_ctm()
        expected = Matrix(1.5, 0, 0, 1.5, -15, 0)
        self.assertEqual(m, expected)

    def test_viewport01_10(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # slice-group-2
        # id="xMinYMin_slice"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMinYMin slice"
        # width="50" height="30"
        # CTM = [1.6666666666666667, 0, 0, 1.6666666666666667, 0, 0]
        element = root.get_element_by_id('xMinYMin_slice02')
        m = element.get_ctm()
        expected = Matrix(1.6666666666666667, 0, 0, 1.6666666666666667, 0, 0)
        self.assertEqual(m, expected)

    def test_viewport01_11(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # slice-group-2
        # id="xMidYMid_slice"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMidYMid slice"
        # width="50" height="30"
        # CTM = [1.6666666666666667, 0, 0,
        #  1.6666666666666667, 0, -18.333333333333336]
        element = root.get_element_by_id('xMidYMid_slice02')
        m = element.get_ctm()
        expected = Matrix(1.6666666666666667, 0, 0,
                          1.6666666666666667, 0, -18.333333333333336)
        self.assertEqual(m, expected)

    def test_viewport01_12(self):
        # See also: SVGPreserveAspectRatio.html
        # https://svgwg.org/svg2-draft/coords.html#ViewBoxAttribute
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_PRESERVE_ASPECT_RATIO))
        root = tree.getroot()

        # slice-group-2
        # id="xMaxYMax_slice"
        # viewBox="0 0 30 40"
        # preserveAspectRatio="xMaxYMax slice"
        # width="50" height="30"
        # CTM = [1.6666666666666667, 0, 0,
        #  1.6666666666666667, 0, -36.66666666666667]
        element = root.get_element_by_id('xMaxYMax_slice02')
        m = element.get_ctm()
        expected = Matrix(1.6666666666666667, 0, 0,
                          1.6666666666666667, 0, -36.66666666666667)
        self.assertEqual(m, expected)

    def test_viewport02(self):
        # nested svg
        # See also: nestedsvg01.html
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'id': 'svg01',
            'width': '10cm',
            'height': '4cm',
            'viewBox': '0 0 400 400',
        })

        svg02 = root.make_sub_element('svg')
        svg02.attributes.update({
            'id': 'svg02',
            'x': '1cm',
            'y': '1cm',
        })

        svg03 = svg02.make_sub_element('svg')
        svg03.attributes.update({
            'id': 'svg03',
            'x': '40',
            'y': '40',
            'width': '80',
            'height': '80',
        })

        vpx, vpy, vpw, vph = root.get_viewport_size()
        self.assertEqual(vpx.tostring(), '0')
        self.assertEqual(vpy.tostring(), '0')
        self.assertEqual(vpw.tostring(), '10cm')
        self.assertEqual(vph.tostring(), '4cm')

        style = root.get_computed_geometry()
        self.assertAlmostEqual(style['x'], 0)
        self.assertAlmostEqual(style['y'], 0)
        # width = 10(cm) = 10 / 2.54 * 96
        self.assertAlmostEqual(style['width'], 377.952756, delta=delta)
        # height = 4(cm) = 4 / 2.54 * 96
        self.assertAlmostEqual(style['height'], 151.181102, delta=delta)

        vpx, vpy, vpw, vph = svg02.get_viewport_size()
        self.assertEqual(vpx.tostring(), '1cm')
        self.assertEqual(vpy.tostring(), '1cm')
        self.assertEqual(vpw.tostring(), '10cm')
        self.assertEqual(vph.tostring(), '4cm')

        style = svg02.get_computed_geometry()
        # x = 1(cm) = 1 / 2.54 * 96
        self.assertAlmostEqual(style['x'], 37.795276, delta=delta)
        # y = 1(cm) = 1 / 2.54 * 96
        self.assertAlmostEqual(style['y'], 37.795276, delta=delta)
        self.assertAlmostEqual(style['width'], 377.952756, delta=delta)
        self.assertAlmostEqual(style['height'], 151.181102, delta=delta)

        vpx, vpy, vpw, vph = svg03.get_viewport_size()
        self.assertEqual(vpx.tostring(), '40')
        self.assertEqual(vpy.tostring(), '40')
        self.assertEqual(vpw.tostring(), '80')
        self.assertEqual(vph.tostring(), '80')

        style = svg03.get_computed_geometry()
        self.assertAlmostEqual(style['x'], 40, delta=delta)
        self.assertAlmostEqual(style['y'], 40, delta=delta)
        self.assertAlmostEqual(style['width'], 80, delta=delta)
        self.assertAlmostEqual(style['height'], 80, delta=delta)

    def test_viewport03(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'viewBox': '0 50 500 200',
        })

        vpx, vpy, vpw, vph = root.get_viewport_size()
        self.assertEqual(vpx.value(direction=SVGLength.DIRECTION_HORIZONTAL), 0)
        self.assertEqual(vpy.value(direction=SVGLength.DIRECTION_VERTICAL), 0)
        self.assertEqual(vpw.value(direction=SVGLength.DIRECTION_HORIZONTAL),
                         Window.inner_width)
        self.assertEqual(vph.value(direction=SVGLength.DIRECTION_VERTICAL),
                         Window.inner_height)

        vbx, vby, vbw, vbh, _ = root.get_view_box()
        self.assertEqual(vbx.value(direction=SVGLength.DIRECTION_HORIZONTAL), 0)
        self.assertEqual(vby.value(direction=SVGLength.DIRECTION_VERTICAL), 50)
        self.assertEqual(vbw.value(direction=SVGLength.DIRECTION_HORIZONTAL),
                         500)
        self.assertEqual(vbh.value(direction=SVGLength.DIRECTION_VERTICAL), 200)


if __name__ == '__main__':
    unittest.main()
