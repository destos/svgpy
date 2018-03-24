#!/usr/bin/env python3

import math
import sys
import unittest

import numpy as np

sys.path.extend(['.', '..'])

from svgpy import Matrix, formatter
from svgpy.matrix import matrix2d


class MatrixTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_matrix2d(self):
        m = matrix2d(1, 2, 3, 4, 5, 6)
        self.assertTrue(
            (m == np.matrix([[1, 3, 5], [2, 4, 6], [0, 0, 1]])).all())

    def test_attribute(self):
        # 3x3
        # [[a c e]
        #  [b d f]
        #  [0 0 1]
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        f = 6
        m = Matrix(a, b, c, d, e, f)
        self.assertEqual(m.a, a)
        self.assertEqual(m.b, b)
        self.assertEqual(m.c, c)
        self.assertEqual(m.d, d)
        self.assertEqual(m.e, e)
        self.assertEqual(m.f, f)

    def test_init(self):
        m = Matrix()  # 1, 0, 0, 1, 0, 0
        self.assertEqual(m.tostring(), 'matrix(1 0 0 1 0 0)')
        self.assertTrue(
            (m.matrix == np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])).all())

    def test_init_type_error1(self):
        self.assertRaises(TypeError, lambda: Matrix(1))

    def test_init_type_error2(self):
        self.assertRaises(TypeError, lambda: Matrix(1, 2))

    def test_init_type_error3(self):
        self.assertRaises(TypeError, lambda: Matrix(1, 2, 3))

    def test_init_type_error4(self):
        self.assertRaises(TypeError, lambda: Matrix(1, 2, 3, 4))

    def test_init_type_error5(self):
        self.assertRaises(TypeError, lambda: Matrix(1, 2, 3, 4, 5))

    def test_init_type_error7(self):
        self.assertRaises(TypeError, lambda: Matrix(1, 2, 3, 4, 5, 6, 7))

    def test_init_normal(self):
        m = Matrix(1.1, 2.1234, 3.5678, 4.9012, 5.8901, 6.000001)
        self.assertEqual(m.tostring(), 'matrix(1.1 2.123 3.568 4.901 5.89 6)')
        self.assertTrue(
            (m.matrix == np.matrix([[1.1, 3.5678, 5.8901],
                                    [2.1234, 4.9012, 6.000001],
                                    [0, 0, 1]])).all())

    def test_flipx(self):
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        f = 6
        m = Matrix(a, b, c, d, e, f)
        m = m.flipx()
        self.assertEqual(m.a, -a)
        self.assertEqual(m.b, -b)
        self.assertEqual(m.c, c)
        self.assertEqual(m.d, d)
        self.assertEqual(m.e, e)
        self.assertEqual(m.f, f)

    def test_flipy(self):
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        f = 6
        m = Matrix(a, b, c, d, e, f)
        m = m.flipy()
        self.assertEqual(m.a, a)
        self.assertEqual(m.b, b)
        self.assertEqual(m.c, -c)
        self.assertEqual(m.d, -d)
        self.assertEqual(m.e, e)
        self.assertEqual(m.f, f)

    def test_frommatrix(self):
        src = np.matrix([[1, 3, 5], [2, 4, 6], [0, 0, 1]])
        m = Matrix.frommatrix(src)
        self.assertTrue((src == m.matrix).all())
        self.assertEqual(m.tostring(), 'matrix(1 2 3 4 5 6)')
        self.assertNotEqual(id(src), id(m.matrix))

    def test_frommatrix_value_error(self):
        src = np.matrix([[1, 3, 5], [2, 4, 6]])
        self.assertRaises(ValueError, lambda: Matrix.frommatrix(src))

    def test_get_angle01(self):
        m = Matrix()
        m.rotate_self(45)
        self.assertEqual(m.get_angle(), 45)

    def test_get_angle02(self):
        m = Matrix()
        m.rotate_self(90)
        self.assertEqual(m.get_angle(), 90)

    def test_get_angle03(self):
        m = Matrix()
        m.rotate_self(135)
        self.assertEqual(m.get_angle(), 135)

    def test_get_angle04(self):
        m = Matrix()
        m.rotate_self(180)
        self.assertEqual(m.get_angle(), 180)

    def test_get_angle05(self):
        m = Matrix()
        m.rotate_self(225)
        # returns -135.00000000000003
        self.assertAlmostEqual(m.get_angle(), -(360 % 225))

    def test_get_angle06(self):
        m = Matrix()
        m.rotate_self(270)
        # returns -90.00000000000001
        self.assertAlmostEqual(m.get_angle(), -(360 % 270))

    def test_get_angle07(self):
        m = Matrix()
        m.rotate_self(315)
        # returns -45.000000000000014
        self.assertAlmostEqual(m.get_angle(), -(360 % 315))

    def test_get_angle08(self):
        m = Matrix()
        m.rotate_self(360)
        # returns -1.4033418597069752e-14
        self.assertAlmostEqual(m.get_angle(), (360 % 360))

    def test_get_angle09(self):
        m = Matrix()
        m.rotate_self(-45)
        self.assertAlmostEqual(m.get_angle(), -45)

    def test_get_angle10(self):
        m = Matrix()
        m.rotate_self(-90)
        self.assertAlmostEqual(m.get_angle(), -90)

    def test_get_angle11(self):
        m = Matrix()
        m.rotate_self(-180)
        self.assertAlmostEqual(m.get_angle(), -180)

    def test_get_angle12(self):
        m = Matrix()
        m.rotate_self(-270)
        # returns 90.00000000000001
        self.assertAlmostEqual(m.get_angle(), (360 % 270))

    def test_get_angle13(self):
        m = Matrix()
        m.rotate_self(90, 24, 24)
        self.assertAlmostEqual(m.get_angle(), 90)

    def test_imul(self):
        m = Matrix()
        m.rotate_self(25, 100, 100)

        b = Matrix()
        b.scale_self(2, 1.5)
        m *= b

        b = Matrix()
        b.skewx_self(25)
        m *= b

        b = Matrix()
        b.translate_self(-100, -70)
        m *= b
        self.assertEqual(m.tostring(),
                         'matrix(1.813 0.845 0.211 1.754 -144.422 -240.168)')

    def test_inverse(self):
        formatter.precision = 4
        m = Matrix()
        m.translate_self(200, 40)
        m.scale_self(1.5)
        # (1.5, 0, 0, 1.5, 200, 40)
        i = m.inverse()
        # (0.6666666666666666, 0, 0,
        #  0.6666666666666666, -133.33333333333334, -26.666666666666668)
        self.assertEqual(m.tostring(),
                         'matrix(1.5 0 0 1.5 200 40)')
        self.assertEqual(i.tostring(),
                         'matrix(0.6667 0 0 0.6667 -133.3333 -26.6667)')

    def test_mul(self):
        m = Matrix()
        m.rotate_self(25, 100, 100)

        b = Matrix()
        b.scale_self(2, 1.5)
        m = m * b

        b = Matrix()
        b.skewx_self(25)
        m = m * b

        b = Matrix()
        b.translate_self(-100, -70)
        m = m * b
        self.assertEqual(m.tostring(),
                         'matrix(1.813 0.845 0.211 1.754 -144.422 -240.168)')

    def test_multiply(self):
        m = Matrix()
        m.rotate_self(25, 100, 100)
        m.scale_self(2, 1.5)
        m.skewx_self(25)
        m.translate_self(-100, -70)
        # a = 1.8126156330108643
        # b = 0.8452365398406982
        # c = 0.21130913496017456
        # d = 1.7536019086837769
        # e = -144.42214965820312
        # f = -240.16839599609375
        self.assertEqual(m.tostring(),
                         'matrix(1.813 0.845 0.211 1.754 -144.422 -240.168)')

    def test_rotate_scale01(self):
        # See also: RotateScale.html
        formatter.precision = 6
        m = Matrix()
        m.translate_self(50, 30)
        m.rotate_self(30)
        # (0.8660254037844387, 0.49999999999999994, -0.49999999999999994,
        #  0.8660254037844387, 50, 30)
        self.assertEqual(m.tostring(),
                         'matrix(0.866025 0.5 -0.5 0.866025 50 30)')

    def test_rotate_scale02(self):
        # See also: RotateScale.html
        formatter.precision = 6
        m = Matrix()
        m.translate_self(200, 40)
        m.scale_self(1.5)
        # (1.5, 0, 0, 1.5, 200, 40)
        self.assertEqual(m.tostring(),
                         'matrix(1.5 0 0 1.5 200 40)')

    def test_rotate01(self):
        # [[cosa -sina 0]
        #  [sina cosa 0]
        #  [0 0 1]]
        m = Matrix()
        m.rotate_self(45)
        r = math.radians(45)
        src = np.matrix([[math.cos(r), -math.sin(r), 0],
                         [math.sin(r), math.cos(r), 0],
                         [0, 0, 1]])
        self.assertTrue((src == m.matrix).all(), (src == m.matrix))
        self.assertAlmostEqual(m.get_angle(False), r)

    def test_rotate02(self):
        m = Matrix()
        m.rotate_self(-45, 24, 22)
        r = math.radians(-45)
        self.assertAlmostEqual(m.get_angle(False), r)
        # translate(-24 -22)
        src = np.matrix([[1, 0, -24], [0, 1, -22], [0, 0, 1]])
        # rotate(-45)
        src = np.matrix([[math.cos(r), -math.sin(r), 0],
                         [math.sin(r), math.cos(r), 0],
                         [0, 0, 1]]) * src
        # translate(24 22)
        src = np.matrix([[1, 0, 24], [0, 1, 22], [0, 0, 1]]) * src
        self.assertTrue((src == m.matrix).all(), (src == m.matrix))

    def test_scale01(self):
        # matrix(x 0 0 y 0 0)
        m = Matrix()
        m.scale_self(1.1, 1.2)
        m.scale_self(2)
        sx, sy = m.get_scale()
        self.assertEqual((sx, sy), (1.1 * 2, 1.2 * 2))
        src = np.matrix([[1.1 * 2, 0, 0], [0, 1.2 * 2, 0], [0, 0, 1]])
        self.assertTrue((src == m.matrix).all(), (src == m.matrix))

        newx, newy = m.point(0, 0)
        self.assertEqual((newx, newy), (0, 0))
        newx, newy = m.point(10, 10)
        self.assertEqual((newx, newy), (1.1 * 2 * 10, 1.2 * 2 * 10))

    def test_set_matrix(self):
        m = Matrix()
        m.set_matrix(1, 2, 3, 4, 5, 6)
        self.assertEqual(m.tostring(), 'matrix(1 2 3 4 5 6)')
        self.assertTrue((m.matrix == np.matrix(
            [[1, 3, 5], [2, 4, 6], [0, 0, 1]])).all())

    def test_tostring01(self):
        formatter.precision = 6
        m = Matrix(1.1, 2.1234, 3.5678, 4.9012, 5.8901, 6.000001)
        self.assertEqual(m.tostring(),
                         'matrix(1.1 2.1234 3.5678 4.9012 5.8901 6.000001)')
        self.assertTrue(
            (m.matrix == np.matrix(
                [[1.1, 3.5678, 5.8901],
                 [2.1234, 4.9012, 6.000001],
                 [0, 0, 1]])).all())

    def test_tostring02(self):
        formatter.precision = 6
        m = Matrix(1.8126156330108643,
                   0.8452365398406982,
                   0.21130913496017456,
                   1.7536019086837769,
                   -144.42214965820312,
                   -240.16839599609375)
        self.assertEqual(
            m.tostring(),
            "matrix(1.812616 0.845237 0.211309 1.753602 -144.42215"
            " -240.168396)")
        self.assertTrue(
            (m.matrix == np.matrix(
                [[1.8126156330108643, 0.21130913496017456, -144.42214965820312],
                 [0.8452365398406982, 1.7536019086837769, -240.16839599609375],
                 [0, 0, 1]])).all())

    def test_tostring03(self):
        m = Matrix(1, 2, 3, 4, 5, 6)
        self.assertEqual(m.tostring(delimiter=', '),
                         'matrix(1, 2, 3, 4, 5, 6)')

    def test_translate01(self):
        # matrix(1 0 0 1 x y)
        m = Matrix()
        m.translate_self(12, 16)
        tx, ty = m.get_translate()
        self.assertEqual((tx, ty), (12, 16))
        src = np.matrix([[1, 0, 12], [0, 1, 16], [0, 0, 1]])
        self.assertTrue((src == m.matrix).all(), (src == m.matrix))

        newx, newy = m.point(0, 0)
        self.assertEqual((newx, newy), (12, 16))
        newx, newy = m.point(10, 10)
        self.assertEqual((newx, newy), (12 + 10, 16 + 10))

        m.translate_self(4, 5)
        tx, ty = m.get_translate()
        self.assertEqual((tx, ty), (12 + 4, 16 + 5))
        src = np.matrix([[1, 0, 4], [0, 1, 5], [0, 0, 1]]) * src
        self.assertTrue((src == m.matrix).all(), (src == m.matrix))

        m.translate_self(-24)
        tx, ty = m.get_translate()
        self.assertEqual((tx, ty), (12 + 4 - 24, 16 + 5 + 0))
        src = np.matrix([[1, 0, -24], [0, 1, 0], [0, 0, 1]]) * src
        self.assertTrue((src == m.matrix).all(), (src == m.matrix))


if __name__ == '__main__':
    unittest.main()
