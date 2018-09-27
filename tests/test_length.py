#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import Font, SVGLength, SVGParser, formatter

places = 0
delta = 1


# Test with: Chrome 64.0 (Linux 64-bit)
class LengthTestCase(unittest.TestCase):
    def setUp(self):
        formatter.precision = 3
        SVGLength.rel_tol = 1e-9
        SVGLength.abs_tol = 1e-9
        Font.default_font_size = 16

    def test_abs(self):
        a = SVGLength('0.1')
        b = abs(a)
        self.assertEqual(0.1, a.value())
        self.assertEqual(0.1, b.value())

        a = SVGLength('-0.1')
        b = abs(a)
        self.assertEqual(-0.1, a.value())
        self.assertEqual(0.1, b.value())

        a = SVGLength('-0.1px')
        b = abs(a)
        self.assertEqual(-0.1, a.value())
        self.assertEqual(0.1, b.value())

    def test_add_cm_in(self):
        # 10.2(cm) + 1.8(in)
        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811023622(px)
        a = a + SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8(px)
        # 10.2(cm) + 2.54(cm) = 14.771999999999998(cm)
        # 385.511811(px) + 172.8(px) = 558.311811(px)
        self.assertEqual('14.772cm', a.tostring())
        self.assertEqual('558.312px', a.tostring(SVGLength.TYPE_PX))
        self.assertEqual('cm', a.unit)
        self.assertEqual(SVGLength('558.311811px'), a)

    def test_add_mm_mm(self):
        # 0.1(mm) + 0.1(mm) + 0.1(mm)
        a = SVGLength('0.1mm')
        a = a + SVGLength('0.1mm')
        a = a + SVGLength('0.1mm')
        self.assertEqual('0.3mm', a.tostring())
        self.assertEqual('mm', a.unit)
        self.assertEqual(0.3, a.value(SVGLength.TYPE_MM))

    def test_convert01(self):
        # with context
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': '16',
        })
        # 1(rem) = 16(px)
        text = group.create_sub_element('text')

        a = SVGLength('1in', context=text)
        self.assertEqual('in', a.unit)
        self.assertEqual('1in', a.tostring())

        a.convert(SVGLength.TYPE_CM)  # 1(in) = 2.54(cm)
        self.assertEqual('cm', a.unit)
        self.assertEqual('2.54cm', a.tostring())

        a.convert(SVGLength.TYPE_PX)  # 2.54(cm) = 96(px)
        self.assertEqual('px', a.unit)
        self.assertEqual('96px', a.tostring())

        a.convert(SVGLength.TYPE_NUMBER)  # 96(px) = 96
        self.assertIsNone(a.unit)
        self.assertEqual('96', a.tostring())

        a.convert(SVGLength.TYPE_MM)  # 96(px) = 25.4(mm)
        self.assertEqual('mm', a.unit)
        self.assertEqual('25.4mm', a.tostring())

        # 100(%) = 16(px)
        a.convert(SVGLength.TYPE_PERCENTAGE)  # 96(px) = 600(%)
        self.assertEqual('%', a.unit)
        self.assertEqual('600%', a.tostring())

        # 100(%) = 1(em)
        a.convert(SVGLength.TYPE_EMS)  # 600(%) = 6(em)
        self.assertEqual('em', a.unit)
        self.assertEqual('6em', a.tostring())

        # 1(ex) = x-height(px)
        # 96(px) -> x-height: 53(px)
        # 96(px) / 53(px) = 1.8113...
        a.convert(SVGLength.TYPE_EXS)
        self.assertEqual('ex', a.unit)
        self.assertEqual('1.811ex', a.tostring())

        # font-family: "DejaVu Sans", sans-serif
        # element font size: 16(px) -> 1(ex) = 9(px)
        # 1.8113(ex) = 1.8113 * 9 = 16.3017...(px)
        # 1(px) = 0.75(pt)
        # 16.3017 * 0.75 = 12.2263...(pt)
        a.convert(SVGLength.TYPE_PT)
        self.assertEqual('pt', a.unit)
        self.assertEqual('12.226pt', a.tostring())

        # 1(pt) = 1 / 12(pc)
        # 12.2263(pt) = 1.0189...(pc)
        a.convert(SVGLength.TYPE_PC)
        self.assertEqual('pc', a.unit)
        self.assertEqual('1.019pc', a.tostring())

    def test_convert02(self):
        # with context
        parser = SVGParser()
        root = parser.create_element('svg')
        root.attributes.update({
            'font-size': '16'
        })
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': '62.5%',
        })
        # 1(rem) = 62.5(%) = 16(px) * 62.5(%) = 10(px)
        text = group.create_sub_element('text')

        a = SVGLength('1in', context=text)
        self.assertEqual('in', a.unit)
        self.assertEqual('1in', a.tostring())

        a.convert(SVGLength.TYPE_CM)  # 1(in) = 2.54(cm)
        self.assertEqual('cm', a.unit)
        self.assertEqual('2.54cm', a.tostring())

        a.convert(SVGLength.TYPE_PX)  # 2.54(cm) = 96(px)
        self.assertEqual('px', a.unit)
        self.assertEqual('96px', a.tostring())

        a.convert(SVGLength.TYPE_NUMBER)  # 96(px) = 96
        self.assertIsNone(a.unit)
        self.assertEqual('96', a.tostring())

        a.convert(SVGLength.TYPE_MM)  # 96(px) = 25.4(mm)
        self.assertEqual('mm', a.unit)
        self.assertEqual('25.4mm', a.tostring())

        # 100(%) = 10(px)
        a.convert(SVGLength.TYPE_PERCENTAGE)  # 96(px) = 960(%)
        self.assertEqual('%', a.unit)
        self.assertEqual('960%', a.tostring())

        # 100(%) = 1(em)
        a.convert(SVGLength.TYPE_EMS)  # 960(%) = 9.6(em)
        self.assertEqual('em', a.unit)
        self.assertEqual('9.6em', a.tostring())

        # 1(ex) = x-height(px)
        # 96(px) -> x-height: 53(px)
        # 96(px) / 53(px) = 1.8113...
        a.convert(SVGLength.TYPE_EXS)
        self.assertEqual('ex', a.unit)
        self.assertEqual('1.811ex', a.tostring())

        # font-family: "DejaVu Sans", sans-serif
        # element font size: 10(px) -> 1(ex) = 5(px)
        # 1.8113(ex) = 1.8113 * 5 = 9.0565(px)
        # 1(px) = 0.75(pt)
        # 9.0565 * 0.75 = 6.7924...(pt)
        a.convert(SVGLength.TYPE_PT)
        self.assertEqual('pt', a.unit)
        self.assertEqual('6.792pt', a.tostring())

        # 1(pt) = 1 / 12(pc)
        # 6.7924(pt) = 0.5660...(pc)
        a.convert(SVGLength.TYPE_PC)
        self.assertEqual('pc', a.unit)
        self.assertEqual('0.566pc', a.tostring())

    def test_convert03(self):
        # without context
        Font.default_font_size = 20

        a = SVGLength('1em')
        self.assertEqual('em', a.unit)
        self.assertEqual('1em', a.tostring())

        # 1(em) = 2(ex)
        a.convert(SVGLength.TYPE_EXS)
        self.assertEqual('ex', a.unit)
        self.assertEqual('2ex', a.tostring())

        # 1(em) = default font size(px)
        a.convert(SVGLength.TYPE_PX)
        self.assertEqual('px', a.unit)
        self.assertEqual('20px', a.tostring())

        # 1(rem) = default font size(px)
        a.convert(SVGLength.TYPE_REMS)
        self.assertEqual('rem', a.unit)
        self.assertEqual('1rem', a.tostring())

        # 1(ch) = default font size / 2(px)
        a.convert(SVGLength.TYPE_CHS)
        self.assertEqual('ch', a.unit)
        self.assertEqual('2ch', a.tostring())

        # 100(%) = default font size(px)
        a.convert(SVGLength.TYPE_PERCENTAGE)
        self.assertEqual('%', a.unit)
        self.assertEqual('100%', a.tostring())

        # 1(ex) = 0.5(em)
        a = SVGLength('1ex')
        a.convert(SVGLength.TYPE_EMS)
        self.assertEqual('em', a.unit)
        self.assertEqual('0.5em', a.tostring())

    def test_eq_cm_mm(self):
        # 1(cm) == 10(mm)
        a = SVGLength('1cm')  # 37.79527559055118
        b = SVGLength('10mm')  # 37.795275590551185
        self.assertNotEqual(a.value(), b.value())
        self.assertAlmostEqual(a.value(), b.value())
        self.assertAlmostEqual(a.value(a.unit), b.value(a.unit))
        self.assertEqual(a.tostring(), b.tostring(a.unit))
        self.assertTrue(a == b)

    def test_eq_none_none(self):
        # 1 == 1.000000001?
        SVGLength.rel_tol = 1e-9
        a = SVGLength('1')
        b = SVGLength('1.000000001')
        self.assertNotEqual(a.value(), b.value())
        self.assertAlmostEqual(a.value(a.unit), b.value(a.unit))
        self.assertEqual(a.tostring(), b.tostring(a.unit))  # '1' == '1'
        self.assertFalse(a == b)  # 1 != 1.000000001

        SVGLength.rel_tol = 1e-8
        self.assertTrue(a == b)  # 1 == 1.00000000

        SVGLength.rel_tol = 1e-9
        SVGLength.abs_tol = 1e-9
        a = SVGLength('0')
        b = SVGLength('-0.000000001')
        self.assertNotEqual(a.value(), b.value())
        self.assertAlmostEqual(a.value(a.unit), b.value(a.unit))
        self.assertEqual(a.tostring(), b.tostring(a.unit))  # '1' == '1'
        self.assertTrue(a == b)

        SVGLength.abs_tol = 1e-10
        self.assertFalse(a == b)

    def test_font_relative_lengths_em01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1em', context=text)
        expected = element_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_ex01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ex', context=text)
        expected = 11
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_cap01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1cap', context=text)
        expected = element_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_ch01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ch', context=text)
        expected = 12.724
        self.assertAlmostEqual(expected, a.value(), msg=a, places=places)

    def test_font_relative_lengths_ic01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ic', context=text)
        expected = element_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_rem01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1rem', context=text)
        expected = base_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_em02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1em', context=text)
        expected = element_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_ex02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ex', context=text)
        expected = 10
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_cap02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1cap', context=text)
        expected = element_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_ch02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ch', context=text)
        expected = 12.3633
        self.assertAlmostEqual(expected, a.value(), msg=a, places=places)

    def test_font_relative_lengths_ic02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ic', context=text)
        expected = element_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_relative_lengths_rem02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1rem', context=text)
        expected = base_font_size
        self.assertAlmostEqual(expected, a.value(), msg=a)

    def test_font_size_vw(self):
        # 'vw unit'
        parser = SVGParser()
        root = parser.create_element('svg')
        root.attributes.update({
            'width': '200mm',
        })
        group = root.create_sub_element('g')
        text = group.create_sub_element('text')
        text.attributes.update({
            'font-size': '8vw',
        })

        a = SVGLength(text.attributes['font-size'].value, context=None)
        expected = 8
        self.assertEqual(expected, a.value(), msg=a)

        a = SVGLength(text.attributes['font-size'].value, context=text)
        expected = 8 * 200 / 100  # 16mm
        self.assertAlmostEqual(expected, a.value(SVGLength.TYPE_MM), msg=a)

    def test_eq_none_none_2(self):
        a = SVGLength('1')
        b = SVGLength('1.0000000001')  # -> 1
        self.assertNotEqual(a.value(), b.value())
        self.assertAlmostEqual(a.value(a.unit), b.value(a.unit))
        self.assertEqual(a.tostring(), b.tostring(a.unit))  # '1' == '1'
        self.assertTrue(a == b)  # 1 == 1

    def test_ge_in_in_4f(self):
        a = SVGLength('1.0001in')  # 1.0001in = 96.0096
        b = SVGLength('1in')  # 1in = 96
        self.assertTrue(a >= b, msg=(a.value(), b.value()))
        self.assertTrue(a > b, msg=(a.value(), b.value()))
        self.assertFalse(a == b, msg=(a.value(), b.value()))

    def test_ge_in_in_5f(self):
        a = SVGLength('1.00001in')  # 1.00001in = 96.00096
        b = SVGLength('1in')  # 1in = 96
        self.assertTrue(a >= b, msg=(a.value(), b.value()))
        self.assertTrue(a > b, msg=(a.value(), b.value()))
        self.assertFalse(a == b, msg=(a.value(), b.value()))

    def test_ge(self):
        a = SVGLength(0.000001)
        b = SVGLength(0.000001)
        self.assertTrue(a >= b, msg=(a.value(), b.value()))
        self.assertFalse(a > b, msg=(a.value(), b.value()))
        self.assertTrue(a == b, msg=(a.value(), b.value()))

    def test_ge_false(self):
        a = SVGLength(0.0000009)
        b = SVGLength(0.000001)
        self.assertFalse(a >= b, msg=(a.value(), b.value()))
        self.assertFalse(a > b, msg=(a.value(), b.value()))
        self.assertFalse(a == b, msg=(a.value(), b.value()))

    def test_iadd(self):
        a = SVGLength('0.1mm')
        a += SVGLength('0.1mm')
        a += SVGLength('0.1mm')  # 0.30000000000000004mm
        self.assertEqual('0.3mm', a.tostring())
        self.assertTrue(a == SVGLength('0.3mm'), msg=a.value(a.unit))

        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811...px
        a += SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8px
        self.assertEqual('14.772cm', a.tostring())  # 10.2 + 4.572 (cm)
        self.assertTrue(SVGLength('558.311811px') == a)  # 385.511811 + 172.8

    def test_imul(self):
        a = SVGLength('1cm')
        a *= 2
        self.assertEqual('2cm', a.tostring())

        a *= SVGLength('11mm')
        self.assertEqual('2.2cm', a.tostring())

    def test_init(self):
        a = SVGLength()
        self.assertEqual(0, a.value())
        self.assertIsNone(a.unit)
        self.assertEqual('0', a.tostring())

    def test_isub(self):
        a = SVGLength('0.1mm')
        a -= SVGLength('0.1mm')
        a -= SVGLength('0.1mm')  # -0.1mm
        self.assertEqual('-0.1mm', a.tostring())
        self.assertTrue(SVGLength('-0.1mm') == a, msg=a.value(a.unit))

        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811...px
        a -= SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8px
        self.assertEqual('5.628cm', a.tostring())  # 10.2 - 4.572 (cm)
        self.assertTrue(SVGLength('212.711811px') == a)  # 385.511811 - 172.8

    def test_itruediv(self):
        a = SVGLength('12mm')
        a /= 10
        self.assertEqual(SVGLength('1.2mm'), a)

        a /= SVGLength('0.12cm')
        self.assertEqual(SVGLength('1mm'), a)

    def test_le(self):
        a = SVGLength('1in')  # 1in = 96
        b = SVGLength('1.0001in')  # 1.0001in = 96.0096
        self.assertTrue(a <= b, msg=(a.value(), b.value()))
        self.assertTrue(a < b, msg=(a.value(), b.value()))
        self.assertFalse(a == b, msg=(a.value(), b.value()))

        a = SVGLength('1in')  # 1in = 96
        b = SVGLength('2.54cm')  # 1in = 2.54cm
        self.assertTrue(a <= b, msg=(a.value(), b.value()))
        self.assertFalse(a < b, msg=(a.value(), b.value()))
        self.assertTrue(a == b, msg=(a.value(), b.value()))

    def test_lt(self):
        a = SVGLength('62.5%')
        b = SVGLength('62.49%')
        self.assertTrue(b < a, msg=(a, b))
        self.assertFalse(b == a, msg=(a, b))

    def test_mul(self):
        a = SVGLength('10cm')
        b = SVGLength('2.5cm')
        c = a * b
        self.assertEqual(SVGLength('25cm'), c)

        c = a * 2.05
        self.assertEqual(SVGLength('20.5cm'), c)

    def test_ne(self):
        a = SVGLength('1cm')  # 37.79527559055118
        b = SVGLength('10mm')  # 37.795275590551185
        self.assertNotEqual(a.value(), b.value())
        self.assertEqual(a.tostring(), b.tostring(a.unit))
        self.assertFalse(a != b)

        a = SVGLength('1')
        b = SVGLength('1.000000001')
        self.assertNotEqual(a.value(), b.value())
        self.assertEqual(a.tostring(), b.tostring(a.unit))  # '1' == '1'
        self.assertTrue(a != b)

        a = SVGLength('1')
        b = SVGLength('1.0000000001')  # -> 1
        self.assertNotEqual(a.value(), b.value())
        self.assertEqual(a.tostring(), b.tostring(a.unit))  # '1' == '1'
        self.assertFalse(a != b)

    def test_neg(self):
        a = SVGLength('10cm')
        b = -a
        self.assertEqual(SVGLength('-10cm'), b)
        self.assertTrue(b.value() < 0)

    def test_negative_zero(self):
        a = SVGLength(-0.0)  # -0.0 -> 0
        self.assertEqual('-0.0', str(a.value()))
        self.assertEqual('0', a.tostring())

        a = SVGLength('-0.0001')
        self.assertEqual('-0.0001', str(a.value()))
        self.assertEqual('0', a.tostring())

    def test_new_value_number(self):
        a = SVGLength()
        a.new_value(1.0001, SVGLength.TYPE_NUMBER)
        self.assertEqual(1.0001, a.value())
        self.assertIsNone(a.unit)
        self.assertEqual('1', a.tostring())

    def test_new_value_percentage(self):
        a = SVGLength()
        a.new_value(92.00042345, SVGLength.TYPE_PERCENTAGE)
        self.assertEqual(92.00042345, a.value(SVGLength.TYPE_PERCENTAGE))
        self.assertEqual('%', a.unit)
        self.assertEqual('92%', a.tostring())

    def test_new_value_percentage2(self):
        parser = SVGParser()
        root = parser.create_element('svg')
        group = root.create_sub_element('g')
        group.attributes.update({
            'font-size': '16',
        })

        a = SVGLength(context=group)
        a.new_value(92.00042345, SVGLength.TYPE_PERCENTAGE)
        self.assertEqual(92.00042345, a.value(SVGLength.TYPE_PERCENTAGE))
        self.assertEqual('%', a.unit)
        self.assertEqual('92%', a.tostring())

    def test_pow(self):
        a = SVGLength('2.5px')
        b = a ** 2
        self.assertEqual(SVGLength('6.25px'), b)

    def test_precision(self):
        a = SVGLength('1cm')  # 37.79527559055118
        self.assertEqual('37.795', a.tostring(SVGLength.TYPE_NUMBER))

        formatter.precision = 4
        self.assertEqual('37.7953', a.tostring(SVGLength.TYPE_NUMBER))

        formatter.precision = 2
        # '37.80' -> '37.8'
        self.assertEqual('37.8', a.tostring(SVGLength.TYPE_NUMBER))

    def test_rmul(self):
        a = SVGLength('0.1mm')
        b = 10 * a
        self.assertEqual(SVGLength('1mm'), b)

        b = 2.2 * a  # 0.22000000000000003 -> 0.22
        self.assertEqual(SVGLength('0.22mm'), b)

    def test_sub(self):
        a = SVGLength('0.1mm')
        a = a - SVGLength('0.1mm')
        a = a - SVGLength('0.1mm')  # -0.1mm
        self.assertEqual('-0.1mm', a.tostring())
        self.assertTrue(SVGLength('-0.1mm') == a, msg=a.value(a.unit))

        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811...px
        a = a - SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8px
        self.assertEqual('5.628cm', a.tostring())  # 10.2 - 4.572 (cm)
        self.assertTrue(SVGLength('212.711811px') == a)  # 385.511811 - 172.8

    def test_truediv(self):
        a = SVGLength('12mm')
        b = a / 10
        self.assertEqual(SVGLength('1.2mm'), b)

        a = b / SVGLength('0.12cm')
        self.assertEqual(SVGLength('1mm'), a)


if __name__ == '__main__':
    unittest.main()
