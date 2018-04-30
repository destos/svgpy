#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import Matrix, PathParser, SVGPathSegment, formatter
from svgpy.path import PathSegment

places = 0
delta = 1


# Test with: Chrome 64.0 (Linux 64-bit)
class PathCurvetoTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_cubic01_path01_bbox(self):
        # See also: cubic01.html
        d = 'M100,200 C100,100 250,100 250,200 C250,300 400,300 400,200'
        path_data = PathParser.parse(d)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic01_path01_length(self):
        # See also: cubic01.html
        d = 'M100,200 C100,100 250,100 250,200 C250,300 400,300 400,200'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 475.7469787597656  # firefox
        expected = 475.74774169921875
        self.assertAlmostEqual(expected, n, places=places)

        d = 'M100,200 C100,100 250,100 250,200 S400,300 400,200'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 475.7469787597656  # firefox
        expected = 475.74774169921875
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic01_path01_normalize(self):
        # See also: cubic01.html
        d = 'M100,200 C100,100 250,100 250,200 S400,300 400,200'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M100,200 C100,100 250,100 250,200 250,300 400,300 400,200'
        self.assertEqual(expected, d)

    def test_cubic01_path01_transform(self):
        # See also: cubic01.html
        d = 'M100,200 C100,100 250,100 250,200 S400,300 400,200'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M50,250 C50,150 200,150 200,250 S350,350 350,250'
        self.assertEqual(expected, d2)

    def test_cubic01_path02_length(self):
        # See also: cubic01.html
        d = 'M100,200 C100,100 250,100 250,200'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 237.87351989746094  # firefox
        expected = 237.87376403808594
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path01_bbox(self):
        # See also: cubic02.html
        d = 'M100,200 C100,100 400,100 400,200'
        path_data = PathParser.parse(d)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_path01_length(self):
        # See also: cubic02.html
        d = 'M100,200 C100,100 400,100 400,200'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 366.38275146484375  # firefox
        expected = 366.3829650878906
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path01_transform(self):
        # See also: cubic02.html
        d = 'M100,200 C100,100 400,100 400,200'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M50,250 C50,150 350,150 350,250'
        self.assertEqual(expected, d2)

    def test_cubic02_path02_bbox(self):
        # See also: cubic02.html
        d = 'M100,500 C25,400 475,400 400,500'
        path_data = PathParser.parse(d)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(91.533577, bbox.x, places=places)
        self.assertAlmostEqual(425, bbox.y, places=places)
        self.assertAlmostEqual(316.932831, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_path02_length(self):
        # See also: cubic02.html
        d = 'M100,500 C25,400 475,400 400,500'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 403.0122985839844  # firefox
        expected = 403.01336669921875
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path02_transform(self):
        # See also: cubic02.html
        d = 'M100,500 C25,400 475,400 400,500'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M50,550 C-25,450 425,450 350,550'
        self.assertEqual(expected, d2)

    def test_cubic02_path03_bbox(self):
        # See also: cubic02.html
        d = 'M100,800 C175,700 325,700 400,800'
        path_data = PathParser.parse(d)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(725, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_path03_length(self):
        # See also: cubic02.html
        d = 'M100,800 C175,700 325,700 400,800'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 347.868408203125  # firefox
        expected = 347.8686828613281
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path03_transform(self):
        # See also: cubic02.html
        d = 'M100,800 C175,700 325,700 400,800'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M50,850 C125,750 275,750 350,850'
        self.assertEqual(expected, d2)

    def test_cubic02_path04_bbox(self):
        # See also: cubic02.html
        d = 'M600,200 C675,100 975,100 900,200'
        path_data = PathParser.parse(d)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(600, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(311.936218, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_path04_length(self):
        # See also: cubic02.html
        d = 'M600,200 C675,100 975,100 900,200'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 383.4436340332031  # firefox
        expected = 383.4443664550781
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path04_transform(self):
        # See also: cubic02.html
        d = 'M600,200 C675,100 975,100 900,200'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M550,250 C625,150 925,150 850,250'
        self.assertEqual(expected, d2)

    def test_cubic02_path05_bbox(self):
        # See also: cubic02.html
        d = 'M600,500 C600,350 900,650 900,500'
        path_data = PathParser.parse(d)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(600, bbox.x, places=places)
        self.assertAlmostEqual(456.69873, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(86.602539, bbox.height, places=places)

    def test_cubic02_path05_length(self):
        # See also: cubic02.html
        d = 'M600,500 C600,350 900,650 900,500'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 375.2682189941406  # firefox
        expected = 375.26849365234375
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path05_transform(self):
        # See also: cubic02.html
        d = 'M600,500 C600,350 900,650 900,500'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M550,550 C550,400 850,700 850,550'
        self.assertEqual(expected, d2)

    def test_cubic02_path06_bbox(self):
        # See also: cubic02.html
        d = 'M600,800 C625,700 725,700 750,800 S875,900 900,800'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(600, bbox.x, places=places)
        self.assertAlmostEqual(725, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic02_path06_length(self):
        # See also: cubic02.html
        d = 'M600,800 C625,700 725,700 750,800 S875,900 900,800'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 457.373046875  # firefox
        expected = 457.37384033203125
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_path06_normalize(self):
        # See also: cubic02.html
        d = 'M600,800 C625,700 725,700 750,800 S875,900 900,800'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M600,800 C625,700 725,700 750,800 775,900 875,900 900,800'
        self.assertEqual(expected, d)

    def test_cubic02_path06_transform(self):
        # See also: cubic02.html
        d = 'M600,800 C625,700 725,700 750,800 S875,900 900,800'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M550,850 C575,750 675,750 700,850 S825,950 850,850'
        self.assertEqual(expected, d2)

    def test_cubic02_01_path01_bbox(self):
        # See also: cubic02_01.html
        d = 'm100,200 c0,-100 300,-100 300,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_01_path01_length(self):
        # See also: cubic02_01.html
        d = 'm100,200 c0,-100 300,-100 300,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 366.38275146484375  # firefox
        expected = 366.3829650878906
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path02_bbox(self):
        # See also: cubic02_01.html
        d = 'm100,500 c-75,-100 375,-100 300,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(91.534, bbox.x, places=places)
        self.assertAlmostEqual(425, bbox.y, places=places)
        self.assertAlmostEqual(316.933, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_01_path02_length(self):
        # See also: cubic02_01.html
        d = 'm100,500 c-75,-100 375,-100 300,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 403.0122985839844  # firefox
        expected = 403.01336669921875
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path03_bbox(self):
        # See also: cubic02_01.html
        d = 'm100,800 c75,-100 225,-100 300,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(725, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_01_path03_length(self):
        # See also: cubic02_01.html
        d = 'm100,800 c75,-100 225,-100 300,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 347.868408203125  # firefox
        expected = 347.8686828613281
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path04_bbox(self):
        # See also: cubic02_01.html
        d = 'm600,200 c75,-100 375,-100 300,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(600, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(311.936, bbox.width, places=places)
        self.assertAlmostEqual(75, bbox.height, places=places)

    def test_cubic02_01_path04_length(self):
        # See also: cubic02_01.html
        d = 'm600,200 c75,-100 375,-100 300,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 383.4436340332031  # firefox
        expected = 383.4443664550781
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path05_bbox(self):
        # See also: cubic02_01.html
        d = 'm600,500 c0,-150 300,150 300,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(600, bbox.x, places=places)
        self.assertAlmostEqual(456.699, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(86.603, bbox.height, places=places)

    def test_cubic02_01_path05_length(self):
        # See also: cubic02_01.html
        d = 'm600,500 c0,-150 300,150 300,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 375.2682189941406  # firefox
        expected = 375.26849365234375
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path06_bbox(self):
        # See also: cubic02_01.html
        d = 'm600,800 c25,-100 125,-100 150,0 s125,100 150,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(600, bbox.x, places=places)
        self.assertAlmostEqual(725, bbox.y, places=places)
        self.assertAlmostEqual(300, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic02_01_path06_length(self):
        # See also: cubic02_01.html
        d = 'm600,800 c25,-100 125,-100 150,0 s125,100 150,0'
        path_data = PathParser.parse(d)

        # "m600,800 c25,-100 125,-100 150,0 s125,100 150,0"
        # -> "M600,800 C625,700 725,700 750,800 S875,900 900,800"
        # -> "M600,800 C625,700 725,700 750,800 C775,900 875,900 900,800"
        n = PathParser.get_total_length(path_data)
        # expected = 457.373046875  # firefox
        expected = 457.37384033203125
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path06_normalize(self):
        # See also: cubic02_01.html
        d = 'm600,800 c25,-100 125,-100 150,0 s125,100 150,0'
        path_data = PathParser.parse(d)

        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = 'M600,800 C625,700 725,700 750,800 775,900 875,900 900,800'
        self.assertEqual(expected, d)

        n = PathParser.get_total_length(normalized)
        expected = 457.37384033203125
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic02_01_path06_transform(self):
        # See also: cubic02_01.html
        d = 'm600,800 c25,-100 125,-100 150,0 s125,100 150,0'
        path_data = PathParser.parse(d)

        # "M600,800 C625,700 725,700 750,800 775,900 875,900 900,800"
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M550,850 C575,750 675,750 700,850 S825,950 850,850'
        self.assertEqual(expected, d2)

    def test_cubic03_path01_bbox(self):
        # See also: cubic03.html
        d = "M100,200" \
            " C120,100 155,100 175,200 S225,300 245,200 300,100 320,200"
        path_data = PathParser.parse(d)
        path_data = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(path_data)
        self.assertAlmostEqual(100, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(220, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic03_path01_length(self):
        # See also: cubic03.html
        # "M" "C" "S" "S"
        d = "M100,200" \
            " C120,100 155,100 175,200 S225,300 245,200 300,100 320,200"

        # "C120,100 155,100 175,200"
        # p1=(175+175-155=195,200+200-100=300)
        #
        # "S225,300 245,200" -> "C195,300 225,300 245,200"
        # p1=(245+245-225=265,200+200-300=100)

        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 524.0918579101562  # firefox
        expected = 524.09228515625
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic03_path01_normalize(self):
        # See also: cubic03.html
        # "M" "C" "S" "S"
        d = "M100,200" \
            " C120,100 155,100 175,200 S225,300 245,200 300,100 320,200"

        # "C120,100 155,100 175,200"
        # p1=(175+175-155=195,200+200-100=300)
        #
        # "S225,300 245,200" -> "C195,300 225,300 245,200"
        # p1=(245+245-225=265,200+200-300=100)

        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = "M100,200" \
                   " C120,100 155,100 175,200 195,300 225,300 245,200" \
                   " 265,100 300,100 320,200"
        self.assertEqual(expected, d)

    def test_cubic03_path01_transform(self):
        # See also: cubic03.html
        d = \
            "M100,200 C120,100 155,100 175,200 S225,300 245,200 300,100 320,200"
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = \
            "M50,250 C70,150 105,150 125,250 S175,350 195,250 250,150 270,250"
        self.assertEqual(expected, d2)

    def test_cubic03_path02_bbox(self):
        # See also: cubic03.html
        d = 'M175,200 C195,300 225,300 245,200 265,100 300,100 320,200'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(175, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(145, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic03_path02_length(self):
        # See also: cubic03.html
        # "M" "C" "S" "S" -> "M" "C" "C"
        d = 'M175,200 C195,300 225,300 245,200 265,100 300,100 320,200'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 348.3697814941406  # firefox
        expected = 348.3702392578125
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic03_path03_bbox(self):
        # See also: cubic03.html
        d = 'm500,200 c20,-100 55,-100 75,0 s50,100 70,0 55,-100 75,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(500, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(220, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic03_path03_length(self):
        # See also: cubic03.html
        # "m" "c" "s" "s"
        d = 'm500,200 c20,-100 55,-100 75,0 s50,100 70,0 55,-100 75,0'

        # "M500,200"
        # (cpx,cpy)=(500,200)
        #
        # "c20,-100 55,-100 75,0" -> "C520,100 555,100 575,200"
        # (cpx,cpy)=(575,200)
        # (x1,y1)=(575+575-555=595,200+200-100=300)
        #
        # "s50,100 70,0" -> "S625,300 645,200" -> "C595,300 625,300 645,200"
        # (cpx,cpy)=(645,200)
        # (x1,y1)=(645+645-625=665,200+200-300=100)
        #
        # "s55,-100 75,0" -> "S700,100 720,200" -> "C665,100 700,100 720,200"

        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 524.092041015625  # firefox
        expected = 524.0925903320312
        self.assertAlmostEqual(expected, n, places=places)

    def test_cubic03_path03_normalize(self):
        # See also: cubic03.html
        # "m" "c" "s" "s"
        d = 'm500,200 c20,-100 55,-100 75,0 s50,100 70,0 55,-100 75,0'

        # "M500,200"
        # (cpx,cpy)=(500,200)
        #
        # "c20,-100 55,-100 75,0" -> "C520,100 555,100 575,200"
        # (cpx,cpy)=(575,200)
        # (x1,y1)=(575+575-555=595,200+200-100=300)
        #
        # "s50,100 70,0" -> "S625,300 645,200" -> "C595,300 625,300 645,200"
        # (cpx,cpy)=(645,200)
        # (x1,y1)=(645+645-625=665,200+200-300=100)
        #
        # "s55,-100 75,0" -> "S700,100 720,200" -> "C665,100 700,100 720,200"

        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = "M500,200 C520,100 555,100 575,200" \
                   " 595,300 625,300 645,200 665,100 700,100 720,200"
        self.assertEqual(expected, d)

    def test_cubic03_path04_bbox(self):
        # See also: cubic03.html
        d = 'm575,200 c20,100 50,100 70,0 20,-100 55,-100 75,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(575, bbox.x, places=places)
        self.assertAlmostEqual(125, bbox.y, places=places)
        self.assertAlmostEqual(145, bbox.width, places=places)
        self.assertAlmostEqual(150, bbox.height, places=places)

    def test_cubic03_path04_length(self):
        # See also: cubic03.html
        # "m" "c" "s" "s" -> "m" "c" "c"
        d = 'm575,200 c20,100 50,100 70,0 20,-100 55,-100 75,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 348.3697204589844  # firefox
        expected = 348.37030029296875
        self.assertAlmostEqual(expected, n, places=places)

    def test_path_curveto_abs(self):
        path_data = list()
        path_data.append(SVGPathSegment('M', 100, 200))
        path_data.append(SVGPathSegment('C', 100, 100, 250, 100, 250, 200))
        path_data.append(SVGPathSegment('S', 400, 300, 400, 200))
        d = PathParser.tostring(path_data)
        expected = 'M100,200 C100,100 250,100 250,200 S400,300 400,200'
        self.assertEqual(expected, d)

    def test_path_curveto_rel(self):
        path_data = list()
        path_data.append(SVGPathSegment('m', 600, 800))
        path_data.append(SVGPathSegment('c', 25, -100, 125, -100, 150, 0))
        path_data.append(SVGPathSegment('s', 125, 100, 150, 0))
        d = PathParser.tostring(path_data)
        expected = 'm600,800 c25,-100 125,-100 150,0 s125,100 150,0'
        self.assertEqual(expected, d)

    def test_quad01_path01_bbox(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300 T1000,300'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(200, bbox.x, places=places)
        self.assertAlmostEqual(175, bbox.y, places=places)
        self.assertAlmostEqual(800, bbox.width, places=places)
        self.assertAlmostEqual(250, bbox.height, places=places)

    def test_quad01_path01_length(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300 T1000,300'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 975.5421142578125  # firefox
        expected = 975.542724609375
        self.assertAlmostEqual(expected, n, places=places)

    def test_quad01_path01_normalize(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300 T1000,300'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = "M200,300" \
                   " C333.333,133.333 466.667,133.333 600,300" \
                   " 733.333,466.667 866.667,466.667 1000,300"
        self.assertEqual(expected, d)

    def test_quad01_path01_transform(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300 T1000,300'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M150,350 Q350,100 550,350 T950,350'
        self.assertEqual(expected, d2)

    def test_quad01_path02_bbox(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(200, bbox.x, places=places)
        self.assertAlmostEqual(175, bbox.y, places=places)
        self.assertAlmostEqual(400, bbox.width, places=places)
        self.assertAlmostEqual(125, bbox.height, places=places)

    def test_quad01_path02_length(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 487.7709655761719  # firefox
        expected = 487.77130126953125
        self.assertAlmostEqual(expected, n, places=places)

    def test_quad02_path01_bbox(self):
        # See also: quad02.html
        d = 'M200,300 Q400,50 600,300 T1000,300 1400,300'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(200, bbox.x, places=places)
        self.assertAlmostEqual(175, bbox.y, places=places)
        self.assertAlmostEqual(1200, bbox.width, places=places)
        self.assertAlmostEqual(250, bbox.height, places=places)

    def test_quad02_path01_length(self):
        # See also: quad02.html
        d = 'M200,300 Q400,50 600,300 T1000,300 1400,300'

        # "Q400,50 600,300"
        # (cpx,cpy)=(600,300), QP1=(400,50)
        # (x1,y1)=(600+600-400=800,300+300-50=550)
        #
        # T1000,300 -> Q800,550 1000,300
        # (cpx,cpy)=(1000,300)
        # (x1,y1)=(1000+1000-800=1200,300+300-550=50)
        #
        # T1400,300 -> Q1200,50 1400,300

        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 1463.3150634765625  # firefox
        expected = 1463.3143310546875
        self.assertAlmostEqual(expected, n, places=places)

    def test_quad02_path01_normalize(self):
        # See also: quad02.html
        d = 'M200,300 Q400,50 600,300 T1000,300 1400,300'

        # "Q400,50 600,300"
        # (cpx,cpy)=(600,300), QP1=(400,50)
        # (x1,y1)=(600+600-400=800,300+300-50=550)
        #
        # T1000,300 -> Q800,550 1000,300
        # (cpx,cpy)=(1000,300)
        # (x1,y1)=(1000+1000-800=1200,300+300-550=50)
        #
        # T1400,300 -> Q1200,50 1400,300

        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = "M200,300" \
                   " C333.333,133.333 466.667,133.333 600,300" \
                   " 733.333,466.667 866.667,466.667 1000,300" \
                   " 1133.333,133.333 1266.667,133.333 1400,300"
        self.assertEqual(expected, d)

    def test_quad02_path01_transform(self):
        # See also: quad01.html
        d = 'M200,300 Q400,50 600,300 T1000,300 1400,300'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M150,350 Q350,100 550,350 T950,350 1350,350'
        self.assertEqual(expected, d2)

    def test_quad02_path02_bbox(self):
        # See also: quad02.html
        d = 'M200,300 Q400,50 600,300 Q800,550 1000,300 Q1200,50 1400,300'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(200, bbox.x, places=places)
        self.assertAlmostEqual(175, bbox.y, places=places)
        self.assertAlmostEqual(1200, bbox.width, places=places)
        self.assertAlmostEqual(250, bbox.height, places=places)

    def test_quad02_path02_length(self):
        # See also: quad02.html
        d = 'M200,300 Q400,50 600,300 Q800,550 1000,300 Q1200,50 1400,300'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 1463.3150634765625  # firefox
        expected = 1463.3143310546875
        self.assertAlmostEqual(expected, n, places=places)

    def test_quad02_path03_bbox(self):
        # See also: quad02.html
        d = 'm200,300 q200,-250 400,0 t400,0 400,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        bbox = PathParser.get_bbox(normalized)
        self.assertAlmostEqual(200, bbox.x, places=places)
        self.assertAlmostEqual(175, bbox.y, places=places)
        self.assertAlmostEqual(1200, bbox.width, places=places)
        self.assertAlmostEqual(250, bbox.height, places=places)

    def test_quad02_path03_length(self):
        # See also: quad02.html
        d = 'm200,300 q200,-250 400,0 t400,0 400,0'
        path_data = PathParser.parse(d)
        n = PathParser.get_total_length(path_data)
        # expected = 1463.3150634765625  # firefox
        expected = 1463.3143310546875
        self.assertAlmostEqual(expected, n, places=places)

    def test_quad02_path03_normalize(self):
        # See also: quad02.html
        d = 'm200,300 q200,-250 400,0 t400,0 400,0'
        path_data = PathParser.parse(d)
        normalized = PathParser.normalize(path_data)
        d = PathParser.tostring(normalized)
        expected = "M200,300" \
                   " C333.333,133.333 466.667,133.333 600,300" \
                   " 733.333,466.667 866.667,466.667 1000,300" \
                   " 1133.333,133.333 1266.667,133.333 1400,300"
        self.assertEqual(expected, d)

    def test_quad02_path03_transform(self):
        # See also: quad01.html
        d = 'm200,300 q200,-250 400,0 t400,0 400,0'
        path_data = PathParser.parse(d)
        matrix = Matrix()
        matrix.translate_self(-50, 50)
        transformed = PathParser.transform(path_data, matrix)
        d2 = PathParser.tostring(transformed)
        expected = 'M150,350 Q350,100 550,350 T950,350 1350,350'
        self.assertEqual(expected, d2)

    def test_segment_curveto_abs(self):
        # See also: cubic01.html
        segment = SVGPathSegment('C')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "M100,200 C100,100 250,100 250,200 S400,300 400,200"
        # "C100,100 250,100 250,200"
        segment = SVGPathSegment('C', 100, 100, 250, 100, 250, 200)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((100, 100, 250, 100, 250, 200), segment.values)
        self.assertEqual((250, 200), segment.end)
        d = segment.tostring()
        expected = 'C100,100 250,100 250,200'
        self.assertEqual(expected, d)

        segment = SVGPathSegment()
        segment.set_curveto_abs(100, 100, 250, 100, 250, 200)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((100, 100, 250, 100, 250, 200), segment.values)
        self.assertEqual((250, 200), segment.end)
        d = segment.tostring()
        expected = 'C100,100 250,100 250,200'
        self.assertEqual(expected, d)

        segment2 = PathSegment.normalize(segment, 100, 200, 0)[0]
        d = segment2.tostring()
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

    def test_segment_curveto_rel(self):
        # See also: cubic02_01.html
        segment = SVGPathSegment('c')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "m600,800 c25,-100 125,-100 150,0 s125,100 150,0"
        segment = SVGPathSegment('c', 25, -100, 125, -100, 150, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((25, -100, 125, -100, 150, 0), segment.values)
        self.assertEqual((150, 0), segment.end)
        d = segment.tostring()
        expected = 'c25,-100 125,-100 150,0'
        self.assertEqual(expected, d)

        segment = SVGPathSegment()
        segment.set_curveto_rel(25, -100, 125, -100, 150, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((25, -100, 125, -100, 150, 0), segment.values)
        self.assertEqual((150, 0), segment.end)
        d = segment.tostring()
        expected = 'c25,-100 125,-100 150,0'
        self.assertEqual(expected, d)

        segment2 = PathSegment.toabsolute(segment, 600, 800, 0)
        d = segment2.tostring()
        expected = 'C625,700 725,700 750,800'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

        segment2 = PathSegment.normalize(segment, 600, 800, 0)[0]
        d = segment2.tostring()
        expected = 'C625,700 725,700 750,800'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

    def test_segment_smooth_curveto_abs(self):
        segment = SVGPathSegment('S')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "S400,300 400,200"
        segment = SVGPathSegment('S', 400, 300, 400, 200)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((400, 300, 400, 200), segment.values)
        self.assertEqual((400, 200), segment.end)
        d = segment.tostring()
        expected = 'S400,300 400,200'
        self.assertEqual(expected, d)

        segment = SVGPathSegment()
        segment.set_smooth_curveto_abs(400, 300, 400, 200)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((400, 300, 400, 200), segment.values)
        self.assertEqual((400, 200), segment.end)
        d = segment.tostring()
        expected = 'S400,300 400,200'
        self.assertEqual(expected, d)

        segment2 = PathSegment.normalize(segment, 250, 200, 0)[0]
        d = segment2.tostring()
        expected = 'C250,200 400,300 400,200'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

    def test_segment_smooth_curveto_rel(self):
        segment = SVGPathSegment('s')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "s125,100 150,0"
        segment = SVGPathSegment('s', 125, 100, 150, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((125, 100, 150, 0), segment.values)
        self.assertEqual((150, 0), segment.end)
        d = segment.tostring()
        expected = 's125,100 150,0'
        self.assertEqual(expected, d)

        segment = SVGPathSegment()
        segment.set_smooth_curveto_rel(125, 100, 150, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((125, 100, 150, 0), segment.values)
        self.assertEqual((150, 0), segment.end)
        d = segment.tostring()
        expected = 's125,100 150,0'
        self.assertEqual(expected, d)

        segment2 = PathSegment.toabsolute(segment, 750, 800, 0)
        d = segment2.tostring()
        expected = 'S875,900 900,800'
        self.assertEqual(expected, d)

        segment2 = PathSegment.normalize(segment, 750, 800, 0)[0]
        d = segment2.tostring()
        expected = 'C750,800 875,900 900,800'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

        # x1=750+750-725=775
        # y1=800+800-700=900
        segment2 = PathSegment.normalize(segment, 750, 800, 0,
                                         x1=775, y1=900)[0]
        d = segment2.tostring()
        expected = 'C775,900 875,900 900,800'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

    def test_segment_quadratic_curveto_abs(self):
        # See also: quad01.html
        segment = SVGPathSegment('Q')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "M200,300 Q400,50 600,300 T1000,300"
        # "Q400,50 600,300"
        segment = SVGPathSegment('Q', 400, 50, 600, 300)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((400, 50, 600, 300), segment.values)
        self.assertEqual((600, 300), segment.end)
        d = segment.tostring()
        self.assertEqual('Q400,50 600,300', d)

        segment = SVGPathSegment()
        segment.set_quadratic_curveto_abs(400, 50, 600, 300)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((400, 50, 600, 300), segment.values)
        self.assertEqual((600, 300), segment.end)
        d = segment.tostring()
        self.assertEqual('Q400,50 600,300', d)

    def test_segment_quadratic_curveto_rel(self):
        # See also: quad01.html
        segment = SVGPathSegment('q')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "M200,300 Q400,50 600,300 T1000,300 1400,300"
        # "m200,300 q200,-250 400,0 t400,0 400,0"
        segment = SVGPathSegment('q', 200, -250, 400, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((200, -250, 400, 0), segment.values)
        self.assertEqual((400, 0), segment.end)
        d = segment.tostring()
        expected = 'q200,-250 400,0'
        self.assertEqual(expected, d)

        segment = SVGPathSegment()
        segment.set_quadratic_curveto_rel(200, -250, 400, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((200, -250, 400, 0), segment.values)
        self.assertEqual((400, 0), segment.end)
        d = segment.tostring()
        expected = 'q200,-250 400,0'
        self.assertEqual(expected, d)

        segment2 = PathSegment.toabsolute(segment, 200, 300, 0)
        d = segment2.tostring()
        expected = 'Q400,50 600,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

        segment2 = PathSegment.normalize(segment, 200, 300, 0)[0]
        d = segment2.tostring()
        expected = 'C333.333,133.333 466.667,133.333 600,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

    def test_segment_smooth_quadratic_curveto_abs(self):
        segment = SVGPathSegment('T')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        # "M200,300 Q400,50 600,300 T1000,300"
        # "T1000,300"
        segment = SVGPathSegment('T', 1000, 300)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((1000, 300), segment.values)
        self.assertEqual((1000, 300), segment.end)
        d = segment.tostring()
        self.assertEqual('T1000,300', d)

        segment = SVGPathSegment()
        segment.set_smooth_quadratic_curveto_abs(1000, 300)
        self.assertTrue(segment.isvalid())
        self.assertTrue(segment.isabsolute())
        self.assertTrue(not segment.isrelative())
        self.assertEqual((1000, 300), segment.values)
        self.assertEqual((1000, 300), segment.end)
        d = segment.tostring()
        self.assertEqual('T1000,300', d)

        # "M200,300"
        # "C333.333,133.333 466.667,133.333 600,300"
        # "C733.333,466.667 866.667,466.667 1000,300"
        # See test_quad02_path01_normalize()
        segment2 = PathSegment.normalize(segment, 600, 300, 0)[0]
        d = segment2.tostring()
        expected = 'C600,300 733.333,300 1000,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

        segment2 = PathSegment.normalize(segment, 600, 300, 0,
                                         x1=800, y1=550)[0]
        d = segment2.tostring()
        expected = 'C733.333,466.667 866.667,466.667 1000,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

    def test_segment_smooth_quadratic_curveto_rel(self):
        # See also: quad02.html
        segment = SVGPathSegment('t')
        self.assertTrue(not segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((), segment.values)
        self.assertEqual((None, None), segment.end)
        d = segment.tostring()
        self.assertEqual('', d)

        segment = SVGPathSegment('t', 400, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((400, 0), segment.values)
        self.assertEqual((400, 0), segment.end)
        d = segment.tostring()
        expected = 't400,0'
        self.assertEqual(expected, d)

        segment = SVGPathSegment()
        segment.set_smooth_quadratic_curveto_rel(400, 0)
        self.assertTrue(segment.isvalid())
        self.assertTrue(not segment.isabsolute())
        self.assertTrue(segment.isrelative())
        self.assertEqual((400, 0), segment.values)
        self.assertEqual((400, 0), segment.end)
        d = segment.tostring()
        expected = 't400,0'
        self.assertEqual(expected, d)

        segment2 = PathSegment.toabsolute(segment, 600, 300, 0)
        d = segment2.tostring()
        expected = 'T1000,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

        # "m200,300 q200,-250 400,0 t400,0 400,0"
        # "M200,300 Q400,50 600,300 T1000,300 1400,300"
        # "m200,300 q200,-250 400,0 t400,0 400,0"
        # See test_quad02_path01_normalize(), test_quad02_path03_normalize()
        segment2 = PathSegment.normalize(segment, 600, 300, 0)[0]
        d = segment2.tostring()
        expected = 'C600,300 733.333,300 1000,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))

        segment2 = PathSegment.normalize(segment, 600, 300, 0,
                                         x1=800, y1=550)[0]
        d = segment2.tostring()
        expected = 'C733.333,466.667 866.667,466.667 1000,300'
        self.assertEqual(expected, d)
        self.assertTrue(id(segment) != id(segment2))


if __name__ == '__main__':
    unittest.main()
