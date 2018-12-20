#!/usr/bin/env python3

import math
import sys
import unittest
from decimal import Decimal

import tinycss2

sys.path.extend(['.', '..'])

from svgpy import formatter
from svgpy.css import CSSStyleDeclaration
from svgpy.css import CSS, CSSImageValue, CSSKeywordValue, CSSMathClamp, \
    CSSMathInvert, CSSMathMax, CSSMathMin, CSSMathNegate, CSSMathOperator, \
    CSSMathProduct, CSSMathSum, CSSNumericType, CSSNumericValue, \
    CSSStyleValue, CSSURLImageValue, CSSUnitValue, CSSUnparsedValue, \
    CSSVariableReferenceValue, PropertyDescriptor, PropertySyntax, \
    StylePropertyMap, StylePropertyMapReadOnly

places = 3


def _debug_print_numeric_value(css_text, node, depth=-1):
    _id = hex(id(node))
    depth += 1
    if depth == 0:
        print()
        print('{}: css_text={}'.format(_id, repr(css_text)))
    print('{}: instance={}'.format(_id, node))
    print('{}: operator={}'.format(_id, node.operator))
    if isinstance(node, CSSMathClamp):
        pass
    elif isinstance(node, (CSSMathInvert, CSSMathNegate)):
        print('{}: value={}'.format(_id, node.value))
        if not isinstance(node.value, CSSUnitValue):
            _debug_print_numeric_value(css_text, node.value, depth)
    else:
        for i, arg in enumerate(node.values):
            print('{}: values[{}]={}'.format(_id, i, arg))
            if not isinstance(arg, CSSUnitValue):
                _debug_print_numeric_value(css_text, arg, depth)


