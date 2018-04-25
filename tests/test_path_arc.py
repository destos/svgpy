#!/usr/bin/env python3

import math
import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import Matrix, PathParser, SVGPathSegment, formatter
from svgpy.path import get_angle, Ellipse

places = 0
delta = 1


# Test with: Chrome 64.0 (Linux 64-bit)
class PathArcTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_arcs01_path01_length(self):
        # See also: arcs01.html
        d = 'M300,200 h-150 a150,150 0 1,0 150,-150 z'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 1006.957763671875  # firefox
        expected = 1006.9581298828125
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs01_path02_length(self):
        # See also: arcs01.html
        d = 'M275,175 v-150 a150,150 0 0,0 -150,150 z'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 535.6527099609375  # firefox
        expected = 535.652587890625
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs01_path03_length(self):
        # See also: arcs01.html
        d = "M600,350 l 50,-25 " \
            "a25,25  -30 0,1 50,-25 l 50,-25 " \
            "a25,50  -30 0,1 50,-25 l 50,-25 " \
            "a25,75  -30 0,1 50,-25 l 50,-25 " \
            "a25,100 -30 0,1 50,-25 l 50,-25"
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        expected = 928.3827514648438
        # expected = 928.4309692382812
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs01_path04_length(self):
        # See also: arcs01.html
        d = 'M950,175 a25,100 0 0,1 50,-25'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 216.15928649902344  # firefox
        expected = 215.92034912109375
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs01_path04_normalize(self):
        # See also: arcs01.html
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 1
        d = 'M950,175 a25,100 0 0,1 50,-25'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M950,175" \
            " C946.243,157.787 951.287,97.252 963.733,72.361" \
            " 976.178,47.47 991.312,67.648 1000,150"
        self.assertEqual(exp, expected)

    def test_arcs01_path05_length(self):
        # See also: arcs01.html
        d = 'M950,175 a25,100 -30 0,1 50,-25'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 239.37266540527344  # firefox
        expected = 239.39996337890625
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs01_path05_normalize(self):
        # See also: arcs01.html
        # x_axis_rotation: -30
        # large_arc_flag: 0
        # sweep_flag: 1
        d = 'M950,175 a25,100 -30 0 1 50,-25'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M950,175" \
            " C917.568,116.885 905.572,69.669 920.741,65.176" \
            " 935.909,60.683 972.499,100.614 1000,150"
        self.assertEqual(exp, expected, msg=d)

    # @unittest.expectedFailure
    def test_arcs01_path06_length(self):
        # See also: arcs01.html
        # (cx,cy)=(945.586, 226.768)
        # s=(950, 175)
        # e=(50, -25)
        d = 'M950,175 a25,100 +30 0,1 50,-25'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 71.29801177978516  # firefox
        expected = 71.29816436767578
        self.assertAlmostEqual(n, expected, places=places)

    # @unittest.expectedFailure
    def test_arcs01_path06_normalize(self):
        # See also: arcs01.html
        # center: (945.586, 226.768)
        # start: (950, 175)
        # end: (50, -25)
        # x_axis_rotation: 30
        # large_arc_flag: 0
        # sweep_flag: 1
        d = 'M950,175 a25,100 +30 0,1 50,-25'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M950,175 C988.939,138.516 994.366,138.049 1000,150"
        self.assertEqual(exp, expected)

    def test_arcs01_path06_normalize_negative(self):
        # See also: arcs01.html
        # center: (945.586, 226.768)
        # start: (950, 175)
        # end: (50, -25)
        # x_axis_rotation: 30
        # large_arc_flag: 1
        # sweep_flag: 0
        d = 'M950,175 a25,100 +30 1,0 50,-25'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M950,175" \
            " C961.201,155.808 930.521,197.64 909.893,240.907" \
            " 889.265,284.175 885.058,315.52 900.052,314.23" \
            " 915.046,312.941 944.611,279.415 969.213,235.806" \
            " 993.814,192.196 1005.855,151.968 1000,150"
        self.assertEqual(exp, expected)

    def test_arcs02_path01_bearing(self):
        # See also: arcs02.html
        # same as 'transform="rotate(90 125 75)"'
        d = 'M 125,75 B90 a100,50 0 0,0 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M125,75 C97.386,75 75,119.772 75,175'
        self.assertEqual(exp, expected)

    def test_arcs02_path01_length(self):
        # See also: arcs02.html
        d = 'M 125,75 a100,50 0 0,0 100,50'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 121.12281799316406  # firefox
        expected = 121.12298583984375
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs02_path01_normalize(self):
        # See also: arcs02.html
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 0
        d = 'M125,75 a100,50 0 0 0 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M125,75 C125,102.614 169.772,125 225,125'
        self.assertEqual(exp, expected)

    def test_arcs02_path02_bearing(self):
        # See also: arcs02.html
        # same as 'transform="rotate(90 125 75)"'
        d = 'M 125,75 B90 a100,50 0 0,1 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M125,75 C125,130.228 102.614,175 75,175'
        self.assertEqual(exp, expected)

    def test_arcs02_path02_length(self):
        # See also: arcs02.html
        d = 'M 125,75 a100,50 0 0,1 100,50'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 121.12287139892578  # firefox
        expected = 121.12297821044922
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs02_path02_normalize(self):
        # See also: arcs02.html
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 1
        d = 'M 125,75 a100,50 0 0,1 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M125,75 C180.228,75 225,97.386 225,125'
        self.assertEqual(exp, expected)

    def test_arcs02_path03_bearing(self):
        # See also: arcs02.html
        # same as 'transform="rotate(90 125 75)"'
        d = 'M 125,75 B90 a100,50 0 1,0 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M125,75 C125,19.772 102.614,-25 75,-25" \
            " 47.386,-25 25,19.772 25,75 25,130.228 47.386,175 75,175"
        self.assertEqual(exp, expected)

    def test_arcs02_path03_length(self):
        # See also: arcs02.html
        d = 'M 125,75 a100,50 0 1,0 100,50'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 363.3684997558594  # firefox
        expected = 363.36895751953125
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs02_path03_normalize(self):
        # See also: arcs02.html
        # x_axis_rotation: 0
        # large_arc_flag: 1
        # sweep_flag: 0
        d = 'M 125,75 a100,50 0 1,0 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M125,75" \
            " C69.772,75 25,97.386 25,125" \
            " 25,152.614 69.772,175 125,175" \
            " 180.228,175 225,152.614 225,125"
        self.assertEqual(exp, expected)

    def test_arcs02_path04_bearing(self):
        # See also: arcs02.html
        # same as 'transform="rotate(90 125 75)"'
        d = 'M 125,75 B90 a100,50 0 1,1 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M125,75 C152.614,75 175,119.772 175,175" \
            " 175,230.228 152.614,275 125,275 97.386,275 75,230.228 75,175"
        self.assertEqual(exp, expected)

    def test_arcs02_path04_length(self):
        # See also: arcs02.html
        d = 'M 125,75 a100,50 0 1,1 100,50'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 363.3686218261719  # firefox
        expected = 363.3689880371094
        self.assertAlmostEqual(n, expected, places=places)

    def test_arcs02_path04_normalize(self):
        # See also: arcs02.html
        # x_axis_rotation: 0
        # large_arc_flag: 1
        # sweep_flag: 1
        d = 'M 125,75 a100,50 0 1,1 100,50'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M125,75" \
            " C125,47.386 169.772,25 225,25" \
            " 280.228,25 325,47.386 325,75" \
            " 325,102.614 280.228,125 225,125"
        self.assertEqual(exp, expected)

    def test_ellipse01_path21_length(self):
        # See also: ellipse01.html
        # ry > rx
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 1
        path_data = list()
        cx = 0
        cy = 0
        rx = 100
        ry = 250
        ellipse = Ellipse(cx, cy, rx, ry)
        cpx, cpy = ellipse.point(20)
        path_data.append(SVGPathSegment('M', cpx, cpy))
        rotation = 0
        fa = 0
        fs = 1
        epx, epy = ellipse.point(-45)
        path_data.append(
            SVGPathSegment('A', rx, ry, rotation, fa, fs, epx, epy))
        # d = PathParser.tostring(path_data)
        # -> "M93.969,-85.505 A100,250 0 0 1 70.711,176.777"

        n = PathParser.get_total_length(path_data)
        # expected = 265.98455810546875  # firefox
        expected = 265.9847106933594
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse01_path21_normalize(self):
        # See also: ellipse01.html
        d = 'M93.969,-85.505 A100,250 0 0 1 70.711,176.777'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M93.969,-85.505" \
            " C96.024,-107.64 104.802,-23.844 97.457,56.022" \
            " 90.111,135.889 67.575,201.684 70.711,176.777"
        self.assertEqual(exp, expected)

    def test_ellipse01_path22_length(self):
        # See also: ellipse01.html
        # ry > rx
        # x_axis_rotation: 0
        # large_arc_flag: 1
        # sweep_flag: 1
        path_data = list()
        cx = 0
        cy = 0
        rx = 100
        ry = 250
        ellipse = Ellipse(cx, cy, rx, ry)
        cpx, cpy = ellipse.point(-60)
        path_data.append(SVGPathSegment('M', cpx, cpy))
        rotation = 0
        fa = 1
        fs = 1
        epx, epy = ellipse.point(30)
        path_data.append(
            SVGPathSegment('A', rx, ry, rotation, fa, fs, epx, epy))
        # d = PathParser.tostring(path_data)
        # -> "M50,216.506 A100,250 0 1 1 86.603,-125"

        n = PathParser.get_total_length(path_data)
        # expected = 799.613037109375  # firefox
        expected = 799.7357177734375
        self.assertAlmostEqual(n, expected, places=places)

    # @unittest.expectedFailure
    def test_ellipse01_path22_normalize(self):
        # See also: ellipse01.html
        d = 'M50,216.506 A100,250 0 1 1 86.603,-125'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M50,216.506" \
            " C-22.172,269.38 -68.138,215.917 -89.023,113.876" \
            " -109.908,11.834 -100.359,-112.642 -65.857,-188.13" \
            " -31.355,-263.618 19.262,-270.777 86.603,-125"
        self.assertEqual(exp, expected)

    def test_ellipse01_path31_length(self):
        # See also: ellipse01.html
        # rx > ry
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 0
        path_data = list()
        cx = 0
        cy = 0
        rx = 250
        ry = 100
        ellipse = Ellipse(cx, cy, rx, ry)
        cpx, cpy = ellipse.point(90 - 20)
        path_data.append(SVGPathSegment('M', cpx, cpy))
        rotation = 0
        fa = 0
        fs = 0
        epx, epy = ellipse.point(90 + 45)
        path_data.append(
            SVGPathSegment('A', rx, ry, rotation, fa, fs, epx, epy))
        # d = PathParser.tostring(path_data)
        # -> "M85.505,-93.969 A250,100 0 0 0 -176.777,-70.711"
        n = PathParser.get_total_length(path_data)
        # expected = 265.98455810546875  # firefox
        expected = 265.9847412109375
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse01_path31_normalize(self):
        # See also: ellipse01.html
        d = 'M85.505,-93.969 A250,100 0 0 0 -176.777,-70.711'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M85.505,-93.969" \
            " C107.64,-96.024 23.844,-104.802 -56.022,-97.457" \
            " -135.889,-90.111 -201.684,-67.575 -176.777,-70.711"
        self.assertEqual(exp, expected)

    def test_ellipse01_path32_length(self):
        # See also: ellipse01.html
        # rx > ry
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 0
        path_data = list()
        cx = 0
        cy = 0
        rx = 250
        ry = 100
        ellipse = Ellipse(cx, cy, rx, ry)
        cpx, cpy = ellipse.point(180 - 20)
        path_data.append(SVGPathSegment('M', cpx, cpy))
        rotation = 0
        fa = 0
        fs = 0
        epx, epy = ellipse.point(180 + 45)
        path_data.append(
            SVGPathSegment('A', rx, ry, rotation, fa, fs, epx, epy))
        # -> "M-234.923,-34.202 A250,100 0 0 0 -176.777,70.711"
        n = PathParser.get_total_length(path_data)
        # expected = 145.73971557617188  # firefox
        # expected = 145.73988342285156
        expected = 145.7400360107422
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse01_path32_normalize(self):
        # See also: ellipse01.html
        d = 'M-234.923,-34.202 A250,100 0 0 0 -176.777,70.711'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M-234.923,-34.202" \
            " C-253.733,3.014 -248.464,20.795 -176.777,70.711"
        self.assertEqual(exp, expected)

    def test_ellipse01_path33_length(self):
        # See also: ellipse01.html
        # rx > ry
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 0
        path_data = list()
        cx = 0
        cy = 0
        rx = 250
        ry = 100
        ellipse = Ellipse(cx, cy, rx, ry)
        cpx, cpy = ellipse.point(270 - 20)
        path_data.append(SVGPathSegment('M', cpx, cpy))
        rotation = 0
        fa = 0
        fs = 0
        epx, epy = ellipse.point(270 + 45)
        path_data.append(
            SVGPathSegment('A', rx, ry, rotation, fa, fs, epx, epy))
        # -> "M-85.505,93.969 A250,100 0 0 0 176.777,70.711"
        n = PathParser.get_total_length(path_data)
        # expected = 265.98455810546875  # firefox
        # expected = 265.98468017578125
        expected = 265.9847106933594
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse01_path33_normalize(self):
        # See also: ellipse01.html
        d = 'M-85.505,93.969 A250,100 0 0 0 176.777,70.711'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M-85.505,93.969" \
            " C-107.64,96.024 -23.844,104.802 56.022,97.457" \
            " 135.889,90.111 201.684,67.575 176.777,70.711"
        self.assertEqual(exp, expected)

    def test_ellipse01_path34_length(self):
        # See also: ellipse01.html
        # rx > ry
        # x_axis_rotation: 0
        # large_arc_flag: 0
        # sweep_flag: 0
        path_data = list()
        cx = 0
        cy = 0
        rx = 250
        ry = 100
        ellipse = Ellipse(cx, cy, rx, ry)
        cpx, cpy = ellipse.point(0 - 20)
        path_data.append(SVGPathSegment('M', cpx, cpy))
        rotation = 0
        fa = 0
        fs = 0
        epx, epy = ellipse.point(0 + 45)
        path_data.append(
            SVGPathSegment('A', rx, ry, rotation, fa, fs, epx, epy))
        # -> 'M234.923,34.202 A250,100 0 0 0 176.777,-70.711'
        n = PathParser.get_total_length(path_data)
        # expected = 145.73971557617188  # firefox
        expected = 145.73988342285156
        self.assertAlmostEqual(n, expected, places=places)

    def test_ellipse01_path34_normalize(self):
        # See also: ellipse01.html
        d = 'M234.923,34.202 A250,100 0 0 0 176.777,-70.711'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M234.923,34.202 C253.733,-3.014 248.464,-20.795 176.777,-70.711"
        self.assertEqual(exp, expected)

    def test_get_angle(self):
        t = get_angle(0, 1)
        expected = 0
        self.assertAlmostEqual(t, expected)

        t = get_angle(1, math.sqrt(3))
        expected = 360 - 30
        self.assertAlmostEqual(t, expected)

        t = get_angle(1, 1)
        expected = 360 - 45
        self.assertAlmostEqual(t, expected)

        t = get_angle(math.sqrt(3), 1)
        expected = 360 - 60
        self.assertAlmostEqual(t, expected)

        t = get_angle(1, 0)
        expected = 270
        self.assertAlmostEqual(t, expected)

        t = get_angle(1, -1)
        expected = 180 + 45
        self.assertAlmostEqual(t, expected)

        t = get_angle(0, -1)
        expected = 180
        self.assertAlmostEqual(t, expected)

        t = get_angle(-1, -1)
        expected = 135
        self.assertAlmostEqual(t, expected)

        t = get_angle(-1, 0)
        expected = 90
        self.assertAlmostEqual(t, expected)

        t = get_angle(-math.sqrt(3), 1)
        expected = 60
        self.assertAlmostEqual(t, expected)

        t = get_angle(-1, 1)
        expected = 45
        self.assertAlmostEqual(t, expected)

        t = get_angle(-1, math.sqrt(3))
        expected = 30
        self.assertAlmostEqual(t, expected)

    def test_path_arc_abs(self):
        # See also: arcs03.html
        # "M360,200 A160,80 0 0 1 200,280"
        d = "M360,200" \
            " A160,80 0 0 1 200,280" \
            " 160,80 0 0 1 40,200" \
            " 160,80 0 0 1 200,120" \
            " 160,80 0 0 1 360,200 z"
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 775.1868286132812  # firefox
        expected = 775.18701171875
        self.assertAlmostEqual(n, expected, places=places)

    def test_path_arc_rel(self):
        # See also: arcs03.html
        # "M 125,75 a100,50 0 0 0 100,50"
        d = "M360,200" \
            " a160,80 0 0 1 -160,80" \
            " 160,80 0 0 1 -160,-80" \
            " 160,80 0 0 1 160,-80" \
            " 160,80 0 0 1 160,80 z"
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 775.1868286132812  # firefox
        expected = 775.18701171875
        self.assertAlmostEqual(n, expected, places=places)

    def test_path_normalize01(self):
        # cx=0 cy=0 r=100
        # large_arc_flag=0, sweep_flag=0
        # angle: 0 to 90
        d = 'M100,0 A100,100 0 0 0 0,-100'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M100,0 C100,-55.228 55.228,-100 0,-100'
        self.assertEqual(exp, expected)

    def test_path_normalize02(self):
        # angle: 90 to 180
        d = 'M0,-100 A100,100 0 0 0 -100,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M0,-100 C-55.228,-100 -100,-55.228 -100,0'
        self.assertEqual(exp, expected)

    def test_path_normalize03(self):
        # angle: 180 to 270
        d = 'M-100,0 A100,100 0 0 0 0,100'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M-100,0 C-100,55.228 -55.228,100 0,100'
        self.assertEqual(exp, expected)

    def test_path_normalize04(self):
        # angle: 270 to 360
        d = 'M0,100 A100,100 0 0 0 100,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M0,100 C55.228,100 100,55.228 100,0'
        self.assertEqual(exp, expected)

    def test_path_normalize05(self):
        # angle: 0 to 30
        d = 'M100,0 A100,100 0 0 0 86.60254037844388,-49.99999999999999'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M100,0 C100,-17.554 95.379,-34.798 86.603,-50'
        self.assertEqual(exp, expected)

    def test_path_normalize06(self):
        # angle: 60 to 120
        d = "M50.000000000000014,-86.60254037844386" \
            " A100,100 0 0 0 -49.99999999999998,-86.60254037844388"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M50,-86.603 C19.06,-104.466 -19.06,-104.466 -50,-86.603'
        self.assertEqual(exp, expected)

    def test_path_normalize07(self):
        # angle: 150 to 210
        d = "M-86.60254037844388,-49.99999999999999" \
            " A100,100 0 0 0 -86.60254037844386,50.000000000000014"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M-86.603,-50 C-104.466,-19.06 -104.466,19.06 -86.603,50'
        self.assertEqual(exp, expected)

    def test_path_normalize08(self):
        # angle: 240 to 300
        d = "M-50.00000000000004,86.60254037844383" \
            " A100,100 0 0 0 50.000000000000014,86.60254037844386"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M-50,86.603 C-19.06,104.466 19.06,104.466 50,86.603'
        self.assertEqual(exp, expected)

    def test_path_normalize09(self):
        # angle: -30 to 30
        d = "M86.60254037844383,50.00000000000004" \
            " A100,100 0 0 0 86.60254037844388,-49.99999999999999"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M86.603,50 C104.466,19.06 104.466,-19.06 86.603,-50'
        self.assertEqual(exp, expected)

    def test_path_normalize10(self):
        # large_arc_flag=1, sweep_flag=0
        # angle: 30 to -30
        d = "M86.60254037844388,-49.99999999999999" \
            " A100,100 0 1 0 86.60254037844386,50.000000000000014"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M86.603,-50" \
            " C63.972,-89.197 17.836,-108.307 -25.882,-96.593" \
            " -69.6,-84.878 -100,-45.261 -100,0" \
            " -100,45.261 -69.6,84.878 -25.882,96.593" \
            " 17.836,108.307 63.972,89.197 86.603,50"
        self.assertEqual(exp, expected)

    def test_path_normalize_negative01(self):
        # cx=0 cy=0 r=100
        # large_arc_flag=0, sweep_flag=1
        # angle: 30 to -30
        d = "M86.60254037844388,-49.99999999999999" \
            " A100,100 0 0 1 86.60254037844386,50.000000000000014"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M86.603,-50 C104.466,-19.06 104.466,19.06 86.603,50'
        self.assertEqual(exp, expected)

    def test_path_normalize_negative02(self):
        # large_arc_flag=1, sweep_flag=1
        # angle: -30 to 30
        d = "M86.60254037844388,50.000000000000014" \
            " A100,100 0 1 1 86.60254037844386,-49.99999999999999"
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = \
            "M86.603,50" \
            " C63.972,89.197 17.836,108.307 -25.882,96.593" \
            " -69.6,84.878 -100,45.261 -100,0" \
            " -100,-45.261 -69.6,-84.878 -25.882,-96.593" \
            " 17.836,-108.307 63.972,-89.197 86.603,-50"
        self.assertEqual(exp, expected)

    def test_path_transform01(self):
        # See also: svg.svg
        # Mm Aa Hh Zz
        d = 'M-27-5a7,7,0,1,0,0,10h54a7,7,0,1,0,0-10z'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.rotate_self(rot_z=45)
        transformed = PathParser.transform(path_data, matrix)
        exp = PathParser.tostring(transformed)
        expected = "M-15.556,-22.627 A7,7 0 1 0 -22.627,-15.556" \
                   " L15.556,22.627 A7,7 0 1 0 22.627,15.556 Z"
        self.assertEqual(exp, expected)

    def test_path_transform02(self):
        # See also: svg.svg
        # Mm Aa Hh Zz
        d = 'M-27-5a7,7,0,1,0,0,10h54a7,7,0,1,0,0-10z'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.rotate_self(rot_z=90)
        transformed = PathParser.transform(path_data, matrix)
        exp = PathParser.tostring(transformed)
        expected = 'M5,-27 A7,7 0 1 0 -5,-27 L-5,27 A7,7 0 1 0 5,27 Z'
        self.assertEqual(exp, expected)

    def test_path_transform03(self):
        # See also: svg.svg
        # Mm Aa Hh Zz
        d = 'M-27-5a7,7,0,1,0,0,10h54a7,7,0,1,0,0-10z'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.rotate_self(rot_z=135)
        transformed = PathParser.transform(path_data, matrix)
        exp = PathParser.tostring(transformed)
        expected = "M22.627,-15.556 A7,7 0 1 0 15.556,-22.627 L-22.627,15.556" \
                   " A7,7 0 1 0 -15.556,22.627 Z"
        self.assertEqual(exp, expected)

    def test_segment_arcto_abs(self):
        segment = SVGPathSegment('A')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual(segment.values, ())
        self.assertEqual(segment.end, (None, None))
        d = segment.tostring()
        self.assertEqual(d, '')

        segment = SVGPathSegment('A', 160, 80, 0, 0, 1, 200, 280)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual(segment.values, (160, 80, 0, 0, 1, 200, 280))
        self.assertEqual(segment.end, (200, 280))
        d = segment.tostring()
        self.assertEqual(d, 'A160,80 0 0 1 200,280')

        segment = SVGPathSegment()
        segment.set_elliptical_arc_abs(160, 80, 0, 0, 1, 200, 280)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual(segment.values, (160, 80, 0, 0, 1, 200, 280))
        self.assertEqual(segment.end, (200, 280))
        d = segment.tostring()
        self.assertEqual(d, 'A160,80 0 0 1 200,280')

    def test_segment_arcto_rel(self):
        segment = SVGPathSegment('a')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual(segment.values, ())
        self.assertEqual(segment.end, (None, None))
        d = segment.tostring()
        self.assertEqual(d, '')

        segment = SVGPathSegment('a', 100, 50, 0, 0, 0, 100, 50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual(segment.values, (100, 50, 0, 0, 0, 100, 50))
        self.assertEqual(segment.end, (100, 50))
        d = segment.tostring()
        self.assertEqual(d, 'a100,50 0 0 0 100,50')

        segment = SVGPathSegment()
        segment.set_elliptical_arc_rel(100, 50, 0, 0, 0, 100, 50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual(segment.values, (100, 50, 0, 0, 0, 100, 50))
        self.assertEqual(segment.end, (100, 50))
        d = segment.tostring()
        self.assertEqual(d, 'a100,50 0 0 0 100,50')


if __name__ == '__main__':
    unittest.main()
