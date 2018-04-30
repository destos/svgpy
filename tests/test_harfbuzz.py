#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy.harfbuzz import HBDirection


class HarfBuzzTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_direction_btt(self):
        # vertically from bottom to top
        direction = HBDirection(HBDirection.HB_DIRECTION_BTT)

        # 'btt' (7) <--> 'ttb' (6)
        self.assertEqual(7, direction.direction)
        self.assertEqual('btt', direction.tostring())
        self.assertEqual(6, direction.reverse().direction)
        self.assertTrue(direction.is_backward())
        self.assertTrue(not direction.is_forward())
        self.assertTrue(not direction.is_horizontal())
        self.assertTrue(direction.is_vertical())
        self.assertTrue(direction.is_valid())

    def test_direction_ltr(self):
        # horizontally from left to right
        direction = HBDirection(HBDirection.HB_DIRECTION_LTR)

        # 'ltr' (4) <--> 'rtl' (5)
        self.assertEqual(4, direction.direction)
        self.assertEqual('ltr', direction.tostring())
        self.assertEqual(5, direction.reverse().direction)
        self.assertTrue(not direction.is_backward())
        self.assertTrue(direction.is_forward())
        self.assertTrue(direction.is_horizontal())
        self.assertTrue(not direction.is_vertical())
        self.assertTrue(direction.is_valid())

    def test_direction_rtl(self):
        # horizontally from right to left
        direction = HBDirection(HBDirection.HB_DIRECTION_RTL)

        # 'rtl' (5) <--> 'ltr' (4)
        self.assertEqual(5, direction.direction)
        self.assertEqual('rtl', direction.tostring())
        self.assertEqual(4, direction.reverse().direction)
        self.assertTrue(direction.is_backward())
        self.assertTrue(not direction.is_forward())
        self.assertTrue(direction.is_horizontal())
        self.assertTrue(not direction.is_vertical())
        self.assertTrue(direction.is_valid())

    def test_direction_ttb(self):
        # vertically from top to bottom
        direction = HBDirection(HBDirection.HB_DIRECTION_TTB)

        # 'ttb' (6) <--> 'btt' (7)
        self.assertEqual(6, direction.direction)
        self.assertEqual('ttb', direction.tostring())
        self.assertEqual(7, direction.reverse().direction)
        self.assertTrue(not direction.is_backward())
        self.assertTrue(direction.is_forward())
        self.assertTrue(not direction.is_horizontal())
        self.assertTrue(direction.is_vertical())
        self.assertTrue(direction.is_valid())


if __name__ == '__main__':
    unittest.main()
