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
        SVGLength.dpi = 96
        Font.default_font_size = 16

    def test_abs(self):
        a = SVGLength('0.1')
        b = abs(a)
        self.assertEqual(a.value(), 0.1)
        self.assertEqual(b.value(), 0.1)

        a = SVGLength('-0.1')
        b = abs(a)
        self.assertEqual(a.value(), -0.1)
        self.assertEqual(b.value(), 0.1)

        a = SVGLength('-0.1px')
        b = abs(a)
        self.assertEqual(a.value(), -0.1)
        self.assertEqual(b.value(), 0.1)

    def test_add_cm_in(self):
        # 10.2(cm) + 1.8(in)
        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811023622(px)
        a = a + SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8(px)
        # 10.2(cm) + 2.54(cm) = 14.771999999999998(cm)
        # 385.511811(px) + 172.8(px) = 558.311811(px)
        self.assertEqual(a.tostring(), '14.772cm')
        self.assertEqual(a.tostring(SVGLength.TYPE_PX), '558.312px')
        self.assertEqual(a.unit, 'cm')
        self.assertEqual(a, SVGLength('558.311811px'))

    def test_add_mm_mm(self):
        # 0.1(mm) + 0.1(mm) + 0.1(mm)
        a = SVGLength('0.1mm')
        a = a + SVGLength('0.1mm')
        a = a + SVGLength('0.1mm')
        self.assertEqual(a.tostring(), '0.3mm')
        self.assertEqual(a.unit, 'mm')
        self.assertEqual(a.value(SVGLength.TYPE_MM), 0.3)

    def test_convert01(self):
        # with context
        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': '16',
        })
        # 1(rem) = 16(px)
        text = group.make_sub_element('text')

        a = SVGLength('1in', context=text)
        self.assertEqual(a.unit, 'in')
        self.assertEqual(a.tostring(), '1in')

        a.convert(SVGLength.TYPE_CM)  # 1(in) = 2.54(cm)
        self.assertEqual(a.unit, 'cm')
        self.assertEqual(a.tostring(), '2.54cm')

        a.convert(SVGLength.TYPE_PX)  # 2.54(cm) = 96(px)
        self.assertEqual(a.unit, 'px')
        self.assertEqual(a.tostring(), '96px')

        a.convert(SVGLength.TYPE_NUMBER)  # 96(px) = 96
        self.assertEqual(a.unit, None)
        self.assertEqual(a.tostring(), '96')

        a.convert(SVGLength.TYPE_MM)  # 96(px) = 25.4(mm)
        self.assertEqual(a.unit, 'mm')
        self.assertEqual(a.tostring(), '25.4mm')

        # 100(%) = 16(px)
        a.convert(SVGLength.TYPE_PERCENTAGE)  # 96(px) = 600(%)
        self.assertEqual(a.unit, '%')
        self.assertEqual(a.tostring(), '600%')

        # 100(%) = 1(em)
        a.convert(SVGLength.TYPE_EMS)  # 600(%) = 6(em)
        self.assertEqual(a.unit, 'em')
        self.assertEqual(a.tostring(), '6em')

        # 1(ex) = x-height(px)
        # 96(px) -> x-height: 53(px)
        # 96(px) / 53(px) = 1.8113...
        a.convert(SVGLength.TYPE_EXS)
        self.assertEqual(a.unit, 'ex')
        self.assertEqual(a.tostring(), '1.811ex')

        # font-family: "DejaVu Sans", sans-serif
        # element font size: 16(px) -> 1(ex) = 9(px)
        # 1.8113(ex) = 1.8113 * 9 = 16.3017...(px)
        # 1(px) = 0.75(pt)
        # 16.3017 * 0.75 = 12.2263...(pt)
        a.convert(SVGLength.TYPE_PT)
        self.assertEqual(a.unit, 'pt')
        self.assertEqual(a.tostring(), '12.226pt')

        # 1(pt) = 1 / 12(pc)
        # 12.2263(pt) = 1.0189...(pc)
        a.convert(SVGLength.TYPE_PC)
        self.assertEqual(a.unit, 'pc')
        self.assertEqual(a.tostring(), '1.019pc')

    def test_convert02(self):
        # with context
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'font-size': '16'
        })
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': '62.5%',
        })
        # 1(rem) = 62.5(%) = 16(px) * 62.5(%) = 10(px)
        text = group.make_sub_element('text')

        a = SVGLength('1in', context=text)
        self.assertEqual(a.unit, 'in')
        self.assertEqual(a.tostring(), '1in')

        a.convert(SVGLength.TYPE_CM)  # 1(in) = 2.54(cm)
        self.assertEqual(a.unit, 'cm')
        self.assertEqual(a.tostring(), '2.54cm')

        a.convert(SVGLength.TYPE_PX)  # 2.54(cm) = 96(px)
        self.assertEqual(a.unit, 'px')
        self.assertEqual(a.tostring(), '96px')

        a.convert(SVGLength.TYPE_NUMBER)  # 96(px) = 96
        self.assertEqual(a.unit, None)
        self.assertEqual(a.tostring(), '96')

        a.convert(SVGLength.TYPE_MM)  # 96(px) = 25.4(mm)
        self.assertEqual(a.unit, 'mm')
        self.assertEqual(a.tostring(), '25.4mm')

        # 100(%) = 10(px)
        a.convert(SVGLength.TYPE_PERCENTAGE)  # 96(px) = 960(%)
        self.assertEqual(a.unit, '%')
        self.assertEqual(a.tostring(), '960%')

        # 100(%) = 1(em)
        a.convert(SVGLength.TYPE_EMS)  # 960(%) = 9.6(em)
        self.assertEqual(a.unit, 'em')
        self.assertEqual(a.tostring(), '9.6em')

        # 1(ex) = x-height(px)
        # 96(px) -> x-height: 53(px)
        # 96(px) / 53(px) = 1.8113...
        a.convert(SVGLength.TYPE_EXS)
        self.assertEqual(a.unit, 'ex')
        self.assertEqual(a.tostring(), '1.811ex')

        # font-family: "DejaVu Sans", sans-serif
        # element font size: 10(px) -> 1(ex) = 5(px)
        # 1.8113(ex) = 1.8113 * 5 = 9.0565(px)
        # 1(px) = 0.75(pt)
        # 9.0565 * 0.75 = 6.7924...(pt)
        a.convert(SVGLength.TYPE_PT)
        self.assertEqual(a.unit, 'pt')
        self.assertEqual(a.tostring(), '6.792pt')

        # 1(pt) = 1 / 12(pc)
        # 6.7924(pt) = 0.5660...(pc)
        a.convert(SVGLength.TYPE_PC)
        self.assertEqual(a.unit, 'pc')
        self.assertEqual(a.tostring(), '0.566pc')

    def test_convert03(self):
        # without context
        Font.default_font_size = 20

        a = SVGLength('1em')
        self.assertEqual(a.unit, 'em')
        self.assertEqual(a.tostring(), '1em')

        # 1(em) = 2(ex)
        a.convert(SVGLength.TYPE_EXS)
        self.assertEqual(a.unit, 'ex')
        self.assertEqual(a.tostring(), '2ex')

        # 1(em) = default font size(px)
        a.convert(SVGLength.TYPE_PX)
        self.assertEqual(a.unit, 'px')
        self.assertEqual(a.tostring(), '20px')

        # 1(rem) = default font size(px)
        a.convert(SVGLength.TYPE_REMS)
        self.assertEqual(a.unit, 'rem')
        self.assertEqual(a.tostring(), '1rem')

        # 1(ch) = default font size / 2(px)
        a.convert(SVGLength.TYPE_CHS)
        self.assertEqual(a.unit, 'ch')
        self.assertEqual(a.tostring(), '2ch')

        # 100(%) = default font size(px)
        a.convert(SVGLength.TYPE_PERCENTAGE)
        self.assertEqual(a.unit, '%')
        self.assertEqual(a.tostring(), '100%')

        # 1(ex) = 0.5(em)
        a = SVGLength('1ex')
        a.convert(SVGLength.TYPE_EMS)
        self.assertEqual(a.unit, 'em')
        self.assertEqual(a.tostring(), '0.5em')

    def test_dpi(self):
        SVGLength.dpi = 96
        self.assertEqual(SVGLength.dpi, 96)

        # 1(in) = 96(px)
        a = SVGLength('1in')
        self.assertEqual(a.tostring(SVGLength.TYPE_PX), '96px')

        SVGLength.dpi = 300
        self.assertEqual(SVGLength.dpi, 300)

        # 1(in) = 300(px)
        self.assertEqual(a.tostring(SVGLength.TYPE_PX), '300px')

        # 1(in) = 2.54(cm)
        self.assertEqual(a.tostring(SVGLength.TYPE_CM), '2.54cm')

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
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1em', context=text)
        expected = element_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_ex01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ex', context=text)
        expected = 11
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_cap01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1cap', context=text)
        expected = element_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_ch01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ch', context=text)
        expected = 12.724
        self.assertAlmostEqual(a.value(), expected, msg=a, places=places)

    def test_font_relative_lengths_ic01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ic', context=text)
        expected = element_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_rem01(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'DejaVu Sans, sans-serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1rem', context=text)
        expected = base_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_em02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1em', context=text)
        expected = element_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_ex02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ex', context=text)
        expected = 10
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_cap02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1cap', context=text)
        expected = element_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_ch02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ch', context=text)
        expected = 12.3633
        self.assertAlmostEqual(a.value(), expected, msg=a, places=places)

    def test_font_relative_lengths_ic02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1ic', context=text)
        expected = element_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_relative_lengths_rem02(self):
        # See also: length02.html
        base_font_size = 18
        element_font_size = 20
        Font.default_font_size = base_font_size

        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-family': 'IPAmjMincho, serif',
            'font-size': str(element_font_size),
        })
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '1em',
        })

        a = SVGLength('1rem', context=text)
        expected = base_font_size
        self.assertAlmostEqual(a.value(), expected, msg=a)

    def test_font_size_vw(self):
        # 'vw unit'
        parser = SVGParser()
        root = parser.make_element('svg')
        root.attributes.update({
            'width': '200mm',
        })
        group = root.make_sub_element('g')
        text = group.make_sub_element('text')
        text.attributes.update({
            'font-size': '8vw',
        })

        a = SVGLength(text.attributes.get('font-size'), context=None)
        expected = 8
        self.assertEqual(a.value(), expected, msg=a)

        a = SVGLength(text.attributes.get('font-size'), context=text)
        expected = 8 * 200 / 100  # 16mm
        self.assertAlmostEqual(a.value(SVGLength.TYPE_MM), expected, msg=a)

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
        self.assertEqual(a.tostring(), '0.3mm')
        self.assertTrue(a == SVGLength('0.3mm'), msg=a.value(a.unit))

        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811...px
        a += SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8px
        self.assertEqual(a.tostring(), '14.772cm')  # 10.2 + 4.572 (cm)
        self.assertTrue(a == SVGLength('558.311811px'))  # 385.511811 + 172.8

    def test_imul(self):
        a = SVGLength('1cm')
        a *= 2
        self.assertEqual(a.tostring(), '2cm')

        a *= SVGLength('11mm')
        self.assertEqual(a.tostring(), '2.2cm')

    def test_init(self):
        a = SVGLength()
        self.assertEqual(a.value(), 0)
        self.assertEqual(a.unit, None)
        self.assertEqual(a.tostring(), '0')

    def test_isub(self):
        a = SVGLength('0.1mm')
        a -= SVGLength('0.1mm')
        a -= SVGLength('0.1mm')  # -0.1mm
        self.assertEqual(a.tostring(), '-0.1mm')
        self.assertTrue(a == SVGLength('-0.1mm'), msg=a.value(a.unit))

        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811...px
        a -= SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8px
        self.assertEqual(a.tostring(), '5.628cm')  # 10.2 - 4.572 (cm)
        self.assertTrue(a == SVGLength('212.711811px'))  # 385.511811 - 172.8

    def test_itruediv(self):
        a = SVGLength('12mm')
        a /= 10
        self.assertEqual(a, SVGLength('1.2mm'))

        a /= SVGLength('0.12cm')
        self.assertEqual(a, SVGLength('1mm'))

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
        self.assertEqual(c, SVGLength('25cm'))

        c = a * 2.05
        self.assertEqual(c, SVGLength('20.5cm'))

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
        self.assertEqual(b, SVGLength('-10cm'))
        self.assertTrue(b.value() < 0)

    def test_negative_zero(self):
        a = SVGLength(-0.0)  # -0.0 -> 0
        self.assertEqual(str(a.value()), '-0.0')
        self.assertEqual(a.tostring(), '0')

        a = SVGLength('-0.0001')
        self.assertEqual(str(a.value()), '-0.0001')
        self.assertEqual(a.tostring(), '0')

    def test_new_value_number(self):
        a = SVGLength()
        a.new_value(1.0001, SVGLength.TYPE_NUMBER)
        self.assertEqual(a.value(), 1.0001)
        self.assertEqual(a.unit, None)
        self.assertEqual(a.tostring(), '1')

    def test_new_value_percentage(self):
        a = SVGLength()
        a.new_value(92.00042345, SVGLength.TYPE_PERCENTAGE)
        self.assertEqual(a.value(SVGLength.TYPE_PERCENTAGE), 92.00042345)
        self.assertEqual(a.unit, '%')
        self.assertEqual(a.tostring(), '92%')

    def test_new_value_percentage2(self):
        parser = SVGParser()
        root = parser.make_element('svg')
        group = root.make_sub_element('g')
        group.attributes.update({
            'font-size': '16',
        })

        a = SVGLength(context=group)
        a.new_value(92.00042345, SVGLength.TYPE_PERCENTAGE)
        self.assertEqual(a.value(SVGLength.TYPE_PERCENTAGE), 92.00042345)
        self.assertEqual(a.unit, '%')
        self.assertEqual(a.tostring(), '92%')

    def test_pow(self):
        a = SVGLength('2.5px')
        b = a ** 2
        self.assertEqual(b, SVGLength('6.25px'))

    def test_precision(self):
        a = SVGLength('1cm')  # 37.79527559055118
        self.assertEqual(a.tostring(SVGLength.TYPE_NUMBER), '37.795')

        formatter.precision = 4
        self.assertEqual(a.tostring(SVGLength.TYPE_NUMBER), '37.7953')

        formatter.precision = 2
        # '37.80' -> '37.8'
        self.assertEqual(a.tostring(SVGLength.TYPE_NUMBER), '37.8')

    def test_rmul(self):
        a = SVGLength('0.1mm')
        b = 10 * a
        self.assertEqual(b, SVGLength('1mm'))

        b = 2.2 * a  # 0.22000000000000003 -> 0.22
        self.assertEqual(b, SVGLength('0.22mm'))

    def test_sub(self):
        a = SVGLength('0.1mm')
        a = a - SVGLength('0.1mm')
        a = a - SVGLength('0.1mm')  # -0.1mm
        self.assertEqual(a.tostring(), '-0.1mm')
        self.assertTrue(a == SVGLength('-0.1mm'), a.value(a.unit))

        a = SVGLength('10.2cm')  # 10.2 * 96 / 2.54 (px) = 385.511811...px
        a = a - SVGLength('1.8in')  # 1.8in = 1.8 * 2.54cm = 4.572cm = 172.8px
        self.assertEqual(a.tostring(), '5.628cm')  # 10.2 - 4.572 (cm)
        self.assertTrue(a == SVGLength('212.711811px'))  # 385.511811 - 172.8

    def test_truediv(self):
        a = SVGLength('12mm')
        b = a / 10
        self.assertEqual(b, SVGLength('1.2mm'))

        a = b / SVGLength('0.12cm')
        self.assertEqual(a, SVGLength('1mm'))


if __name__ == '__main__':
    unittest.main()
