#!/usr/bin/env python3

import sys
import unittest

import numpy as np

sys.path.extend(['.', '..'])

from svgpy import DOMMatrix, SVGTransform, SVGTransformList, formatter


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
        self.assertEqual(SVGTransform.TRANSFORM_MATRIX, t.type)
        self.assertEqual('matrix(1, 2, 3, 4, 5, 6)', t.tostring())
        self.assertTrue(t.matrix == DOMMatrix([1, 2, 3, 4, 5, 6]))
        self.assertTrue((t.matrix.matrix == np.matrix(
            [[1, 3, 0, 5],
             [2, 4, 0, 6],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        )).all())

        t = SVGTransform()
        t.set_matrix(-1, 1.2, 3, -1.4, 5, 1.6)
        self.assertEqual(SVGTransform.TRANSFORM_MATRIX, t.type)
        self.assertEqual('matrix(-1, 1.2, 3, -1.4, 5, 1.6)', t.tostring())
        self.assertTrue(t.matrix == DOMMatrix([-1, 1.2, 3, -1.4, 5, 1.6]))

    def test_transform_rotate(self):
        r = -30
        cx = 24
        cy = 16
        m = DOMMatrix()
        m.translate_self(cx, cy)
        m.rotate_self(rot_z=r)
        m.translate_self(-cx, -cy)

        t = SVGTransform('rotate', r, cx, cy)
        self.assertEqual(SVGTransform.TRANSFORM_ROTATE, t.type)
        self.assertEqual('rotate(-30, 24, 16)', t.tostring())
        self.assertTrue(t.matrix == m)

        cx = 12.3456
        cy = -0
        m = DOMMatrix()
        m.translate_self(cx, cy)
        m.rotate_self(rot_z=r)
        m.translate_self(-cx, -cy)

        t = SVGTransform()
        t.set_rotate(r, cx, cy)
        self.assertEqual(SVGTransform.TRANSFORM_ROTATE, t.type)
        self.assertEqual('rotate(-30, 12.346, 0)', t.tostring())
        self.assertTrue(t.matrix == m)

        cx = -0
        cy = -0
        m = DOMMatrix()
        m.rotate_self(rot_z=r)

        t = SVGTransform()
        t.set_rotate(r, cx, cy)
        self.assertEqual(SVGTransform.TRANSFORM_ROTATE, t.type)
        self.assertEqual('rotate(-30)', t.tostring())
        self.assertTrue(t.matrix == m)

    def test_transform_scale(self):
        sx = 1.5
        sy = 1.5
        m = DOMMatrix()
        m.scale_self(sx, sy)

        t = SVGTransform('scale', sx, sy)
        self.assertEqual(SVGTransform.TRANSFORM_SCALE, t.type)
        self.assertEqual('scale(1.5)', t.tostring())
        self.assertTrue(t.matrix == m)

        sy = -0
        m = DOMMatrix()
        m.scale_self(sx, sy)

        t = SVGTransform()
        t.set_scale(sx, sy)
        self.assertEqual(SVGTransform.TRANSFORM_SCALE, t.type)
        self.assertEqual('scale(1.5, 0)', t.tostring())
        self.assertTrue(t.matrix == m)

    def test_transform_skewx(self):
        a = 190.0001
        m = DOMMatrix()
        m.skew_x_self(a)

        t = SVGTransform('skewX', a)
        self.assertEqual(SVGTransform.TRANSFORM_SKEWX, t.type)
        self.assertEqual('skewX(190)', t.tostring())
        self.assertTrue(t.matrix == m)

        a = -120.4567
        m = DOMMatrix()
        m.skew_x_self(a)

        t = SVGTransform()
        t.set_skewx(a)
        self.assertEqual(SVGTransform.TRANSFORM_SKEWX, t.type)
        self.assertEqual('skewX(-120.457)', t.tostring())
        self.assertTrue(t.matrix == m)

    def test_transform_skewy(self):
        a = 190.0001
        m = DOMMatrix()
        m.skew_y_self(a)

        t = SVGTransform('skewY', a)
        self.assertEqual(SVGTransform.TRANSFORM_SKEWY, t.type)
        self.assertEqual('skewY(190)', t.tostring())
        self.assertTrue(t.matrix == m)

        a = -120.4567
        m = DOMMatrix()
        m.skew_y_self(a)

        t = SVGTransform()
        t.set_skewy(a)
        self.assertEqual(SVGTransform.TRANSFORM_SKEWY, t.type)
        self.assertEqual('skewY(-120.457)', t.tostring())
        self.assertTrue(t.matrix == m)

    def test_transform_translate(self):
        tx = 100
        ty = -100
        m = DOMMatrix()
        m.translate_self(tx, ty)

        t = SVGTransform('translate', tx, ty)
        self.assertEqual(SVGTransform.TRANSFORM_TRANSLATE, t.type)
        self.assertEqual('translate(100, -100)', t.tostring())
        self.assertTrue(t.matrix == m)

        tx = -1.5
        ty = -0
        m = DOMMatrix()
        m.translate_self(tx, ty)

        t = SVGTransform()
        t.set_translate(tx, ty)
        self.assertEqual(SVGTransform.TRANSFORM_TRANSLATE, t.type)
        self.assertEqual('translate(-1.5)', t.tostring())
        self.assertTrue(t.matrix == m)

    def test_transform_list_add(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        self.assertEqual(2, len(transform_list))
        transform_list = transform_list + SVGTransformList.parse(
            'skewY(30) translate(200,30)')
        self.assertTrue(isinstance(transform_list, SVGTransformList))
        self.assertEqual(4, len(transform_list))
        self.assertEqual(
            'translate(50, 30) rotate(30) skewY(30) translate(200, 30)',
            transform_list.tostring())

    def test_transform_list_consolidate(self):
        # See also: RotateScale.html
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        self.assertEqual(2, len(transform_list))
        t = transform_list.consolidate()
        self.assertEqual(1, len(transform_list))
        self.assertEqual(transform_list[0], t)
        m = DOMMatrix([0.8660254037844387,
                       0.49999999999999994,
                       -0.49999999999999994,
                       0.8660254037844387,
                       50,
                       30])
        self.assertEqual(SVGTransform.TRANSFORM_MATRIX, t.type)
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
        self.assertEqual(4, len(transform_list))
        self.assertEqual(
            'translate(50, 30) rotate(30) skewY(30) translate(200, 30)',
            transform_list.tostring())

    def test_transform_list_parse01(self):
        formatter.precision = 4

        t = "matrix(0.88889, 2.33334, 3.55555, 4.78787, 5.00004, 6.00006)" \
            " rotate(25.11155 0.0 0.0) scale(2.22222 2.22222)" \
            " skewX(-36.11224) skewY(180.55564)" \
            " translate(-100.44444 0.0)"
        transform_list = SVGTransformList.parse(t)
        self.assertEqual(6, len(transform_list))
        self.assertEqual('matrix(0.8889, 2.3333, 3.5556, 4.7879, 5, 6.0001)',
                         transform_list[0].tostring())
        self.assertEqual('rotate(25.1116)',
                         transform_list[1].tostring())
        self.assertEqual('scale(2.2222)',
                         transform_list[2].tostring())
        self.assertEqual('skewX(-36.1122)',
                         transform_list[3].tostring())
        self.assertEqual('skewY(180.5556)',
                         transform_list[4].tostring())
        self.assertEqual('translate(-100.4444)',
                         transform_list[5].tostring())

    def test_transform_list_parse02(self):
        t = ' translate ( 1500e-2 .5e+2 ) scale ( .5,.25 ) rotate ( 45.0.5.7 ) '
        transform_list = SVGTransformList.parse(t)
        self.assertEqual(3, len(transform_list))
        self.assertEqual('translate(15, 50)',
                         transform_list[0].tostring())
        self.assertEqual('scale(0.5, 0.25)',
                         transform_list[1].tostring())
        self.assertEqual('rotate(45, 0.5, 0.7)',
                         transform_list[2].tostring())

    def test_transform_list_parse03(self):
        t = "\ttranslate\t(\t1500e-2\t.5e+2\t)\nscale\t(\t.5,.25\t)\n" \
            "rotate\t(\t45.0.5.7\t)\n"
        transform_list = SVGTransformList.parse(t)
        self.assertEqual(3, len(transform_list))
        self.assertEqual('translate(15, 50)',
                         transform_list[0].tostring())
        self.assertEqual('scale(0.5, 0.25)',
                         transform_list[1].tostring())
        self.assertEqual('rotate(45, 0.5, 0.7)',
                         transform_list[2].tostring())


if __name__ == '__main__':
    unittest.main()
