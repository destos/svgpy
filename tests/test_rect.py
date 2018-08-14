#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import DOMRect, DOMRectReadOnly


class RectTestCase(unittest.TestCase):
    def test_and00(self):
        # valid rectangle AND invalid rectangle
        w = 10
        h = 20
        xa = 100
        ya = 100
        a = DOMRectReadOnly(xa, ya, w, h)
        b = DOMRectReadOnly()
        c = a & b
        self.assertIsInstance(c, DOMRect)
        self.assertEqual(xa, a.x)
        self.assertEqual(ya, a.y)
        self.assertEqual(w, a.width)
        self.assertEqual(h, a.height)
        self.assertIsNone(b.x)
        self.assertIsNone(b.y)
        self.assertEqual(0, b.width)
        self.assertEqual(0, b.height)
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_and01(self):
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

    def test_and02(self):
        # left-upper
        w = 10
        h = 20
        xa = 100
        ya = 100
        xb = xa - w
        yb = ya - h / 2
        a = DOMRectReadOnly(xa, ya, w, h)
        b = DOMRectReadOnly(xb, yb, w, h)
        c = a & b
        self.assertIsInstance(c, DOMRect)
        self.assertEqual(xa, a.x)
        self.assertEqual(ya, a.y)
        self.assertEqual(w, a.width)
        self.assertEqual(h, a.height)
        self.assertEqual(xb, b.x)
        self.assertEqual(yb, b.y)
        self.assertEqual(w, b.width)
        self.assertEqual(h, b.height)
        expected_x = xa
        expected_y = ya
        expected_w = w
        expected_h = h
        self.assertEqual(expected_x, c.x, msg=(a, b, c))
        self.assertEqual(expected_y, c.y, msg=(a, b, c))
        self.assertEqual(expected_w, c.width, msg=(a, b, c))
        self.assertEqual(expected_h, c.height, msg=(a, b, c))

    def test_and03(self):
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

    def test_and04(self):
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

    def test_and05(self):
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

    def test_and06(self):
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

    def test_and07(self):
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

    def test_and08(self):
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

    def test_and09(self):
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

    def test_and10(self):
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

    def test_and11(self):
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

    def test_and12(self):
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

    def test_and13(self):
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

    def test_and14(self):
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

    def test_and15(self):
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

    def test_and16(self):
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

    def test_and17(self):
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

    def test_and18(self):
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

    def test_eq01(self):
        a = DOMRect()
        b = DOMRect()
        self.assertEqual(b, a)

    def test_eq02(self):
        a = DOMRect(0, 0)
        b = DOMRect()
        self.assertNotEqual(b, a)

    def test_eq03(self):
        a = DOMRect()
        b = DOMRect(0, 0)
        self.assertNotEqual(b, a)

    def test_eq04(self):
        a = DOMRect(10, 20)
        b = DOMRect(10, 20)
        self.assertEqual(b, a)

    def test_eq05(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 100, 200)
        self.assertEqual(b, a)

    def test_eq06(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(15, 20, 100, 200)
        self.assertNotEqual(b, a)

    def test_eq07(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 25, 100, 200)
        self.assertNotEqual(b, a)

    def test_eq08(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(15, 25, 100, 200)
        self.assertNotEqual(b, a)

    def test_eq09(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 105, 200)
        self.assertNotEqual(b, a)

    def test_eq10(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 100, 205)
        self.assertNotEqual(b, a)

    def test_eq11(self):
        a = DOMRect(10, 20, 100, 200)
        b = DOMRect(10, 20, 105, 205)
        self.assertNotEqual(b, a)

    def test_from_rect(self):
        x = -200
        y = -100
        width = 600
        height = 300
        rect = DOMRect.from_rect({'x': x,
                                  'y': y,
                                  'width': width,
                                  'height': height,
                                  })
        self.assertIsInstance(rect, DOMRect)
        self.assertFalse(rect.isempty())
        self.assertTrue(rect.isvalid())
        self.assertEqual(x, rect.x)
        self.assertEqual(x, rect.left)
        self.assertEqual(y, rect.y)
        self.assertEqual(y, rect.top)
        self.assertEqual(x + width, rect.right)
        self.assertEqual(y + height, rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)

    def test_iand(self):
        # a: (100, 100) - (200, 300)
        # b: (150, 150) - (200, 200)
        ax = 100
        ay = 100
        aw = 100
        ah = 200
        bx = 150
        by = 150
        bw = 50
        bh = 50
        cx = 150
        cy = 150
        cw = 50
        ch = 50
        a = DOMRect(ax, ay, aw, ah)
        b = DOMRectReadOnly(bx, by, bw, bh)
        a &= b
        self.assertIsInstance(a, DOMRect)
        self.assertEqual(cx, a.x)
        self.assertEqual(cy, a.y)
        self.assertEqual(cw, a.width)
        self.assertEqual(ch, a.height)
        self.assertEqual(bx, b.x)
        self.assertEqual(by, b.y)
        self.assertEqual(bw, b.width)
        self.assertEqual(bh, b.height)

    def test_intersect01(self):
        a = DOMRect()
        b = DOMRect()
        c = a.intersect(b)
        self.assertTrue(c.isempty())
        self.assertTrue(not c.isvalid())

    def test_intersect02(self):
        a = DOMRect()
        b = DOMRect(30, 50, 100, 200)
        c = a.intersect(b)
        self.assertTrue(c.isempty())
        self.assertTrue(not c.isvalid())
        self.assertTrue(a.isempty())
        self.assertTrue(not a.isvalid())
        self.assertEqual((30, 50, 100, 200), (b.x, b.y, b.width, b.height))

    def test_intersect03(self):
        a = DOMRect(30, 50, 100, 200)
        b = DOMRect()
        c = a.intersect(b)
        self.assertTrue(not c.isempty())
        self.assertTrue(c.isvalid())
        self.assertEqual((30, 50, 100, 200), (c.x, c.y, c.width, c.height))
        self.assertEqual((30, 50, 100, 200), (a.x, a.y, a.width, a.height))
        self.assertTrue(b.isempty())
        self.assertTrue(not b.isvalid())

    def test_ior(self):
        ax = 100
        ay = 100
        aw = 100
        ah = 200
        bx = 150
        by = 150
        bw = 50
        bh = 50
        cx = min(ax, bx)
        cy = min(ay, by)
        cw = max(ax + aw, bx + bw) - min(ax, bx)
        ch = max(ay + ah, by + bh) - min(ay, by)
        a = DOMRect(ax, ay, aw, ah)
        b = DOMRectReadOnly(bx, by, bw, bh)
        a |= b
        self.assertIsInstance(a, DOMRect)
        self.assertEqual(cx, a.x)
        self.assertEqual(cy, a.y)
        self.assertEqual(cw, a.width)
        self.assertEqual(ch, a.height)
        self.assertEqual(bx, b.x)
        self.assertEqual(by, b.y)
        self.assertEqual(bw, b.width)
        self.assertEqual(bh, b.height)

    def test_or(self):
        ax = 100
        ay = 100
        aw = 100
        ah = 200
        bx = 150
        by = 150
        bw = 50
        bh = 50
        cx = min(ax, bx)
        cy = min(ay, by)
        cw = max(ax + aw, bx + bw) - min(ax, bx)
        ch = max(ay + ah, by + bh) - min(ay, by)
        a = DOMRectReadOnly(ax, ay, aw, ah)
        b = DOMRectReadOnly(bx, by, bw, bh)
        c = a | b
        self.assertIsInstance(c, DOMRect)
        self.assertEqual(ax, a.x)
        self.assertEqual(ay, a.y)
        self.assertEqual(aw, a.width)
        self.assertEqual(ah, a.height)
        self.assertEqual(bx, b.x)
        self.assertEqual(by, b.y)
        self.assertEqual(bw, b.width)
        self.assertEqual(bh, b.height)
        self.assertEqual(cx, c.x)
        self.assertEqual(cy, c.y)
        self.assertEqual(cw, c.width)
        self.assertEqual(ch, c.height)

    def test_property(self):
        x = -200
        y = -100
        width = 600
        height = 300
        rect = DOMRect(x, y, width, height)
        self.assertFalse(rect.isempty())
        self.assertTrue(rect.isvalid())
        self.assertEqual(x, rect.x)
        self.assertEqual(x, rect.left)
        self.assertEqual(y, rect.y)
        self.assertEqual(y, rect.top)
        self.assertEqual(x + width, rect.right)
        self.assertEqual(y + height, rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)
        x = 100
        y = 200
        width = 300
        height = 600
        rect.x = x
        rect.y = y
        rect.width = width
        rect.height = height
        self.assertFalse(rect.isempty())
        self.assertTrue(rect.isvalid())
        self.assertEqual(x, rect.x)
        self.assertEqual(x, rect.left)
        self.assertEqual(y, rect.y)
        self.assertEqual(y, rect.top)
        self.assertEqual(x + width, rect.right)
        self.assertEqual(y + height, rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)

    def test_read_only_from_rect(self):
        x = -200
        y = -100
        width = 600
        height = 300
        rect = DOMRectReadOnly.from_rect({'x': x,
                                          'y': y,
                                          'width': width,
                                          'height': height,
                                          })
        self.assertIsInstance(rect, DOMRectReadOnly)
        self.assertNotIsInstance(rect, DOMRect)
        self.assertFalse(rect.isempty())
        self.assertTrue(rect.isvalid())
        self.assertEqual(x, rect.x)
        self.assertEqual(x, rect.left)
        self.assertEqual(y, rect.y)
        self.assertEqual(y, rect.top)
        self.assertEqual(x + width, rect.right)
        self.assertEqual(y + height, rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)

    def test_read_only_iand(self):
        a = DOMRectReadOnly()
        b = DOMRectReadOnly()
        a &= b
        self.assertIsNone(a)

        a = DOMRectReadOnly()
        b = DOMRect()
        a &= b
        self.assertIsNone(a)

    def test_read_only_init01(self):
        width = 0
        height = 0
        rect = DOMRectReadOnly()
        self.assertTrue(rect.isempty())
        self.assertFalse(rect.isvalid())
        self.assertIsNone(rect.x)
        self.assertIsNone(rect.left)
        self.assertIsNone(rect.y)
        self.assertIsNone(rect.top)
        self.assertIsNone(rect.right)
        self.assertIsNone(rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)

    def test_read_only_init02(self):
        x = -200
        y = -100
        width = 0
        height = 0
        rect = DOMRectReadOnly(x, y, width, height)
        self.assertTrue(rect.isempty())
        self.assertFalse(rect.isvalid())
        self.assertEqual(x, rect.x)
        self.assertEqual(x, rect.left)
        self.assertEqual(y, rect.y)
        self.assertEqual(y, rect.top)
        self.assertEqual(x + width, rect.right)
        self.assertEqual(y + height, rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)

    def test_read_only_init03(self):
        x = -200
        y = -100
        width = 600
        height = 300
        rect = DOMRectReadOnly(x, y, width, height)
        self.assertFalse(rect.isempty())
        self.assertTrue(rect.isvalid())
        self.assertEqual(x, rect.x)
        self.assertEqual(x, rect.left)
        self.assertEqual(y, rect.y)
        self.assertEqual(y, rect.top)
        self.assertEqual(x + width, rect.right)
        self.assertEqual(y + height, rect.bottom)
        self.assertEqual(width, rect.width)
        self.assertEqual(height, rect.height)

    def test_read_only_ior(self):
        a = DOMRectReadOnly()
        b = DOMRectReadOnly()
        a |= b
        self.assertIsNone(a)

        a = DOMRectReadOnly()
        b = DOMRect()
        a |= b
        self.assertIsNone(a)

    def test_tojson(self):
        x = -200
        y = -100
        width = 600
        height = 300
        rect = DOMRect(x, y, width, height)
        json = rect.tojson()
        self.assertEqual(x, json['x'])
        self.assertEqual(y, json['y'])
        self.assertEqual(width, json['width'])
        self.assertEqual(height, json['height'])
        o = DOMRect.from_rect(json)
        self.assertEqual(o, rect)
        self.assertEqual(x, o.x)
        self.assertEqual(y, o.y)
        self.assertEqual(width, o.width)
        self.assertEqual(height, o.height)

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
