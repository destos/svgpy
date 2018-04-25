#!/usr/bin/env python3

import sys
import unittest

import numpy as np

sys.path.extend(['.', '..'])

from svgpy import Matrix, SVGTransform, SVGTransformList, formatter


class TransformListTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_transform_init(self):
        t = SVGTransform()
        self.assertEqual(t.type, SVGTransform.TRANSFORM_UNKNOWN)
        self.assertEqual(t.tostring(), '')
        self.assertIsNone(t.matrix)

    def test_transform_init_not_implemented_error(self):
        self.assertRaises(NotImplementedError,
                          lambda: SVGTransform('unknown', 1))

        self.assertRaises(NotImplementedError,
                          lambda: SVGTransform('unknown'))

    def test_transform_matrix(self):
        t = SVGTransform('matrix', 1, 2, 3, 4, 5, 6)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_MATRIX)
        self.assertEqual(t.tostring(), 'matrix(1 2 3 4 5 6)')
        self.assertTrue(t.matrix == Matrix(1, 2, 3, 4, 5, 6))
        self.assertTrue((t.matrix.matrix == np.matrix(
            [[1, 3, 0, 5],
             [2, 4, 0, 6],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        )).all())

        t = SVGTransform()
        t.set_matrix(-1, 1.2, 3, -1.4, 5, 1.6)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_MATRIX)
        self.assertEqual(t.tostring(), 'matrix(-1 1.2 3 -1.4 5 1.6)')
        self.assertTrue(t.matrix == Matrix(-1, 1.2, 3, -1.4, 5, 1.6))

    def test_transform_rotate(self):
        r = -30
        cx = 24
        cy = 16
        m = Matrix()
        m.translate_self(cx, cy)
        m.rotate_self(rot_z=r)
        m.translate_self(-cx, -cy)

        t = SVGTransform('rotate', r, cx, cy)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_ROTATE)
        self.assertEqual(t.tostring(), 'rotate(-30 24 16)')
        self.assertTrue(t.matrix == m)

        cx = 12.3456
        cy = -0
        m = Matrix()
        m.translate_self(cx, cy)
        m.rotate_self(rot_z=r)
        m.translate_self(-cx, -cy)

        t = SVGTransform()
        t.set_rotate(r, cx, cy)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_ROTATE)
        self.assertEqual(t.tostring(), 'rotate(-30 12.346 0)')
        self.assertTrue(t.matrix == m)

        cx = -0
        cy = -0
        m = Matrix()
        m.rotate_self(rot_z=r)

        t = SVGTransform()
        t.set_rotate(r, cx, cy)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_ROTATE)
        self.assertEqual(t.tostring(), 'rotate(-30)')
        self.assertTrue(t.matrix == m)

    def test_transform_scale(self):
        sx = 1.5
        sy = 1.5
        m = Matrix()
        m.scale_self(sx, sy)

        t = SVGTransform('scale', sx, sy)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_SCALE)
        self.assertEqual(t.tostring(), 'scale(1.5)')
        self.assertTrue(t.matrix == m)

        sy = -0
        m = Matrix()
        m.scale_self(sx, sy)

        t = SVGTransform()
        t.set_scale(sx, sy)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_SCALE)
        self.assertEqual(t.tostring(), 'scale(1.5 0)')
        self.assertTrue(t.matrix == m)

    def test_transform_skewx(self):
        a = 190.0001
        m = Matrix()
        m.skewx_self(a)

        t = SVGTransform('skewX', a)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_SKEWX)
        self.assertEqual(t.tostring(), 'skewX(190)')
        self.assertTrue(t.matrix == m)

        a = -120.4567
        m = Matrix()
        m.skewx_self(a)

        t = SVGTransform()
        t.set_skewx(a)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_SKEWX)
        self.assertEqual(t.tostring(), 'skewX(-120.457)')
        self.assertTrue(t.matrix == m)

    def test_transform_skewy(self):
        a = 190.0001
        m = Matrix()
        m.skewy_self(a)

        t = SVGTransform('skewY', a)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_SKEWY)
        self.assertEqual(t.tostring(), 'skewY(190)')
        self.assertTrue(t.matrix == m)

        a = -120.4567
        m = Matrix()
        m.skewy_self(a)

        t = SVGTransform()
        t.set_skewy(a)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_SKEWY)
        self.assertEqual(t.tostring(), 'skewY(-120.457)')
        self.assertTrue(t.matrix == m)

    def test_transform_translate(self):
        tx = 100
        ty = -100
        m = Matrix()
        m.translate_self(tx, ty)

        t = SVGTransform('translate', tx, ty)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_TRANSLATE)
        self.assertEqual(t.tostring(), 'translate(100 -100)')
        self.assertTrue(t.matrix == m)

        tx = -1.5
        ty = -0
        m = Matrix()
        m.translate_self(tx, ty)

        t = SVGTransform()
        t.set_translate(tx, ty)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_TRANSLATE)
        self.assertEqual(t.tostring(), 'translate(-1.5)')
        self.assertTrue(t.matrix == m)

    def test_transform_list_add(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        self.assertEqual(len(transform_list), 2)
        transform_list = transform_list + SVGTransformList.parse(
            'skewY(30) translate(200,30)')
        self.assertTrue(isinstance(transform_list, SVGTransformList))
        self.assertEqual(len(transform_list), 4)
        self.assertEqual(
            transform_list.tostring(),
            'translate(50 30) rotate(30) skewY(30) translate(200 30)')

    def test_transform_list_consolidate(self):
        # See also: RotateScale.html
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        self.assertEqual(len(transform_list), 2)
        t = transform_list.consolidate()
        self.assertEqual(len(transform_list), 1)
        self.assertEqual(t, transform_list[0])
        m = Matrix(
            0.8660254037844387, 0.49999999999999994, -0.49999999999999994,
            0.8660254037844387, 50, 30)
        self.assertEqual(t.type, SVGTransform.TRANSFORM_MATRIX)
        self.assertTrue(t.matrix == m)

    def test_transform_list_consolidate_none(self):
        transform_list = SVGTransformList()
        t = transform_list.consolidate()
        self.assertIsNone(t)

    def test_transform_list_consolidate_type_error(self):
        transform_list = SVGTransformList()
        transform_list.append('str')
        self.assertRaises(TypeError, lambda: transform_list.consolidate())

    def test_transform_list_iadd(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        transform_list += SVGTransformList.parse(
            'skewY(30) translate(200,30)')
        self.assertTrue(isinstance(transform_list, SVGTransformList))
        self.assertEqual(len(transform_list), 4)
        self.assertEqual(
            transform_list.tostring(),
            'translate(50 30) rotate(30) skewY(30) translate(200 30)')

    def test_transform_list_parse01(self):
        formatter.precision = 4

        t = "matrix(0.88889 2.33334 3.55555 4.78787 5.00004 6.00006)" \
            " rotate(25.11155 0.0 0.0) scale(2.22222 2.22222)" \
            " skewX(-36.11224) skewY(180.55564)" \
            " translate(-100.44444 0.0)"
        transform_list = SVGTransformList.parse(t)
        self.assertEqual(len(transform_list), 6)
        self.assertEqual(transform_list[0].tostring(),
                         'matrix(0.8889 2.3333 3.5556 4.7879 5 6.0001)')
        self.assertEqual(transform_list[1].tostring(), 'rotate(25.1116)')
        self.assertEqual(transform_list[2].tostring(), 'scale(2.2222)')
        self.assertEqual(transform_list[3].tostring(), 'skewX(-36.1122)')
        self.assertEqual(transform_list[4].tostring(), 'skewY(180.5556)')
        self.assertEqual(transform_list[5].tostring(), 'translate(-100.4444)')

    def test_transform_list_parse02(self):
        t = ' translate ( 1500e-2 .5e+2 ) scale ( .5,.25 ) rotate ( 45.0.5.7 ) '
        transform_list = SVGTransformList.parse(t)
        self.assertEqual(len(transform_list), 3)
        self.assertEqual(transform_list[0].tostring(), 'translate(15 50)')
        self.assertEqual(transform_list[1].tostring(), 'scale(0.5 0.25)')
        self.assertEqual(transform_list[2].tostring(), 'rotate(45 0.5 0.7)')

    def test_transform_list_parse03(self):
        t = "\ttranslate\t(\t1500e-2\t.5e+2\t)\nscale\t(\t.5,.25\t)\n" \
            "rotate\t(\t45.0.5.7\t)\n"
        transform_list = SVGTransformList.parse(t)
        self.assertEqual(len(transform_list), 3)
        self.assertEqual(transform_list[0].tostring(), 'translate(15 50)')
        self.assertEqual(transform_list[1].tostring(), 'scale(0.5 0.25)')
        self.assertEqual(transform_list[2].tostring(), 'rotate(45 0.5 0.7)')


if __name__ == '__main__':
    unittest.main()
