#!/usr/bin/env python3

import math
import sys
import unittest

import numpy as np

sys.path.extend(['.', '..'])

from svgpy import Matrix, formatter
from svgpy.matrix import matrix2d, matrix3d

places = 9


class MatrixTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_matrix2d(self):
        m = matrix2d(1, 2, 3, 4, 5, 6)
        self.assertTrue(
            (np.matrix([[1, 3, 0, 5],
                        [2, 4, 0, 6],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]) == m).all())

    def test_matrix3d(self):
        m = matrix3d(1, 2, 3, 4,
                     5, 6, 7, 8,
                     9, 10, 11, 12,
                     13, 14, 15, 16)
        self.assertTrue(
            (np.matrix([[1, 5, 9, 13],
                        [2, 6, 10, 14],
                        [3, 7, 11, 15],
                        [4, 8, 12, 16]]) == m).all())

    def test_attribute(self):
        m = Matrix()
        m.a = 1
        m.b = 2
        m.c = 3
        m.d = 4
        m.e = 5
        m.f = 6
        self.assertTrue(m.is2d)
        self.assertEqual(1, m.a)
        self.assertEqual(2, m.b)
        self.assertEqual(3, m.c)
        self.assertEqual(4, m.d)
        self.assertEqual(5, m.e)
        self.assertEqual(6, m.f)

    def test_attribute3d(self):
        m = Matrix(is2d=False)
        m.m11 = 1
        m.m12 = 2
        m.m13 = 3
        m.m14 = 4
        m.m21 = 5
        m.m22 = 6
        m.m23 = 7
        m.m24 = 8
        m.m31 = 9
        m.m32 = 10
        m.m33 = 11
        m.m34 = 12
        m.m41 = 13
        m.m42 = 14
        m.m43 = 15
        m.m44 = 16
        self.assertTrue(not m.is2d)
        self.assertEqual(1, m.m11)
        self.assertEqual(2, m.m12)
        self.assertEqual(3, m.m13)
        self.assertEqual(4, m.m14)
        self.assertEqual(5, m.m21)
        self.assertEqual(6, m.m22)
        self.assertEqual(7, m.m23)
        self.assertEqual(8, m.m24)
        self.assertEqual(9, m.m31)
        self.assertEqual(10, m.m32)
        self.assertEqual(11, m.m33)
        self.assertEqual(12, m.m34)
        self.assertEqual(13, m.m41)
        self.assertEqual(14, m.m42)
        self.assertEqual(15, m.m43)
        self.assertEqual(16, m.m44)

    def test_init(self):
        m = Matrix()
        self.assertEqual('matrix(1 0 0 1 0 0)', m.tostring())
        self.assertTrue(
            (np.matrix([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]) == m.matrix).all())

    def test_init3d(self):
        m = Matrix(is2d=False)
        self.assertEqual(
            'matrix3d(1 0 0 0 0 1 0 0 0 0 1 0 0 0 0 1)',
            m.tostring())
        self.assertTrue(
            (np.matrix([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]) == m.matrix).all())

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

    def test_init_type_error15(self):
        self.assertRaises(TypeError,
                          lambda: Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                         11, 12, 13, 14, 15))

    def test_init_type_error17(self):
        self.assertRaises(TypeError,
                          lambda: Matrix(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                         11, 12, 13, 14, 15, 16, 17))

    def test_flipx(self):
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        f = 6
        m = Matrix(a, b, c, d, e, f)
        o = m.flipx()
        self.assertEqual(-a, o.a)
        self.assertEqual(-b, o.b)
        self.assertEqual(c, o.c)
        self.assertEqual(d, o.d)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_flipx3d(self):
        m11 = 1
        m12 = 2
        m13 = 3
        m14 = 4
        m21 = 5
        m22 = 6
        m23 = 7
        m24 = 8
        m31 = 9
        m32 = 10
        m33 = 11
        m34 = 12
        m41 = 13
        m42 = 14
        m43 = 15
        m44 = 16
        m = Matrix(m11, m12, m13, m14,
                   m21, m22, m23, m24,
                   m31, m32, m33, m34,
                   m41, m42, m43, m44)
        o = m.flipx()
        self.assertEqual(-1, o.m11)
        self.assertEqual(-2, o.m12)
        self.assertEqual(-3, o.m13)
        self.assertEqual(-4, o.m14)
        self.assertEqual(5, o.m21)
        self.assertEqual(6, o.m22)
        self.assertEqual(7, o.m23)
        self.assertEqual(8, o.m24)
        self.assertEqual(9, o.m31)
        self.assertEqual(10, o.m32)
        self.assertEqual(11, o.m33)
        self.assertEqual(12, o.m34)
        self.assertEqual(13, o.m41)
        self.assertEqual(14, o.m42)
        self.assertEqual(15, o.m43)
        self.assertEqual(16, o.m44)

    def test_flipy(self):
        a = 1
        b = 2
        c = 3
        d = 4
        e = 5
        f = 6
        m = Matrix(a, b, c, d, e, f)
        m = m.flipy()
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(-c, m.c)
        self.assertEqual(-d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)

    def test_flipy3d(self):
        m11 = 1
        m12 = 2
        m13 = 3
        m14 = 4
        m21 = 5
        m22 = 6
        m23 = 7
        m24 = 8
        m31 = 9
        m32 = 10
        m33 = 11
        m34 = 12
        m41 = 13
        m42 = 14
        m43 = 15
        m44 = 16
        m = Matrix(m11, m12, m13, m14,
                   m21, m22, m23, m24,
                   m31, m32, m33, m34,
                   m41, m42, m43, m44)
        o = m.flipy()
        self.assertEqual(1, o.m11)
        self.assertEqual(2, o.m12)
        self.assertEqual(3, o.m13)
        self.assertEqual(4, o.m14)
        self.assertEqual(-5, o.m21)
        self.assertEqual(-6, o.m22)
        self.assertEqual(-7, o.m23)
        self.assertEqual(-8, o.m24)
        self.assertEqual(9, o.m31)
        self.assertEqual(10, o.m32)
        self.assertEqual(11, o.m33)
        self.assertEqual(12, o.m34)
        self.assertEqual(13, o.m41)
        self.assertEqual(14, o.m42)
        self.assertEqual(15, o.m43)
        self.assertEqual(16, o.m44)

    def test_frommatrix(self):
        src = np.matrix([[1, 3, 0, 5],
                         [2, 4, 0, 6],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        m = Matrix.frommatrix(src)
        self.assertTrue((src == m.matrix).all())
        self.assertEqual('matrix(1 2 3 4 5 6)', m.tostring())
        self.assertNotEqual(id(src), id(m.matrix))

    def test_frommatrix3d(self):
        src = np.matrix([[1, 5, 9, 13],
                         [2, 6, 10, 14],
                         [3, 7, 11, 15],
                         [4, 8, 12, 16]])
        m = Matrix.frommatrix(src)
        self.assertTrue((src == m.matrix).all())
        self.assertEqual(
            'matrix3d(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16)',
            m.tostring())
        self.assertNotEqual(id(src), id(m.matrix))

    def test_frommatrix_value_error(self):
        # not 4x4
        src = np.matrix([[1, 3, 5],
                         [2, 4, 6],
                         [0, 0, 1]])
        self.assertRaises(ValueError, lambda: Matrix.frommatrix(src))

    def test_get_angle01(self):
        m = Matrix()
        m.rotate_self(0, 0, 45)
        self.assertEqual(45, m.get_angle())

    def test_get_angle02(self):
        m = Matrix()
        m.rotate_self(0, 0, 90)
        self.assertEqual(90, m.get_angle())

    def test_get_angle03(self):
        m = Matrix()
        m.rotate_self(0, 0, 135)
        self.assertEqual(135, m.get_angle())

    def test_get_angle04(self):
        m = Matrix()
        m.rotate_self(0, 0, 180)
        self.assertEqual(180, m.get_angle())

    def test_get_angle05(self):
        m = Matrix()
        m.rotate_self(0, 0, 225)
        # returns -135.00000000000003
        self.assertAlmostEqual(-(360 % 225), m.get_angle())

    def test_get_angle06(self):
        m = Matrix()
        m.rotate_self(0, 0, 270)
        # returns -90.00000000000001
        self.assertAlmostEqual(-(360 % 270), m.get_angle())

    def test_get_angle07(self):
        m = Matrix()
        m.rotate_self(0, 0, 315)
        # returns -45.000000000000014
        self.assertAlmostEqual(-(360 % 315), m.get_angle())

    def test_get_angle08(self):
        m = Matrix()
        m.rotate_self(0, 0, 360)
        # returns -1.4033418597069752e-14
        self.assertAlmostEqual((360 % 360), m.get_angle())

    def test_get_angle09(self):
        m = Matrix()
        m.rotate_self(0, 0, -45)
        self.assertAlmostEqual(-45, m.get_angle())

    def test_get_angle10(self):
        m = Matrix()
        m.rotate_self(0, 0, -90)
        self.assertAlmostEqual(-90, m.get_angle())

    def test_get_angle11(self):
        m = Matrix()
        m.rotate_self(0, 0, -180)
        self.assertAlmostEqual(-180, m.get_angle())

    def test_get_angle12(self):
        m = Matrix()
        m.rotate_self(0, 0, -270)
        # returns 90.00000000000001
        self.assertAlmostEqual((360 % 270), m.get_angle())

    def test_get_angle13(self):
        m = Matrix()
        m.translate_self(24, 24)
        m.rotate_self(0, 0, 90)
        m.translate_self(-24, -24)
        self.assertAlmostEqual(90, m.get_angle())

    def test_imul(self):
        m = Matrix()
        r = Matrix()

        r *= m.translate(100, 100)
        r *= m.rotate(0, 0, 25)
        r *= m.translate(-100, -100)
        r *= m.scale(2, 1.5)
        r *= m.skewx(25)
        r *= m.translate(-100, -70)

        self.assertEqual(
            'matrix(1 0 0 1 0 0)',
            m.tostring())
        self.assertEqual(
            'matrix(1.813 0.845 0.211 1.754 -144.422 -240.168)',
            r.tostring())

    def test_inverse(self):
        formatter.precision = 4
        m = Matrix()
        m.translate_self(200, 40)
        m.scale_self(1.5)
        # (1.5, 0, 0, 1.5, 200, 40)
        i = m.inverse()
        # (0.6666666666666666, 0, 0,
        #  0.6666666666666666, -133.33333333333334, -26.666666666666668)
        self.assertEqual(
            'matrix(1.5 0 0 1.5 200 40)',
            m.tostring())
        self.assertEqual(
            'matrix(0.6667 0 0 0.6667 -133.3333 -26.6667)',
            i.tostring())

    def test_mul(self):
        m = Matrix()
        r = Matrix()

        r = r * m.translate(100, 100)
        r = r * m.rotate(0, 0, 25)
        r = r * m.translate(-100, -100)
        r = r * m.scale(2, 1.5)
        r = r * m.skewx(25)
        r = r * m.translate(-100, -70)

        self.assertEqual(
            'matrix(1 0 0 1 0 0)',
            m.tostring())
        self.assertEqual(
            'matrix(1.813 0.845 0.211 1.754 -144.422 -240.168)',
            r.tostring())

    def test_multiply01(self):
        m = Matrix()
        m.translate_self(100, 100)
        m.rotate_self(0, 0, 25)
        m.translate_self(-100, -100)
        m.scale_self(2, 1.5)
        m.skewx_self(25)
        m.translate_self(-100, -70)
        # a = 1.8126156330108643
        # b = 0.8452365398406982
        # c = 0.21130913496017456
        # d = 1.7536019086837769
        # e = -144.42214965820312
        # f = -240.16839599609375
        self.assertEqual(
            'matrix(1.813 0.845 0.211 1.754 -144.422 -240.168)',
            m.tostring())

    def test_multiply02(self):
        # See also: RotateScale.html
        formatter.precision = 6
        m = Matrix()
        m.translate_self(50, 30)
        m.rotate_self(0, 0, 30)
        # (0.8660254037844387, 0.49999999999999994, -0.49999999999999994,
        #  0.8660254037844387, 50, 30)
        self.assertEqual(
            'matrix(0.866025 0.5 -0.5 0.866025 50 30)',
            m.tostring())

    def test_multiply03(self):
        # See also: RotateScale.html
        formatter.precision = 6
        m = Matrix()
        m.translate_self(200, 40)
        m.scale_self(1.5)
        # (1.5, 0, 0, 1.5, 200, 40)
        self.assertEqual(
            'matrix(1.5 0 0 1.5 200 40)',
            m.tostring())

    def test_rotate01(self):
        m = Matrix()
        m.rotate_self(0, 0, 15)
        m.rotate_self(0, 0, 10)
        m.rotate_self(0, 0, 20)

        self.assertTrue(m.is2d)
        a = 0.7071067811865476
        b = 0.7071067811865475
        c = -0.7071067811865475
        d = 0.7071067811865476
        e = 0
        f = 0
        self.assertAlmostEqual(a, m.a, places=places)
        self.assertAlmostEqual(b, m.b, places=places)
        self.assertAlmostEqual(c, m.c, places=places)
        self.assertAlmostEqual(d, m.d, places=places)
        self.assertAlmostEqual(e, m.e, places=places)
        self.assertAlmostEqual(f, m.f, places=places)

        t = m.get_angle()
        self.assertAlmostEqual(45, t, places=places)

    def test_rotate02(self):
        m = Matrix()
        m.rotate_self(15)
        m.rotate_self(10)
        m.rotate_self(20)

        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 0.7071067811865476
        m23 = 0.7071067811865475
        m24 = 0
        m31 = 0
        m32 = -0.7071067811865475
        m33 = 0.7071067811865476
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        self.assertTrue(not m.is2d)
        self.assertAlmostEqual(m11, m.m11, places=places)
        self.assertAlmostEqual(m12, m.m12, places=places)
        self.assertAlmostEqual(m13, m.m13, places=places)
        self.assertAlmostEqual(m14, m.m14, places=places)
        self.assertAlmostEqual(m21, m.m21, places=places)
        self.assertAlmostEqual(m22, m.m22, places=places)
        self.assertAlmostEqual(m23, m.m23, places=places)
        self.assertAlmostEqual(m24, m.m24, places=places)
        self.assertAlmostEqual(m31, m.m31, places=places)
        self.assertAlmostEqual(m32, m.m32, places=places)
        self.assertAlmostEqual(m33, m.m33, places=places)
        self.assertAlmostEqual(m34, m.m34, places=places)
        self.assertAlmostEqual(m41, m.m41, places=places)
        self.assertAlmostEqual(m42, m.m42, places=places)
        self.assertAlmostEqual(m43, m.m43, places=places)
        self.assertAlmostEqual(m44, m.m44, places=places)

        rot_x, rot_y, rot_z = m.get_angle()
        self.assertAlmostEqual(45, rot_x, places=places)
        self.assertAlmostEqual(0, rot_y, places=places)
        self.assertAlmostEqual(0, rot_z, places=places)

    def test_rotate03(self):
        m = Matrix()
        m.rotate_self(0, 15)
        m.rotate_self(0, 10)
        m.rotate_self(0, 20)

        m11 = 0.7071067811865476
        m12 = 0
        m13 = -0.7071067811865475
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0.7071067811865475
        m32 = 0
        m33 = 0.7071067811865476
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        self.assertTrue(not m.is2d)
        self.assertAlmostEqual(m11, m.m11, places=places)
        self.assertAlmostEqual(m12, m.m12, places=places)
        self.assertAlmostEqual(m13, m.m13, places=places)
        self.assertAlmostEqual(m14, m.m14, places=places)
        self.assertAlmostEqual(m21, m.m21, places=places)
        self.assertAlmostEqual(m22, m.m22, places=places)
        self.assertAlmostEqual(m23, m.m23, places=places)
        self.assertAlmostEqual(m24, m.m24, places=places)
        self.assertAlmostEqual(m31, m.m31, places=places)
        self.assertAlmostEqual(m32, m.m32, places=places)
        self.assertAlmostEqual(m33, m.m33, places=places)
        self.assertAlmostEqual(m34, m.m34, places=places)
        self.assertAlmostEqual(m41, m.m41, places=places)
        self.assertAlmostEqual(m42, m.m42, places=places)
        self.assertAlmostEqual(m43, m.m43, places=places)
        self.assertAlmostEqual(m44, m.m44, places=places)

        rot_x, rot_y, rot_z = m.get_angle()
        self.assertAlmostEqual(0, rot_x, places=places)
        self.assertAlmostEqual(45, rot_y, places=places)
        self.assertAlmostEqual(0, rot_z, places=places)

    def test_rotate04(self):
        m = Matrix()
        m.rotate_self(15, 45, 90)

        m11 = 4.329780281177467e-17
        m12 = 0.7071067811865476
        m13 = -0.7071067811865475
        m14 = 0
        m21 = -0.9659258262890683
        m22 = 0.18301270189221935
        m23 = 0.18301270189221933
        m24 = 0
        m31 = 0.2588190451025208
        m32 = 0.6830127018922193
        m33 = 0.6830127018922194
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        self.assertTrue(not m.is2d)
        self.assertAlmostEqual(m11, m.m11, places=places)
        self.assertAlmostEqual(m12, m.m12, places=places)
        self.assertAlmostEqual(m13, m.m13, places=places)
        self.assertAlmostEqual(m14, m.m14, places=places)
        self.assertAlmostEqual(m21, m.m21, places=places)
        self.assertAlmostEqual(m22, m.m22, places=places)
        self.assertAlmostEqual(m23, m.m23, places=places)
        self.assertAlmostEqual(m24, m.m24, places=places)
        self.assertAlmostEqual(m31, m.m31, places=places)
        self.assertAlmostEqual(m32, m.m32, places=places)
        self.assertAlmostEqual(m33, m.m33, places=places)
        self.assertAlmostEqual(m34, m.m34, places=places)
        self.assertAlmostEqual(m41, m.m41, places=places)
        self.assertAlmostEqual(m42, m.m42, places=places)
        self.assertAlmostEqual(m43, m.m43, places=places)
        self.assertAlmostEqual(m44, m.m44, places=places)

        rot_x, rot_y, rot_z = m.get_angle()
        self.assertAlmostEqual(15, rot_x, places=places)
        self.assertAlmostEqual(45, rot_y, places=places)
        self.assertAlmostEqual(90, rot_z, places=places)

    def test_rotate05(self):
        m = Matrix()
        m.rotate_self(45, 45, 45)
        m.rotate_self(135, 90, 90)
        m.rotate_self(90, 135, 135)

        m11 = -0.875
        m12 = -0.22855339059327365
        m13 = 0.42677669529663675
        m14 = 0
        m21 = 0.22855339059327387
        m22 = 0.5821067811865475
        m23 = 0.7803300858899107
        m24 = 0
        m31 = -0.42677669529663687
        m32 = 0.7803300858899106
        m33 = -0.45710678118654746
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        self.assertTrue(not m.is2d)
        self.assertAlmostEqual(m11, m.m11, places=places)
        self.assertAlmostEqual(m12, m.m12, places=places)
        self.assertAlmostEqual(m13, m.m13, places=places)
        self.assertAlmostEqual(m14, m.m14, places=places)
        self.assertAlmostEqual(m21, m.m21, places=places)
        self.assertAlmostEqual(m22, m.m22, places=places)
        self.assertAlmostEqual(m23, m.m23, places=places)
        self.assertAlmostEqual(m24, m.m24, places=places)
        self.assertAlmostEqual(m31, m.m31, places=places)
        self.assertAlmostEqual(m32, m.m32, places=places)
        self.assertAlmostEqual(m33, m.m33, places=places)
        self.assertAlmostEqual(m34, m.m34, places=places)
        self.assertAlmostEqual(m41, m.m41, places=places)
        self.assertAlmostEqual(m42, m.m42, places=places)
        self.assertAlmostEqual(m43, m.m43, places=places)
        self.assertAlmostEqual(m44, m.m44, places=places)

    def test_scale01(self):
        # matrix(x 0 0 y 0 0)
        m = Matrix()
        m.scale_self(1.1, 1.2)
        m.scale_self(2)
        sx, sy = m.get_scale()
        self.assertEqual((1.1 * 2, 1.2 * 2), (sx, sy))

        src = np.matrix([[1.1 * 2, 0, 0, 0],
                         [0, 1.2 * 2, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        self.assertTrue((src == m.matrix).all())

        x, y = m.point(0, 0)
        self.assertEqual((0, 0), (x, y))

        x, y = m.point(10, 10)
        self.assertEqual((1.1 * 2 * 10, 1.2 * 2 * 10), (x, y))

    def test_set_matrix(self):
        m = Matrix()
        m.set_matrix(1, 2, 3, 4, 5, 6)
        self.assertTrue(m.is2d)
        self.assertEqual('matrix(1 2 3 4 5 6)', m.tostring())
        self.assertTrue((np.matrix(
            [[1, 3, 0, 5],
             [2, 4, 0, 6],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]) == m.matrix).all())

    def test_set_matrix3d(self):
        m = Matrix()
        m.set_matrix(1, 2, 3, 4,
                     5, 6, 7, 8,
                     9, 10, 11, 12,
                     13, 14, 15, 16)
        self.assertTrue(not m.is2d)
        self.assertEqual(
            'matrix3d(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16)',
            m.tostring())
        self.assertTrue((np.matrix(
            [[1, 5, 9, 13],
             [2, 6, 10, 14],
             [3, 7, 11, 15],
             [4, 8, 12, 16]]) == m.matrix).all())

    def test_tostring01(self):
        formatter.precision = 6
        m = Matrix(1.1, 2.1234, 3.5678, 4.9012, 5.8901, 6.000001)
        self.assertEqual(
            'matrix(1.1 2.1234 3.5678 4.9012 5.8901 6.000001)',
            m.tostring())

    def test_tostring02(self):
        formatter.precision = 6
        m = Matrix(1.8126156330108643,
                   0.8452365398406982,
                   0.21130913496017456,
                   1.7536019086837769,
                   -144.42214965820312,
                   -240.16839599609375)
        self.assertEqual(
            "matrix(1.812616 0.845237 0.211309 1.753602 -144.42215"
            " -240.168396)",
            m.tostring())

    def test_tostring03(self):
        m = Matrix(1, 2, 3, 4, 5, 6)
        self.assertEqual(
            'matrix(1, 2, 3, 4, 5, 6)',
            m.tostring(delimiter=', '))

    def test_translate(self):
        m = Matrix()
        m.translate_self(12, 16)
        tx, ty = m.get_translate()
        self.assertEqual((12, 16), (tx, ty))
        src = np.matrix([[1, 0, 0, 12],
                         [0, 1, 0, 16],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        self.assertTrue((src == m.matrix).all())

        x, y = m.point(0, 0)
        self.assertEqual((12, 16), (x, y))

        x, y = m.point(10, 10)
        self.assertEqual((12 + 10, 16 + 10), (x, y))

        m.translate_self(4, 5)
        tx, ty = m.get_translate()
        self.assertEqual((12 + 4, 16 + 5), (tx, ty))

        src = np.matrix([[1, 0, 0, 4],
                         [0, 1, 0, 5],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]) * src
        self.assertTrue((src == m.matrix).all())

        m.translate_self(-24)
        tx, ty = m.get_translate()
        self.assertEqual((12 + 4 - 24, 16 + 5 + 0), (tx, ty))

        src = np.matrix([[1, 0, 0, -24],
                         [0, 1, 0, 0],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]]) * src
        self.assertTrue((src == m.matrix).all())

    def test_translate3d(self):
        m = Matrix(is2d=False)
        m.translate_self(10, 20, 30)
        tx, ty, tz = m.get_translate()
        self.assertEqual((10, 20, 30), (tx, ty, tz))
        self.assertEqual(
            'matrix3d(1 0 0 0 0 1 0 0 0 0 1 0 10 20 30 1)',
            m.tostring())

        m.translate_self(10, 20, 30)
        tx, ty, tz = m.get_translate()
        self.assertEqual((20, 40, 60), (tx, ty, tz))
        self.assertEqual(
            'matrix3d(1 0 0 0 0 1 0 0 0 0 1 0 20 40 60 1)',
            m.tostring())

        m.translate_self(10, 20)
        tx, ty, tz = m.get_translate()
        self.assertEqual((30, 60, 60), (tx, ty, tz))
        self.assertEqual(
            'matrix3d(1 0 0 0 0 1 0 0 0 0 1 0 30 60 60 1)',
            m.tostring())


if __name__ == '__main__':
    unittest.main()
