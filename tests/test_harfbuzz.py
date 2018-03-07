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
        self.assertEqual(direction.direction, 7)
        self.assertEqual(direction.tostring(), 'btt')
        self.assertEqual(direction.reverse().direction, 6)
        self.assertEqual(direction.is_backward(), True)
        self.assertEqual(direction.is_forward(), False)
        self.assertEqual(direction.is_horizontal(), False)
        self.assertEqual(direction.is_vertical(), True)
        self.assertEqual(direction.is_valid(), True)

    def test_direction_ltr(self):
        # horizontally from left to right
        direction = HBDirection(HBDirection.HB_DIRECTION_LTR)

        # 'ltr' (4) <--> 'rtl' (5)
        self.assertEqual(direction.direction, 4)
        self.assertEqual(direction.tostring(), 'ltr')
        self.assertEqual(direction.reverse().direction, 5)
        self.assertEqual(direction.is_backward(), False)
        self.assertEqual(direction.is_forward(), True)
        self.assertEqual(direction.is_horizontal(), True)
        self.assertEqual(direction.is_vertical(), False)
        self.assertEqual(direction.is_valid(), True)

    def test_direction_rtl(self):
        # horizontally from right to left
        direction = HBDirection(HBDirection.HB_DIRECTION_RTL)

        # 'rtl' (5) <--> 'ltr' (4)
        self.assertEqual(direction.direction, 5)
        self.assertEqual(direction.tostring(), 'rtl')
        self.assertEqual(direction.reverse().direction, 4)
        self.assertEqual(direction.is_backward(), True)
        self.assertEqual(direction.is_forward(), False)
        self.assertEqual(direction.is_horizontal(), True)
        self.assertEqual(direction.is_vertical(), False)
        self.assertEqual(direction.is_valid(), True)

    def test_direction_ttb(self):
        # vertically from top to bottom
        direction = HBDirection(HBDirection.HB_DIRECTION_TTB)

        # 'ttb' (6) <--> 'btt' (7)
        self.assertEqual(direction.direction, 6)
        self.assertEqual(direction.tostring(), 'ttb')
        self.assertEqual(direction.reverse().direction, 7)
        self.assertEqual(direction.is_backward(), False)
        self.assertEqual(direction.is_forward(), True)
        self.assertEqual(direction.is_horizontal(), False)
        self.assertEqual(direction.is_vertical(), True)
        self.assertEqual(direction.is_valid(), True)
