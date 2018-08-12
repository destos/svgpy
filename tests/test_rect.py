#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import DOMRect


class RectTestCase(unittest.TestCase):
    def test_eq01(self):
        a = DOMRect()
        b = DOMRect()
        f = a == b
        self.assertTrue(f)

    def test_eq02(self):
        a = DOMRect(0, 0)
        b = DOMRect()
        f = a != b
        self.assertTrue(f)

    def test_eq03(self):
        a = DOMRect()
        b = DOMRect(0, 0)
        f = a != b
        self.assertTrue(f)

    def test_eq04(self):
        a = DOMRect(10, 20)
        b = DOMRect(10, 20)
        f = a == b
        self.assertTrue(f)

    def test_eq05(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 100, 200)
        f = a == b
        self.assertTrue(f)

    def test_eq06(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(15, 20, 100, 200)
        f = a != b
        self.assertTrue(f)

    def test_eq07(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 25, 100, 200)
        f = a != b
        self.assertTrue(f)

    def test_eq08(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(15, 25, 100, 200)
        f = a != b
        self.assertTrue(f)

    def test_eq09(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 105, 200)
        f = a != b
        self.assertTrue(f)

    def test_eq10(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 100, 205)
        f = a != b
        self.assertTrue(f)

    def test_eq11(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 105, 205)
        f = a != b
        self.assertTrue(f)

    def test_intersect00(self):
        # valid rectangle AND invalid rectangle
        w = 10
        h = 20
        xa = 100
        ya = 100
        a = DOMRect(xa, ya, w, h)
        b = DOMRect()
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect01(self):
        # invalid rectangle AND valid rectangle
        w = 10
        h = 20
        xb = 100
        yb = 100
        a = DOMRect()
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = None
        expected_y = None
        expected_w = 0
        expected_h = 0
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect02(self):
        # left-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect03(self):
        # left-upper overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w / 2
        expected_h = h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect04(self):
        # upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya - h
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect05(self):
        # upper overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect06(self):
        # right-upper overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa + w / 2
        expected_y = ya
        expected_w = w / 2
        expected_h = h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect07(self):
        # right-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect08(self):
        # left
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect09(self):
        # left overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w / 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect10(self):
        # same position
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect11(self):
        # right overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa + w / 2
        expected_y = ya
        expected_w = w / 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect12(self):
        # right
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect13(self):
        # left-lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect14(self):
        # left-lower overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya + h / 2
        expected_w = w / 2
        expected_h = h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect15(self):
        # lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya + h
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect16(self):
        # lower overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya + h / 2
        expected_w = w
        expected_h = h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect17(self):
        # right-lower overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa + w / 2
        expected_y = ya + h / 2
        expected_w = w / 2
        expected_h = h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersect18(self):
        # right-lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a & b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_intersected_invalid_invalid(self):
        a = DOMRect()
        b = DOMRect()
        c = a.intersect(b)
        self.assertTrue(c.isempty())
        self.assertTrue(not c.isvalid())

    def test_intersected_invalid_valid(self):
        a = DOMRect()
        b = DOMRect(30, 50, 100, 200)
        c = a.intersect(b)
        self.assertTrue(c.isempty())
        self.assertTrue(not c.isvalid())
        self.assertTrue(a.isempty())
        self.assertTrue(not a.isvalid())
        self.assertEqual((30, 50, 100, 200), (b.x, b.y, b.width, b.height))

    def test_intersected_valid_invalid(self):
        a = DOMRect(30, 50, 100, 200)
        b = DOMRect()
        c = a.intersect(b)
        self.assertTrue(not c.isempty())
        self.assertTrue(c.isvalid())
        self.assertEqual((30, 50, 100, 200), (c.x, c.y, c.width, c.height))
        self.assertEqual((30, 50, 100, 200), (a.x, a.y, a.width, a.height))
        self.assertTrue(b.isempty())
        self.assertTrue(not b.isvalid())

    def test_unite_point01(self):
        # left-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xb
        expected_y = yb
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point02(self):
        # upper-left
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xb
        expected_y = yb
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point03(self):
        # upper-right
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = yb
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point04(self):
        # right-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w + w / 2
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = yb
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point05(self):
        # left
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xb
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point06(self):
        # center
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point07(self):
        # right
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w + w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point08(self):
        # left-lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya + h + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xb
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point09(self):
        # lower-left
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya + h + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point10(self):
        # lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya + h + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point11(self):
        # lower-right
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya + h + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_point12(self):
        # right-lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w + w / 2
        yb = ya + h + h / 2
        a = DOMRect(xa, ya, w, h)
        c = a.unite(xb, yb)
        expected_x = xa
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, c))
        self.assertEqual(expected_y, c.y, msg=(a, c))
        self.assertEqual(expected_w, c.width, msg=(a, c))
        self.assertEqual(expected_h, c.height, msg=(a, c))

    def test_unite_rect01(self):
        # left-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = yb
        expected_w = w * 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect02(self):
        # left-upper overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = yb
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect03(self):
        # upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya - h
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = yb
        expected_w = w
        expected_h = h * 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect04(self):
        # upper overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = yb
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect05(self):
        # right-upper overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = yb
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect06(self):
        # right-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya - h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = yb
        expected_w = w * 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect07(self):
        # left
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = ya
        expected_w = w * 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect08(self):
        # left overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect09(self):
        # same position
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect10(self):
        # right overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect11(self):
        # right
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w * 2
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect12(self):
        # left-lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = ya
        expected_w = w * 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect13(self):
        # left-lower overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xb
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect14(self):
        # lower overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect15(self):
        # lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa
        yb = ya + h
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h + h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect16(self):
        # right-lower overlapped
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w / 2
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w + w / 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_unite_rect17(self):
        # right-lower
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa + w
        yb = ya + h / 2
        a = DOMRect(xa, ya, w, h)
        b = DOMRect(xb, yb, w, h)
        c = a | b
        expected_x = xa
        expected_y = ya
        expected_w = w * 2
        expected_h = h + h / 2
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_united_invalid_invalid(self):
        a = DOMRect()
        b = DOMRect()
        c = a.unite(b.x, b.y, b.width, b.height)
        self.assertTrue(c.isempty())
        self.assertTrue(not c.isvalid())

    def test_united_invalid_valid(self):
        a = DOMRect()
        b = DOMRect(30, 50, 100, 200)
        c = a.unite(b.x, b.y, b.width, b.height)
        self.assertTrue(not c.isempty())
        self.assertTrue(c.isvalid())
        self.assertEqual((30, 50, 100, 200), (c.x, c.y, c.width, c.height))
        self.assertTrue(a.isempty())
        self.assertTrue(not a.isvalid())
        self.assertEqual((30, 50, 100, 200), (b.x, b.y, b.width, b.height))

    def test_united_valid_invalid(self):
        a = DOMRect(30, 50, 100, 200)
        b = DOMRect()
        c = a.unite(b.x, b.y, b.width, b.height)
        self.assertTrue(not c.isempty())
        self.assertTrue(c.isvalid())
        self.assertEqual((30, 50, 100, 200), (a.x, a.y, a.width, a.height))
        self.assertTrue(b.isempty())
        self.assertTrue(not b.isvalid())


if __name__ == '__main__':
    unittest.main()
