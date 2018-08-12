#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import DOMMatrix, PathParser, SVGPathSegment, formatter

places = 0
delta = 1


# Test with: Chrome 64.0 (Linux 64-bit)
class PathLinetoTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 6

    def test_bearing01_bbox(self):
        # See also: bearing01.html
        d = 'M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(111.976, bbox.x, places=places)
        self.assertAlmostEqual(10, bbox.y, places=places)
        self.assertAlmostEqual(76.048, bbox.width, places=places)
        self.assertAlmostEqual(72.326, bbox.height, places=places)

    def test_bearing01_length(self):
        # See also: bearing01.html
        d = 'M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        expected = 235
        self.assertAlmostEqual(expected, n)

    def test_bearing01_normalize(self):
        # See also: bearing01.html
        d = 'M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = \
            "M150,10 L188.023799,37.625907 173.5,82.325563 126.5,82.325563" \
            " 111.976201,37.625907 Z"
        self.assertEqual(expected, d)

    def test_bearing01_transform01(self):
        # See also: bearing01.html
        d = 'M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z'
        path_data = PathParser.parse(d)

        matrix = DOMMatrix()
        matrix.translate_self(10, 10)
        transformed = PathParser.transform(path_data, matrix)
        d = PathParser.tostring(transformed)
        expected = \
            "M160,20 L198.023799,47.625907 183.5,92.325563 136.5,92.325563" \
            " 121.976201,47.625907 Z"
        self.assertEqual(expected, d)

    def test_bearing01_transform02(self):
        # See also: bearing01.html
        d = 'M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z'
        path_data = PathParser.parse(d)

        matrix = DOMMatrix()
        matrix = matrix.flip_y()
        transformed = PathParser.transform(path_data, matrix)
        d = PathParser.tostring(transformed)
        expected = \
            "M150,-10 L188.023799,-37.625907 173.5,-82.325563" \
            " 126.5,-82.325563 111.976201,-37.625907 Z"
        self.assertEqual(expected, d)

    def test_lineto_abs_length(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 100, 100))
        path_data.append(SVGPathSegment('L', 300, 100))
        path_data.append(SVGPathSegment('L', 200, 300))
        path_data.append(SVGPathSegment('z'))
        d = PathParser.tostring(path_data)
        expected = 'M100,100 L300,100 200,300 z'
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(path_data)
        # sqrt((300 - 100) ** 2 + (100 - 100) ** 2)
        # + sqrt((200 - 300) ** 2 + (300 - 100) ** 2)
        # + sqrt((100 - 200) ** 2 + (100 - 300) ** 2)
        # = 647.2135954999579
        expected = 647.2135954999579
        self.assertAlmostEqual(expected, n)

    def test_lineto_abs_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 100, 100))
        path_data.append(SVGPathSegment('L', 300, 100))
        path_data.append(SVGPathSegment('L', 200, 300))
        path_data.append(SVGPathSegment('z'))

        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M100,100 L300,100 200,300 Z'
        self.assertEqual(expected, d)

    def test_lineto_rel_length(self):
        # See also: bearing01.html
        # "M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z"
        path_data = list()
        path_data.append(SVGPathSegment('m', 150, 10))
        path_data.append(
            SVGPathSegment('l', 38.02379873562253, 27.62590685774624))
        path_data.append(
            SVGPathSegment('l', -14.52379873562252, 44.69965626587222))
        path_data.append(SVGPathSegment('l', -47, 0))
        path_data.append(
            SVGPathSegment('l', -14.52379873562254, -44.69965626587221))
        path_data.append(SVGPathSegment('z'))
        d = PathParser.tostring(path_data)
        expected = "m150,10" \
                   " l38.023799,27.625907" \
                   " -14.523799,44.699656" \
                   " -47,0" \
                   " -14.523799,-44.699656" \
                   " z"
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(path_data)
        expected = 235
        self.assertAlmostEqual(expected, n)

    def test_lineto_rel_normalize(self):
        # See also: bearing01.html
        # "M150,10 B36 h47 b72 h47 b72 h47 b72 h47 Z"
        path_data = list()
        path_data.append(SVGPathSegment('m', 150, 10))
        path_data.append(
            SVGPathSegment('l', 38.02379873562253, 27.62590685774624))
        path_data.append(
            SVGPathSegment('l', -14.52379873562252, 44.69965626587222))
        path_data.append(SVGPathSegment('l', -47, 0))
        path_data.append(
            SVGPathSegment('l', -14.52379873562254, -44.69965626587221))
        path_data.append(SVGPathSegment('z'))
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = \
            "M150,10 L188.023799,37.625907 173.5,82.325563 126.5,82.325563" \
            " 111.976201,37.625907 Z"
        self.assertEqual(expected, d)

    def test_moveto_abs_length(self):
        # implicit lineto
        path_data = list()
        path_data.append(SVGPathSegment('M', 100, 100))
        path_data.append(SVGPathSegment('M', 50, 0))
        path_data.append(SVGPathSegment('M', 0, 50))
        path_data.append(SVGPathSegment('z'))
        d = PathParser.tostring(path_data)
        expected = 'M100,100 50,0 0,50 z'
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(path_data)
        # (100, 100) - (50, 0) - (0, 50) - (100, 100)
        # sqrt((50 - 100) ** 2 + (0 - 100) ** 2)
        # + sqrt((0 - 50) ** 2 + (50 - 0) ** 2)
        # + sqrt((100 - 0) ** 2 + (100 - 50) ** 2)
        # = 294.3174758686337
        expected = 294.3174758686337
        self.assertAlmostEqual(expected, n)

    def test_moveto_abs_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 100, 100))
        path_data.append(SVGPathSegment('M', 50, 0))
        path_data.append(SVGPathSegment('M', 0, 50))
        path_data.append(SVGPathSegment('z'))
        normalized = PathParser.normalize(path_data)
        exp = PathParser.tostring(normalized)
        expected = 'M100,100 50,0 0,50 Z'
        self.assertEqual(expected, exp)

    def test_moveto_rel_bbox(self):
        # implicit "lineto" command
        path_data = list()
        path_data.append(SVGPathSegment('m', 100, 100))
        path_data.append(SVGPathSegment('m', 50, 0))
        path_data.append(SVGPathSegment('m', 0, 50))
        path_data.append(SVGPathSegment('m', -50, 0))
        path_data.append(SVGPathSegment('z'))
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertEqual(100, bbox.x)
        self.assertEqual(100, bbox.y)
        self.assertEqual(50, bbox.width)
        self.assertEqual(50, bbox.height)

    def test_moveto_rel_length(self):
        # implicit "lineto" command
        path_data = list()
        path_data.append(SVGPathSegment('m', 100, 100))
        path_data.append(SVGPathSegment('m', 50, 0))
        path_data.append(SVGPathSegment('m', 0, 50))
        path_data.append(SVGPathSegment('m', -50, 0))
        path_data.append(SVGPathSegment('z'))
        n = PathParser.get_total_length(path_data)
        expected = 200
        self.assertEqual(expected, n)

    def test_moveto_rel_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 100, 100))
        path_data.append(SVGPathSegment('m', 50, 0))
        path_data.append(SVGPathSegment('m', 0, 50))
        path_data.append(SVGPathSegment('z'))
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M100,100 150,100 150,150 Z'
        self.assertEqual(expected, d)

    def test_horizontal_lineto_abs_length(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 0, 50))
        path_data.append(SVGPathSegment('H', 100))
        d = PathParser.tostring(path_data)
        expected = 'M0,50 H100'
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(path_data)
        expected = 100
        self.assertAlmostEqual(expected, n)

    def test_horizontal_lineto_abs_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 0, 50))
        path_data.append(SVGPathSegment('H', 100))
        normalize = PathParser.normalize(path_data)
        d = PathParser.tostring(normalize)
        expected = 'M0,50 L100,50'
        self.assertEqual(expected, d)

    def test_horizontal_lineto_rel_bbox(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 100, 50))
        path_data.append(SVGPathSegment('h', -100))
        normalized = PathParser.normalize(path_data)
        # "M100,50 L0,50"
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(0, bbox.x, places=places)
        self.assertAlmostEqual(50, bbox.y, places=places)
        self.assertAlmostEqual(100, bbox.width, places=places)
        self.assertAlmostEqual(0, bbox.height, places=places)

    def test_horizontal_lineto_rel_length(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 100, 50))
        path_data.append(SVGPathSegment('h', -100))
        d = PathParser.tostring(path_data)
        expected = 'm100,50 h-100'
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(path_data)
        expected = 100
        self.assertAlmostEqual(expected, n)

    def test_horizontal_lineto_rel_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 100, 50))
        path_data.append(SVGPathSegment('h', -100))
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M100,50 L0,50'
        self.assertEqual(expected, d)

    def test_path_parse01(self):
        # "M0.1,0.2 0.3,4.5 -6.7,-0.8 8.8,0.1 999e-3,0.5 1e+3,0.4 z"
        # skip invalid segment ("777")
        d = 'M0.1.2.3,4.5,-6.7-.8 8.8,.10 999e-3.5 1e+3.4 777z'
        path_data = PathParser.parse(d)
        self.assertEqual(7, len(path_data))

        self.assertEqual('M', path_data[0].type)
        self.assertEqual('M', path_data[1].type)
        self.assertEqual('M', path_data[2].type)
        self.assertEqual('M', path_data[3].type)
        self.assertEqual('M', path_data[4].type)
        self.assertEqual('M', path_data[5].type)
        self.assertEqual('z', path_data[6].type)

        self.assertEqual((0.1, 0.2), path_data[0].values)
        self.assertEqual((0.3, 4.5), path_data[1].values)
        self.assertEqual((-6.7, -0.8), path_data[2].values)
        self.assertEqual((8.8, 0.1), path_data[3].values)
        self.assertEqual((999e-3, 0.5), path_data[4].values)
        self.assertEqual((1e+3, 0.4), path_data[5].values)
        self.assertEqual((), path_data[6].values)

    def test_path_parse02(self):
        # skip invalid segments ("L", "L" and "l")
        # "M100,100 L200,100 l10,100"
        d = 'M100,100 L L L200,100 l l0,100'
        path_data = PathParser.parse(d)

        d = PathParser.tostring(path_data)
        expected = 'M100,100 L200,100 l0,100'
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(path_data)
        expected = 200
        self.assertAlmostEqual(expected, n)

    def test_path_tostring_null(self):
        # skip invalid segments
        path_data = list()
        path_data.append(SVGPathSegment('M'))
        path_data.append(SVGPathSegment('l'))
        path_data.append(SVGPathSegment('l'))
        path_data.append(SVGPathSegment('l'))
        path_data.append(SVGPathSegment('z'))
        d = PathParser.tostring(path_data)
        expected = 'z'
        self.assertEqual(expected, d)

    def test_segment_null(self):
        segment = SVGPathSegment()
        self.assertTrue(not segment.isvalid())
        self.assertIsNone(segment.type)
        self.assertIsNone(segment.isabsolute())
        self.assertIsNone(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)

    def test_segment_bearing_abs(self):
        segment = SVGPathSegment('B')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        exp = segment.tostring()
        self.assertEqual('', exp)

        segment = SVGPathSegment('B')
        bearing = segment.get_bearing(-90)
        self.assertEqual(-90, bearing)
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)

        segment = SVGPathSegment()
        segment.set_bearing_abs(-45)
        bearing = segment.get_bearing(-90)
        self.assertEqual(-45, bearing)
        self.assertEqual(segment.values, (-45,))
        self.assertEqual((None, None), segment.end)

        segment = SVGPathSegment('B', 45)
        self.assertEqual((45,), segment.values)
        bearing = segment.get_bearing(-90)
        self.assertEqual(45, bearing)

        segment = SVGPathSegment('B', -45)
        exp = segment.tostring()
        self.assertEqual('B-45', exp)

    def test_segment_bearing_rel(self):
        segment = SVGPathSegment('b')
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        exp = segment.tostring()
        self.assertEqual('', exp)

        segment = SVGPathSegment()
        bearing = segment.get_bearing(-90)
        self.assertEqual(-90, bearing)
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)

        segment = SVGPathSegment()
        segment.set_bearing_rel(-45)
        bearing = segment.get_bearing(-90)
        self.assertEqual(-135, bearing)
        self.assertEqual((-45,), segment.values)
        self.assertEqual((None, None), segment.end)

        segment = SVGPathSegment('b', 45)
        self.assertEqual((45,), segment.values)
        bearing = segment.get_bearing(-90)
        self.assertEqual(-45, bearing)

        segment = SVGPathSegment('b', -45)
        exp = segment.tostring()
        self.assertEqual('b-45', exp)

    def test_segment_horizontal_lineto_abs(self):
        segment = SVGPathSegment('H')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        segment = SVGPathSegment('H', 100)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((100,), segment.values)
        self.assertEqual((100, None), segment.end)
        d = segment.tostring()
        self.assertEqual('H100', d)

        segment = SVGPathSegment()
        segment.set_horizontal_lineto_abs(50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((50,), segment.values)
        self.assertEqual((50, None), segment.end)
        d = segment.tostring()
        self.assertEqual('H50', d)

    def test_segment_horizontal_lineto_rel(self):
        segment = SVGPathSegment('h')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        segment = SVGPathSegment('h', 100)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((100,), segment.values)
        self.assertEqual((100, 0), segment.end)
        d = segment.tostring()
        self.assertEqual('h100', d)

        segment = SVGPathSegment()
        segment.set_horizontal_lineto_rel(50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((50,), segment.values)
        self.assertEqual((50, 0), segment.end)
        d = segment.tostring()
        self.assertEqual('h50', d)

    def test_segment_lineto_abs(self):
        segment = SVGPathSegment('L')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        segment = SVGPathSegment()
        segment.set_lineto_abs(100, 50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((100, 50), segment.values)
        self.assertEqual((100, 50), segment.end)
        d = segment.tostring()
        self.assertEqual('L100,50', d)

        segment = SVGPathSegment('L', -50, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((-50, 0), segment.values)
        self.assertEqual((-50, 0), segment.end)
        d = segment.tostring()
        self.assertEqual('L-50,0', d)

    def test_segment_moveto_abs(self):
        segment = SVGPathSegment('M')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        exp = segment.tostring()
        self.assertEqual('', exp)

        segment = SVGPathSegment('M', 100, 50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((100, 50), segment.values)
        self.assertEqual((100, 50), segment.end)
        exp = segment.tostring()
        self.assertEqual('M100,50', exp)

        segment = SVGPathSegment()
        segment.set_moveto_abs(100, 100)
        segment.set_moveto_abs(50, 0)  # overwrite
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((50, 0), segment.values)
        self.assertEqual((50, 0), segment.end)
        exp = segment.tostring()
        self.assertEqual('M50,0', exp)

    def test_segment_moveto_rel(self):
        segment = SVGPathSegment('m')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        exp = segment.tostring()
        self.assertEqual('', exp)

        segment = SVGPathSegment('m', 100, 50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((100, 50), segment.values)
        self.assertEqual((100, 50), segment.end)
        exp = segment.tostring()
        self.assertEqual('m100,50', exp)

        segment = SVGPathSegment()
        segment.set_moveto_rel(100, 100)
        segment.set_moveto_rel(50, 0)  # overwrite
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((50, 0), segment.values)
        self.assertEqual((50, 0), segment.end)
        exp = segment.tostring()
        self.assertEqual('m50,0', exp)

    def test_segment_vertical_lineto_abs(self):
        segment = SVGPathSegment('V')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        segment = SVGPathSegment('V', -50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((-50,), segment.values)
        self.assertEqual((None, -50), segment.end)
        d = segment.tostring()
        self.assertEqual('V-50', d)

        segment = SVGPathSegment()
        segment.set_vertical_lineto_abs(150)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((150,), segment.values)
        self.assertEqual((None, 150), segment.end)
        d = segment.tostring()
        self.assertEqual('V150', d)

    def test_segment_vertical_lineto_rel(self):
        segment = SVGPathSegment('v')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        segment = SVGPathSegment('v', -50)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((-50,), segment.values)
        self.assertEqual((0, -50), segment.end)
        d = segment.tostring()
        self.assertEqual('v-50', d)

        segment = SVGPathSegment()
        segment.set_vertical_lineto_rel(150)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((150,), segment.values)
        self.assertEqual((0, 150), segment.end)
        d = segment.tostring()
        self.assertEqual('v150', d)

    def test_vertical_lineto_abs_length(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 50, 50))
        path_data.append(SVGPathSegment('V', 150))
        n = PathParser.get_total_length(path_data)
        expected = 100
        self.assertEqual(expected, n)

    def test_vertical_lineto_abs_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 50, 50))
        path_data.append(SVGPathSegment('V', 150))
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M50,50 L50,150'
        self.assertEqual(expected, d)

    def test_vertical_lineto_rel_length(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 50, 50))
        path_data.append(SVGPathSegment('v', -50))
        n = PathParser.get_total_length(path_data)
        expected = 50
        self.assertEqual(expected, n)

    def test_vertical_lineto_rel_normalize(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 50, 50))
        path_data.append(SVGPathSegment('v', -50))
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M50,50 L50,0'
        self.assertEqual(expected, d)

    def test_triangle01_bbox(self):
        # See also: triangle01.html
        d = 'M 100 100 L 300 100 L 200 300 z'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(100, bbox.y, places=places)
        self.assertAlmostEqual(200, bbox.width, places=places)
        self.assertAlmostEqual(200, bbox.height, places=places)

    def test_triangle01_abs_length(self):
        # See also: triangle01.html
        d = 'M 100 100 L 300 100 L 200 300 z'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        expected = 647.213623046875
        self.assertAlmostEqual(expected, n, places=places)

    def test_triangle01_abs_normalize(self):
        # See also: triangle01.html
        d = 'M 100 100 L 300 100 L 200 300 z'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M100,100 L300,100 200,300 Z'
        self.assertEqual(expected, d)

    def test_triangle01_rel_length(self):
        # See also: triangle01.html
        d = 'm100,100 l200,0 l-100,200 z'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        expected = 647.213623046875
        self.assertAlmostEqual(expected, n, places=places)

    def test_triangle01_rel_normalize(self):
        # See also: triangle01.html
        d = 'm100,100 l200,0 l-100,200 z'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M100,100 L300,100 200,300 Z'
        self.assertEqual(expected, d)


if __name__ == '__main__':
    unittest.main()
