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
    SVGPathDataSettings, SVGPreserveAspectRatio, SVGZoomAndPan, window, \
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

    def test_bbox01_01(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('defs-1')
        bbox = element.get_bbox()
        self.assertEqual(Rect(), bbox, msg=element)

    def test_bbox01_02(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('rect-1')
        bbox = element.get_bbox()
        self.assertEqual(Rect(20, 20, 40, 40), bbox, msg=element.id)

    def test_bbox01_03(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('group-1')
        bbox = element.get_bbox()
        self.assertEqual(Rect(30, 30, 40, 40), bbox, msg=element.id)

    def test_bbox01_04(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('use-1')
        bbox = element.get_bbox()
        self.assertEqual(Rect(30, 30, 40, 40), bbox, msg=element.id)

    def test_bbox01_05(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('group-2')
        bbox = element.get_bbox()
        self.assertEqual(Rect(10, 10, 100, 100), bbox, msg=element.id)

    def test_bbox01_06(self):
        # See https://svgwg.org/svg2-draft/coords.html#BoundingBoxes
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_BBOX01))
        root = tree.getroot()

        element = root.get_element_by_id('rect-2')
        bbox = element.get_bbox()
        self.assertEqual(Rect(10, 10, 100, 100), bbox, msg=element.id)

    def test_bbox02_01(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root
        bbox = element.get_bbox()
        self.assertAlmostEqual(11.101, bbox.x, msg=element.id, delta=delta)
        self.assertAlmostEqual(11.101, bbox.y, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.width, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.height, msg=element.id, delta=delta)

    def test_bbox02_02(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('gtop')
        bbox = element.get_bbox()
        self.assertAlmostEqual(11.101, bbox.x, msg=element.id, delta=delta)
        self.assertAlmostEqual(11.101, bbox.y, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.width, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.height, msg=element.id, delta=delta)

    def test_bbox02_03(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('svgstar')
        bbox = element.get_bbox()
        self.assertAlmostEqual(-38.899, bbox.x, msg=element.id, delta=delta)
        self.assertAlmostEqual(-38.899, bbox.y, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.width, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.height, msg=element.id, delta=delta)

    def test_bbox02_04(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('svgbar')
        bbox = element.get_bbox()
        self.assertAlmostEqual(-38.899, bbox.x, msg=element.id, delta=delta)
        self.assertAlmostEqual(-7, bbox.y, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.width, msg=element.id, delta=delta)
        self.assertAlmostEqual(14, bbox.height, msg=element.id, delta=delta)

    def test_bbox02_08(self):
        # from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/svg.svg
        # See also svg.svg
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        element = root.get_element_by_id('usetop')
        bbox = element.get_bbox()
        self.assertAlmostEqual(11.101, bbox.x, msg=element.id, delta=delta)
        self.assertAlmostEqual(11.101, bbox.y, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.width, msg=element.id, delta=delta)
        self.assertAlmostEqual(77.798, bbox.height, msg=element.id, delta=delta)

    def test_circle00_length(self):
        # circle: initial value
        parser = SVGParser()
        circle = parser.make_element('circle')

        style = circle.get_computed_style()
        self.assertEqual(0, style['cx'])
        self.assertEqual(0, style['cy'])
        self.assertEqual(0, style['r'])

        path_data = circle.get_path_data()
        self.assertEqual(0, len(path_data))

        n = circle.get_total_length()
        expected = 0
        self.assertAlmostEqual(expected, n)

    def test_circle01_bbox(self):
        parser = SVGParser()
        circle = parser.make_element('circle')
        circle.attributes.update({
            'cx': '200',
            'cy': '300',
            'r': '100',
        })

        bbox = circle.get_bbox()
        self.assertEqual(200 - 100, bbox.x)
        self.assertEqual(300 - 100, bbox.y)
        self.assertEqual(100 * 2, bbox.width)
        self.assertEqual(100 * 2, bbox.height)

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
        self.assertEqual(cx, style['cx'])
        self.assertEqual(cy, style['cy'])
        self.assertEqual(r, style['r'])

        path_data = circle.get_path_data()
        d = PathParser.tostring(path_data)
        expected = \
            "M700,200" \
            " A100,100 0 0 1 600,300" \
            " 100,100 0 0 1 500,200" \
            " 100,100 0 0 1 600,100" \
            " 100,100 0 0 1 700,200 Z"
        self.assertEqual(expected, d, msg=d)

        n = circle.get_total_length()
        expected = 2 * math.pi * r
        self.assertAlmostEqual(expected, n)

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
        self.assertEqual(expected, exp)

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
        self.assertAlmostEqual(expected, style['cx'])

        # cy = 400 * 50% = 200
        expected = 200
        self.assertAlmostEqual(expected, style['cy'])

        # r = sqrt((width) ** 2 + (height) ** 2) / sqrt(2) * 10%
        #  = sqrt(1200 ** 2 + 400 ** 2) / sqrt(2) * 10%
        #  = 89.44271909999159
        expected = 89.44271909999159
        self.assertAlmostEqual(expected, style['r'], places=places)

        n = circle.get_total_length()
        # 2 * pi * r = 561.9851784832581
        expected = 561.9851784832581
        self.assertAlmostEqual(expected, n, places=places)

    def test_computed_style02(self):
        # See also: Units.html
        # Relative units
        # Default font size: 16px
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_UNITS))
        root = tree.getroot()

        rect = root.get_element_by_id('rect_rel_01')
        style = rect.get_computed_style()
        self.assertEqual(['Verdana'], style['font-family'], msg=style)
        self.assertEqual(150, style['font-size'], msg=style)
        self.assertEqual(Font.WEIGHT_NORMAL, style['font-weight'], msg=style)
        self.assertEqual(0, style['x'], msg=style)
        self.assertEqual(400, style['y'], msg=style)
        self.assertEqual(375, style['width'], msg=style)
        self.assertEqual(187.5, style['height'], msg=style)
        self.assertEqual(0, style['rx'], msg=style)
        self.assertEqual(0, style['ry'], msg=style)
        self.assertAlmostEqual(37.5, style['stroke-width'], msg=style,
                               places=places)

        rect = root.get_element_by_id('rect_rel_03')
        style = rect.get_computed_style()
        self.assertEqual(['Verdana'], style['font-family'], msg=style)
        self.assertEqual(150, style['font-size'], msg=style)
        self.assertEqual(Font.WEIGHT_NORMAL, style['font-weight'], msg=style)
        self.assertEqual(0, style['x'], msg=style)
        self.assertEqual(600, style['y'], msg=style)
        self.assertEqual(375, style['width'], msg=style)
        self.assertEqual(187.5, style['height'], msg=style)
        self.assertEqual(0, style['rx'], msg=style)
        self.assertEqual(0, style['ry'], msg=style)
        self.assertAlmostEqual(37.5, style['stroke-width'], msg=style,
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
        self.assertEqual(['Verdana'], style['font-family'], msg=style)
        self.assertEqual(150, style['font-size'], msg=style)
        self.assertEqual(Font.WEIGHT_NORMAL, style['font-weight'], msg=style)
        self.assertEqual(0, style['x'], msg=style)
        self.assertEqual(400, style['y'], msg=style)
        self.assertEqual(400, style['width'], msg=style)
        self.assertEqual(200, style['height'], msg=style)
        self.assertEqual(0, style['rx'], msg=style)
        self.assertEqual(0, style['ry'], msg=style)
        self.assertAlmostEqual(31.62, style['stroke-width'], msg=style,
                               places=places)

        rect = root.get_element_by_id('rect_per_03')
        style = rect.get_computed_style()
        # print(sorted(style.items()))
        self.assertEqual(['Verdana'], style['font-family'], msg=style)
        self.assertEqual(150, style['font-size'], msg=style)
        self.assertEqual(Font.WEIGHT_NORMAL, style['font-weight'], msg=style)
        self.assertEqual(0, style['x'], msg=style)
        self.assertEqual(600, style['y'], msg=style)
        self.assertEqual(400, style['width'], msg=style)
        self.assertEqual(200, style['height'], msg=style)
        self.assertEqual(0, style['rx'], msg=style)
        self.assertEqual(0, style['ry'], msg=style)
        self.assertAlmostEqual(31.62, style['stroke-width'], msg=style,
                               places=places)

    def test_computed_style04(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.set_style({
            'fill': 'red',
            'stroke': 'blue',
            'stroke-width': '1',
        })
        rect = group.make_sub_element('rect')
        rect.attributes.update({
            'fill': 'white',
            'stroke-width': '5',
        })

        self.assertEqual(
            {
                'style': 'fill: red; stroke-width: 1; stroke: blue;',
            },
            group.attributes)
        self.assertEqual(
            {
                'fill': 'white',
                'stroke-width': '5',
            },
            rect.attributes)
        css_style = rect.get_computed_style()
        self.assertEqual('white', css_style.get('fill'))
        self.assertEqual('blue', css_style.get('stroke'))
        self.assertEqual(5, css_style.get('stroke-width'))

    def test_computed_style05(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'fill': 'white',
            'stroke-width': '5',
        })
        rect = group.make_sub_element('rect')
        rect.attributes.set_style({
            'fill': 'red',
            'stroke': 'blue',
            'stroke-width': '1',
        })

        self.assertEqual(
            {
                'fill': 'white',
                'stroke-width': '5',
            },
            group.attributes)
        self.assertEqual(
            {
                'style': 'fill: red; stroke-width: 1; stroke: blue;',
            },
            rect.attributes)
        css_style = rect.get_computed_style()
        self.assertEqual('red', css_style.get('fill'))
        self.assertEqual('blue', css_style.get('stroke'))
        self.assertEqual(1, css_style.get('stroke-width'))

    def test_computed_style06(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.set_style({
            'fill': 'red',
            'stroke': 'blue',
            'stroke-width': '1',
        })
        rect = group.make_sub_element('rect')
        rect.attributes.set_style({
            'fill': 'white',
            'stroke-width': '5',
        })

        self.assertEqual(
            {
                'style': 'fill: red; stroke-width: 1; stroke: blue;',
            },
            group.attributes)
        self.assertEqual(
            {
                'style': 'fill: white; stroke-width: 5;',
            },
            rect.attributes)
        css_style = rect.get_computed_style()
        self.assertEqual('white', css_style.get('fill'))
        self.assertEqual('blue', css_style.get('stroke'))
        self.assertEqual(5, css_style.get('stroke-width'))

    def test_element_attributes(self):
        parser = SVGParser()
        root = parser.make_element('svg')

        root.attributes.set('width', '20cm')
        root.attributes.set('height', '10cm')
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(2, len(root.attrib))
        self.assertTrue('width' in root.attributes)
        self.assertTrue('height' in root.attributes)
        self.assertTrue('x' not in root.attributes)
        self.assertTrue(root.attributes.has('width'))
        self.assertTrue(root.attributes.has('height'))
        self.assertTrue(not root.attributes.has('x'))

        width = root.attributes.pop('width')
        self.assertEqual(1, len(root.attributes))
        self.assertEqual(1, len(root.attrib))
        self.assertEqual('20cm', width)
        self.assertTrue('width' not in root.attributes)
        self.assertTrue('height' in root.attributes)
        self.assertTrue(not root.attributes.has('width'))
        self.assertTrue(root.attributes.has('height'))

        del root.attributes['height']
        self.assertEqual(0, len(root.attributes))
        self.assertEqual(0, len(root.attrib))
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
        self.assertEqual(2, len(root.attributes))
        self.assertEqual(2, len(root.attrib))
        self.assertEqual('15cm', width)
        self.assertEqual('10cm', height)
        self.assertTrue(x is None)
        self.assertTrue(root.attributes.has('width'))
        self.assertTrue(root.attributes.has('height'))
        self.assertTrue(not root.attributes.has('x'))

        x = root.attributes.get('x', '100')
        self.assertEqual('100', x)

        self.assertTrue('viewBox' not in root.attributes)

        view_box = root.attributes.setdefault('viewBox', '0 0 200 100')
        self.assertEqual('0 0 200 100', view_box)

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
        self.assertEqual(expected, root.tostring().decode())

        lang = attributes.get('lang')
        self.assertIsNone(lang)
        self.assertTrue(not attributes.has_ns(None, 'lang'))

        lang = attributes.get_ns(Element.XML_NAMESPACE_URI, 'lang')
        expected = 'ja'
        self.assertEqual(expected, lang)

        space = attributes.get_ns(Element.XML_NAMESPACE_URI,
                                  'space')  # deprecated
        self.assertIsNone(space)
        self.assertTrue(not attributes.has_ns(Element.XML_NAMESPACE_URI,
                                              'space'))

        space = attributes.get_ns(Element.XML_NAMESPACE_URI,
                                  'space', 'preserve')
        expected = 'preserve'
        self.assertEqual(expected, space)

        lang = attributes.pop_ns(Element.XML_NAMESPACE_URI, 'lang', 'en')
        expected = 'ja'
        self.assertEqual(expected, lang)
        self.assertTrue(not attributes.has_ns(Element.XML_NAMESPACE_URI,
                                              'lang'))

        expected = "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
                   "<text/></svg>"
        self.assertEqual(expected, root.tostring().decode())

        lang = attributes.setdefault_ns(Element.XML_NAMESPACE_URI, 'lang', 'en')
        expected = 'en'
        self.assertEqual(expected, lang)
        self.assertTrue(attributes.has_ns(Element.XML_NAMESPACE_URI, 'lang'))

        expected = "<svg xmlns=\"http://www.w3.org/2000/svg\">" \
                   "<text xml:lang=\"en\"/></svg>"
        self.assertEqual(expected, root.tostring().decode())

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
        self.assertEqual(4, len(circle.keys()))
        self.assertEqual(4, len(circle.attributes))
        self.assertEqual(4, len(circle.attrib))
        self.assertEqual('120', circle.attributes.get('r'))
        self.assertEqual('100', circle.attributes.get('cx'))
        self.assertEqual('200', circle.attributes.get('cy'))
        self.assertEqual('red', circle.attributes.get('stroke'))
        self.assertEqual('5', circle.attributes.get('stroke-width'))
        self.assertEqual('10 5', circle.attributes.get('stroke-dasharray'))

        style = circle.attributes.get('style')
        expected = 'stroke-dasharray: 10 5; stroke-width: 5; stroke: red;'
        self.assertEqual(expected, style)
        self.assertTrue(circle.attributes.has('r'))
        self.assertTrue(circle.attributes.has('cx'))
        self.assertTrue(circle.attributes.has('cy'))
        self.assertTrue(circle.attributes.has('style'))
        self.assertTrue(circle.attributes.has('stroke'))
        self.assertTrue(circle.attributes.has('stroke-width'))
        self.assertTrue(circle.attributes.has('stroke-dasharray'))

        d = circle.attributes.get_style()
        self.assertEqual(3, len(d))
        self.assertEqual('red', d['stroke'])
        self.assertEqual('5', d['stroke-width'])
        self.assertEqual('10 5', d['stroke-dasharray'])

        sw = circle.attributes.pop('stroke-width')
        self.assertEqual(4, len(circle.keys()))
        self.assertEqual('5', sw)
        self.assertEqual('120', circle.attributes.get('r'))
        self.assertEqual('100', circle.attributes.get('cx'))
        self.assertEqual('200', circle.attributes.get('cy'))
        self.assertEqual('red', circle.attributes.get('stroke'))
        self.assertEqual('10 5', circle.attributes.get('stroke-dasharray'))
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
        self.assertEqual(expected, style)

        d = circle.attributes.get_style()
        self.assertEqual(2, len(d))
        self.assertEqual('red', d['stroke'])
        self.assertEqual('10 5', d['stroke-dasharray'])

        circle.attributes.update({
            'cx': '500',
            'cy': '800',
            'stroke': 'green',
        })
        self.assertEqual(4, len(circle.keys()))
        self.assertEqual('120', circle.attributes.get('r'))
        self.assertEqual('500', circle.attributes.get('cx'))
        self.assertEqual('800', circle.attributes.get('cy'))
        self.assertEqual('green', circle.attributes.get('stroke'))
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
        self.assertEqual(expected, style)

        d = circle.attributes.get_style()
        self.assertEqual(2, len(d))
        self.assertEqual('green', d['stroke'])
        self.assertEqual('10 5', d['stroke-dasharray'])

        self.assertTrue('fill' not in circle.attributes)
        self.assertTrue('fill' not in circle.attrib)
        d = circle.attributes.get_style()
        d.update({
            'fill': 'none',
        })
        circle.attributes.set_style(d)
        self.assertTrue('fill' in circle.attributes)
        self.assertTrue('fill' not in circle.attrib)
        self.assertEqual(4, len(circle.keys()))
        self.assertEqual('120', circle.attributes.get('r'))
        self.assertEqual('500', circle.attributes.get('cx'))
        self.assertEqual('800', circle.attributes.get('cy'))
        self.assertEqual('none', circle.attributes.get('fill'))
        self.assertEqual('green', circle.attributes.get('stroke'))
        self.assertEqual('10 5', circle.attributes.get('stroke-dasharray'))
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
        self.assertEqual(expected, style)

        circle.attributes.pop('stroke')
        self.assertEqual(4, len(circle.keys()))

        circle.attributes.pop('stroke')  # remove twice
        self.assertEqual(4, len(circle.keys()))

        circle.attributes.pop('stroke-width')
        self.assertEqual(4, len(circle.keys()))

        circle.attributes.pop('stroke-dasharray')
        self.assertEqual(4, len(circle.keys()))

        style = circle.attributes.get('style')
        expected = 'fill: none;'
        self.assertEqual(expected, style)

        fill = circle.attributes.pop('fill', 'red')
        self.assertEqual('none', fill)

        fill = circle.attributes.pop('fill', 'red')  # remove twice
        self.assertEqual('red', fill)

        style = circle.attributes.get('style')
        self.assertEqual(3, len(circle.keys()))
        self.assertEqual('120', circle.attributes.get('r'))
        self.assertEqual('500', circle.attributes.get('cx'))
        self.assertEqual('800', circle.attributes.get('cy'))
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
        self.assertEqual(expected, style)
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
        self.assertEqual(expected, value)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        circle.attributes.set_ns(None, 'fill', 'white')
        value = circle.attributes.pop_ns(None, 'fill')
        expected = 'white'
        self.assertEqual(expected, value)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        value = circle.attributes.pop_ns(None, 'fill', 'black')
        expected = 'black'
        self.assertEqual(expected, value)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        value = circle.attributes.setdefault_ns(None, 'stroke', 'black')
        expected = 'blue'
        self.assertEqual(expected, value)
        self.assertTrue(circle.attributes.has_ns(None, 'style'))
        self.assertTrue(not circle.attributes.has_ns(None, 'fill'))
        self.assertTrue(circle.attributes.has_ns(None, 'stroke'))

        circle.attributes.update({'stroke': 'white'})
        value = circle.attributes.get_ns(None, 'style')
        expected = 'stroke: white;'
        self.assertEqual(expected, value)
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
        self.assertEqual([], class_list)

    def test_element_class_list02(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        root.class_name = 'Border'
        class_name = root.class_name
        self.assertEqual('Border', class_name)

        class_list = root.class_list
        self.assertEqual(['Border'], class_list)

    def test_element_class_list03(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        root.class_name = 'Border Label'
        class_name = root.class_name
        self.assertEqual('Border Label', class_name)

        class_list = root.class_list
        self.assertEqual(['Border', 'Label'], class_list)

    def test_element_find_by_class_names01(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_CUBIC01))
        root = tree.getroot()

        # not match
        elements = root.get_elements_by_class_name('NotExistClass')
        self.assertEqual(0, len(elements))

        # match
        elements = root.get_elements_by_class_name('Connect')
        self.assertEqual(4, len(elements))
        self.assertTrue(isinstance(elements[0], SVGPolylineElement))
        self.assertTrue(isinstance(elements[1], SVGPolylineElement))
        self.assertTrue(isinstance(elements[2], SVGPolylineElement))
        self.assertTrue(isinstance(elements[3], SVGPolylineElement))

        # match
        elements = root.get_elements_by_class_name('SamplePath')
        self.assertEqual(1, len(elements))
        self.assertTrue(isinstance(elements[0], SVGPathElement))

        # not match
        elements = root.get_elements_by_class_name('Connect SamplePath')
        self.assertEqual(0, len(elements))

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
        self.assertEqual(3, len(elements))
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
        self.assertEqual(0, len(elements))

        # tag '{http://www.w3.org/2000/svg}path' -> found
        name = '{{{}}}{}'.format(Element.SVG_NAMESPACE_URI, 'path')
        elements = root.findall(name)
        self.assertEqual(3, len(elements))

        # local-name 'path' -> found
        elements = root.get_elements_by_local_name('path')
        self.assertEqual(3, len(elements))

        elements = root.get_elements_by_local_name(
            'path',
            namespaces={'svg': Element.SVG_NAMESPACE_URI})
        self.assertEqual(3, len(elements))

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
        self.assertEqual('path', element.local_name)

    def test_element_find_by_tag_name(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        parent = root.get_element_by_id('gtop')
        root.attributes.set_ns(Element.XHTML_NAMESPACE_URI,
                               'html',
                               Element.XHTML_NAMESPACE_URI)
        video = parent.make_sub_element_ns(Element.XHTML_NAMESPACE_URI,
                                           'video')
        source = video.make_sub_element_ns(Element.XHTML_NAMESPACE_URI,
                                           'source')

        # <g>(id=svgstar), <path>(id=svgbar),
        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        # <html:video>, <html:source>
        tag = '*'
        elements = parent.get_elements_by_tag_name(tag)
        self.assertEqual(7, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('g'))
        self.assertEqual(1, tags.count('path'))
        self.assertEqual(3, tags.count('use'))
        self.assertEqual(1, tags.count('html:video'))
        self.assertEqual(1, tags.count('html:source'))

        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        tag = 'use'
        elements = parent.get_elements_by_tag_name(tag)
        self.assertEqual(3, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(3, tags.count('use'))

        # (not found)
        tag = 'video'
        elements = parent.get_elements_by_tag_name(tag)
        self.assertEqual(0, len(elements))

        # <html:video>
        tag = 'html:video'
        elements = parent.get_elements_by_tag_name(tag)
        self.assertEqual(1, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('html:video'))

    def test_element_find_by_tag_name_ns(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_SVG))
        root = tree.getroot()

        parent = root.get_element_by_id('gtop')
        root.attributes.set_ns(Element.XHTML_NAMESPACE_URI,
                               'html',
                               Element.XHTML_NAMESPACE_URI)
        video = parent.make_sub_element_ns(Element.XHTML_NAMESPACE_URI,
                                           'video')
        source = video.make_sub_element_ns(Element.XHTML_NAMESPACE_URI,
                                           'source')

        # <g>(id=svgstar), <path>(id=svgbar),
        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        # <html:video>, <html:source>
        namespace = None
        local_name = '*'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(7, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('g'))
        self.assertEqual(1, tags.count('path'))
        self.assertEqual(3, tags.count('use'))
        self.assertEqual(1, tags.count('html:video'))
        self.assertEqual(1, tags.count('html:source'))

        # <g>(id=svgstar), <path>(id=svgbar),
        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        # <html:video>, <html:source>
        namespace = '*'
        local_name = '*'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(7, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('g'))
        self.assertEqual(1, tags.count('path'))
        self.assertEqual(3, tags.count('use'))
        self.assertEqual(1, tags.count('html:video'))
        self.assertEqual(1, tags.count('html:source'))

        # <g>(id=svgstar), <path>(id=svgbar),
        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        namespace = Element.SVG_NAMESPACE_URI
        local_name = '*'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(5, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('g'))
        self.assertEqual(1, tags.count('path'))
        self.assertEqual(3, tags.count('use'))

        # <html:video>, <html:source>
        namespace = Element.XHTML_NAMESPACE_URI
        local_name = '*'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(2, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('html:video'))
        self.assertEqual(1, tags.count('html:source'))

        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        namespace = '*'
        local_name = 'use'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(3, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(3, tags.count('use'))

        # <html:source>
        namespace = '*'
        local_name = 'source'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(1, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('html:source'))

        # <use>(id=use1), <use>(id=use2), <use>(id=use3)
        namespace = Element.SVG_NAMESPACE_URI
        local_name = 'use'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(3, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(3, tags.count('use'))

        # <html:video>
        namespace = Element.XHTML_NAMESPACE_URI
        local_name = 'video'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(1, len(elements))
        tags = [x.tag_name for x in elements]
        self.assertEqual(1, tags.count('html:video'))

        # (not found)
        namespace = Element.XHTML_NAMESPACE_URI
        local_name = 'use'
        elements = parent.get_elements_by_tag_name_ns(namespace, local_name)
        self.assertEqual(0, len(elements))

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
        self.assertTrue(display)

        display = group.isdisplay()  # inline > none
        self.assertTrue(not display)

        display = text.isdisplay()  # inline > none > none
        self.assertTrue(not display)

    def test_element_iter(self):
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ROTATE_SCALE))
        root = tree.getroot()

        for element in root:
            if element.node_type == Node.COMMENT_NODE:
                self.assertIsInstance(element, Comment)
                self.assertEqual('#comment', element.node_name)
                self.assertIsNotNone(element.data)
            else:
                self.assertEqual(Node.ELEMENT_NODE, element.node_type)

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
        self.assertEqual(expected, root.tostring().decode())

    def test_element_make_sub_element_html(self):
        parser = SVGParser()
        nsmap = {
            None: Element.SVG_NAMESPACE_URI,
            'html': Element.XHTML_NAMESPACE_URI
        }
        root = parser.make_element('svg', nsmap=nsmap)
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual('svg', root.tag_name)
        self.assertEqual('svg', root.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', root.namespace_uri)

        video = root.make_sub_element('video')
        self.assertTrue(isinstance(video, HTMLVideoElement))
        self.assertEqual('video', video.tag_name)
        self.assertEqual('video', video.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', video.namespace_uri)

        tag = '{{{}}}{}'.format(Element.XHTML_NAMESPACE_URI, 'audio')
        audio = root.make_sub_element(tag)
        self.assertTrue(isinstance(audio, HTMLAudioElement))
        self.assertEqual(tag, audio.tag)
        self.assertEqual('html:audio', audio.tag_name)
        self.assertEqual('audio', audio.local_name)
        self.assertEqual('http://www.w3.org/1999/xhtml', audio.namespace_uri)

        tag = '{{{}}}{}'.format(Element.XHTML_NAMESPACE_URI, 'source')
        source = audio.make_sub_element_ns(Element.XHTML_NAMESPACE_URI,
                                           'source')
        self.assertTrue(isinstance(source, HTMLElement))
        self.assertEqual(tag, source.tag)
        self.assertEqual('html:source', source.tag_name)
        self.assertEqual('source', source.local_name)
        self.assertEqual('http://www.w3.org/1999/xhtml', source.namespace_uri)

    def test_element_make_sub_element_svg01(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual('svg', root.tag)
        self.assertEqual('svg', root.tag_name)
        self.assertEqual('svg', root.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', root.namespace_uri)

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
        self.assertEqual(expected, root.tostring().decode())

    def test_element_make_sub_element_svg02(self):
        parser = SVGParser()
        root = parser.make_element_ns('http://www.w3.org/2000/svg', 'svg')
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual('{http://www.w3.org/2000/svg}svg', root.tag)
        self.assertEqual('svg', root.tag_name)
        self.assertEqual('svg', root.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', root.namespace_uri)

        g = root.make_sub_element('g')
        self.assertTrue(isinstance(g, SVGGElement))
        self.assertEqual('g', g.tag)
        self.assertEqual('g', g.tag_name)
        self.assertEqual('g', g.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', g.namespace_uri)

        path = g.make_sub_element_ns('http://www.w3.org/2000/svg', 'path')
        self.assertTrue(isinstance(path, SVGPathElement))
        self.assertEqual('{http://www.w3.org/2000/svg}path', path.tag)
        self.assertEqual('path', path.tag_name)
        self.assertEqual('path', path.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', path.namespace_uri)

        rect = g.make_sub_element_ns(None, 'rect', index=0)
        self.assertTrue(isinstance(rect, SVGRectElement))
        self.assertEqual('rect', rect.tag)
        self.assertEqual('rect', rect.tag_name)
        self.assertEqual('rect', rect.local_name)
        self.assertEqual('http://www.w3.org/2000/svg', rect.namespace_uri)

    def test_ellipse01_length(self):
        # ellipse: initial value
        parser = SVGParser()
        ellipse = parser.make_element('ellipse')

        path_data = ellipse.get_path_data()
        self.assertEqual(0, len(path_data))

        n = ellipse.get_total_length()
        self.assertEqual(0, n)

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
        self.assertEqual(0, len(path_data))

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = ellipse.get_path_data(settings)
        self.assertEqual(0, len(path_data))

        n = ellipse.get_total_length()
        self.assertEqual(0, n)

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
        self.assertEqual(0, len(path_data))

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = ellipse.get_path_data(settings)
        self.assertEqual(0, len(path_data))

        n = ellipse.get_total_length()
        self.assertEqual(0, n)

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
        self.assertEqual(6, len(path_data))
        self.assertEqual(expected, d, msg=d)

        n = ellipse.get_total_length()
        expected = 2 * math.pi * 100
        self.assertAlmostEqual(expected, n)

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
        self.assertEqual(expected, d, msg=d)

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
        self.assertEqual(6, len(path_data))
        self.assertEqual(expected, d, msg=d)

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
        self.assertEqual(expected, d, msg=d)

        n = ellipse.get_total_length()
        # expected = 1150.816162109375  # firefox
        expected = 1150.81787109375
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(6, len(path_data))
        self.assertEqual(expected, d, msg=d)

        n = ellipse.get_total_length()
        # expected = 1150.8154296875  # firefox
        expected = 1150.818115234375
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(0, style['cx'])
        self.assertEqual(0, style['cy'])
        self.assertEqual(250, style['rx'])
        self.assertEqual(100, style['ry'])

        path_data = ellipse.get_path_data()
        d = PathParser.tostring(path_data)
        expected = "M250,0" \
                   " A250,100 0 0 1 0,100" \
                   " 250,100 0 0 1 -250,0" \
                   " 250,100 0 0 1 0,-100" \
                   " 250,100 0 0 1 250,0 Z"
        self.assertEqual(expected, d, msg=d)

        n = ellipse.get_total_length()
        # expected = 1150.816162109375  # firefox
        expected = 1150.81787109375
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(200 - 100, bbox.x)
        self.assertEqual(300 - 200, bbox.y)
        self.assertEqual(100 * 2, bbox.width)
        self.assertEqual(200 * 2, bbox.height)

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
        self.assertEqual(expected, exp)

        # no viewBox
        # transform="translate(50,30)"
        # transform="rotate(30)"
        g = root.get_element_by_id('g12')
        matrix = g.get_ctm()
        exp = matrix.tostring()
        expected = 'matrix(0.866 0.5 -0.5 0.866 50 30)'
        self.assertEqual(expected, exp)

    def test_line01_length(self):
        parser = SVGParser()
        line = parser.make_element('line')

        path_data = line.get_path_data()
        self.assertEqual(0, len(path_data))

        settings = SVGPathDataSettings()
        settings.normalize = True
        path_data = line.get_path_data(settings)
        self.assertEqual(0, len(path_data))

        n = line.get_total_length()
        self.assertEqual(0, n)

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
        self.assertEqual(2, len(path_data))

        d = PathParser.tostring(path_data)
        expected = 'M0,0 L100,0'
        self.assertEqual(expected, d)

        n = line.get_total_length()
        expected = 100
        self.assertEqual(expected, n)

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
        self.assertEqual(2, len(path_data))

        d = PathParser.tostring(path_data)
        expected = 'M0,100 L0,-100'
        self.assertEqual(expected, d)

        n = line.get_total_length()
        expected = 200
        self.assertEqual(expected, n)

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
        self.assertEqual(2, len(path_data))

        d = PathParser.tostring(path_data)
        expected = 'M-100,-100 L100,100'
        self.assertEqual(expected, d)

        n = line.get_total_length()
        expected = math.sqrt((100 - -100) ** 2 + (100 - -100) ** 2)
        self.assertEqual(expected, n)

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
        self.assertEqual(2, len(path_data))

        d = PathParser.tostring(path_data)
        expected = 'M100,200 L-100,-200'
        self.assertEqual(expected, d)

        n = line.get_total_length()
        expected = math.sqrt((-100 - 100) ** 2 + (-200 - 200) ** 2)
        self.assertEqual(expected, n)

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
        self.assertEqual(100, bbox.x)
        self.assertEqual(200, bbox.y)
        self.assertEqual(300 - 100, bbox.width)
        self.assertEqual(400 - 200, bbox.height)

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
        self.assertEqual(20, len(root))
        self.assertEqual('svg', root.local_name)
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual('title', root[0].local_name)
        self.assertEqual('desc', root[1].local_name)
        self.assertEqual('style', root[2].local_name)
        self.assertEqual('rect', root[3].local_name)
        self.assertTrue(isinstance(root[3], SVGRectElement))
        self.assertEqual('polyline', root[4].local_name)
        self.assertTrue(isinstance(root[4], SVGPolylineElement))
        self.assertEqual('polyline', root[5].local_name)
        self.assertTrue(isinstance(root[5], SVGPolylineElement))
        self.assertEqual('polyline', root[6].local_name)
        self.assertTrue(isinstance(root[6], SVGPolylineElement))
        self.assertEqual('polyline', root[7].local_name)
        self.assertTrue(isinstance(root[7], SVGPolylineElement))
        self.assertEqual('path', root[8].local_name)
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
        self.assertEqual(20, len(root))
        self.assertEqual('svg', root.local_name)
        self.assertTrue(isinstance(root, SVGSVGElement))
        self.assertEqual('title', root[0].local_name)
        self.assertEqual('desc', root[1].local_name)
        self.assertEqual('style', root[2].local_name)
        self.assertEqual('rect', root[3].local_name)
        self.assertTrue(isinstance(root[3], SVGRectElement))
        self.assertEqual('polyline', root[4].local_name)
        self.assertTrue(isinstance(root[4], SVGPolylineElement))
        self.assertEqual('polyline', root[5].local_name)
        self.assertTrue(isinstance(root[5], SVGPolylineElement))
        self.assertEqual('polyline', root[6].local_name)
        self.assertTrue(isinstance(root[6], SVGPolylineElement))
        self.assertEqual('polyline', root[7].local_name)
        self.assertTrue(isinstance(root[7], SVGPolylineElement))
        self.assertEqual('path', root[8].local_name)
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

    # @unittest.expectedFailure
    def test_path01_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path01')
        # [0.378 0 0 0.378 151.181 0]
        ctm = path.get_ctm()
        # exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 151.17708333333331,
        #  0.0009765624999955354]
        # expected = 'matrix(0.378 0 0 0.378 151.177 0)'
        # self.assertEqual(expected, exp, msg=ctm)
        a, b, c, d, e, f = [0.3779427083333333, 0, 0, 0.3779427083333333,
                            151.17708333333331, 0.0009765624999955354]
        self.assertAlmostEqual(a, ctm.a, places=places)
        self.assertAlmostEqual(b, ctm.b, places=places)
        self.assertAlmostEqual(c, ctm.c, places=places)
        self.assertAlmostEqual(d, ctm.d, places=places)
        self.assertAlmostEqual(e, ctm.e, places=places)
        self.assertAlmostEqual(f, ctm.f, places=places)

    # @unittest.expectedFailure
    def test_path02_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path02')
        # [0.378 0 0 0.378 302.362 0]
        ctm = path.get_ctm()
        # exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 302.35416666666663,
        #  0.0009765624999955354]
        # expected = 'matrix(0.378 0 0 0.378 302.354 0)'
        # self.assertEqual(expected, exp, msg=ctm)
        a, b, c, d, e, f = [0.3779427083333333, 0, 0, 0.3779427083333333,
                            302.35416666666663, 0.0009765624999955354]
        self.assertAlmostEqual(a, ctm.a, places=places)
        self.assertAlmostEqual(b, ctm.b, places=places)
        self.assertAlmostEqual(c, ctm.c, places=places)
        self.assertAlmostEqual(d, ctm.d, places=places)
        self.assertAlmostEqual(e, ctm.e, places=places)
        self.assertAlmostEqual(f, ctm.f, places=places)

    # @unittest.expectedFailure
    def test_path03_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path03')
        # [0.378 0 0 0.378 151.181 94.488]
        ctm = path.get_ctm()
        # exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 151.17708333333331,
        #  94.48665364583333]
        # expected = 'matrix(0.378 0 0 0.378 151.177 94.487)'
        # self.assertEqual(expected, exp, msg=ctm)
        a, b, c, d, e, f = [0.3779427083333333, 0, 0, 0.3779427083333333,
                            151.17708333333331, 94.48665364583333]
        self.assertAlmostEqual(a, ctm.a, places=places)
        self.assertAlmostEqual(b, ctm.b, places=places)
        self.assertAlmostEqual(c, ctm.c, places=places)
        self.assertAlmostEqual(d, ctm.d, places=places)
        self.assertAlmostEqual(e, ctm.e, places=places)
        self.assertAlmostEqual(f, ctm.f, places=places)

    # @unittest.expectedFailure
    def test_path04_ctm(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path04')
        # [0.378 0 0 0.378 302.362 94.488]
        ctm = path.get_ctm()
        # exp = ctm.tostring()
        # [0.3779427083333333, 0, 0, 0.3779427083333333, 302.35416666666663,
        #  94.48665364583333]
        # expected = 'matrix(0.378 0 0 0.378 302.354 94.487)'
        # self.assertEqual(expected, exp, msg=ctm)
        a, b, c, d, e, f = [0.3779427083333333, 0, 0, 0.3779427083333333,
                            302.35416666666663, 94.48665364583333]
        self.assertAlmostEqual(a, ctm.a, places=places)
        self.assertAlmostEqual(b, ctm.b, places=places)
        self.assertAlmostEqual(c, ctm.c, places=places)
        self.assertAlmostEqual(d, ctm.d, places=places)
        self.assertAlmostEqual(e, ctm.e, places=places)
        self.assertAlmostEqual(f, ctm.f, places=places)

    def test_path01_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path01')
        n = path.get_total_length()
        expected = 121.12298583984375
        self.assertAlmostEqual(expected, n, delta=delta)

    def test_path02_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path02')
        n = path.get_total_length()
        expected = 121.12297821044922
        self.assertAlmostEqual(expected, n, delta=delta)

    def test_path03_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path03')
        n = path.get_total_length()
        expected = 363.36895751953125
        self.assertAlmostEqual(expected, n, delta=delta)

    def test_path04_length(self):
        # See also: arcs02.html
        parser = SVGParser()
        tree = parser.parse(StringIO(SVG_ARCS02))
        root = tree.getroot()

        path = root.get_element_by_id('path04')
        n = path.get_total_length()
        expected = 363.3689880371094
        self.assertAlmostEqual(expected, n, delta=delta)

    def test_polygon01_bbox(self):
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        polygon.attributes.update({
            'points': "350,75 379,161 469,161 397,215 423,301 350,250" 
                      " 277,301 303,215 231,161 321,161",
        })

        bbox = polygon.get_bbox()
        self.assertEqual(231, bbox.x)
        self.assertEqual(75, bbox.y)
        self.assertEqual(469 - 231, bbox.width)
        self.assertEqual(301 - 75, bbox.height)

    def test_polygon02_length(self):
        # See also: polygon01.html
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        points = \
            "350,75 379,161 469,161 397,215 423,301 350,250" \
            " 277,301 303,215 231,161 321,161"
        polygon.attributes.set('points', points)
        pts = polygon.points
        self.assertEqual(10, len(pts))
        self.assertEqual((350, 75), pts[0])
        self.assertEqual((379, 161), pts[1])
        self.assertEqual((469, 161), pts[2])
        self.assertEqual((397, 215), pts[3])
        self.assertEqual((423, 301), pts[4])
        self.assertEqual((350, 250), pts[5])
        self.assertEqual((277, 301), pts[6])
        self.assertEqual((303, 215), pts[7])
        self.assertEqual((231, 161), pts[8])
        self.assertEqual((321, 161), pts[9])

        path_data = polygon.get_path_data()
        self.assertEqual(11, len(path_data))
        self.assertEqual('M', path_data[0].type)
        self.assertEqual('L', path_data[1].type)
        self.assertEqual('L', path_data[2].type)
        self.assertEqual('L', path_data[3].type)
        self.assertEqual('L', path_data[4].type)
        self.assertEqual('L', path_data[5].type)
        self.assertEqual('L', path_data[6].type)
        self.assertEqual('L', path_data[7].type)
        self.assertEqual('L', path_data[8].type)
        self.assertEqual('L', path_data[9].type)
        self.assertEqual('Z', path_data[10].type)
        self.assertEqual((350, 75), path_data[0].values)
        self.assertEqual((379, 161), path_data[1].values)
        self.assertEqual((469, 161), path_data[2].values)
        self.assertEqual((397, 215), path_data[3].values)
        self.assertEqual((423, 301), path_data[4].values)
        self.assertEqual((350, 250), path_data[5].values)
        self.assertEqual((277, 301), path_data[6].values)
        self.assertEqual((303, 215), path_data[7].values)
        self.assertEqual((231, 161), path_data[8].values)
        self.assertEqual((321, 161), path_data[9].values)
        self.assertEqual((), path_data[10].values)

        n = polygon.get_total_length()
        expected = 899.3055419921875
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(expected, exp)

    def test_polygon03_length(self):
        # See also: polygon01.html
        parser = SVGParser()
        polygon = parser.make_element('polygon')
        points = \
            "850,75 958,137.5 958,262.5" \
            " 850,325 742,262.6 742,137.5"
        polygon.attributes.set('points', points)
        pts = polygon.points
        self.assertEqual(6, len(pts))
        self.assertEqual((850, 75), pts[0])
        self.assertEqual((958, 137.5), pts[1])
        self.assertEqual((958, 262.5), pts[2])
        self.assertEqual((850, 325), pts[3])
        self.assertEqual((742, 262.6), pts[4])
        self.assertEqual((742, 137.5), pts[5])

        path_data = polygon.get_path_data()
        self.assertEqual(7, len(path_data))
        self.assertEqual('M', path_data[0].type)
        self.assertEqual('L', path_data[1].type)
        self.assertEqual('L', path_data[2].type)
        self.assertEqual('L', path_data[3].type)
        self.assertEqual('L', path_data[4].type)
        self.assertEqual('L', path_data[5].type)
        self.assertEqual('Z', path_data[6].type)
        self.assertEqual((850, 75), path_data[0].values)
        self.assertEqual((958, 137.5), path_data[1].values)
        self.assertEqual((958, 262.5), path_data[2].values)
        self.assertEqual((850, 325), path_data[3].values)
        self.assertEqual((742, 262.6), path_data[4].values)
        self.assertEqual((742, 137.5), path_data[5].values)
        self.assertEqual((), path_data[6].values)

        d = PathParser.tostring(path_data)
        expected = \
            "M850,75 L958,137.5 958,262.5 850,325 742,262.6 742,137.5 Z"
        self.assertEqual(expected, d)

        n = polygon.get_total_length()
        expected = 749.1731567382812
        self.assertAlmostEqual(expected, n, places=places)

    def test_polyline01_length(self):
        parser = SVGParser()
        polyline = parser.make_element('polyline')

        style = polyline.get_computed_geometry()
        points = style['points']
        self.assertEqual(0, len(points))

        n = polyline.get_total_length()
        expected = 0
        self.assertEqual(expected, n)

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
        self.assertEqual(22, len(points))
        self.assertEqual((50, 375), points[0])
        self.assertEqual((150, 375), points[1])
        self.assertEqual((150, 325), points[2])
        # ...
        self.assertEqual((1050, 25), points[19])
        self.assertEqual((1050, 375), points[20])
        self.assertEqual((1150, 375), points[21])

        path_data = polyline.get_path_data()
        self.assertEqual(22, len(path_data))
        self.assertEqual('M', path_data[0].type)
        self.assertEqual('L', path_data[1].type)
        # ...
        self.assertEqual('L', path_data[21].type)

        n = polyline.get_total_length()
        expected = 3100
        self.assertEqual(expected, n)

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
        self.assertEqual(expected, exp)

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
        self.assertAlmostEqual(expected, n, places=places)

    def test_polyline04_bbox(self):
        parser = SVGParser()
        polyline = parser.make_element('polyline')
        polyline.attributes.update({
            'points': "350,75 379,161 469,161 397,215 423,301 350,250" 
                      " 277,301 303,215 231,161 321,161",
        })

        bbox = polyline.get_bbox()
        self.assertEqual(231, bbox.x)
        self.assertEqual(75, bbox.y)
        self.assertEqual(469 - 231, bbox.width)
        self.assertEqual(301 - 75, bbox.height)

    def test_preserve_aspect_ratio01(self):
        par = SVGPreserveAspectRatio()  # -> xMidYMid meet
        self.assertEqual('xMidYMid', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMidYMid meet', par.tostring())

    def test_preserve_aspect_ratio02(self):
        par = SVGPreserveAspectRatio('slice')  # -> xMidYMid meet
        self.assertEqual('xMidYMid', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMidYMid meet', par.tostring())

    def test_preserve_aspect_ratio03(self):
        par = SVGPreserveAspectRatio('xMidYMin')  # -> xMidYMin meet
        self.assertEqual('xMidYMin', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMidYMin meet', par.tostring())

    def test_preserve_aspect_ratio04(self):
        par = SVGPreserveAspectRatio('xMaxYMin slice')
        self.assertEqual('xMaxYMin', par.align)
        self.assertEqual('slice', par.meet_or_slice)
        self.assertEqual('xMaxYMin slice', par.tostring())

    def test_preserve_aspect_ratio05(self):
        par = SVGPreserveAspectRatio('XMinYMid slice')
        self.assertEqual('XMinYMid', par.align)
        self.assertEqual('slice', par.meet_or_slice)
        self.assertEqual('XMinYMid slice', par.tostring())

    def test_preserve_aspect_ratio06(self):
        par = SVGPreserveAspectRatio('xMidYMid')  # -> xMidYMid meet
        self.assertEqual('xMidYMid', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMidYMid meet', par.tostring())

    def test_preserve_aspect_ratio07(self):
        par = SVGPreserveAspectRatio('xMaxYMid')  # -> xMaxYMid meet
        self.assertEqual('xMaxYMid', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMaxYMid meet', par.tostring())

    def test_preserve_aspect_ratio08(self):
        par = SVGPreserveAspectRatio('xMinYMax slice')
        self.assertEqual('xMinYMax', par.align)
        self.assertEqual('slice', par.meet_or_slice)
        self.assertEqual('xMinYMax slice', par.tostring())

    def test_preserve_aspect_ratio09(self):
        par = SVGPreserveAspectRatio('xMidYMax meet')
        self.assertEqual('xMidYMax', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMidYMax meet', par.tostring())

    def test_preserve_aspect_ratio10(self):
        par = SVGPreserveAspectRatio('xMaxYMax meet')
        self.assertEqual('xMaxYMax', par.align)
        self.assertEqual('meet', par.meet_or_slice)
        self.assertEqual('xMaxYMax meet', par.tostring())

    def test_preserve_aspect_ratio11(self):
        par = SVGPreserveAspectRatio('none')
        self.assertEqual('none', par.align)
        self.assertIsNone(par.meet_or_slice)
        self.assertEqual('none', par.tostring())

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
        self.assertEqual(0, bbox.x)
        self.assertEqual(0, bbox.y)
        self.assertEqual(400, bbox.width)
        self.assertEqual(200, bbox.height)

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
        self.assertEqual(0.5, bbox.x)
        self.assertEqual(0.5, bbox.y)
        self.assertEqual(29, bbox.width)
        self.assertEqual(39, bbox.height)

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
        self.assertEqual(0, len(path_data))

        settings = SVGPathDataSettings()
        settings.normalize = True
        normalized = rect.get_path_data(settings)
        self.assertEqual(0, len(normalized))

        n = rect.get_total_length()
        self.assertEqual(0, n)

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
        self.assertEqual(6, len(path_data))
        d = PathParser.tostring(path_data)
        expected = "M20,10 H120 V130 H20 V10 Z"
        self.assertEqual(expected, d)

        n = rect.get_total_length()
        # (100 + 120) * 2 = 440
        self.assertEqual(440, n)

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
        self.assertEqual(expected, exp)

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
        self.assertEqual(10, len(path_data))
        d = PathParser.tostring(path_data)
        expected = \
            "M150,100" \
            " H450 A50,50 0 0 1 500,150" \
            " V250 A50,50 0 0 1 450,300" \
            " H150 A50,50 0 0 1 100,250" \
            " V150 A50,50 0 0 1 150,100 Z"
        self.assertEqual(expected, d)

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625  # chrome
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(expected, exp)

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
        self.assertEqual(10, len(path_data))
        d = PathParser.tostring(path_data)
        expected = \
            "M50,0 H350 A50,25 0 0 1 400,25" \
            " V175 A50,25 0 0 1 350,200" \
            " H50 A50,25 0 0 1 0,175" \
            " V25 A50,25 0 0 1 50,0 Z"
        self.assertEqual(expected, d)

        n = rect.get_total_length()
        # expected = 1142.2462158203125  # firefox
        expected = 1142.2459716796875  # chrome
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(expected, exp)

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
        self.assertEqual(6, len(path_data))
        d = PathParser.tostring(path_data)
        expected = 'M150,150 H550 V350 H150 V150 Z'
        self.assertEqual(expected, d)

        n = rect.get_total_length()
        # (400 + 200) * 2 = 1200
        expected = 1200
        self.assertEqual(expected, n)

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
        self.assertEqual(10, len(path_data))
        d = PathParser.tostring(path_data)
        expected = \
            "M200,150" \
            " H500 A50,50 0 0 1 550,200" \
            " V300 A50,50 0 0 1 500,350" \
            " H200 A50,50 0 0 1 150,300" \
            " V200 A50,50 0 0 1 200,150 Z"
        self.assertEqual(expected, d)

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625  # chrome
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertEqual(10, len(path_data))
        d = PathParser.tostring(path_data)
        expected = \
            "M200,150" \
            " H500 A50,50 0 0 1 550,200" \
            " V300 A50,50 0 0 1 500,350" \
            " H200 A50,50 0 0 1 150,300" \
            " V200 A50,50 0 0 1 200,150 Z"
        self.assertEqual(expected, d)

        n = rect.get_total_length()
        # (400 - 50 * 2) * 2 + (200 - 50 * 2) * 2 + 2 * pi * 50
        # -> 1114.1592653589794
        expected = 1114.2037353515625  # chrome
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertAlmostEqual(expected, n, places=places)

        path_data = rect.get_path_data()
        self.assertEqual(10, len(path_data))
        d = PathParser.tostring(path_data)
        expected = \
            "M200,150" \
            " H500 A50,50 0 0 1 550,200" \
            " V300 A50,50 0 0 1 500,350" \
            " H200 A50,50 0 0 1 150,300" \
            " V200 A50,50 0 0 1 200,150 Z"
        self.assertEqual(expected, d)

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
        self.assertAlmostEqual(expected, n, places=places)

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
        self.assertAlmostEqual(expected, style['width'])

        expected = 400 * 0.5
        self.assertAlmostEqual(expected, style['height'])

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
        self.assertEqual(expected, scale)

        root.current_scale = 1.5
        scale = root.current_scale
        expected = 1.5
        self.assertEqual(expected, scale)

        # child svg element
        scale = child.current_scale
        expected = 1
        self.assertEqual(expected, scale)

        child.current_scale = 1.5
        scale = child.current_scale
        expected = 1
        self.assertEqual(expected, scale)

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
        self.assertEqual(expected, translate)

        root.current_translate = 100, -100
        translate = root.current_translate
        expected = 100, -100
        self.assertEqual(expected, translate)

        # child svg element
        translate = child.current_translate
        expected = 0, 0
        self.assertEqual(expected, translate)

        child.current_translate = 100, -100
        translate = child.current_translate
        expected = 0, 0
        self.assertEqual(expected, translate)

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
        self.assertEqual(expected, m)

        # id="svg01"
        element = root.get_element_by_id('svg01')
        view_box = element.get_view_box()
        par = SVGPreserveAspectRatio('none')
        expected = \
            SVGLength(0), SVGLength(0), SVGLength(1500), SVGLength(1000), par
        self.assertEqual(expected, view_box)

        # CTM = [0.2, 0, 0, 0.2, 0, 0]
        m = element.get_ctm()
        expected = Matrix(0.2, 0, 0, 0.2, 0, 0)
        self.assertEqual(expected, m)

        # id="rect01"
        element = root.get_element_by_id('rect01')

        # CTM = [0.2, 0, 0, 0.2, 0, 0]
        m = element.get_ctm()
        expected = Matrix(0.2, 0, 0, 0.2, 0, 0)
        self.assertEqual(expected, m)

        # id="svg02"
        element = root.get_element_by_id('svg02')
        view_box = element.get_view_box()
        par = SVGPreserveAspectRatio('none')
        expected = \
            SVGLength(0), SVGLength(0), SVGLength(1500), SVGLength(1000), par
        self.assertEqual(expected, view_box)

        # CTM = [0.1, 0, 0, 0.2, 300, 0]
        m = element.get_ctm()
        expected = Matrix(0.1, 0, 0, 0.2, 300, 0)
        self.assertEqual(expected, m)

        # id="rect02"
        element = root.get_element_by_id('rect02')

        # CTM = [0.1, 0, 0, 0.2, 300, 0]
        m = element.get_ctm()
        expected = Matrix(0.1, 0, 0, 0.2, 300, 0)
        self.assertEqual(expected, m)

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
        self.assertEqual(SVGZoomAndPan.ZOOMANDPAN_MAGNIFY, zap)

        # CTM: [1, 0, 0, 1, 0, 0] ->
        # [1.2, 0, 0, 1.2, 100, 50] * [1, 0, 0, 1, 50, 25]
        # = [1.2, 0, 0, 1.2, 160, 80]
        m = element.get_ctm()
        expected = Matrix(1.2, 0, 0, 1.2, 160, 80)
        self.assertEqual(expected, m)

        element.attributes.update({
            'zoomAndPan': 'disable',
        })

        # CTM: [1, 0, 0, 1, 0, 0] -> [1, 0, 0, 1, 50, 25]
        m = element.get_ctm()
        expected = Matrix(1, 0, 0, 1, 50, 25)
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, (vpx, vpy, vpw, vph))

        vbx, vby, vbw, vbh, par = element.get_view_box()
        expected = SVGLength(0), SVGLength(0), SVGLength(30), SVGLength(40)
        self.assertEqual(expected, (vbx, vby, vbw, vbh))
        self.assertEqual('xMinYMin', par.align)
        self.assertEqual('meet', par.meet_or_slice)

        # CTM = [0.75, 0, 0, 0.75, 0, 0]
        m = element.get_ctm()
        expected = Matrix(0.75, 0, 0, 0.75, 0, 0)
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual(expected, m)

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
        self.assertEqual('0', vpx.tostring())
        self.assertEqual('0', vpy.tostring())
        self.assertEqual('10cm', vpw.tostring())
        self.assertEqual('4cm', vph.tostring())

        style = root.get_computed_geometry()
        self.assertAlmostEqual(0, style['x'])
        self.assertAlmostEqual(0, style['y'])
        # width = 10(cm) = 10 / 2.54 * 96
        self.assertAlmostEqual(377.952756, style['width'], delta=delta)
        # height = 4(cm) = 4 / 2.54 * 96
        self.assertAlmostEqual(151.181102, style['height'], delta=delta)

        vpx, vpy, vpw, vph = svg02.get_viewport_size()
        self.assertEqual('1cm', vpx.tostring())
        self.assertEqual('1cm', vpy.tostring())
        self.assertEqual('10cm', vpw.tostring())
        self.assertEqual('4cm', vph.tostring())

        style = svg02.get_computed_geometry()
        # x = 1(cm) = 1 / 2.54 * 96
        self.assertAlmostEqual(37.795276, style['x'], delta=delta)
        # y = 1(cm) = 1 / 2.54 * 96
        self.assertAlmostEqual(37.795276, style['y'], delta=delta)
        self.assertAlmostEqual(377.952756, style['width'], delta=delta)
        self.assertAlmostEqual(151.181102, style['height'], delta=delta)

        vpx, vpy, vpw, vph = svg03.get_viewport_size()
        self.assertEqual('40', vpx.tostring())
        self.assertEqual('40', vpy.tostring())
        self.assertEqual('80', vpw.tostring())
        self.assertEqual('80', vph.tostring())

        style = svg03.get_computed_geometry()
        self.assertAlmostEqual(40, style['x'], delta=delta)
        self.assertAlmostEqual(40, style['y'], delta=delta)
        self.assertAlmostEqual(80, style['width'], delta=delta)
        self.assertAlmostEqual(80, style['height'], delta=delta)

    def test_viewport03(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'viewBox': '0 50 500 200',
        })

        vpx, vpy, vpw, vph = root.get_viewport_size()
        self.assertEqual(0, vpx.value())
        self.assertEqual(0, vpy.value())
        self.assertEqual(window.inner_width, vpw.value())
        self.assertEqual(window.inner_height, vph.value())

        vbx, vby, vbw, vbh, _ = root.get_view_box()
        self.assertEqual(0, vbx.value())
        self.assertEqual(50, vby.value())
        self.assertEqual(500, vbw.value())
        self.assertEqual(200, vbh.value())


if __name__ == '__main__':
    unittest.main()
