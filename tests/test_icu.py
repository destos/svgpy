#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import icu
from svgpy.icu import UBiDi, UBreakIterator, ULocale, ffi, \
    u_error_name, u_str_from_utf8, u_str_to_utf8, u_strlen, u_success


class ICUTestCase(unittest.TestCase):
    def test_bidi01(self):
        # http://unicode.org/cldr/utility/bidi.jsp
        para = UBiDi()
        # 'mark 3.1% مارْك 2.0.'
        text = 'mark 3.1% \u0645\u0627\u0631\u0652\u0643 2.0.'
        para.set_para(text, UBiDi.UBIDI_DEFAULT_RTL)
        self.assertTrue(u_success(para.status), msg=para.status)

        direction = para.get_direction()
        self.assertEqual(direction, UBiDi.UBIDI_MIXED)

        count = para.count_runs()
        self.assertEqual(count, 4)

        items = [x for x in para.visual_iter()]
        expected = [
            'mark 3.1% ',
            '2.0',
            ' \u0643\u0652\u0631\u0627\u0645',
            '.'
        ]
        self.assertEqual(items, expected)

    def test_bidi02(self):
        # https://svgwg.org/svg2-draft/images/text/rtl-text.svg
        para = UBiDi()
        # 'داستان SVG 1.1 SE طولا ني است.'
        # text = 'داستان SVG 1.1 SE طولا ني است.'
        text = \
            "\u062f\u0627\u0633\u062a\u0627\u0646" \
            " SVG 1.1 SE" \
            " \u0637\u0648\u0644\u0627" \
            " \u0646\u064a" \
            " \u0627\u0633\u062a."
        para.set_para(text, UBiDi.UBIDI_DEFAULT_RTL)
        self.assertTrue(u_success(para.status), msg=para.status)

        direction = para.get_direction()
        self.assertEqual(direction, UBiDi.UBIDI_MIXED)

        count = para.count_runs()
        self.assertEqual(count, 3)

        logical_start, length, direction = para.get_visual_run(0)
        self.assertEqual(direction, UBiDi.UBIDI_RTL)
        self.assertEqual(text[logical_start:logical_start + length],
                         " \u0637\u0648\u0644\u0627" 
                         " \u0646\u064a"
                         " \u0627\u0633\u062a.")

        logical_start, length, direction = para.get_visual_run(1)
        self.assertEqual(direction, UBiDi.UBIDI_LTR)
        self.assertEqual(text[logical_start:logical_start + length],
                         'SVG 1.1 SE')

        logical_start, length, direction = para.get_visual_run(2)
        self.assertEqual(direction, UBiDi.UBIDI_RTL)
        self.assertEqual(text[logical_start:logical_start + length],
                         '\u062f\u0627\u0633\u062a\u0627\u0646 ')

    def test_break_iterator_get_available(self):
        count = UBreakIterator.count_available()
        self.assertTrue(count > 0)

        locale = UBreakIterator.get_available(0)
        self.assertIsNotNone(locale)

        locale = UBreakIterator.get_available(count - 1)
        self.assertIsNotNone(locale)

        locale = UBreakIterator.get_available(count)
        self.assertIsNone(locale)

    def test_break_iterator_word01(self):
        bi = UBreakIterator(UBreakIterator.UBRK_WORD, 'en_US')

        offset = bi.first()
        self.assertEqual(offset, 0)

        offset = bi.next()
        self.assertEqual(offset, -1)

        offset = bi.last()
        self.assertEqual(offset, 0)

        offset = bi.previous()
        self.assertEqual(offset, -1)

    def test_break_iterator_word02(self):
        bi = UBreakIterator(UBreakIterator.UBRK_WORD,
                            'en_US',
                            'Make haste slowly.')

        # |Make| |haste| |slowly|.|
        # |0....4.5.....0.1......7.8
        offset = bi.first()
        self.assertEqual(offset, 0)

        offset = bi.next()
        self.assertEqual(offset, 4)

        offset = bi.last()
        self.assertEqual(offset, 18)

        offset = bi.previous()
        self.assertEqual(offset, 17)

    def test_break_iterator_iter_character01(self):
        bi = UBreakIterator(
            UBreakIterator.UBRK_CHARACTER,
            'ja_JP',
            'あｱa\U00020000!')
        items = [x for x in bi]
        expected = ['あ', 'ｱ', 'a', '\U00020000', '!']
        self.assertEqual(items, expected)

    def test_break_iterator_iter_sentence01(self):
        # http://www.unicode.org/reports/tr29/#Sentence_Boundaries
        # http://unicode.org/cldr/utility/bidi.jsp
        text = "He said, “Are you going?” John shook his head." \
               " “Are you going?” John asked."
        bi = UBreakIterator(UBreakIterator.UBRK_SENTENCE, 'en_US')
        bi.set_text(text)
        items = [x for x in bi]
        expected = [
            'He said, “Are you going?” ',
            'John shook his head. ',
            '“Are you going?” ',
            'John asked.']
        self.assertEqual(items, expected)

    def test_break_iterator_iter_word01(self):
        # http://userguide.icu-project.org/boundaryanalysis
        # http://unicode.org/cldr/utility/bidi.jsp
        text = 'Your balance is $1,234.56... I think.'
        bi = UBreakIterator(UBreakIterator.UBRK_WORD, 'en_US')
        bi.set_text(text)
        items = [x for x in bi]
        expected = [
            'Your', ' ',
            'balance', ' ',
            'is', ' ',
            '$', '1,234.56', '.', '.', '.', ' ',
            'I', ' ',
            'think', '.']
        self.assertEqual(items, expected)

    def test_break_iterator_iter_word02(self):
        # http://userguide.icu-project.org/boundaryanalysis
        text = 'Parlez-vous français ?'
        bi = UBreakIterator(UBreakIterator.UBRK_WORD, 'fr_FR')
        bi.set_text(text)
        items = [x for x in bi]
        expected = [
            'Parlez', '-',
            'vous', ' ',
            'français', ' ', '?']
        self.assertEqual(items, expected)

    def test_break_iterator_iter_word03(self):
        # https://stackoverflow.com/questions/44507838/breakiterator-not-working-correctly-with-chinese-text
        text = 'I like to eat apples. 我喜欢吃苹果。'
        bi = UBreakIterator(UBreakIterator.UBRK_WORD, 'zh_CN')
        bi.set_text(text)
        items = [x for x in bi]
        expected = [
            'I', ' ',
            'like', ' ',
            'to', ' ',
            'eat', ' ',
            'apples', '.', ' ',
            '我',
            '喜欢',
            '吃',
            '苹果',
            '。']
        self.assertEqual(items, expected)

    def test_break_iterator_iter_line02(self):
        # http://userguide.icu-project.org/boundaryanalysis
        text = 'Parlez-vous français ?'
        bi = UBreakIterator(UBreakIterator.UBRK_LINE, 'fr_FR')
        bi.set_text(text)
        items = [x for x in bi]
        expected = [
            'Parlez-',
            'vous ',
            'français ?']
        self.assertEqual(items, expected)

    def test_locale_get_character_orientation01(self):
        locale = ULocale('en_US')
        layout = locale.get_character_orientation()
        self.assertEqual(layout, ULocale.ULOC_LAYOUT_LTR)

    def test_locale_get_character_orientation02(self):
        locale = ULocale('fa')
        layout = locale.get_character_orientation()
        self.assertEqual(layout, ULocale.ULOC_LAYOUT_RTL)

    def test_locale_get_character_orientation03(self):
        locale = ULocale('und-Zzzz')
        layout = locale.get_character_orientation()
        self.assertEqual(layout, ULocale.ULOC_LAYOUT_LTR)

    def test_locale_get_default(self):
        locale = ULocale.get_default()
        language = locale.get_language()
        self.assertTrue(language is not None)

    def test_locale_get_language01(self):
        locale = ULocale('sr-Latn-RS-REVISED@currency=USD')
        language = locale.get_language()
        self.assertEqual(language, 'sr')

    def test_locale_get_language02(self):
        locale = ULocale('und-Zzzz')
        language = locale.get_language()
        self.assertEqual(language, 'und')

    def test_locale_get_line_orientation01(self):
        locale = ULocale('en_US')
        layout = locale.get_line_orientation()
        self.assertEqual(layout, ULocale.ULOC_LAYOUT_TTB)

    def test_locale_get_line_orientation03(self):
        locale = ULocale('und-Zzzz')
        layout = locale.get_line_orientation()
        self.assertEqual(layout, ULocale.ULOC_LAYOUT_TTB)

    def test_locale_get_script01(self):
        locale = ULocale('sr-Latn-RS-REVISED@currency=USD')
        script = locale.get_script()
        self.assertEqual(script, 'Latn')

    def test_locale_get_script02(self):
        locale = ULocale('und-Zzzz')
        script = locale.get_script()
        self.assertEqual(script, 'Zzzz')

    def test_str_to_utf8(self):
        text = 'あｱa\U00020000!'

        # u_strFromUTF8(): str -> UChar*
        dest = ffi.new('UChar[256]')
        dest_length = ffi.new('int32_t *')
        src = ffi.new('char[]', text.encode())
        status = ffi.new('UErrorCode *')
        u_str_from_utf8(dest, len(dest), dest_length, src, len(src), status)
        self.assertEqual(status[0], 0)

        # auto (cffi): str -> UChar*
        dest2 = ffi.new('UChar[]', text)
        length = u_strlen(dest2)
        self.assertEqual(len(dest2) - 1, length)
        self.assertEqual([dest[n] for n in range(length)],
                         [dest2[n] for n in range(length)])

        self.assertEqual(ffi.string(dest2), text)

        # u_strToUTF8(): UChar* -> char* -> str
        src = dest
        dest = ffi.new('char[512]')
        dest_length = ffi.new('int32_t *')
        status[0] = 0
        u_str_to_utf8(dest, len(dest), dest_length, src, len(src), status)
        self.assertEqual(status[0], 0)
        self.assertEqual(ffi.string(dest).decode(), text)

    def test_version(self):
        version = icu.version
        self.assertIsInstance(version, str)


if __name__ == '__main__':
    unittest.main()
