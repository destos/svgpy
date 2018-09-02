#!/usr/bin/env python3

import sys
import unittest

import numpy as np

sys.path.extend(['.', '..'])

from svgpy import DOMMatrix, SVGTransform, SVGTransformList, formatter


class TransformTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_transform_init(self):
        t = SVGTransform()
        self.assertEqual(t.type, SVGTransform.SVG_TRANSFORM_UNKNOWN)
        self.assertEqual(t.tostring(), '')
        self.assertIsNone(t.matrix)

    def test_transform_init_not_implemented_error(self):
        self.assertRaises(NotImplementedError,
                          lambda: SVGTransform('unknown', 1))

        self.assertRaises(NotImplementedError,
                          lambda: SVGTransform('unknown'))

    def test_transform_set_matrix(self):
        t = SVGTransform('matrix', 1, 2, 3, 4, 5, 6)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_MATRIX, t.type)
        self.assertEqual('matrix(1, 2, 3, 4, 5, 6)', t.tostring())
        self.assertTrue(t.matrix == DOMMatrix([1, 2, 3, 4, 5, 6]))
        self.assertTrue((t.matrix.matrix == np.matrix(
            [[1, 3, 0, 5],
             [2, 4, 0, 6],
             [0, 0, 1, 0],
             [0, 0, 0, 1]]
        )).all())

        t = SVGTransform()
        matrix = DOMMatrix([-1, 1.2, 3, -1.4, 5, 1.6])
        t.set_matrix(matrix)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_MATRIX, t.type)
        self.assertEqual('matrix(-1, 1.2, 3, -1.4, 5, 1.6)', t.tostring())
        self.assertTrue(t.matrix == DOMMatrix([-1, 1.2, 3, -1.4, 5, 1.6]))
        self.assertEqual(0, t.angle)

        t = SVGTransform()
        matrix = DOMMatrix(is2d=False)
        self.assertFalse(matrix.is2d)
        # t.set_matrix(matrix)
        self.assertRaises(ValueError, lambda: t.set_matrix(matrix))

    def test_transform_set_rotate(self):
        r = -30
        cx = 24
        cy = 16
        m = DOMMatrix()
        m.translate_self(cx, cy)
        m.rotate_self(rot_z=r)
        m.translate_self(-cx, -cy)

        t = SVGTransform('rotate', r, cx, cy)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_ROTATE, t.type)
        self.assertEqual('rotate(-30, 24, 16)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(r, t.angle)

        cx = 12.3456
        cy = -0
        m = DOMMatrix()
        m.translate_self(cx, cy)
        m.rotate_self(rot_z=r)
        m.translate_self(-cx, -cy)

        t = SVGTransform()
        t.set_rotate(r, cx, cy)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_ROTATE, t.type)
        self.assertEqual('rotate(-30, 12.346, 0)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(r, t.angle)

        cx = -0
        cy = -0
        m = DOMMatrix()
        m.rotate_self(rot_z=r)

        t = SVGTransform()
        t.set_rotate(r, cx, cy)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_ROTATE, t.type)
        self.assertEqual('rotate(-30)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(r, t.angle)

    def test_transform_set_scale(self):
        sx = 1.5
        sy = 1.5
        m = DOMMatrix()
        m.scale_self(sx, sy)

        t = SVGTransform('scale', sx, sy)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_SCALE, t.type)
        self.assertEqual('scale(1.5)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(0, t.angle)

        sy = -0
        m = DOMMatrix()
        m.scale_self(sx, sy)

        t = SVGTransform()
        t.set_scale(sx, sy)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_SCALE, t.type)
        self.assertEqual('scale(1.5, 0)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(0, t.angle)

    def test_transform_set_skew_x(self):
        a = 190.0001
        m = DOMMatrix()
        m.skew_x_self(a)

        t = SVGTransform('skewX', a)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_SKEWX, t.type)
        self.assertEqual('skewX(190)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(a, t.angle)

        a = -120.4567
        m = DOMMatrix()
        m.skew_x_self(a)

        t = SVGTransform()
        t.set_skew_x(a)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_SKEWX, t.type)
        self.assertEqual('skewX(-120.457)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(a, t.angle)

    def test_transform_set_skew_y(self):
        a = 190.0001
        m = DOMMatrix()
        m.skew_y_self(a)

        t = SVGTransform('skewY', a)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_SKEWY, t.type)
        self.assertEqual('skewY(190)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(a, t.angle)

        a = -120.4567
        m = DOMMatrix()
        m.skew_y_self(a)

        t = SVGTransform()
        t.set_skew_y(a)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_SKEWY, t.type)
        self.assertEqual('skewY(-120.457)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(a, t.angle)

    def test_transform_set_translate(self):
        tx = 100
        ty = -100
        m = DOMMatrix()
        m.translate_self(tx, ty)

        t = SVGTransform('translate', tx, ty)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_TRANSLATE, t.type)
        self.assertEqual('translate(100, -100)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(0, t.angle)

        tx = -1.5
        ty = -0
        m = DOMMatrix()
        m.translate_self(tx, ty)

        t = SVGTransform()
        t.set_translate(tx, ty)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_TRANSLATE, t.type)
        self.assertEqual('translate(-1.5)', t.tostring())
        self.assertTrue(t.matrix == m)
        self.assertEqual(0, t.angle)


class TransformListTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3

    def test_transform_list_add(self):
        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 50, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, 30),
        ]
        transform_list = SVGTransformList(iterable)
        self.assertEqual(2, len(transform_list))

        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_SKEWY, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 200, 30),
        ]
        transform_list = transform_list + SVGTransformList(iterable)
        self.assertIsInstance(transform_list, SVGTransformList)
        self.assertEqual(4, len(transform_list))
        self.assertEqual(
            'translate(50, 30) rotate(30) skewY(30) translate(200, 30)',
            transform_list.tostring())

        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_SKEWX, -30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, -30),
        ]
        transform_list = transform_list + iterable
        self.assertEqual(6, len(transform_list))

        iterable = (
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, -50, -30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, -30),
        )
        transform_list = transform_list + iterable
        self.assertEqual(8, len(transform_list))

    def test_transform_list_clear(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        self.assertEqual(2, len(transform_list))

        transform_list.clear()
        self.assertEqual(0, len(transform_list))

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
        self.assertEqual(SVGTransform.SVG_TRANSFORM_MATRIX, t.type)
        self.assertTrue(t.matrix == m)

    def test_transform_list_consolidate_none(self):
        transform_list = SVGTransformList()
        t = transform_list.consolidate()
        self.assertIsNone(t)

    def test_transform_list_extend(self):
        transform_list = SVGTransformList()
        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 50, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, 30),
        ]
        transform_list.extend(iterable)
        self.assertEqual(2, len(transform_list))

        iterable = [
            'translate(50, 30)',
            'rotate(30)',
        ]
        # transform_list.extend(iterable)
        self.assertRaises(
            TypeError,
            lambda: transform_list.extend(iterable))

    def test_transform_list_get_item(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')

        t = transform_list.get_item(0)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_TRANSLATE, t.type)

        t = transform_list.get_item(1)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_ROTATE, t.type)

        t = transform_list.get_item(-1)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_ROTATE, t.type)

        # t = transform_list.get_item(2)
        self.assertRaises(IndexError, lambda: transform_list.get_item(2))

    def test_transform_list_iadd(self):
        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 50, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, 30),
        ]
        transform_list = SVGTransformList(iterable)

        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_SKEWY, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 200, 30),
        ]
        transform_list += SVGTransformList(iterable)
        self.assertIsInstance(transform_list, SVGTransformList)
        self.assertEqual(4, len(transform_list))
        self.assertEqual(
            'translate(50, 30) rotate(30) skewY(30) translate(200, 30)',
            transform_list.tostring())

        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_SKEWX, -30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, -30),
        ]
        transform_list += iterable
        self.assertEqual(6, len(transform_list))

        iterable = (
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, -50, -30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, -30),
        )
        transform_list += iterable
        self.assertEqual(8, len(transform_list))

    def test_transform_list_init(self):
        transform_list = SVGTransformList()
        expected = 0
        self.assertEqual(expected, len(transform_list))
        self.assertEqual(expected, transform_list.length)
        self.assertEqual(expected, transform_list.number_of_items)

        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 50, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, 30),
        ]
        transform_list = SVGTransformList(iterable)
        expected = 2
        self.assertEqual(expected, len(transform_list))
        self.assertEqual(expected, transform_list.length)
        self.assertEqual(expected, transform_list.number_of_items)
        t = transform_list[0]
        self.assertEqual(SVGTransform.SVG_TRANSFORM_TRANSLATE, t.type)
        t = transform_list[1]
        self.assertEqual(SVGTransform.SVG_TRANSFORM_ROTATE, t.type)

        iterable = [
            'translate(50, 30)',
            'rotate(30)',
        ]
        self.assertRaises(TypeError, lambda: SVGTransformList(iterable))

    def test_transform_list_initialize(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        self.assertEqual(2, len(transform_list))

        transform = SVGTransform(SVGTransform.SVG_TRANSFORM_SKEWX, 45)
        o = transform_list.initialize(transform)
        self.assertEqual(1, len(transform_list))
        self.assertEqual(transform, o)

        self.assertRaises(
            TypeError,
            lambda: transform_list.initialize('skewX(45)', 0))

    def test_transform_list_insert_item_before(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        o = transform_list.insert_item_before(t, 0)
        # -> "scale(...) translate(...) rotate(...)"
        self.assertEqual(t, o)
        types = [x.type for x in transform_list]
        self.assertEqual([SVGTransform.SVG_TRANSFORM_SCALE,
                          SVGTransform.SVG_TRANSFORM_TRANSLATE,
                          SVGTransform.SVG_TRANSFORM_ROTATE],
                         types)

        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        o = transform_list.insert_item_before(t, 1)
        # -> "translate(...) scale(...) rotate(...)"
        self.assertEqual(t, o)
        types = [x.type for x in transform_list]
        self.assertEqual([SVGTransform.SVG_TRANSFORM_TRANSLATE,
                          SVGTransform.SVG_TRANSFORM_SCALE,
                          SVGTransform.SVG_TRANSFORM_ROTATE],
                         types)

        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        o = transform_list.insert_item_before(t, 2)
        # -> "translate(...) rotate(...) scale(...)"
        self.assertEqual(t, o)
        types = [x.type for x in transform_list]
        self.assertEqual([SVGTransform.SVG_TRANSFORM_TRANSLATE,
                          SVGTransform.SVG_TRANSFORM_ROTATE,
                          SVGTransform.SVG_TRANSFORM_SCALE],
                         types)

        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        o = transform_list.insert_item_before(t, -1)
        # -> "translate(...) scale(...) rotate(...)"
        self.assertEqual(t, o)
        types = [x.type for x in transform_list]
        self.assertEqual([SVGTransform.SVG_TRANSFORM_TRANSLATE,
                          SVGTransform.SVG_TRANSFORM_SCALE,
                          SVGTransform.SVG_TRANSFORM_ROTATE],
                         types)

        self.assertRaises(
            TypeError,
            lambda: transform_list.insert_item_before('scale(1.5)', 0))

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

    def test_transform_list_remove_item(self):
        iterable = [
            SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, 50, 30),
            SVGTransform(SVGTransform.SVG_TRANSFORM_ROTATE, 30),
        ]
        transform_list = SVGTransformList(iterable)
        i = 0
        t = transform_list[i]
        o = transform_list.remove_item(i)
        self.assertEqual(1, len(transform_list))
        self.assertTrue(o not in transform_list)
        self.assertEqual(t, o)
        self.assertEqual(SVGTransform.SVG_TRANSFORM_TRANSLATE, o.type)

        self.assertRaises(IndexError,
                          lambda: transform_list.remove_item(1))

    def test_transform_list_replace_item(self):
        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        o = transform_list.replace_item(t, 0)
        # -> "scale(...) rotate(...)"
        self.assertEqual(t, o)
        types = [x.type for x in transform_list]
        self.assertEqual([SVGTransform.SVG_TRANSFORM_SCALE,
                          SVGTransform.SVG_TRANSFORM_ROTATE],
                         types)

        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        o = transform_list.replace_item(t, 1)
        # -> "translate(...) scale(...)"
        self.assertEqual(t, o)
        types = [x.type for x in transform_list]
        self.assertEqual([SVGTransform.SVG_TRANSFORM_TRANSLATE,
                          SVGTransform.SVG_TRANSFORM_SCALE],
                         types)

        transform_list = SVGTransformList.parse('translate(50,30) rotate(30)')
        t = SVGTransform(SVGTransform.SVG_TRANSFORM_SCALE, 1.5)
        self.assertRaises(
            IndexError,
            lambda: transform_list.replace_item(t, 2))

        self.assertRaises(
            TypeError,
            lambda: transform_list.replace_item('scale(1.5)', 0))


if __name__ == '__main__':
    unittest.main()
