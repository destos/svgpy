#!/usr/bin/env python3

import sys
import unittest

import numpy as np

sys.path.extend(['.', '..'])

from svgpy import DOMMatrix, DOMMatrixReadOnly, formatter
from svgpy.geometry.matrix import matrix2d, matrix3d

places = 9


class MatrixTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_eq(self):
        m1 = DOMMatrixReadOnly()
        m2 = DOMMatrix()
        self.assertEqual(m2, m1)

        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m1 = DOMMatrixReadOnly([m11, m12, m13, m14,
                                m21, m22, m23, m24,
                                m31, m32, m33, m34,
                                m41, m42, m43, m44])
        m2 = DOMMatrix([m11, m12, m13, m14,
                        m21, m22, m23, m24,
                        m31, m32, m33, m34,
                        m41, m42, m43, m44])
        self.assertEqual(m2, m1)

    def test_flip_x_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrix([a, b, c, d, e, f])
        o = m.flip_x()
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(o.is2d)
        self.assertEqual(-a, o.a)
        self.assertEqual(-b, o.b)
        self.assertEqual(c, o.c)
        self.assertEqual(d, o.d)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_flip_x_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrix([m11, m12, m13, m14,
                       m21, m22, m23, m24,
                       m31, m32, m33, m34,
                       m41, m42, m43, m44])
        o = m.flip_x()
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(-m11, o.m11)
        self.assertEqual(-m12, o.m12)
        self.assertEqual(-m13, o.m13)
        self.assertEqual(-m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_flip_y_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrix([a, b, c, d, e, f])
        o = m.flip_y()
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertEqual(a, o.a)
        self.assertEqual(b, o.b)
        self.assertEqual(-c, o.c)
        self.assertEqual(-d, o.d)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_flip_y_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrix([m11, m12, m13, m14,
                       m21, m22, m23, m24,
                       m31, m32, m33, m34,
                       m41, m42, m43, m44])
        o = m.flip_y()
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(-m21, o.m21)
        self.assertEqual(-m22, o.m22)
        self.assertEqual(-m23, o.m23)
        self.assertEqual(-m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_from_array_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        m = DOMMatrix.from_float_array([a, b, c, d, e, f])
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertIsInstance(m, DOMMatrix)
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_from_array_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrix.from_float_array([m11, m12, m13, m14,
                                        m21, m22, m23, m24,
                                        m31, m32, m33, m34,
                                        m41, m42, m43, m44])
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertIsInstance(m, DOMMatrix)
        self.assertFalse(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_from_matrix_2d01(self):
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        m = DOMMatrix.from_matrix({'a': a,
                                   'b': b,
                                   'c': c,
                                   'd': d,
                                   'e': e,
                                   'f': f})
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertIsInstance(m, DOMMatrix)
        self.assertTrue(m.is2d)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)

    def test_from_matrix_3d01(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrix.from_matrix({'m11': m11,
                                   'm12': m12,
                                   'm13': m13,
                                   'm14': m14,
                                   'm21': m21,
                                   'm22': m22,
                                   'm23': m23,
                                   'm24': m24,
                                   'm31': m31,
                                   'm32': m32,
                                   'm33': m33,
                                   'm34': m34,
                                   'm41': m41,
                                   'm42': m42,
                                   'm43': m43,
                                   'm44': m44,
                                   })
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertIsInstance(m, DOMMatrix)
        self.assertFalse(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_get_angle01(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 45)
        self.assertEqual(45, m.get_angle())

    def test_get_angle02(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 90)
        self.assertEqual(90, m.get_angle())

    def test_get_angle03(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 135)
        self.assertEqual(135, m.get_angle())

    def test_get_angle04(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 180)
        self.assertEqual(180, m.get_angle())

    def test_get_angle05(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 225)
        # returns -135.00000000000003
        self.assertAlmostEqual(-(360 % 225), m.get_angle())

    def test_get_angle06(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 270)
        # returns -90.00000000000001
        self.assertAlmostEqual(-(360 % 270), m.get_angle())

    def test_get_angle07(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 315)
        # returns -45.000000000000014
        self.assertAlmostEqual(-(360 % 315), m.get_angle())

    def test_get_angle08(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, 360)
        # returns -1.4033418597069752e-14
        self.assertAlmostEqual((360 % 360), m.get_angle())

    def test_get_angle09(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, -45)
        self.assertAlmostEqual(-45, m.get_angle())

    def test_get_angle10(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, -90)
        self.assertAlmostEqual(-90, m.get_angle())

    def test_get_angle11(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, -180)
        self.assertAlmostEqual(-180, m.get_angle())

    def test_get_angle12(self):
        m = DOMMatrix()
        m.rotate_self(0, 0, -270)
        # returns 90.00000000000001
        self.assertAlmostEqual((360 % 270), m.get_angle())

    def test_get_angle13(self):
        m = DOMMatrix()
        m.translate_self(24, 24)
        m.rotate_self(0, 0, 90)
        m.translate_self(-24, -24)
        self.assertAlmostEqual(90, m.get_angle())

    def test_imul(self):
        m = DOMMatrix()
        r = DOMMatrix()

        r *= m.translate(100, 100)
        r *= m.rotate(0, 0, 25)
        r *= m.translate(-100, -100)
        r *= m.scale(2, 1.5)
        r *= m.skew_x(25)
        r *= m.translate(-100, -70)

        self.assertEqual(
            'matrix(1, 0, 0, 1, 0, 0)',
            m.tostring())
        self.assertEqual(
            'matrix(1.813, 0.845, 0.211, 1.754, -144.422, -240.168)',
            r.tostring())

    def test_init_2d(self):
        m = DOMMatrix()
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        self.assertTrue(m.is2d)
        self.assertTrue(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

        self.assertEqual('matrix(1, 0, 0, 1, 0, 0)',
                         m.tostring())
        self.assertTrue(
            (np.matrix([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]) == m.matrix).all())

    def test_init_3d(self):
        m = DOMMatrix(is2d=False)
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        self.assertFalse(m.is2d)
        self.assertTrue(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

        self.assertEqual(
            'matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1)',
            m.tostring())
        self.assertTrue(
            (np.matrix([[1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, 0],
                        [0, 0, 0, 1]]) == m.matrix).all())

    def test_init_from_array_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrix([a, b, c, d, e, f])
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_init_from_array_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrix([m11, m12, m13, m14,
                       m21, m22, m23, m24,
                       m31, m32, m33, m34,
                       m41, m42, m43, m44])
        self.assertFalse(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_init_from_array_error(self):
        self.assertRaises(TypeError,
                          lambda: DOMMatrix([1]))

        self.assertRaises(TypeError,
                          lambda: DOMMatrix([1, 2, 3, 4, 5]))

        self.assertRaises(TypeError,
                          lambda: DOMMatrix([1, 2, 3, 4, 5, 6, 7]))

        self.assertRaises(TypeError,
                          lambda: DOMMatrix([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                             11, 12, 13, 14, 15]))

        self.assertRaises(TypeError,
                          lambda: DOMMatrix([1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
                                             11, 12, 13, 14, 15, 16, 17]))

    def test_inverse(self):
        formatter.precision = 4
        m = DOMMatrix()
        m.translate_self(200, 40)
        m.scale_self(1.5)
        # (1.5, 0, 0, 1.5, 200, 40)
        i = m.inverse()
        # (0.6666666666666666, 0, 0,
        #  0.6666666666666666, -133.33333333333334, -26.666666666666668)
        self.assertEqual(
            'matrix(1.5, 0, 0, 1.5, 200, 40)',
            m.tostring())
        self.assertEqual(
            'matrix(0.6667, 0, 0, 0.6667, -133.3333, -26.6667)',
            i.tostring())

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

    def test_mul(self):
        m = DOMMatrix()
        r = DOMMatrix()

        r = r * m.translate(100, 100)
        r = r * m.rotate(0, 0, 25)
        r = r * m.translate(-100, -100)
        r = r * m.scale(2, 1.5)
        r = r * m.skew_x(25)
        r = r * m.translate(-100, -70)

        self.assertEqual(
            'matrix(1, 0, 0, 1, 0, 0)',
            m.tostring())
        self.assertEqual(
            'matrix(1.813, 0.845, 0.211, 1.754, -144.422, -240.168)',
            r.tostring())

    def test_multiply01(self):
        m = DOMMatrix()
        m.translate_self(100, 100)
        m.rotate_self(0, 0, 25)
        m.translate_self(-100, -100)
        m.scale_self(2, 1.5)
        m.skew_x_self(25)
        m.translate_self(-100, -70)
        # a = 1.8126156330108643
        # b = 0.8452365398406982
        # c = 0.21130913496017456
        # d = 1.7536019086837769
        # e = -144.42214965820312
        # f = -240.16839599609375
        self.assertEqual(
            'matrix(1.813, 0.845, 0.211, 1.754, -144.422, -240.168)',
            m.tostring())

    def test_multiply02(self):
        # See also: RotateScale.html
        formatter.precision = 6
        m = DOMMatrix()
        m.translate_self(50, 30)
        m.rotate_self(0, 0, 30)
        # (0.8660254037844387, 0.49999999999999994, -0.49999999999999994,
        #  0.8660254037844387, 50, 30)
        self.assertEqual(
            'matrix(0.866025, 0.5, -0.5, 0.866025, 50, 30)',
            m.tostring())

    def test_multiply03(self):
        # See also: RotateScale.html
        formatter.precision = 6
        m = DOMMatrix()
        m.translate_self(200, 40)
        m.scale_self(1.5)
        # (1.5, 0, 0, 1.5, 200, 40)
        self.assertEqual(
            'matrix(1.5, 0, 0, 1.5, 200, 40)',
            m.tostring())

    def test_property_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        m = DOMMatrix()
        m.a = a
        m.b = b
        m.c = c
        m.d = d
        m.e = e
        m.f = f
        self.assertTrue(m.is2d)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_property_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrix(is2d=False)
        m.m11 = m11
        m.m12 = m12
        m.m13 = m13
        m.m14 = m14
        m.m21 = m21
        m.m22 = m22
        m.m23 = m23
        m.m24 = m24
        m.m31 = m31
        m.m32 = m32
        m.m33 = m33
        m.m34 = m34
        m.m41 = m41
        m.m42 = m42
        m.m43 = m43
        m.m44 = m44
        self.assertFalse(m.is2d)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_property_is2d(self):
        m = DOMMatrix()
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.a = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.b = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.c = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.d = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.e = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.f = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m11 = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m12 = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m13 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m14 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m21 = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m22 = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m23 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m24 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m31 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m32 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m33 = 0
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m34 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m41 = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m42 = 1
        self.assertTrue(m.is2d)

        m = DOMMatrix()
        m.m43 = 1
        self.assertFalse(m.is2d)  # 3d

        m = DOMMatrix()
        m.m44 = 0
        self.assertFalse(m.is2d)  # 3d

    def test_read_only_flip_x_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly([a, b, c, d, e, f])
        o = m.flip_x()
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(o.is2d)
        self.assertEqual(-a, o.a)
        self.assertEqual(-b, o.b)
        self.assertEqual(c, o.c)
        self.assertEqual(d, o.d)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_read_only_flip_x_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrixReadOnly([m11, m12, m13, m14,
                               m21, m22, m23, m24,
                               m31, m32, m33, m34,
                               m41, m42, m43, m44])
        o = m.flip_x()
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(-m11, o.m11)
        self.assertEqual(-m12, o.m12)
        self.assertEqual(-m13, o.m13)
        self.assertEqual(-m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_flip_y_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly([a, b, c, d, e, f])
        o = m.flip_y()
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertEqual(a, o.a)
        self.assertEqual(b, o.b)
        self.assertEqual(-c, o.c)
        self.assertEqual(-d, o.d)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_read_only_flip_y_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrixReadOnly([m11, m12, m13, m14,
                               m21, m22, m23, m24,
                               m31, m32, m33, m34,
                               m41, m42, m43, m44])
        o = m.flip_y()
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(-m21, o.m21)
        self.assertEqual(-m22, o.m22)
        self.assertEqual(-m23, o.m23)
        self.assertEqual(-m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_from_array_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        m = DOMMatrixReadOnly.from_float_array([a, b, c, d, e, f])
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertNotIsInstance(m, DOMMatrix)
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_from_array_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrixReadOnly.from_float_array([m11, m12, m13, m14,
                                                m21, m22, m23, m24,
                                                m31, m32, m33, m34,
                                                m41, m42, m43, m44])
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertNotIsInstance(m, DOMMatrix)
        self.assertFalse(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_from_matrix_2d01(self):
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        m = DOMMatrixReadOnly.from_matrix({'a': a,
                                           'b': b,
                                           'c': c,
                                           'd': d,
                                           'e': e,
                                           'f': f})
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertNotIsInstance(m, DOMMatrix)
        self.assertTrue(m.is2d)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)

    def test_read_only_from_matrix_2d02(self):
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        m = DOMMatrixReadOnly.from_matrix({'a': a,
                                           'b': b,
                                           'c': c,
                                           'd': d,
                                           'e': e,
                                           'f': f,
                                           'is2d': True,
                                           })
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertNotIsInstance(m, DOMMatrix)
        self.assertTrue(m.is2d)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)

    def test_read_only_from_matrix_3d01(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrixReadOnly.from_matrix({'m11': m11,
                                           'm12': m12,
                                           'm13': m13,
                                           'm14': m14,
                                           'm21': m21,
                                           'm22': m22,
                                           'm23': m23,
                                           'm24': m24,
                                           'm31': m31,
                                           'm32': m32,
                                           'm33': m33,
                                           'm34': m34,
                                           'm41': m41,
                                           'm42': m42,
                                           'm43': m43,
                                           'm44': m44,
                                           })
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertNotIsInstance(m, DOMMatrix)
        self.assertFalse(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_from_matrix_3d02(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrixReadOnly.from_matrix({'m11': m11,
                                           'm12': m12,
                                           'm13': m13,
                                           'm14': m14,
                                           'm21': m21,
                                           'm22': m22,
                                           'm23': m23,
                                           'm24': m24,
                                           'm31': m31,
                                           'm32': m32,
                                           'm33': m33,
                                           'm34': m34,
                                           'm41': m41,
                                           'm42': m42,
                                           'm43': m43,
                                           'm44': m44,
                                           'is2d': False,
                                           })
        self.assertIsInstance(m, DOMMatrixReadOnly)
        self.assertNotIsInstance(m, DOMMatrix)
        self.assertFalse(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_2d(self):
        m = DOMMatrixReadOnly()
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        self.assertTrue(m.is2d)
        self.assertTrue(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_3d(self):
        m = DOMMatrixReadOnly(is2d=False)
        a = 1
        b = 0
        c = 0
        d = 1
        e = 0
        f = 0
        self.assertFalse(m.is2d)
        self.assertTrue(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_array_2d(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly([a, b, c, d, e, f])
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_array_3d(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrixReadOnly([m11, m12, m13, m14,
                               m21, m22, m23, m24,
                               m31, m32, m33, m34,
                               m41, m42, m43, m44])
        self.assertFalse(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_array_error(self):
        # invalid length:
        # DOMMatrixReadOnly([1, 0, 0, 1, 0])
        # 2d, 6 elements
        self.assertRaises(TypeError,
                          lambda: DOMMatrixReadOnly([1, 0, 0, 1, 0]))

        # [2d, 6 elements] or [3d, 16 elements]
        self.assertRaises(TypeError,
                          lambda: DOMMatrixReadOnly([11, 12, 13, 14,
                                                     21, 22, 23]))

        # 3d, 16 elements
        self.assertRaises(TypeError,
                          lambda: DOMMatrixReadOnly([11, 12, 13, 14,
                                                     21, 22, 23, 24,
                                                     31, 32, 33, 34,
                                                     41, 42, 43, 44,
                                                     51]))

    def test_read_only_init_from_matrix_2d01(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly(a=a, b=b, c=c, d=d, e=e, f=f)
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_matrix_2d02(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly(a=a, b=b, c=c, d=d, e=e, f=f, is2d=True)
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_matrix_2d03(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly(m11=a, m12=b, m21=c, m22=d, m41=e, m42=f)
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_matrix_2d04(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        m = DOMMatrixReadOnly(m11=a, m12=b, m21=c, m22=d, m41=e, m42=f,
                              is2d=True)
        self.assertTrue(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        m11 = a
        m12 = b
        m13 = 0
        m14 = 0
        m21 = c
        m22 = d
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = e
        m42 = f
        m43 = 0
        m44 = 1
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_matrix_3d01(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrixReadOnly(m11=m11, m12=m12, m13=m13, m14=m14,
                              m21=m21, m22=m22, m23=m23, m24=m24,
                              m31=m31, m32=m32, m33=m33, m34=m34,
                              m41=m41, m42=m42, m43=m43, m44=m44)
        self.assertFalse(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_matrix_3d02(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        a = m11
        b = m12
        c = m21
        d = m22
        e = m41
        f = m42
        m = DOMMatrixReadOnly(m11=m11, m12=m12, m13=m13, m14=m14,
                              m21=m21, m22=m22, m23=m23, m24=m24,
                              m31=m31, m32=m32, m33=m33, m34=m34,
                              m41=m41, m42=m42, m43=m43, m44=m44,
                              is2d=False)
        self.assertFalse(m.is2d)
        self.assertFalse(m.isidentity)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)

    def test_read_only_init_from_matrix_error(self):
        # validation error:
        # a == m11
        # DOMMatrixReadOnly(a=1, m11=11)
        m = DOMMatrixReadOnly(a=11, m11=11)
        self.assertEqual(m.a, m.m11)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(a=1, m11=11))

        # b == m12
        m = DOMMatrixReadOnly(b=12, m12=12)
        self.assertEqual(m.b, m.m12)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(b=0, m12=12))

        # c == m21
        m = DOMMatrixReadOnly(c=21, m21=21)
        self.assertEqual(m.c, m.m21)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(c=0, m21=21))

        # d == m22
        m = DOMMatrixReadOnly(d=22, m22=22)
        self.assertEqual(m.d, m.m22)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(d=1, m22=22))

        # e == m41
        m = DOMMatrixReadOnly(e=41, m41=41)
        self.assertEqual(m.e, m.m41)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(e=0, m41=41))

        # f == m42
        m = DOMMatrixReadOnly(f=42, m42=42)
        self.assertEqual(m.f, m.m42)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(f=0, m42=42))

        # 2d, m13 == 0
        # DOMMatrixReadOnly(is2d=True, m13=1)
        m = DOMMatrixReadOnly(is2d=True, m13=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m13=1))

        # 2d, m14 == 0
        m = DOMMatrixReadOnly(is2d=True, m14=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m14=1))

        # 2d, m23 == 0
        m = DOMMatrixReadOnly(is2d=True, m23=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m23=1))

        # 2d, m24 == 0
        m = DOMMatrixReadOnly(is2d=True, m24=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m24=1))

        # 2d, m31 == 0
        m = DOMMatrixReadOnly(is2d=True, m31=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m31=1))

        # 2d, m32 == 0
        m = DOMMatrixReadOnly(is2d=True, m32=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m32=1))

        # 2d, m34 == 0
        m = DOMMatrixReadOnly(is2d=True, m34=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m34=1))

        # 2d, m43 == 0
        m = DOMMatrixReadOnly(is2d=True, m43=-0)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m43=1))

        # 2d, m33 == 1
        m = DOMMatrixReadOnly(is2d=True, m33=1)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m33=0))

        # 2d, m44 == 1
        m = DOMMatrixReadOnly(is2d=True, m44=1)
        self.assertTrue(m.is2d)
        self.assertRaises(ValueError,
                          lambda: DOMMatrixReadOnly(is2d=True, m44=0))

        # invalid keyword:
        # DOMMatrixReadOnly(m100=100)
        self.assertRaises(TypeError,
                          lambda: DOMMatrixReadOnly(m100=100))

    def test_read_only_inverse(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        tx = 100
        ty = 200
        tz = -100
        m = DOMMatrixReadOnly([m11, m12, m13, m14,
                               m21, m22, m23, m24,
                               m31, m32, m33, m34,
                               m41, m42, m43, m44])
        o = m.translate(tx, ty, tz)
        o = o.inverse()
        self.assertFalse(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m41 = -tx
        m42 = -ty
        m43 = -tz
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_imul(self):
        m = DOMMatrixReadOnly()
        r = DOMMatrixReadOnly()
        m *= r
        self.assertIsNone(m)

        m = DOMMatrixReadOnly()
        r = DOMMatrix()
        m *= r
        self.assertIsNone(m)

    def test_read_only_rotate_axis_angle_x(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        x = 100
        y = 0
        z = 0
        angle = 45
        m = DOMMatrixReadOnly()
        o = m.rotate_axis_angle(x, y, z, angle)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m22 = 0.7071067811865476
        m23 = 0.7071067811865476
        m32 = -0.7071067811865476
        m33 = 0.7071067811865476
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_axis_angle_y(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        x = 0
        y = 100
        z = 0
        angle = 45
        m = DOMMatrixReadOnly()
        o = m.rotate_axis_angle(x, y, z, angle)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 = 0.7071067811865476
        m13 = -0.7071067811865476
        m31 = 0.7071067811865476
        m33 = 0.7071067811865476
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_axis_angle_z(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        x = 0
        y = 0
        z = 100
        angle = 45
        m = DOMMatrixReadOnly()
        o = m.rotate_axis_angle(x, y, z, angle)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 = 0.7071067811865476
        m12 = 0.7071067811865476
        m21 = -0.7071067811865476
        m22 = 0.7071067811865476
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_axis_angle_xyz(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        x = 100
        y = 100
        z = 100
        angle = 45
        m = DOMMatrixReadOnly()
        o = m.rotate_axis_angle(x, y, z, angle)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 = 0.804737854124365
        m12 = 0.5058793634016805
        m13 = -0.31061721752604554
        m21 = -0.31061721752604554
        m22 = 0.804737854124365
        m23 = 0.5058793634016805
        m31 = 0.5058793634016805
        m32 = -0.31061721752604554
        m33 = 0.804737854124365
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_x(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        rot_x = 45
        rot_y = 0
        rot_z = 0
        m = DOMMatrixReadOnly()
        o = m.rotate(rot_x, rot_y, rot_z)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m22 = 0.7071067811865476
        m23 = 0.7071067811865476
        m32 = -0.7071067811865476
        m33 = 0.7071067811865476
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_xyz(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        rot_x = 45
        rot_y = 45
        rot_z = 45
        m = DOMMatrixReadOnly()
        o = m.rotate(rot_x, rot_y, rot_z)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 = 0.5000000000000001
        m12 = 0.5000000000000001
        m13 = -0.7071067811865476
        m21 = -0.14644660940672627
        m22 = 0.853553390593274
        m23 = 0.5000000000000001
        m31 = 0.853553390593274
        m32 = -0.14644660940672627
        m33 = 0.5000000000000001
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_y(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        rot_x = 0
        rot_y = 45
        rot_z = 0
        m = DOMMatrixReadOnly()
        o = m.rotate(rot_x, rot_y, rot_z)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 = 0.7071067811865476
        m13 = -0.7071067811865476
        m31 = 0.7071067811865476
        m33 = 0.7071067811865476
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_rotate_z(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        rot_x = 0
        rot_y = 0
        rot_z = 45
        m = DOMMatrixReadOnly()
        o = m.rotate(rot_x, rot_y, rot_z)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 = 0.7071067811865476
        m12 = 0.7071067811865476
        m21 = -0.7071067811865476
        m22 = 0.7071067811865476
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(o.is2d)
        self.assertAlmostEqual(m11, o.m11, places=places)
        self.assertAlmostEqual(m12, o.m12, places=places)
        self.assertAlmostEqual(m13, o.m13, places=places)
        self.assertEqual(m14, o.m14)
        self.assertAlmostEqual(m21, o.m21, places=places)
        self.assertAlmostEqual(m22, o.m22, places=places)
        self.assertAlmostEqual(m23, o.m23, places=places)
        self.assertEqual(m24, o.m24)
        self.assertAlmostEqual(m31, o.m31, places=places)
        self.assertAlmostEqual(m32, o.m32, places=places)
        self.assertAlmostEqual(m33, o.m33, places=places)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_scale(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        sx = 1.1
        sy = 1.2
        sz = 1.3
        ox = 10
        oy = 20
        oz = 30
        m = DOMMatrixReadOnly()
        o = m.scale(sx, sy, sz, ox, oy, oz)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 *= sx
        m22 *= sy
        m33 *= sz
        m41 = -1
        m42 = -4
        m43 = -9
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_read_only_skew_x(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        angle = 45
        m = DOMMatrixReadOnly([a, b, c, d, e, f])
        o = m.skew_x(angle)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        c = 32
        d = 34
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(o.is2d)
        self.assertEqual(a, o.a)
        self.assertEqual(b, o.b)
        self.assertAlmostEqual(c, o.c, places=places)
        self.assertAlmostEqual(d, o.d, places=places)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_read_only_skew_y(self):
        a = 11
        b = 12
        c = 21
        d = 22
        e = 41
        f = 42
        angle = 45
        m = DOMMatrixReadOnly([a, b, c, d, e, f])
        o = m.skew_y(angle)
        self.assertEqual(a, m.a)
        self.assertEqual(b, m.b)
        self.assertEqual(c, m.c)
        self.assertEqual(d, m.d)
        self.assertEqual(e, m.e)
        self.assertEqual(f, m.f)
        a = 31.999999999999996
        b = 34
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(o.is2d)
        self.assertAlmostEqual(a, o.a, places=places)
        self.assertAlmostEqual(b, o.b, places=places)
        self.assertEqual(c, o.c)
        self.assertEqual(d, o.d)
        self.assertEqual(e, o.e)
        self.assertEqual(f, o.f)

    def test_read_only_translate(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 100
        m42 = 200
        m43 = 300
        m44 = 1
        m = DOMMatrixReadOnly.from_matrix({'m41': m41,
                                           'm42': m42,
                                           'm43': m43,
                                           })
        x = 10
        y = 20
        z = 30
        o = m.translate(x, y, z)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m41 += x
        m42 += y
        m43 += z
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

    def test_rotate_self01(self):
        m = DOMMatrix()
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

    def test_rotate_self02(self):
        m = DOMMatrix()
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
        self.assertFalse(m.is2d)
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

    def test_rotate_self03(self):
        m = DOMMatrix()
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

    def test_rotate_self04(self):
        m = DOMMatrix()
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

    def test_rotate_self05(self):
        m = DOMMatrix()
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

    def test_rotate_from_vector_self(self):
        m11 = 0.44721359549995804
        m12 = 0.8944271909999159
        m13 = 0
        m14 = 0
        m21 = -0.8944271909999159
        m22 = 0.44721359549995804
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        x = 1
        y = 2
        m = DOMMatrix()
        o = m.rotate_from_vector_self(x, y)
        self.assertEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertTrue(m.is2d)
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

    def test_scale(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        m41 = 0
        m42 = 0
        m43 = 0
        m44 = 1
        sx = 1.1
        sy = 1.2
        sz = 1.3
        ox = 10
        oy = 20
        oz = 30
        m = DOMMatrix()
        o = m.scale(sx, sy, sz, ox, oy, oz)
        o = o.scale(sx, sy, sz, ox, oy, oz)
        self.assertTrue(m.is2d)
        self.assertEqual(m11, m.m11)
        self.assertEqual(m12, m.m12)
        self.assertEqual(m13, m.m13)
        self.assertEqual(m14, m.m14)
        self.assertEqual(m21, m.m21)
        self.assertEqual(m22, m.m22)
        self.assertEqual(m23, m.m23)
        self.assertEqual(m24, m.m24)
        self.assertEqual(m31, m.m31)
        self.assertEqual(m32, m.m32)
        self.assertEqual(m33, m.m33)
        self.assertEqual(m34, m.m34)
        self.assertEqual(m41, m.m41)
        self.assertEqual(m42, m.m42)
        self.assertEqual(m43, m.m43)
        self.assertEqual(m44, m.m44)
        m11 *= sx * sx
        m22 *= sy * sy
        m33 *= sz * sz
        m41 = -2.1000000000000014
        m42 = -8.799999999999997
        m43 = -20.700000000000003
        self.assertNotEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

        _sx, _sy = m.get_scale()
        self.assertEqual(1, _sx)
        self.assertEqual(1, _sy)

        _sx, _sy, _sz = o.get_scale()
        self.assertEqual(sx * sx, _sx)
        self.assertEqual(sy * sy, _sy)
        self.assertEqual(sz * sz, _sz)

    def test_scale3d_self(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        # m41 = 0
        # m42 = 0
        # m43 = 0
        m44 = 1
        scale = 1.1
        ox = 10
        oy = 20
        oz = 30
        m = DOMMatrix()
        o = m.scale3d_self(scale, ox, oy, oz)
        o = o.scale3d_self(scale, ox, oy, oz)
        m11 *= scale * scale
        m22 *= scale * scale
        m33 *= scale * scale
        m41 = -2.1000000000000014
        m42 = -4.200000000000003
        m43 = -6.300000000000004
        self.assertEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

        _sx, _sy, _sz = o.get_scale()
        self.assertEqual(scale * scale, _sx)
        self.assertEqual(scale * scale, _sy)
        self.assertEqual(scale * scale, _sz)

    def test_scale_self(self):
        m11 = 1
        m12 = 0
        m13 = 0
        m14 = 0
        m21 = 0
        m22 = 1
        m23 = 0
        m24 = 0
        m31 = 0
        m32 = 0
        m33 = 1
        m34 = 0
        # m41 = 0
        # m42 = 0
        # m43 = 0
        m44 = 1
        sx = 1.1
        sy = 1.2
        sz = 1.3
        ox = 10
        oy = 20
        oz = 30
        m = DOMMatrix()
        o = m.scale_self(sx, sy, sz, ox, oy, oz)
        o = o.scale_self(sx, sy, sz, ox, oy, oz)
        m11 *= sx * sx
        m22 *= sy * sy
        m33 *= sz * sz
        m41 = -2.1000000000000014
        m42 = -8.799999999999997
        m43 = -20.700000000000003
        self.assertEqual(id(o), id(m))
        self.assertIsInstance(o, DOMMatrix)
        self.assertFalse(o.is2d)
        self.assertEqual(m11, o.m11)
        self.assertEqual(m12, o.m12)
        self.assertEqual(m13, o.m13)
        self.assertEqual(m14, o.m14)
        self.assertEqual(m21, o.m21)
        self.assertEqual(m22, o.m22)
        self.assertEqual(m23, o.m23)
        self.assertEqual(m24, o.m24)
        self.assertEqual(m31, o.m31)
        self.assertEqual(m32, o.m32)
        self.assertEqual(m33, o.m33)
        self.assertEqual(m34, o.m34)
        self.assertEqual(m41, o.m41)
        self.assertEqual(m42, o.m42)
        self.assertEqual(m43, o.m43)
        self.assertEqual(m44, o.m44)

        _sx, _sy, _sz = o.get_scale()
        self.assertEqual(sx * sx, _sx)
        self.assertEqual(sy * sy, _sy)
        self.assertEqual(sz * sz, _sz)

    def test_tostring01(self):
        formatter.precision = 6
        m = DOMMatrix([1.1, 2.1234, 3.5678, 4.9012, 5.8901, 6.000001])
        self.assertEqual(
            'matrix(1.1, 2.1234, 3.5678, 4.9012, 5.8901, 6.000001)',
            m.tostring())
        self.assertEqual(
            'matrix(1.1 2.1234 3.5678 4.9012 5.8901 6.000001)',
            m.tostring(delimiter=' '))

    def test_tojson(self):
        m11 = 11
        m12 = 12
        m13 = 13
        m14 = 14
        m21 = 21
        m22 = 22
        m23 = 23
        m24 = 24
        m31 = 31
        m32 = 32
        m33 = 33
        m34 = 34
        m41 = 41
        m42 = 42
        m43 = 43
        m44 = 44
        m = DOMMatrixReadOnly([m11, m12, m13, m14,
                               m21, m22, m23, m24,
                               m31, m32, m33, m34,
                               m41, m42, m43, m44])
        json = m.tojson()
        o = DOMMatrix.from_matrix(json)
        self.assertEqual(o, m)

    def test_tostring02(self):
        formatter.precision = 6
        m = DOMMatrix([1.8126156330108643,
                       0.8452365398406982,
                       0.21130913496017456,
                       1.7536019086837769,
                       -144.42214965820312,
                       -240.16839599609375])
        self.assertEqual(
            "matrix(1.812616, 0.845237, 0.211309, 1.753602, -144.42215,"
            " -240.168396)",
            m.tostring())
        self.assertEqual(
            "matrix(1.812616 0.845237 0.211309 1.753602 -144.42215"
            " -240.168396)",
            m.tostring(delimiter=' '))

    def test_translate_self(self):
        m = DOMMatrix()
        o = m.translate_self(12, 16)
        self.assertEqual(id(o), id(m))
        tx, ty = m.get_translate()
        self.assertEqual((12, 16), (tx, ty))
        src = np.matrix([[1, 0, 0, 12],
                         [0, 1, 0, 16],
                         [0, 0, 1, 0],
                         [0, 0, 0, 1]])
        self.assertTrue((src == m.matrix).all())

        x, y = m.transform_point(0, 0)
        self.assertEqual((12, 16), (x, y))

        x, y = m.transform_point(10, 10)
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

    def test_translate_self_3d(self):
        m = DOMMatrix(is2d=False)
        m.translate_self(10, 20, 30)
        tx, ty, tz = m.get_translate()
        self.assertEqual((10, 20, 30), (tx, ty, tz))
        self.assertEqual(
            'matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 10, 20, 30, 1)',
            m.tostring())

        m.translate_self(10, 20, 30)
        tx, ty, tz = m.get_translate()
        self.assertEqual((20, 40, 60), (tx, ty, tz))
        self.assertEqual(
            'matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 20, 40, 60, 1)',
            m.tostring())

        m.translate_self(10, 20)
        tx, ty, tz = m.get_translate()
        self.assertEqual((30, 60, 60), (tx, ty, tz))
        self.assertEqual(
            'matrix3d(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 30, 60, 60, 1)',
            m.tostring())


if __name__ == '__main__':
    unittest.main()
