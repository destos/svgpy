#!/usr/bin/env python3

import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy import window
from svgpy.core import MediaQueryList


class MediaQueryTestCase(unittest.TestCase):
    def setUp(self):
        screen = window.screen
        screen.color_depth = 24
        screen.orientation = 'landscape'
        screen.device_pixel_ratio = 1
        screen.update = 'none'
        screen.width = 1280
        screen.height = 720
        screen.scan = 'progressive'
        screen.color_gamut = 'srgb'
        window.media = 'screen'
        window.inner_width = 1280
        window.inner_height = 720
        window.page_zoom_scale = 1

    def test_match_boolean_color(self):
        query = '(color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = '(color > 0)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.color_depth = 0
        query = '(color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.color_depth = 0
        query = '(color > 0)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_boolean_grid(self):
        query = '(grid)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_boolean_pointer(self):
        query = '(pointer)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_boolean_update(self):
        window.screen.update = 'slow'
        query = '(update: fast) or (update: slow)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.update = 'fast'
        query = '(update)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.update = 'none'
        query = '(update)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.update = 'none'
        query = 'not (update)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.update = 'none'
        query = '(update: none)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.update = 'none'
        query = 'not (update)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    @unittest.expectedFailure
    def test_match_invalid_grammar01(self):
        # FIXME: invalid grammar cause RecursionError.
        query = '(example, all,)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_grammar02(self):
        query = '&test, speech'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.media = 'speech'
        query = '&test, speech'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_invalid_grammar03(self):
        query = 'or and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_mf_name01(self):
        # unknown media feature
        query = 'screen and (max-weight: 3000) and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_mf_name02(self):
        # unknown media feature
        # 'discrete' media feature with min/max prefix
        window.screen.orientation = 'portrait'
        query = '(min-orientation: portrait)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_mf_name03(self):
        # unknown media feature
        # 'discrete' media feature with min/max prefix
        query = '(min-grid: 0)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_mf_value01(self):
        # 25.4cm == 960px
        query = 'screen and (min-width: 25.4cm) and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        # unknown unit
        query = 'screen and (min-width: 0.254m) and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_mf_value02(self):
        # unknown unit
        query = '(color: 20example)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_invalid_op(self):
        query = '(color) and (width > 600px) and (height > 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        # mix 'and' and 'or' at the same level
        query = '(color) and (width > 600px) or (height > 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_list_media(self):
        query = 'test;,all'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_list_media_boolean01(self):
        query = 'screen and (color), projection and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.media = 'print'
        query = 'screen and (color), projection and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.media = 'projection'
        query = 'screen and (color), projection and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.media = 'projection'
        window.screen.color_depth = 0
        query = 'screen and (color), projection and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_media01(self):
        query = 'all'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_media02(self):
        query = 'screen'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = 'print'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_media03(self):
        window.media = 'print'
        query = 'screen'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.media = 'print'
        query = 'print'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_media04(self):
        # unknown media
        query = 'unknown'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        query = 'not unknown'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_media_boolean01(self):
        query = 'screen and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.color_depth = 0
        query = 'screen and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_media_not_boolean01(self):
        query = 'not screen and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.media = 'print'
        query = 'not screen and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.media = 'print'
        window.screen.color_depth = 0
        query = 'not screen and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_plain_color_gamut(self):
        query = '(color-gamut: srgb)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = '(color-gamut: p3)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.color_gamut = 'rec2020'
        query = '(color-gamut: rec2020)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_plain_orientation(self):
        query = '(orientation: landscape)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = '(orientation: portrait)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.orientation = 'portrait'
        query = '(orientation: landscape)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.orientation = 'portrait'
        query = '(orientation: portrait)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_plain_resolution01(self):
        query = 'not (resolution: -300dpi)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = '(min-resolution: 1dppx)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = '(min-resolution: 2dppx)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.device_pixel_ratio = 2
        query = '(min-resolution: 2dppx)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_plain_resolution02(self):
        # page zoom scale: 90%
        # 1dppx * 0.9 = 0.9dppx = 86.4dpi = 34.0157...dpcm
        window.page_zoom_scale = 0.9
        query = '(resolution: 0.9dppx)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.page_zoom_scale = 0.9
        query = '(resolution: 86.4dpi)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.page_zoom_scale = 0.9
        query = '(min-resolution: 34.1dpcm)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.page_zoom_scale = 0.9
        query = '(min-resolution: 34.0dpcm)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_plain_scan(self):
        query = '(scan: progressive)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        query = '(scan: interlace)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.scan = 'interlace'
        query = '(scan: progressive)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.scan = 'interlace'
        query = '(scan: interlace)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_plain_width(self):
        window.inner_width = 599
        query = '(width: 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_width = 600
        query = '(width: 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 601
        query = '(width: 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_range_aspect_ratio(self):
        query = '(aspect-ratio: 16/9)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        # 16/9 >= 1/1
        query = '(min-aspect-ratio: 1/1)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        # 16/9 <= 4/3
        query = '(max-aspect-ratio: 4/3)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_range_color_index(self):
        query = '(min-color-index: 256)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.color_depth = 8
        query = '(min-color-index: 256)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.color_depth = 4
        query = '(min-color-index: 17)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.screen.color_depth = 4
        query = '(min-color-index: 16)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.color_depth = 4
        query = '(0 < color-index <= 16)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_range_height01(self):
        window.inner_height = 600
        query = '(height > 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_height = 601
        query = '(height > 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_height = 600
        query = '(600px < height)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_height = 601
        query = '(600px < height)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_height = 720
        query = '(height > -100px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_range_height02(self):
        # '(height >= 600px)'
        window.inner_height = 599
        query = '(min-height: 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_height = 600
        query = '(min-height: 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_height = 601
        query = '(min-height: 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_range_monochrome(self):
        query = '(monochrome)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        query = '(monochrome: 0)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.monochrome = 2
        query = '(monochrome)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.monochrome = 2
        query = '(min-monochrome: 2)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.monochrome = 2
        query = '(monochrome >= 2)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.screen.monochrome = 2
        query = '(monochrome > 2)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_range_width01(self):
        window.inner_width = 599
        query = '(width >= 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_width = 600
        query = '(width >= 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 601
        query = '(width >= 600px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 1280
        query = 'not (width <= -100px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_range_width02(self):
        window.inner_width = 400
        query = '(400px < width < 1000px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_width = 401
        query = '(400px < width < 1000px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 999
        query = '(400px < width < 1000px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 1000
        query = '(400px < width < 1000px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_range_width03(self):
        # 1em = 16px
        window.inner_width = 40 * 16 - 1
        query = '(width <= 40em)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 40 * 16
        query = '(width <= 40em)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 40 * 16 + 1
        query = '(width <= 40em)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_width = 40 * 16 - 1
        query = '(max-width: 40em)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 40 * 16
        query = '(max-width: 40em)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 40 * 16 + 1
        query = '(max-width: 40em)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

    def test_match_range_width04(self):
        # '(width >= 320.01px)'
        window.inner_width = 320
        query = '(min-width: 320.01px)'
        mql = MediaQueryList(query)
        self.assertTrue(not mql.matches)

        window.inner_width = 320.01
        query = '(min-width: 320.01px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

        window.inner_width = 320.02
        query = '(min-width: 320.01px)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)

    def test_match_only_media_boolean01(self):
        query = 'only screen and (color)'
        mql = MediaQueryList(query)
        self.assertTrue(mql.matches)


if __name__ == '__main__':
    unittest.main()