class CSSTypesTestCase(unittest.TestCase):

    def setUp(self):
        formatter.precision = 6
        CSSUnitValue.rel_tol = 1e-9

    def test_css_math_clamp_tostring(self):
        # CSSMathClamp.tostring()
        a = CSSMathClamp(CSS.number(1), CSS.number(2), CSS.number(3))
        self.assertEqual('clamp(1, 2, 3)', a.tostring())

    def test_css_math_product_tostring(self):
        # CSSMathProduct.tostring()
        a = CSSMathProduct(CSS.number(1), CSS.number(2), CSS.number(3))
        self.assertEqual('calc(1 * 2 * 3)', a.tostring())
        # print(a.tostring())

    def test_css_math_sum(self):
        # CSSMathSum()
        # CSSMathSum(CSS.number(1), CSS.number(1)).type() => {}
        a = CSS.number(1)
        b = CSS.number(1)
        c = CSSMathSum(a, b)
        self.assertEqual(2, len(c.values))
        self.assertEqual(a, c.values[0])
        self.assertEqual(b, c.values[1])
        t = CSSNumericType()
        self.assertEqual(t, c.type())

        # CSSMathSum(CSS.number(1), CSS.px(1)) => Incompatible types
        a = CSS.number(1)
        b = CSS.px(1)
        self.assertRaises(ValueError, lambda: CSSMathSum(a, b))

        # CSSMathSum(CSS.px(1), CSS.em(1)).type() => {length: 1}
        a = CSS.px(1)
        b = CSS.em(1)
        c = CSSMathSum(a, b)
        self.assertEqual(2, len(c.values))
        self.assertEqual(a, c.values[0])
        self.assertEqual(b, c.values[1])
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, c.type())

        # CSSMathSum(CSS.px(1), CSS.percent(1)).type()
        #  => {length: 1, percentHint: "length"}
        a = CSS.px(1)
        b = CSS.percent(1)
        c = CSSMathSum(a, b)
        self.assertEqual(2, len(c.values))
        self.assertEqual(a, c.values[0])
        self.assertEqual(b, c.values[1])
        t = CSSNumericType()
        t.length = 1
        t.percent_hint = 'length'
        self.assertEqual(t, c.type())

        # CSSMathSum(CSS.dppx(1), CSS.percent(1)).type()
        #  => {percentHint: "resolution", resolution: 1}
        a = CSS.dppx(1)
        b = CSS.percent(1)
        c = CSSMathSum(a, b)
        self.assertEqual(2, len(c.values))
        self.assertEqual(a, c.values[0])
        self.assertEqual(b, c.values[1])
        t = CSSNumericType()
        t.resolution = 1
        t.percent_hint = 'resolution'
        self.assertEqual(t, c.type())

        # CSSMathSum(
        #  CSS.px(1), new CSSMathSum(CSS.px(1), CSS.percent(1))).type()
        #  => {length: 1, percentHint: "length"}
        a = CSS.px(1)
        b = CSSMathSum(CSS.px(1), CSS.percent(1))
        c = CSSMathSum(a, b)
        self.assertEqual(2, len(c.values))
        self.assertEqual(a, c.values[0])
        self.assertEqual(b, c.values[1])
        t = CSSNumericType()
        t.length = 1
        t.percent_hint = 'length'
        self.assertEqual(t, c.type())

    def test_css_math_sum_add(self):
        # CSSMathSum.add()
        # CSSMathSum(CSS.cm(10), CSS.cm(100))
        a = CSSMathSum(CSS.cm(10), CSS.cm(100))
        self.assertIsInstance(a.operator, CSSMathOperator)
        self.assertEqual(CSSMathOperator.SUM, a.operator)
        self.assertEqual(2, len(a.values))
        self.assertEqual(10, a.values[0].value)
        self.assertEqual('cm', a.values[0].unit)
        self.assertEqual(100, a.values[1].value)
        self.assertEqual('cm', a.values[1].unit)

        # CSSMathSum(CSS.cm(10), CSS.cm(100)).add(CSS.cm(20))
        # => CSSUnitValue(130, 'cm')
        b = a.add(CSS.cm(20))
        self.assertEqual(CSSMathOperator.SUM, a.operator)
        self.assertEqual(2, len(a.values))
        self.assertEqual(10, a.values[0].value)
        self.assertEqual('cm', a.values[0].unit)
        self.assertEqual(100, a.values[1].value)
        self.assertEqual('cm', a.values[1].unit)

        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(130, b.value)
        self.assertEqual('cm', b.unit)

        # CSSMathSum(CSS.cm(10), CSS.cm(100)).add(CSS.mm(50))
        # => CSSMathSum(CSS.cm(10), CSS.cm(100), CSS.mm(50))
        b = a.add(CSS.mm(50))
        self.assertEqual(CSSMathOperator.SUM, a.operator)
        self.assertEqual(2, len(a.values))
        self.assertEqual(10, a.values[0].value)
        self.assertEqual('cm', a.values[0].unit)
        self.assertEqual(100, a.values[1].value)
        self.assertEqual('cm', a.values[1].unit)

        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(CSSMathOperator.SUM, b.operator)
        self.assertEqual(3, len(b.values))
        self.assertEqual(10, b.values[0].value)
        self.assertEqual('cm', b.values[0].unit)
        self.assertEqual(100, b.values[1].value)
        self.assertEqual('cm', b.values[1].unit)
        self.assertEqual(50, b.values[2].value)
        self.assertEqual('mm', b.values[2].unit)

    def test_css_math_sum_equals(self):
        # CSSMathSum.equals()
        a = CSSMathSum(CSS.px(1), CSS.px(2))
        b = CSSMathSum(CSS.px(3))
        self.assertFalse(a.equals(b))

        b = CSSMathSum(CSS.px(2), CSS.px(1))
        self.assertFalse(a.equals(b))

        b = CSSMathSum(CSS.px(1), CSS.px(2))
        self.assertTrue(a.equals(b))

        a = CSS.in_(1)
        b = a.to('cm')
        c = a.to('in')
        self.assertFalse(a.equals(b, c))

        b = b.to('in')
        self.assertTrue(a.equals(b, c))

    def test_css_math_sum_to(self):
        # TODO: implement test_css_math_sum_to().
        # CSSMathSum.to()
        # a = CSSMathSum(CSS.number(1), CSS.number(2))
        # b = a.to('number')
        #
        # a = CSSMathSum(CSS.pt(1), CSS.px(2))
        # b = a.to('px')
        pass

    def test_css_math_sum_tostring(self):
        # CSSMathSum.tostring()
        a = CSSMathSum(CSS.number(1), CSS.number(2), CSS.number(3))
        self.assertEqual('calc(1 + 2 + 3)', a.tostring())

        a = CSSMathSum(-1, CSSMathNegate(2), CSSMathNegate(3))
        self.assertEqual('calc(-1 - 2 - 3)', a.tostring())

        a = CSSMathSum(1, CSSMathProduct(2, 3))
        self.assertEqual('calc(1 + (2 * 3))', a.tostring())

        a = CSSMathSum(1, CSSMathNegate(CSSMathProduct(2, 3)))
        self.assertEqual('calc(1 - (2 * 3))', a.tostring())

        a = CSSMathSum(1, CSSMathProduct(CSSMathNegate(2), 3))
        self.assertEqual('calc(1 + ((-2) * 3))', a.tostring())

    def test_css_numeric_type_apply_percent_hint(self):
        t = CSSNumericType()
        t.length = 1
        CSSNumericType.apply_percent_hint(t, CSSNumericType.LENGTH)
        self.assertEqual(2, len(t))
        self.assertEqual(1, t['length'])
        self.assertEqual('length', t['percent_hint'])

    def test_css_numeric_value_parse_calc00(self):
        # CSSNumericValue.parse(): 'calc()'
        text = 'calc()'
        # a = CSSNumericValue.parse(text)
        self.assertRaises(ValueError, lambda: CSSNumericValue.parse(text))

        text = 'calc(1)'
        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(1, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

    def test_css_numeric_value_parse_calc01(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 + 2 + 3 + 4)'
        # => CSSMathSum(1, 2, 3, 4)

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(4, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[3]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(4, b.value)
        self.assertEqual('number', b.unit)

        expected = 1 + 2 + 3 + 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc02(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(-1 - 2 - 3 - 4)'
        # => CSSMathSum(-1, CSSMathNegate(2), CSSMathNegate(3),
        #  CSSMathNegate(4))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(4, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(-1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathNegate)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSMathNegate)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('number', c.unit)

        expected = -1 - 2 - 3 - 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc03(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 * 2 * 3 * 4)'

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathProduct)
        self.assertEqual(4, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[3]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(4, b.value)
        self.assertEqual('number', b.unit)

        expected = 1 * 2 * 3 * 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc04(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 + 2 * 3 * 4)'
        # => CSSMathSum(1, CSSMathProduct(2, 3, 4))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(3, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[2]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(4, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 + 2 * 3 * 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc05(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 - 2 * 3 * 4)'
        # => CSSMathSum(1, CSSMathNegate(CSSMathProduct(2, 3, 4)))
        # == CSSMathSum(1, CSSMathProduct(CSSMathNegate(2), 3, 4))
        # FIXME: parse 'calc(a - b * c * d)'.

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(3, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathNegate)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(2, d.value)
        self.assertEqual('number', d.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[2]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(4, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 - 2 * 3 * 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc06(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 * 2 + 3 + 4)'
        # => CSSMathSum(CSSMathProduct(1, 2), 3, 4)

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(3, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(1, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(4, b.value)
        self.assertEqual('number', b.unit)

        expected = 1 * 2 + 3 + 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc07(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 + 2 * 3 - 4)'
        # => CSSMathSum(1, CSSMathProduct(2, 3), CSSMathNegate(4))
        # == CSSMathSum(1, CSSMathSum(CSSMathProduct(2, 3), CSSMathNegate(4)))
        # FIXME: parse 'calc(a + b * c - d)'

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathProduct)
        self.assertEqual(2, len(c.values))

        d = c.values[0]
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(2, d.value)
        self.assertEqual('number', d.unit)

        d = c.values[1]
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(3, d.value)
        self.assertEqual('number', d.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSMathNegate)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(4, d.value)
        self.assertEqual('number', d.unit)

        expected = 1 + 2 * 3 - 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc08(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 * 2 - 3 * 4)'
        # => CSSMathSum(CSSMathProduct(1, 2),
        #               CSSMathNegate(CSSMathProduct(3, 4)))
        # == CSSMathSum(CSSMathProduct(1, 2),
        #               CSSMathProduct(CSSMathNegate(3), 4))
        # FIXME: parse 'calc(a * b - c * d)'

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(1, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathNegate)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(3, d.value)
        self.assertEqual('number', d.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(4, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 * 2 - 3 * 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc09(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 * 2 * 3 - 4)'
        # => CSSMathSum(CSSMathProduct(1, 2, 3), CSSMathNegate(4))

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(3, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(1, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[2]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('number', c.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathNegate)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(4, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 * 2 * 3 - 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc10(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 / 2)'
        # => CSSMathProduct(1, CSSMathInvert(2))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathProduct)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathInvert)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 / 2
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc11(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 / 2 / 3 / 4)'
        # => CSSMathProduct(1, CSSMathInvert(2), CSSMathInvert(3),
        #                   CSSMathInvert(4))

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathProduct)
        self.assertEqual(4, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathInvert)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSMathInvert)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('number', c.unit)

        b = a.values[3]
        self.assertIsInstance(b, CSSMathInvert)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(4, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 / 2 / 3 / 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc12(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 / 2 + 3 / 4)'
        # => CSSMathSum(CSSMathProduct(1, CSSMathInvert(2)),
        #               CSSMathProduct(3, CSSMathInvert(4)))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(1, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSMathInvert)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(2, d.value)
        self.assertEqual('number', d.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSMathInvert)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(4, d.value)
        self.assertEqual('number', d.unit)

        expected = 1 / 2 + 3 / 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc13(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 / 2 - 3 / 4)'
        # => CSSMathSum(CSSMathProduct(1, CSSMathInvert(2)),
        #               CSSMathNegate(CSSMathProduct(3, CSSMathInvert(4))))
        # == CSSMathSum(CSSMathProduct(1, CSSMathInvert(2)),
        #               CSSMathProduct(CSSMathNegate(3), CSSMathInvert(4)))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(1, c.value)
        self.assertEqual('number', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSMathInvert)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(2, d.value)
        self.assertEqual('number', d.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathNegate)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(3, d.value)
        self.assertEqual('number', d.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSMathInvert)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(4, d.value)
        self.assertEqual('number', d.unit)

        expected = 1 / 2 - 3 / 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc14(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 - 2 / 3 + 4)'
        # => CSSMathSum(1, CSSMathNegate(CSSMathProduct(2, CSSMathInvert(3))),
        #               4)
        # == CSSMathSum(1, CSSMathProduct(CSSMathNegate(2), CSSMathInvert(3)),
        #               4)

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(3, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathNegate)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(2, d.value)
        self.assertEqual('number', d.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSMathInvert)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(3, d.value)
        self.assertEqual('number', d.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(4, b.value)
        self.assertEqual('number', b.unit)

        expected = 1 - 2 / 3 + 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc15(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        text = 'calc(1 - 2 / 3 * 4)'
        # => CSSMathSum(1,
        #               CSSMathProduct(CSSMathNegate(2), CSSMathInvert(3), 4))
        # == CSSMathSum(1,
        #               CSSMathProduct(CSSMathProduct(CSSMathNegate(2),
        #                                             CSSMathInvert(3)),
        #                              4))
        # FIXME: parse 'calc(a - b / c * d)'.

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathProduct)
        self.assertEqual(2, len(c.values))

        d = c.values[0]
        self.assertIsInstance(d, CSSMathNegate)
        e = d.value
        self.assertIsInstance(e, CSSUnitValue)
        self.assertEqual(2, e.value)
        self.assertEqual('number', e.unit)

        d = c.values[1]
        self.assertIsInstance(d, CSSMathInvert)
        e = d.value
        self.assertIsInstance(e, CSSUnitValue)
        self.assertEqual(3, e.value)
        self.assertEqual('number', e.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(4, c.value)
        self.assertEqual('number', c.unit)

        expected = 1 - 2 / 3 * 4
        self.assertEqual(expected, a.to('number'))

    def test_css_numeric_value_parse_calc16(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        text = 'calc(56em + 10%)'
        # => CSSMathSum(CSS.em(56), CSS.percent(10))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(56, b.value)
        self.assertEqual('em', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(10, b.value)
        self.assertEqual('percent', b.unit)

        self.assertRaises(ValueError, lambda: a.to('em'))

        t = a.type()
        self.assertEqual(2, len(t))
        self.assertEqual(1, t['length'])
        self.assertEqual('length', t['percent_hint'])

    def test_css_numeric_value_parse_calc17(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        text = 'calc(1px * 2em)'
        # => CSSMathProduct(CSS.px(1), CSS.em(2))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathProduct)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('px', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('em', b.unit)

        self.assertRaises(ValueError, lambda: a.to('em'))

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(2, t['length'])

    def test_css_numeric_value_parse_calc18(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        text = 'calc(100vw / 35)'
        # => CSSMathSum(CSS.vw(100 / 35))  ... blink
        # == CSSMathProduct(CSS.vw(100), CSSMathInvert(35))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathProduct)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(100, b.value)
        self.assertEqual('vw', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathInvert)
        c = b.value
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(35, c.value)
        self.assertEqual('number', c.unit)

        n = a.to('vw')
        expected = 100 / 35
        self.assertEqual(expected, n.value)
        self.assertEqual('vw', n.unit)

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(1, t['length'])

    def test_css_numeric_value_parse_calc19(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        # See [css-typed-om] EXAMPLE 5.1
        text = 'calc(1em + 5px)'
        # => CSSMathSum(CSS.em(1), CSS.px(5))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('em', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(5, b.value)
        self.assertEqual('px', b.unit)

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(1, t['length'])

    def test_css_numeric_value_parse_calc20(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        # See [css-typed-om] EXAMPLE 5.2
        text = 'calc(1em + 5px * 2)'
        # => CSSMathSum(CSS.em(1), CSSMathProduct(CSS.px(5), 2))

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('em', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(5, c.value)
        self.assertEqual('px', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('number', c.unit)

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('px'))
        self.assertRaises(ValueError, lambda: a.to('number'))

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(1, t['length'])

    def test_css_numeric_value_parse_calc22(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        # See [css-typed-om] EXAMPLE 9
        text = 'calc(1px - 2 * 3em)'
        # =>
        # CSSMathSum(
        #     CSS.px(1),
        #     CSSMathNegate(
        #         CSSMathProduct(
        #             2,
        #             CSS.em(3)
        #         )
        #     )
        # )
        # == CSSMathSum(CSS.px(1),
        #               CSSMathProduct(CSSMathNegate(2), CSS.em(3)))

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('px', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSMathProduct)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSMathNegate)
        d = c.value
        self.assertIsInstance(d, CSSUnitValue)
        self.assertEqual(2, d.value)
        self.assertEqual('number', d.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(3, c.value)
        self.assertEqual('em', c.unit)

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('px'))
        self.assertRaises(ValueError, lambda: a.to('number'))

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(1, t['length'])

    def test_css_numeric_value_parse_calc23(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        # See [css-typed-om] EXAMPLE 10.1
        text = 'calc(1px + 2px + 3px)'
        # =>
        # CSSMathSum(
        #     CSS.px(1),
        #     CSS.px(2),
        #     CSS.px(3)
        # )

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(3, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('px', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('px', b.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('px', b.unit)

        n = a.to('px')
        expected = 1 + 2 + 3
        self.assertEqual(expected, n.value)
        self.assertEqual('px', n.unit)

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(1, t['length'])

    def test_css_numeric_value_parse_calc24(self):
        # CSSNumericValue.parse(): 'calc()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        # See [css-typed-om] EXAMPLE 10.2
        text = 'calc(calc(1px + 2px) + 3px)'
        # =>
        # CSSMathSum(
        #     CSSMathSum(
        #         CSS.px(1),
        #         CSS.px(2)
        #     ),
        #     CSS.px(3)
        # )

        a = CSSNumericValue.parse(text)
        # _debug_print_numeric_value(text, a)
        self.assertIsInstance(a, CSSMathSum)
        self.assertEqual(2, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(1, c.value)
        self.assertEqual('px', c.unit)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual(2, c.value)
        self.assertEqual('px', c.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('px', b.unit)

        n = a.to('px')
        expected = (1 + 2) + 3
        self.assertEqual(expected, n.value)
        self.assertEqual('px', n.unit)

        t = a.type()
        self.assertEqual(1, len(t))
        self.assertEqual(1, t['length'])

    def test_css_numeric_value_parse_clamp(self):
        # CSSNumericValue.parse(): 'clamp()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        text = 'clamp(1, 2, 3)'

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathClamp)
        self.assertEqual(text, a.tostring())

        b = a.min
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.val
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('number', b.unit)

        b = a.max
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('number', b.unit)

        self.assertRaises(ValueError, lambda: a.to('number'))

        t = a.type()
        self.assertEqual(0, len(t))

    def test_css_numeric_value_parse_max(self):
        # CSSNumericValue.parse(): 'max()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        text = 'max(1, 2, 3)'

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathMax)
        self.assertEqual(3, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('number', b.unit)

        expected = max(1, 2, 3)
        self.assertEqual(expected, a.to('number'))

        t = a.type()
        self.assertEqual(0, len(t))

    def test_css_numeric_value_parse_min(self):
        # CSSNumericValue.parse(): 'min()'
        # CSSNumericValue.to()
        # CSSNumericValue.type()
        text = 'min(1, 2, 3)'

        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSMathMin)
        self.assertEqual(3, len(a.values))
        self.assertEqual(text, a.tostring())

        b = a.values[0]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(1, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[1]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(2, b.value)
        self.assertEqual('number', b.unit)

        b = a.values[2]
        self.assertIsInstance(b, CSSUnitValue)
        self.assertEqual(3, b.value)
        self.assertEqual('number', b.unit)

        expected = min(1, 2, 3)
        self.assertEqual(expected, a.to('number'))

        t = a.type()
        self.assertEqual(0, len(t))

    def test_css_numeric_value_parse_numeric_value(self):
        # CSSNumericValue.parse()
        text = ''
        # a = CSSNumericValue.parse(text)
        self.assertRaises(ValueError, lambda: CSSNumericValue.parse(text))

        text = 'px'
        # a = CSSNumericValue.parse(text)
        self.assertRaises(ValueError, lambda: CSSNumericValue.parse(text))

        text = '0'
        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual('number', a.unit)
        self.assertEqual(0, a.value)

        text = '0%'
        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual('percent', a.unit)
        self.assertEqual(0, a.value)

        text = '0px'
        a = CSSNumericValue.parse(text)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual('px', a.unit)
        self.assertEqual(0, a.value)

    def test_css_numeric_value_to_sum01(self):
        # CSSNumericValue.to_sum()
        a = CSSMathSum(1, 2, 3)

        b = a.to_sum()
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(1, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('number', c.unit)
        expected = 1 + 2 + 3
        self.assertEqual(expected, c.value)

        b = a.to_sum('number', 'percent')
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('number', c.unit)
        expected = 1 + 2 + 3
        self.assertEqual(expected, c.value)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('percent', c.unit)
        expected = 0
        self.assertEqual(expected, c.value)

    def test_css_numeric_value_to_sum02(self):
        # CSSNumericValue.to_sum()
        a = CSSMathSum(CSS.em(1),
                       CSS.ex(2),
                       CSS.ch(3),
                       CSS.ic(4),
                       CSS.rem(5),
                       CSS.lh(6),
                       CSS.rlh(7),
                       CSSMathSum(CSS.px(1), CSS.in_(1)))

        b = a.to_sum()
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(8, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('ch', c.unit)
        self.assertEqual(3, c.value)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('em', c.unit)
        self.assertEqual(1, c.value)

        c = b.values[2]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('ex', c.unit)
        self.assertEqual(2, c.value)

        c = b.values[3]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('ic', c.unit)
        self.assertEqual(4, c.value)

        c = b.values[4]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('lh', c.unit)
        self.assertEqual(6, c.value)

        c = b.values[5]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('px', c.unit)
        expected = 1 + 96
        self.assertEqual(expected, c.value)

        c = b.values[6]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('rem', c.unit)
        self.assertEqual(5, c.value)

        c = b.values[7]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('rlh', c.unit)
        self.assertEqual(7, c.value)

    def test_css_numeric_value_to_sum03(self):
        # CSSNumericValue.to_sum()
        a = CSSMathSum(CSS.pt(1), CSS.pc(2), CSS.vw(0.1))

        b = a.to_sum()
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(2, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('px', c.unit)
        # 1pt = 1 * 96 / 72 (px)
        # 2pc = 2 * 12 (pt) = 24 * 96 / 72 (px)
        expected = 1 * 96 / 72 + 24 * 96 / 72
        self.assertEqual(expected, c.value)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('vw', c.unit)
        self.assertEqual(0.1, c.value)

        b = a.to_sum('pt', 'vw', 'vh')
        self.assertIsInstance(b, CSSMathSum)
        self.assertEqual(3, len(b.values))

        c = b.values[0]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('pt', c.unit)
        # 2pc = 2 * 12 (pt)
        expected = 1 + 24
        self.assertEqual(expected, c.value)

        c = b.values[1]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('vw', c.unit)
        self.assertEqual(0.1, c.value)

        c = b.values[2]
        self.assertIsInstance(c, CSSUnitValue)
        self.assertEqual('vh', c.unit)
        self.assertEqual(0, c.value)

    def test_css_style_value_parse_css_wide_keywords(self):
        property_name = 'color'

        # CSS-wide keywords
        text = 'initial'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('initial', value.tostring())

        text = 'Inherit'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('inherit', value.tostring())

        text = 'UNSET'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('unset', value.tostring())

    def test_css_style_value_parse_alignment_baseline(self):
        property_name = 'alignment-baseline'

        text = 'baseline'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_baseline_shift(self):
        property_name = 'baseline-shift'

        text = 'sub'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_clip_path(self):
        property_name = 'clip-path'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url("#clip1")'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'circle(50%) stroke-box'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_clip_rule(self):
        property_name = 'clip-rule'

        text = 'nonzero'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_color(self):
        property_name = 'color'

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = '#ff0000'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))
        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'rgb(0 255 0)'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))
        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_color_interpolation(self):
        property_name = 'color-interpolation'

        text = 'sRGB'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_color_interpolation_filters(self):
        property_name = 'color-interpolation-filters'

        text = 'linearRGB'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_color_rendering(self):
        property_name = 'color-rendering'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_cursor(self):
        property_name = 'cursor'

        text = "url(example.svg#linkcursor)," \
               " url(hyper.cur)," \
               " url(hyper.png) 2 3," \
               " pointer"
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('url("example.svg#linkcursor")', value.tostring())

        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(4, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('url("example.svg#linkcursor")', value.tostring())

        value = values[1]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('url("hyper.cur")', value.tostring())

        value = values[2]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('url("hyper.png") 2 3', value.tostring())

        value = values[3]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('pointer', value.tostring())

    def test_css_style_value_parse_custom_property01(self):
        property_name = '--foo-bar'

        text = 'var(--foo)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnparsedValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(1, value.length)
        self.assertEqual(1, len(value))

        item = value[0]
        self.assertIsInstance(item, CSSVariableReferenceValue)
        self.assertEqual('--foo', item.variable)
        self.assertIsNone(item.fallback)

    def test_css_style_value_parse_custom_property02(self):
        property_name = '--foo-bar'

        # See [css-typed-om] EXAMPLE 7
        text = 'calc(42px + var(--foo, 15em) + var(--bar, var(--far) + 15px))'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnparsedValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(5, len(value))

        a = value[0]
        self.assertIsInstance(a, str)
        self.assertEqual('calc(42px + ', a)

        a = value[1]
        self.assertIsInstance(a, CSSVariableReferenceValue)
        self.assertEqual('--foo', a.variable)
        fb = a.fallback
        self.assertIsInstance(fb, CSSUnparsedValue)
        self.assertEqual(1, len(fb))

        b = fb[0]
        self.assertIsInstance(b, str)
        self.assertEqual(' 15em', b)

        a = value[2]
        self.assertIsInstance(a, str)
        self.assertEqual(' + ', a)

        a = value[3]
        self.assertIsInstance(a, CSSVariableReferenceValue)
        self.assertEqual('--bar', a.variable)
        fb = a.fallback
        self.assertIsInstance(fb, CSSUnparsedValue)
        self.assertEqual(3, len(fb))

        b = fb[0]
        self.assertIsInstance(b, str)
        self.assertEqual(' ', b)

        b = fb[1]
        self.assertIsInstance(b, CSSVariableReferenceValue)
        self.assertEqual('--far', b.variable)
        self.assertIsNone(b.fallback)

        b = fb[2]
        self.assertIsInstance(b, str)
        self.assertEqual(' + 15px', b)

        a = value[4]
        self.assertIsInstance(a, str)
        self.assertEqual(')', a)

    def test_css_style_value_parse_cx(self):
        property_name = 'cx'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_cy(self):
        property_name = 'cy'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_d(self):
        property_name = 'd'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'M0,0 L100,100'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_direction(self):
        property_name = 'direction'

        text = 'ltr'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_display(self):
        property_name = 'display'

        text = 'inline'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_dominant_baseline(self):
        property_name = 'dominant-baseline'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_fill(self):
        property_name = 'fill'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '#000'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#foo) red'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'context-fill'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_fill_opacity(self):
        property_name = 'fill-opacity'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_fill_rule(self):
        property_name = 'fill-rule'

        text = 'nonzero'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_filter(self):
        property_name = 'filter'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'blur(0px) brightness(0%) contrast(0%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'url("#foo")'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_flood_color(self):
        property_name = 'flood-color'

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = '#ff0000'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))
        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'rgb(0 255 0)'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))
        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_flood_opacity(self):
        property_name = 'flood-opacity'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_font(self):
        property_name = 'font'

        text = '80% sans-serif'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'x-large/110% "new century schoolbook", serif'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_family(self):
        property_name = 'font-family'

        text = 'Helvetica, Verdana, sans-serif'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_feature_settings(self):
        property_name = 'font-feature-settings'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '"smcp", "swsh" 2'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_kerning(self):
        property_name = 'font-kerning'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_language_override(self):
        property_name = 'font-language-override'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '"SRB"'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_max_size(self):
        property_name = 'font-max-size'

        text = 'xx-small'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'larger'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'infinity'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0em'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('em', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_font_min_size(self):
        property_name = 'font-min-size'

        text = 'xx-small'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'larger'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0em'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('em', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_font_size(self):
        property_name = 'font-size'

        text = 'xx-small'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'larger'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0em'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('em', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_font_size_adjust(self):
        property_name = 'font-size-adjust'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

    def test_css_style_value_parse_font_stretch(self):
        property_name = 'font-stretch'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_font_style(self):
        property_name = 'font-style'

        text = 'oblique'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'oblique 0deg'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_synthesis(self):
        property_name = 'font-synthesis'

        text = 'weight'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'style'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'weight style'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_synthesis_small_caps(self):
        property_name = 'font-synthesis-small-caps'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_synthesis_style(self):
        property_name = 'font-synthesis-style'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_synthesis_weight(self):
        property_name = 'font-synthesis-weight'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant(self):
        property_name = 'font-variant'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = "common-ligatures discretionary-ligatures" \
               " historical-ligatures contextual small-caps lining-nums" \
               " proportional-nums diagonal-fractions ordinal slashed-zero" \
               " jis78 full-width ruby sub"
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_alternates(self):
        property_name = 'font-variant-alternates'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'historical-forms'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'stylistic("salt" 1)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'historical-forms stylistic("salt" 1)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_caps(self):
        property_name = 'font-variant-caps'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_east_asian(self):
        property_name = 'font-variant-east-asian'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'jis78 full-width ruby'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_emoji(self):
        property_name = 'font-variant-emoji'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_ligatures(self):
        property_name = 'font-variant-ligatures'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = "common-ligatures discretionary-ligatures" \
               " historical-ligatures contextual"
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_numeric(self):
        property_name = 'font-variant-numeric'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'lining-nums proportional-nums diagonal-fractions ordinal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variant_position(self):
        property_name = 'font-variant-position'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_variation_settings(self):
        property_name = 'font-variation-settings'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '"wght" 1.0, "wdth" 1.0, "slnt" 0.0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_font_weight(self):
        property_name = 'font-weight'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

    def test_css_style_value_parse_glyph_orientation_vertical(self):
        property_name = 'glyph-orientation-vertical'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0deg'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('deg', value.unit)

    def test_css_style_value_parse_height(self):
        property_name = 'height'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'fit-content(50%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_image_rendering(self):
        property_name = 'image-rendering'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_inline_size(self):
        property_name = 'inline-size'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0em'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('em', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_inline_sizing(self):
        property_name = 'inline-sizing'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_isolation(self):
        property_name = 'isolation'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'isolate'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_letter_spacing(self):
        property_name = 'letter-spacing'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0em'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('em', value.unit)

    def test_css_style_value_parse_line_height(self):
        property_name = 'line-height'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

    def test_css_style_value_parse_line_sizing(self):
        property_name = 'line-sizing'

        text = 'current-behavior'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_lighting_color(self):
        property_name = 'lighting-color'

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = '#ff0000'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))
        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'rgb(0 255 0)'
        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(1, len(values))
        value = values[0]
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_marker(self):
        property_name = 'marker'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#marker)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_marker_end(self):
        property_name = 'marker-end'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#marker)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_marker_mid(self):
        property_name = 'marker-mid'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#marker)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_marker_start(self):
        property_name = 'marker-start'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#marker)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask(self):
        property_name = 'mask'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'linear-gradient(black 0%, transparent 100%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSImageValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#mask)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#mask) 0% 0% repeat border-box add match-source'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_clip(self):
        property_name = 'mask-clip'

        text = 'border-box'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'border-box, fill-box, no-clip'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_composite(self):
        property_name = 'mask-composite'

        text = 'add'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'add, exclude'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_image(self):
        property_name = 'mask-image'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'linear-gradient(black 0%, transparent 100%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSImageValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#mask)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual(text, value.tostring())

        text = 'linear-gradient(black 0%, transparent 100%), url(#mask)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_mode(self):
        property_name = 'mask-mode'

        text = 'match-source'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'match-source, alpha'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_origin(self):
        property_name = 'mask-origin'

        text = 'border-box'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'border-box, fill-box'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_position(self):
        property_name = 'mask-position'

        text = 'left'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0% 0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'left, 0% 0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_repeat(self):
        property_name = 'mask-repeat'

        text = 'repeat'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'repeat space'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'repeat, repeat space'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_size(self):
        property_name = 'mask-size'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'auto 0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'auto 0%, 0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_mask_type(self):
        property_name = 'mask-type'

        text = 'luminance'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_max_height(self):
        property_name = 'max-height'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'fit-content(0%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_max_width(self):
        property_name = 'max-width'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'fit-content(0%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_min_height(self):
        property_name = 'min-height'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'fit-content(0%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_min_width(self):
        property_name = 'min-width'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'fit-content(0%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_opacity(self):
        property_name = 'opacity'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_overflow(self):
        property_name = 'overflow'

        text = 'visible'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

        text = 'visible auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_overflow_x(self):
        property_name = 'overflow-x'

        text = 'visible'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_overflow_y(self):
        property_name = 'overflow-y'

        text = 'visible'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_paint_order(self):
        property_name = 'paint-order'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'fill stroke markers'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSStyleValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_pointer_events(self):
        property_name = 'pointer-events'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_r(self):
        property_name = 'r'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_rx(self):
        property_name = 'rx'

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_ry(self):
        property_name = 'ry'

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_shape_image_threshold(self):
        property_name = 'shape-image-threshold'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

    def test_css_style_value_parse_shape_inside(self):
        property_name = 'shape-inside'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'circle(120px at 150px 150px)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#wrap)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'circle(120px at 150px 150px) url(#wrap)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_shape_margin(self):
        property_name = 'shape-margin'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_shape_padding(self):
        property_name = 'shape-padding'

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

    def test_css_style_value_parse_shape_rendering(self):
        property_name = 'shape-rendering'

        text = 'optimizeSpeed'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_shape_subtract(self):
        property_name = 'shape-subtract'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'circle(50% at 50% 50%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#rect2)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'circle(50% at 50% 50%) url(#rect2)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_stop_color(self):
        property_name = 'stop-color'

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = '#CD853F'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '#CD853F icc-color(FooColors, Sandy23C)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_stop_opacity(self):
        property_name = 'stop-opacity'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_stroke(self):
        property_name = 'stroke'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#s1)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#s1) black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_stroke_dasharray(self):
        property_name = 'stroke-dasharray'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '5'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '5, 3, 2'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_stroke_dashoffset(self):
        property_name = 'stroke-dashoffset'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_stroke_linecap(self):
        property_name = 'stroke-linecap'

        text = 'butt'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_stroke_linejoin(self):
        property_name = 'stroke-linejoin'

        text = 'miter'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_stroke_miterlimit(self):
        property_name = 'stroke-miterlimit'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

    def test_css_style_value_parse_stroke_opacity(self):
        property_name = 'stroke-opacity'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_stroke_width(self):
        property_name = 'stroke-width'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_text_align(self):
        property_name = 'text-align'

        text = 'center'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '"." center'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_align_all(self):
        property_name = 'text-align-all'

        text = 'start'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_align_last(self):
        property_name = 'text-align-last'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_anchor(self):
        property_name = 'text-anchor'

        text = 'start'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration(self):
        property_name = 'text-decoration'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'underline solid black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'underline solid rgb(0 0 0)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration_color(self):
        property_name = 'text-decoration-color'

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '#000'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'rgb(0 0 0)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration_fill(self):
        property_name = 'text-decoration-fill'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '#000'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'rgb(0 0 0)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#fill)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration_line(self):
        property_name = 'text-decoration-line'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'underline overline line-through blink'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration_stroke(self):
        property_name = 'text-decoration-stroke'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentcolor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'currentColor'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('currentcolor', value.tostring())

        text = 'black'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '#000'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'rgb(0 0 0)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'url(#fill)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration_style(self):
        property_name = 'text-decoration-style'

        text = 'solid'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_decoration_width(self):
        property_name = 'text-decoration-width'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

    def test_css_style_value_parse_text_indent(self):
        property_name = 'text-indent'

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px hanging'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0px hanging each-line'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_orientation(self):
        property_name = 'text-orientation'

        text = 'mixed'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_overflow(self):
        property_name = 'text-overflow'

        text = 'fade'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '""'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'fade(50%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '"" fade'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '".." ".."'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_rendering(self):
        property_name = 'text-rendering'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_space_collapse(self):
        property_name = 'text-space-collapse'

        text = 'collapse'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_space_trim(self):
        property_name = 'text-space-trim'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'trim-inner discard-before discard-after'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_text_wrap(self):
        property_name = 'text-wrap'

        text = 'wrap'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_unicode_bidi(self):
        property_name = 'unicode-bidi'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_vector_effect(self):
        property_name = 'vector-effect'

        text = 'none'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = 'non-scaling-size fixed-position'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_vertical_align(self):
        property_name = 'vertical-align'

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = 'baseline'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0px baseline'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_visibility(self):
        property_name = 'visibility'

        text = 'visible'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_white_space(self):
        property_name = 'white-space'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_width(self):
        property_name = 'width'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

        text = 'fit-content(50%)'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_will_change(self):
        property_name = 'will-change'

        text = 'auto'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        # TODO: TBC: parse 'will-change' property.
        text = 'background, opacity'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('background', value.tostring())

        values = CSSStyleValue.parse_all(property_name, text)
        self.assertEqual(2, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('background', value.tostring())

        value = values[1]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('opacity', value.tostring())

    def test_css_style_value_parse_word_spacing(self):
        property_name = 'word-spacing'

        text = 'normal'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_writing_mode(self):
        property_name = 'writing-mode'

        text = 'horizontal-tb'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual(text, value.tostring())

    def test_css_style_value_parse_x(self):
        property_name = 'x'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_x1(self):
        property_name = 'x1'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_x2(self):
        property_name = 'x2'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_y(self):
        property_name = 'y'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_y1(self):
        property_name = 'y1'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_style_value_parse_y2(self):
        property_name = 'y2'

        text = '0'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('number', value.unit)

        text = '0px'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('px', value.unit)

        text = '0%'
        value = CSSStyleValue.parse(property_name, text)
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual(text, value.tostring())
        self.assertEqual(0, value.value)
        self.assertEqual('percent', value.unit)

    def test_css_support01(self):
        property_name = 'width'

        text = 'inherit'
        result = CSS.supports(property_name, text)
        self.assertTrue(result)

        text = 'auto'
        result = CSS.supports(property_name, text)
        self.assertTrue(result)

        text = '0'
        result = CSS.supports(property_name, text)
        self.assertTrue(result)

        text = '0px'
        result = CSS.supports(property_name, text)
        self.assertTrue(result)

        text = 'none'
        result = CSS.supports(property_name, text)
        self.assertFalse(result)

        text = 'inherit auto'
        result = CSS.supports(property_name, text)
        self.assertFalse(result)

    def test_css_unit_value(self):
        # CSSUnitValue()
        n = math.pi  # 3.141592653589793...
        a = CSS.number(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('number', a.unit)
        self.assertEqual('3.141593', a.tostring())
        t = CSSNumericType()
        self.assertEqual(t, a.type())

        formatter.precision = 2
        self.assertEqual('3.14', a.tostring())

        n = 1.5
        a = CSS.percent(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('percent', a.unit)
        self.assertEqual('1.5%', a.tostring())
        t = CSSNumericType()
        t.percent = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.em(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('em', a.unit)
        self.assertEqual('1.5em', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.ex(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('ex', a.unit)
        self.assertEqual('1.5ex', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.ch(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('ch', a.unit)
        self.assertEqual('1.5ch', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.ic(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('ic', a.unit)
        self.assertEqual('1.5ic', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.rem(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('rem', a.unit)
        self.assertEqual('1.5rem', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.lh(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('lh', a.unit)
        self.assertEqual('1.5lh', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.rlh(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('rlh', a.unit)
        self.assertEqual('1.5rlh', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.vw(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('vw', a.unit)
        self.assertEqual('1.5vw', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.vh(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('vh', a.unit)
        self.assertEqual('1.5vh', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.vi(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('vi', a.unit)
        self.assertEqual('1.5vi', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.vb(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('vb', a.unit)
        self.assertEqual('1.5vb', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.vmin(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('vmin', a.unit)
        self.assertEqual('1.5vmin', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.vmax(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('vmax', a.unit)
        self.assertEqual('1.5vmax', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.cm(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('cm', a.unit)
        self.assertEqual('1.5cm', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.mm(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('mm', a.unit)
        self.assertEqual('1.5mm', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.q(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('q', a.unit)
        self.assertEqual('1.5q', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.in_(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('in', a.unit)
        self.assertEqual('1.5in', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.pt(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('pt', a.unit)
        self.assertEqual('1.5pt', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.pc(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('pc', a.unit)
        self.assertEqual('1.5pc', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 1.5
        a = CSS.px(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('px', a.unit)
        self.assertEqual('1.5px', a.tostring())
        t = CSSNumericType()
        t.length = 1
        self.assertEqual(t, a.type())

        n = 90
        a = CSS.deg(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('deg', a.unit)
        self.assertEqual('90deg', a.tostring())
        t = CSSNumericType()
        t.angle = 1
        self.assertEqual(t, a.type())

        n = 100
        a = CSS.grad(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('grad', a.unit)
        self.assertEqual('100grad', a.tostring())
        t = CSSNumericType()
        t.angle = 1
        self.assertEqual(t, a.type())

        n = math.radians(90)  # 1.5707963267948966
        a = CSS.rad(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('rad', a.unit)
        self.assertEqual('1.57rad', a.tostring())
        t = CSSNumericType()
        t.angle = 1
        self.assertEqual(t, a.type())

        n = 0.25
        a = CSS.turn(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('turn', a.unit)
        self.assertEqual('0.25turn', a.tostring())
        t = CSSNumericType()
        t.angle = 1
        self.assertEqual(t, a.type())

        n = 1
        a = CSS.s(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('s', a.unit)
        self.assertEqual('1s', a.tostring())
        t = CSSNumericType()
        t.time = 1
        self.assertEqual(t, a.type())

        n = 1000
        a = CSS.ms(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('ms', a.unit)
        self.assertEqual('1000ms', a.tostring())
        t = CSSNumericType()
        t.time = 1
        self.assertEqual(t, a.type())

        n = 60
        a = CSS.hz(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('hz', a.unit)
        self.assertEqual('60hz', a.tostring())
        t = CSSNumericType()
        t.frequency = 1
        self.assertEqual(t, a.type())

        n = 0.06
        a = CSS.khz(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('khz', a.unit)
        self.assertEqual('0.06khz', a.tostring())
        t = CSSNumericType()
        t.frequency = 1
        self.assertEqual(t, a.type())

        n = 96
        a = CSS.dpi(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('dpi', a.unit)
        self.assertEqual('96dpi', a.tostring())
        t = CSSNumericType()
        t.resolution = 1
        self.assertEqual(t, a.type())

        n = 96
        a = CSS.dpi(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('dpi', a.unit)
        self.assertEqual('96dpi', a.tostring())
        t = CSSNumericType()
        t.resolution = 1
        self.assertEqual(t, a.type())

        n = 96 / 2.54  # 37.79527559055118...
        a = CSS.dpcm(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('dpcm', a.unit)
        self.assertEqual('37.8dpcm', a.tostring())
        t = CSSNumericType()
        t.resolution = 1
        self.assertEqual(t, a.type())

        n = 1.0
        a = CSS.dppx(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('dppx', a.unit)
        self.assertEqual('1dppx', a.tostring())
        t = CSSNumericType()
        t.resolution = 1
        self.assertEqual(t, a.type())

        n = 1
        a = CSS.fr(n)
        self.assertIsInstance(a, CSSUnitValue)
        self.assertEqual(n, a.value)
        self.assertEqual('fr', a.unit)
        self.assertEqual('1fr', a.tostring())
        t = CSSNumericType()
        t.flex = 1
        self.assertEqual(t, a.type())

    def test_css_unit_value_add(self):
        pass
        # v = CSS.cm(10)
        # result = val.add(CSS.cm(15))
        # print(result.values)
        # result = val.add(CSS.in_(15), 120)
        # print([result.operator, result.values])

    def test_css_unit_value_eq(self):
        a = CSS.number(1)

        CSSUnitValue.rel_tol = 1e-9

        difference = Decimal(1e-10)
        self.assertTrue(a == CSS.number(1 - difference))

        difference = Decimal(1e-9)
        self.assertTrue(a == CSS.number(1 - difference))

        difference = Decimal(1e-8)
        self.assertFalse(a == CSS.number(1 - difference))

        CSSUnitValue.rel_tol = 1e-4

        difference = Decimal(1e-5)
        self.assertTrue(a == CSS.number(1 - difference))

        difference = Decimal(1e-4)
        self.assertTrue(a == CSS.number(1 - difference))

        difference = Decimal(1e-3)
        self.assertFalse(a == CSS.number(1 - difference))

    def test_css_unit_value_eq_cm(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.cm(1)

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_dpi(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.dpi(96)

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))
        self.assertRaises(ValueError, lambda: a == CSS.cm(1))
        self.assertRaises(ValueError, lambda: a == CSS.mm(1))
        self.assertRaises(ValueError, lambda: a == CSS.q(1))
        self.assertRaises(ValueError, lambda: a == CSS.in_(1))
        self.assertRaises(ValueError, lambda: a == CSS.pt(1))
        self.assertRaises(ValueError, lambda: a == CSS.pc(1))
        self.assertRaises(ValueError, lambda: a == CSS.px(1))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertTrue(a == CSS.dpi(96))
        self.assertTrue(a <= CSS.dpi(96))
        self.assertTrue(a >= CSS.dpi(96))

        self.assertTrue(a == CSS.dpcm(Decimal(96) / Decimal(2.54)))
        self.assertTrue(a <= CSS.dpcm(Decimal(96) / Decimal(2.54)))
        self.assertTrue(a >= CSS.dpcm(Decimal(96) / Decimal(2.54)))

        self.assertTrue(a == CSS.dppx(96 / 96))
        self.assertTrue(a <= CSS.dppx(96 / 96))
        self.assertTrue(a >= CSS.dppx(96 / 96))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_in(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.in_(1 / Decimal(2.54))

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_mm(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.mm(10)

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_number(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.number(1)

        self.assertTrue(a == 1)
        self.assertTrue(a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))
        self.assertRaises(ValueError, lambda: a == CSS.cm(1))
        self.assertRaises(ValueError, lambda: a == CSS.mm(1))
        self.assertRaises(ValueError, lambda: a == CSS.q(1))
        self.assertRaises(ValueError, lambda: a == CSS.in_(1))
        self.assertRaises(ValueError, lambda: a == CSS.pt(1))
        self.assertRaises(ValueError, lambda: a == CSS.pc(1))
        self.assertRaises(ValueError, lambda: a == CSS.px(1))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_pc(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.pc(1 / Decimal(2.54) * Decimal(6))

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_percent(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.percent(1)

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertTrue(a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))
        self.assertRaises(ValueError, lambda: a == CSS.cm(1))
        self.assertRaises(ValueError, lambda: a == CSS.mm(1))
        self.assertRaises(ValueError, lambda: a == CSS.q(1))
        self.assertRaises(ValueError, lambda: a == CSS.in_(1))
        self.assertRaises(ValueError, lambda: a == CSS.pt(1))
        self.assertRaises(ValueError, lambda: a == CSS.pc(1))
        self.assertRaises(ValueError, lambda: a == CSS.px(1))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_pt(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.pt(1 / Decimal(2.54) * Decimal(72))

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_px(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.px(1 / Decimal(2.54) * Decimal(96))

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_eq_q(self):
        # CSSUnitValue() == CSSUnitValue()
        # CSSUnitValue() <= CSSUnitValue()
        # CSSUnitValue() >= CSSUnitValue()
        a = CSS.q(40)

        self.assertRaises(ValueError, lambda: a == 1)
        self.assertRaises(ValueError, lambda: a == CSS.number(1))
        self.assertRaises(ValueError, lambda: a == CSS.percent(1))

        self.assertRaises(ValueError, lambda: a == CSS.em(1))
        self.assertRaises(ValueError, lambda: a == CSS.ex(1))
        self.assertRaises(ValueError, lambda: a == CSS.ch(1))
        self.assertRaises(ValueError, lambda: a == CSS.ic(1))
        self.assertRaises(ValueError, lambda: a == CSS.rem(1))
        self.assertRaises(ValueError, lambda: a == CSS.lh(1))
        self.assertRaises(ValueError, lambda: a == CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vw(1))
        self.assertRaises(ValueError, lambda: a == CSS.vh(1))
        self.assertRaises(ValueError, lambda: a == CSS.vi(1))
        self.assertRaises(ValueError, lambda: a == CSS.vb(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a == CSS.vmax(1))

        self.assertTrue(a == CSS.cm(1))
        self.assertTrue(a <= CSS.cm(1))
        self.assertTrue(a >= CSS.cm(1))

        self.assertTrue(a == CSS.mm(10))
        self.assertTrue(a <= CSS.mm(10))
        self.assertTrue(a >= CSS.mm(10))

        self.assertTrue(a == CSS.q(40))
        self.assertTrue(a <= CSS.q(40))
        self.assertTrue(a >= CSS.q(40))

        self.assertTrue(a == CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a <= CSS.in_(1 / Decimal(2.54)))
        self.assertTrue(a >= CSS.in_(1 / Decimal(2.54)))

        self.assertTrue(a == CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a <= CSS.pt(1 / Decimal(2.54) * Decimal(72)))
        self.assertTrue(a >= CSS.pt(1 / Decimal(2.54) * Decimal(72)))

        self.assertTrue(a == CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a <= CSS.pc(1 / Decimal(2.54) * Decimal(6)))
        self.assertTrue(a >= CSS.pc(1 / Decimal(2.54) * Decimal(6)))

        self.assertTrue(a == CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a <= CSS.px(1 / Decimal(2.54) * Decimal(96)))
        self.assertTrue(a >= CSS.px(1 / Decimal(2.54) * Decimal(96)))

        self.assertRaises(ValueError, lambda: a == CSS.deg(1))
        self.assertRaises(ValueError, lambda: a == CSS.grad(1))
        self.assertRaises(ValueError, lambda: a == CSS.rad(1))
        self.assertRaises(ValueError, lambda: a == CSS.turn(1))

        self.assertRaises(ValueError, lambda: a == CSS.s(1))
        self.assertRaises(ValueError, lambda: a == CSS.ms(1))

        self.assertRaises(ValueError, lambda: a == CSS.hz(1))
        self.assertRaises(ValueError, lambda: a == CSS.khz(1))

        self.assertRaises(ValueError, lambda: a == CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a == CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a == CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a == CSS.fr(1))

    def test_css_unit_value_gt_cm(self):
        # CSSUnitValue() > CSSUnitValue()
        a = CSS.cm(1)

        difference = Decimal(1e-9)
        self.assertTrue(CSS.number(1) == CSS.number(1 - difference))

        difference = Decimal(1e-8)
        self.assertFalse(CSS.number(1) == CSS.number(1 - difference))

        self.assertRaises(ValueError, lambda: a > 1)
        self.assertRaises(ValueError, lambda: a > CSS.number(1))
        self.assertRaises(ValueError, lambda: a > CSS.percent(1))

        self.assertRaises(ValueError, lambda: a > CSS.em(1))
        self.assertRaises(ValueError, lambda: a > CSS.ex(1))
        self.assertRaises(ValueError, lambda: a > CSS.ch(1))
        self.assertRaises(ValueError, lambda: a > CSS.ic(1))
        self.assertRaises(ValueError, lambda: a > CSS.rem(1))
        self.assertRaises(ValueError, lambda: a > CSS.lh(1))
        self.assertRaises(ValueError, lambda: a > CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a > CSS.vw(1))
        self.assertRaises(ValueError, lambda: a > CSS.vh(1))
        self.assertRaises(ValueError, lambda: a > CSS.vi(1))
        self.assertRaises(ValueError, lambda: a > CSS.vb(1))
        self.assertRaises(ValueError, lambda: a > CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a > CSS.vmax(1))

        b = CSS.cm(Decimal(a.value) - difference)
        self.assertTrue(a > b)

        b = CSS.cm(Decimal(a.value) - difference).to('mm')
        self.assertTrue(a > b)

        b = CSS.cm(Decimal(a.value) - difference).to('Q')
        self.assertTrue(a > b)

        b = CSS.cm(Decimal(a.value) - difference).to('in')
        self.assertTrue(a > b)

        b = CSS.cm(Decimal(a.value) - difference).to('pt')
        self.assertTrue(a > b)

        b = CSS.cm(Decimal(a.value) - difference).to('pc')
        self.assertTrue(a > b)

        b = CSS.cm(Decimal(a.value) - difference).to('px')
        self.assertTrue(a > b)

        self.assertRaises(ValueError, lambda: a > CSS.deg(1))
        self.assertRaises(ValueError, lambda: a > CSS.grad(1))
        self.assertRaises(ValueError, lambda: a > CSS.rad(1))
        self.assertRaises(ValueError, lambda: a > CSS.turn(1))

        self.assertRaises(ValueError, lambda: a > CSS.s(1))
        self.assertRaises(ValueError, lambda: a > CSS.ms(1))

        self.assertRaises(ValueError, lambda: a > CSS.hz(1))
        self.assertRaises(ValueError, lambda: a > CSS.khz(1))

        self.assertRaises(ValueError, lambda: a > CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a > CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a > CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a > CSS.fr(1))

    def test_css_unit_value_lt_cm(self):
        # CSSUnitValue() < CSSUnitValue()
        a = CSS.cm(1)

        difference = Decimal(1e-10)
        self.assertTrue(CSS.number(1) == CSS.number(1 + difference))

        difference = Decimal(1e-9)
        self.assertFalse(CSS.number(1) == CSS.number(1 + difference))

        self.assertRaises(ValueError, lambda: a < 1)
        self.assertRaises(ValueError, lambda: a < CSS.number(1))
        self.assertRaises(ValueError, lambda: a < CSS.percent(1))

        self.assertRaises(ValueError, lambda: a < CSS.em(1))
        self.assertRaises(ValueError, lambda: a < CSS.ex(1))
        self.assertRaises(ValueError, lambda: a < CSS.ch(1))
        self.assertRaises(ValueError, lambda: a < CSS.ic(1))
        self.assertRaises(ValueError, lambda: a < CSS.rem(1))
        self.assertRaises(ValueError, lambda: a < CSS.lh(1))
        self.assertRaises(ValueError, lambda: a < CSS.rlh(1))
        self.assertRaises(ValueError, lambda: a < CSS.vw(1))
        self.assertRaises(ValueError, lambda: a < CSS.vh(1))
        self.assertRaises(ValueError, lambda: a < CSS.vi(1))
        self.assertRaises(ValueError, lambda: a < CSS.vb(1))
        self.assertRaises(ValueError, lambda: a < CSS.vmin(1))
        self.assertRaises(ValueError, lambda: a < CSS.vmax(1))

        b = CSS.cm(Decimal(a.value) + difference)
        self.assertTrue(a < b)

        b = CSS.cm(Decimal(a.value) + difference).to('mm')
        self.assertTrue(a < b)

        b = CSS.cm(Decimal(a.value) + difference).to('Q')
        self.assertTrue(a < b)

        b = CSS.cm(Decimal(a.value) + difference).to('in')
        self.assertTrue(a < b)

        b = CSS.cm(Decimal(a.value) + difference).to('pt')
        self.assertTrue(a < b)

        b = CSS.cm(Decimal(a.value) + difference).to('pc')
        self.assertTrue(a < b)

        b = CSS.cm(Decimal(a.value) + difference).to('px')
        self.assertTrue(a < b)

        self.assertRaises(ValueError, lambda: a < CSS.deg(1))
        self.assertRaises(ValueError, lambda: a < CSS.grad(1))
        self.assertRaises(ValueError, lambda: a < CSS.rad(1))
        self.assertRaises(ValueError, lambda: a < CSS.turn(1))

        self.assertRaises(ValueError, lambda: a < CSS.s(1))
        self.assertRaises(ValueError, lambda: a < CSS.ms(1))

        self.assertRaises(ValueError, lambda: a < CSS.hz(1))
        self.assertRaises(ValueError, lambda: a < CSS.khz(1))

        self.assertRaises(ValueError, lambda: a < CSS.dpi(1))
        self.assertRaises(ValueError, lambda: a < CSS.dpcm(1))
        self.assertRaises(ValueError, lambda: a < CSS.dppx(1))

        self.assertRaises(ValueError, lambda: a < CSS.fr(1))

    def test_css_unit_value_to_cm(self):
        # CSSUnitValue.to(): 'cm' => any
        unit = 'cm'
        n = 1.0
        a = CSS.cm(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_deg(self):
        # CSSUnitValue.to(): 'deg' => any
        unit = 'deg'
        n = 90.0
        a = CSS.deg(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        b = a.to('deg')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('deg', b.unit)
        self.assertAlmostEqual(90.0, b.value, places=places)

        b = a.to('grad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('grad', b.unit)
        self.assertAlmostEqual(100.0, b.value, places=places)

        b = a.to('rad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('rad', b.unit)
        self.assertAlmostEqual(1.5707963267948966, b.value, places=places)

        b = a.to('turn')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('turn', b.unit)
        self.assertAlmostEqual(0.25, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_dpcm(self):
        # CSSUnitValue.to(): 'dpcm' => any
        unit = 'dpcm'
        n = 96.0 / 2.54
        a = CSS.dpcm(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        b = a.to('dpi')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dpi', b.unit)
        self.assertAlmostEqual(96.0, b.value, places=places)

        b = a.to('dpcm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dpcm', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        b = a.to('dppx')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dppx', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_dpi(self):
        # CSSUnitValue.to(): 'dpi' => any
        unit = 'dpi'
        n = 96.0
        a = CSS.dpi(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        b = a.to('dpi')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dpi', b.unit)
        self.assertAlmostEqual(96.0, b.value, places=places)

        b = a.to('dpcm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dpcm', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        b = a.to('dppx')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dppx', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_dppx(self):
        # CSSUnitValue.to(): 'dppx' => any
        unit = 'dppx'
        n = 1.0
        a = CSS.dppx(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        b = a.to('dpi')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dpi', b.unit)
        self.assertAlmostEqual(96.0, b.value, places=places)

        b = a.to('dpcm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dpcm', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        b = a.to('dppx')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('dppx', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_em(self):
        # CSSUnitValue.to(): 'em' => any
        unit = 'em'
        n = 1.0
        a = CSS.em(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        b = a.to('em')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('em', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_fr(self):
        # CSSUnitValue.to(): 'fr' => any
        unit = 'fr'
        n = 1.0
        a = CSS.fr(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        b = a.to('fr')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('fr', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

    def test_css_unit_value_to_grad(self):
        # CSSUnitValue.to(): 'grad' => any
        unit = 'grad'
        n = 100.0
        a = CSS.grad(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        b = a.to('deg')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('deg', b.unit)
        self.assertAlmostEqual(90.0, b.value, places=places)

        b = a.to('grad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('grad', b.unit)
        self.assertAlmostEqual(100.0, b.value, places=places)

        b = a.to('rad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('rad', b.unit)
        self.assertAlmostEqual(1.5707963267948966, b.value, places=places)

        b = a.to('turn')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('turn', b.unit)
        self.assertAlmostEqual(0.25, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_in(self):
        # CSSUnitValue.to(): 'in' => any
        unit = 'in'
        n = 1 / 2.54
        a = CSS.in_(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_mm(self):
        # CSSUnitValue.to(): 'mm' => any
        unit = 'mm'
        n = 10.0
        a = CSS.mm(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_ms(self):
        # CSSUnitValue.to(): 'ms' => any
        unit = 'ms'
        n = 1000.0
        a = CSS.ms(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        b = a.to('s')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('s', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('ms')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('ms', b.unit)
        self.assertAlmostEqual(1000.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_number(self):
        # CSSUnitValue.to(): 'number' => any
        unit = 'number'
        n = 1.0
        a = CSS.number(n)

        b = a.to('number')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('number', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_pc(self):
        # CSSUnitValue.to(): 'pc' => any
        unit = 'pc'
        n = 6 / 2.54
        a = CSS.pc(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_percent(self):
        # CSSUnitValue.to(): 'percent' => any
        unit = 'percent'
        n = 100.0
        a = CSS.percent(n)

        self.assertRaises(ValueError, lambda: a.to('number'))

        b = a.to('percent')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('percent', b.unit)
        self.assertAlmostEqual(100.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_pt(self):
        # CSSUnitValue.to(): 'pt' => any
        unit = 'pt'
        n = 72 / 2.54
        a = CSS.pt(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_px(self):
        # CSSUnitValue.to(): 'px' => any
        unit = 'px'
        n = 96 / 2.54
        a = CSS.px(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_q(self):
        # CSSUnitValue.to(): 'Q' => any
        unit = 'q'
        n = 40.0
        a = CSS.q(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))

        b = a.to('cm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('cm', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('mm')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('mm', b.unit)
        self.assertAlmostEqual(10.0, b.value, places=places)

        b = a.to('Q')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('q', b.unit)
        self.assertAlmostEqual(40.0, b.value, places=places)

        b = a.to('in')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('in', b.unit)
        self.assertAlmostEqual(0.39370078740157477, b.value, places=places)

        b = a.to('pt')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pt', b.unit)
        self.assertAlmostEqual(28.346456692913385, b.value, places=places)

        b = a.to('pc')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('pc', b.unit)
        self.assertAlmostEqual(2.3622047244094486, b.value, places=places)

        b = a.to('px')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('px', b.unit)
        self.assertAlmostEqual(37.79527559055118, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_rad(self):
        # CSSUnitValue.to(): 'rad' => any
        unit = 'rad'
        n = math.radians(90.0)
        a = CSS.rad(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        b = a.to('deg')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('deg', b.unit)
        self.assertAlmostEqual(90.0, b.value, places=places)

        b = a.to('grad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('grad', b.unit)
        self.assertAlmostEqual(100.0, b.value, places=places)

        b = a.to('rad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('rad', b.unit)
        self.assertAlmostEqual(1.5707963267948966, b.value, places=places)

        b = a.to('turn')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('turn', b.unit)
        self.assertAlmostEqual(0.25, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_s(self):
        # CSSUnitValue.to(): 's' => any
        unit = 's'
        n = 1.0
        a = CSS.s(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        self.assertRaises(ValueError, lambda: a.to('deg'))
        self.assertRaises(ValueError, lambda: a.to('grad'))
        self.assertRaises(ValueError, lambda: a.to('rad'))
        self.assertRaises(ValueError, lambda: a.to('turn'))

        b = a.to('s')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('s', b.unit)
        self.assertAlmostEqual(1.0, b.value, places=places)

        b = a.to('ms')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('ms', b.unit)
        self.assertAlmostEqual(1000.0, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_css_unit_value_to_turn(self):
        # CSSUnitValue.to(): 'turn' => any
        unit = 'turn'
        n = 0.25
        a = CSS.turn(n)

        self.assertRaises(ValueError, lambda: a.to('number'))
        self.assertRaises(ValueError, lambda: a.to('percent'))

        self.assertRaises(ValueError, lambda: a.to('em'))
        self.assertRaises(ValueError, lambda: a.to('ex'))
        self.assertRaises(ValueError, lambda: a.to('ch'))
        self.assertRaises(ValueError, lambda: a.to('ic'))
        self.assertRaises(ValueError, lambda: a.to('rem'))
        self.assertRaises(ValueError, lambda: a.to('lh'))
        self.assertRaises(ValueError, lambda: a.to('rlh'))
        self.assertRaises(ValueError, lambda: a.to('vw'))
        self.assertRaises(ValueError, lambda: a.to('vh'))
        self.assertRaises(ValueError, lambda: a.to('vi'))
        self.assertRaises(ValueError, lambda: a.to('vb'))
        self.assertRaises(ValueError, lambda: a.to('vmin'))
        self.assertRaises(ValueError, lambda: a.to('vmax'))
        self.assertRaises(ValueError, lambda: a.to('cm'))
        self.assertRaises(ValueError, lambda: a.to('mm'))
        self.assertRaises(ValueError, lambda: a.to('Q'))
        self.assertRaises(ValueError, lambda: a.to('in'))
        self.assertRaises(ValueError, lambda: a.to('pt'))
        self.assertRaises(ValueError, lambda: a.to('pc'))
        self.assertRaises(ValueError, lambda: a.to('px'))

        b = a.to('deg')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('deg', b.unit)
        self.assertAlmostEqual(90.0, b.value, places=places)

        b = a.to('grad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('grad', b.unit)
        self.assertAlmostEqual(100.0, b.value, places=places)

        b = a.to('rad')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('rad', b.unit)
        self.assertAlmostEqual(1.5707963267948966, b.value, places=places)

        b = a.to('turn')
        self.assertEqual(unit, a.unit)
        self.assertAlmostEqual(n, a.value, places=places)
        self.assertEqual('turn', b.unit)
        self.assertAlmostEqual(0.25, b.value, places=places)

        self.assertRaises(ValueError, lambda: a.to('s'))
        self.assertRaises(ValueError, lambda: a.to('ms'))

        self.assertRaises(ValueError, lambda: a.to('Hz'))
        self.assertRaises(ValueError, lambda: a.to('kHz'))

        self.assertRaises(ValueError, lambda: a.to('dpi'))
        self.assertRaises(ValueError, lambda: a.to('dpcm'))
        self.assertRaises(ValueError, lambda: a.to('dppx'))

        self.assertRaises(ValueError, lambda: a.to('fr'))

    def test_property_descriptor_support(self):
        # syntax = '*'
        desc = PropertyDescriptor(
            name='--foo',
            inherits=False,
            syntax='*',
        )

        # <length>
        text = '0px'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.LENGTH, syntax)

        # <number>
        text = '0.0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.NUMBER, syntax)

        # <percentage>
        text = '0%'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.PERCENTAGE, syntax)

        # <length-percentage>
        text = 'calc(1px + 1in)'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.LENGTH_PERCENTAGE, syntax)

        # <color>
        text = 'currentColor'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.CUSTOM_IDENT, syntax)

        text = 'black'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#f00'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#00ff00'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = 'rgb(0 255 0)'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        # <image>
        text = 'image("http://www.example.com/pinkish.gif")'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.IMAGE, syntax)

        # <url>
        text = 'url("http://www.example.com/pinkish.gif")'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.URL, syntax)

        # <integer>
        text = '0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.INTEGER, syntax)

        # <angle>
        text = '0deg'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.ANGLE, syntax)

        # <time>
        text = '0s'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.TIME, syntax)

        # <resolution>
        text = '0dpi'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.RESOLUTION, syntax)

        # <custom-ident>
        text = 'none'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.CUSTOM_IDENT, syntax)

        # CSS-wide keyword
        text = 'inherit'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

    def test_property_descriptor_support_color(self):
        # <color>
        desc = PropertyDescriptor(
            name='--foo',
            inherits=False,
            syntax='<color>',
        )

        text = 'currentColor'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.CUSTOM_IDENT, syntax)

        text = 'transparent'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = 'black'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#123'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#1234'  # 4 digits
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#12345'  # 5 digits
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

        text = '#123456'  # 6 digits
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#1234567'  # 7 digits
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

        text = '#12345678'  # 8 digits
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = '#123456789'  # 9 digits
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

        text = 'rgb(0 255 0)'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.COLOR, syntax)

        text = 'none'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

    def test_property_descriptor_support_custom_ident01(self):
        # syntax = <custom-ident>
        desc = PropertyDescriptor(
            name='border-width',
            inherits=True,
            syntax='[ <length> | thick | medium | thin ]{1,4}',
        )

        text = 'initial'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'inherit'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'unset'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'default'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'thick'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.CUSTOM_IDENT, syntax)

        text = 'none'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

    def test_property_descriptor_support_custom_ident02(self):
        # syntax = <custom-ident>
        desc = PropertyDescriptor(
            name='font-family',
            inherits=True,
            syntax="[ <string> | serif | sans-serif | cursive | fantasy"
                   " | monospace ]#",
        )

        text = 'initial'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'inherit'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'unset'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertIsNone(syntax)

        text = 'sans-serif'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.CUSTOM_IDENT, syntax)

        text = '"Helvetica"'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.CUSTOM_IDENT, syntax)

    def test_property_descriptor_support_integer(self):
        # syntax = <integer>
        desc = PropertyDescriptor(
            name='--foo',
            inherits=True,
            syntax='none | <integer>+',
        )

        text = '0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.INTEGER, syntax)

        text = '0.0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

    def test_property_descriptor_support_length_percentage(self):
        # syntax = <length-percentage>
        desc = PropertyDescriptor(
            name='line-height',
            inherits=True,
            syntax='normal | <number> || <length-percentage>',
        )

        text = '0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.NUMBER, syntax)

        text = '0%'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.LENGTH_PERCENTAGE, syntax)

        text = '0em'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.LENGTH_PERCENTAGE, syntax)

        text = 'calc(1em * 1.1)'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.LENGTH_PERCENTAGE, syntax)

    def test_property_descriptor_support_number(self):
        # syntax = <number>
        desc = PropertyDescriptor(
            name='--foo',
            inherits=True,
            syntax='none | <number>+',
        )

        text = '0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.NUMBER, syntax)

        text = '0.0'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.NUMBER, syntax)

    def test_property_descriptor_support_percentage(self):
        # syntax = <percentage>
        desc = PropertyDescriptor(
            name='--foo',
            inherits=False,
            syntax='none | <percentage>+',
        )

        text = '0%'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.PERCENTAGE, syntax)

        desc = PropertyDescriptor(
            name='--foo',
            inherits=False,
            syntax='none | <number>+',
        )
        result, syntax = desc.support(token)
        self.assertFalse(result)
        self.assertIsNone(syntax)

    def test_property_descriptor_support_url(self):
        # syntax = <url>
        desc = PropertyDescriptor(
            name='--foo',
            inherits=True,
            syntax='none | <url>+',
        )

        text = 'url("http://www.example.com/pinkish.gif")'
        token = tinycss2.parse_one_component_value(text)
        result, syntax = desc.support(token)
        self.assertTrue(result)
        self.assertEqual(PropertySyntax.URL, syntax)

    def test_style_property_map_set(self):
        decl = CSSStyleDeclaration()
        style_map = StylePropertyMap(decl)

        value = CSSKeywordValue('auto')
        style_map.set('width', value)
        result = decl.get_property_value('width')
        self.assertEqual('auto', result)

        value = CSS.px(100)
        style_map.set('height', value)
        result = decl.get_property_value('height')
        expected = '100px'
        self.assertEqual(expected, result)

        url1 = CSSURLImageValue('tl.png')
        url2 = CSSURLImageValue('tr.png')
        style_map.set('background-image', url1, url2)
        result = decl.get_property_value('background-image')
        expected = 'url("tl.png"), url("tr.png")'
        self.assertEqual(expected, result)

    def test_style_property_map_read_only_get(self):
        decl = CSSStyleDeclaration()
        decl.set_property('width', 'auto')
        decl.set_property('height', '100px')
        decl.set_property('background-image', 'url(tl.png), url(tr.png)')

        style_map = StylePropertyMapReadOnly(decl)
        self.assertEqual(3, len(style_map))
        self.assertEqual(3, style_map.size)

        # 'width'
        value = style_map.get('width')
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('auto', value.tostring())
        self.assertEqual('auto', value.value)

        values = style_map.get_all('width')
        self.assertEqual(1, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSKeywordValue)
        self.assertEqual('auto', value.tostring())
        self.assertEqual('auto', value.value)

        # 'height'
        value = style_map.get('height')
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual('100px', value.tostring())
        self.assertEqual(100, value.value)
        self.assertEqual('px', value.unit)

        values = style_map.get_all('height')
        self.assertEqual(1, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSUnitValue)
        self.assertEqual('100px', value.tostring())
        self.assertEqual(100, value.value)
        self.assertEqual('px', value.unit)

        # 'background-image'
        value = style_map.get('background-image')
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual('url("tl.png")', value.tostring())
        self.assertEqual('tl.png', value.value)

        values = style_map.get_all('background-image')
        self.assertEqual(2, len(values))

        value = values[0]
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual('url("tl.png")', value.tostring())
        self.assertEqual('tl.png', value.value)

        value = values[1]
        self.assertIsInstance(value, CSSURLImageValue)
        self.assertEqual('url("tr.png")', value.tostring())
        self.assertEqual('tr.png', value.value)


if __name__ == '__main__':
    unittest.main()
