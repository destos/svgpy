#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy.fontconfig import FontConfig


# $ mkdir -p ~/.config/fontconfig
# edit ~/.config/fontconfig/fonts.conf
class FontConfigTestCase(unittest.TestCase):
    def test_config_list(self):
        files = FontConfig.get_config_files()
        # for file in files:
        #     print(file)
        self.assertTrue(len(files) > 0)

    def test_list01(self):
        s = FontConfig.list()
        self.assertTrue(len(s) > 0)

    def test_list02(self):
        # "DejaVu Sans"
        pattern = 'DejaVu Sans'
        s = FontConfig.list(pattern)
        self.assertTrue(len(s) > 0,
                        msg='"{}" is not installed.'.format(pattern))

    def test_list03(self):
        # weight: bold
        pattern = 'DejaVu Sans:weight=bold'
        s = FontConfig.list(pattern)
        self.assertTrue(len(s) > 0,
                        msg='"{}" is not installed.'.format(pattern))

    def test_list04(self):
        # slant: oblique
        pattern = 'DejaVu Sans:slant=oblique'
        s = FontConfig.list(pattern)
        self.assertTrue(len(s) > 0,
                        msg='"{}" is not installed.'.format(pattern))

    def test_list05(self):
        # slant: italic
        pattern = 'DejaVu Sans:slant=italic'
        s = FontConfig.list(pattern)
        self.assertTrue(len(s) == 0,
                        msg='"{}" is not installed.'.format(pattern))

    def test_list06(self):
        # weight: bold
        # slant: oblique
        pattern = 'DejaVu Sans:weight=bold:slant=oblique'
        s = FontConfig.list(pattern)
        self.assertTrue(len(s) >= 2,
                        msg='"{}" is not installed.'.format(pattern))

    def test_list07(self):
        # weight: bold
        # slant: oblique
        # width: semi-condensed
        pattern = 'DejaVu Sans:weight=bold:slant=oblique:width=semicondensed'
        s = FontConfig.list(pattern)
        self.assertTrue(len(s) >= 1,
                        msg='"{}" is not installed.'.format(pattern))

    def test_list08(self):
        # weight: bold
        pattern = 'DejaVu Sans:weight=bold'
        fc_elements = [FontConfig.FC_FAMILY, FontConfig.FC_WEIGHT]
        # '%{family}\t%{weight}'
        fc_format = '\t'.join(['%{{{}}}'.format(x) for x in fc_elements])
        s = FontConfig.list(pattern, fc_elements, fc_format)
        self.assertTrue(len(s) > 0,
                        msg='"{}" is not installed.'.format(pattern))

        expected = '200'  # bold
        for matched in iter(s):
            items = matched.split('\t')
            self.assertEqual(expected, items[1])

    def test_match01(self):
        if sys.platform == 'win32' or sys.platform == 'darwin':
            pattern = 'Verdana'
        else:
            pattern = 'DejaVu Sans'
        s = FontConfig.match(pattern)
        self.assertTrue(len(s) > 0,
                        msg='"{}" is not installed.'.format(pattern))

    def test_match02(self):
        for pattern in ['serif', 'sans-serif', 'monospace']:
            s = FontConfig.match(pattern)
            self.assertTrue(
                len(s) > 0,
                msg='fontconfig: "{}" is not configured.'.format(pattern))

    def test_version(self):
        version = FontConfig.version
        major = version // 10000
        t = version % 10000
        minor = t // 100
        # revision = t % 100
        # print(version, major, minor, revision)
        self.assertTrue(major >= 2)
        if major == 2:
            self.assertTrue(minor >= 10)


if __name__ == '__main__':
    unittest.main()
