# Copyright (C) 2018 Tetsuya Miura <miute.dev@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


class Screen(object):
    """Represents the [cssom-view] Screen."""

    DEFAULT_HORIZONTAL_RESOLUTION = 96
    DEFAULT_VERTICAL_RESOLUTION = 96

    DEFAULT_SCREEN_HEIGHT = 720
    DEFAULT_SCREEN_WIDTH = 1280

    COLOR_GAMUT_SRGB = 'srgb'
    COLOR_GAMUT_P3 = 'p3'
    COLOR_GAMUT_REC2020 = 'rec2020'

    MEDIA_ALL = 'all'
    MEDIA_PRINT = 'print'
    MEDIA_SCREEN = 'screen'
    MEDIA_SPEECH = 'speech'

    ORIENTATION_LANDSCAPE = 'landscape'
    ORIENTATION_PORTRAIT = 'portrait'

    SCAN_INTERLACE = 'interlace'
    SCAN_PROGRESSIVE = 'progressive'

    UPDATE_NONE = 'none'
    UPDATE_SLOW = 'slow'
    UPDATE_FAST = 'fast'

    def __init__(self):
        self._width = Screen.DEFAULT_SCREEN_WIDTH
        self._height = Screen.DEFAULT_SCREEN_HEIGHT
        self._color_depth = 24
        self._orientation = Screen.ORIENTATION_LANDSCAPE
        self._horizontal_resolution = Screen.DEFAULT_HORIZONTAL_RESOLUTION
        self._vertical_resolution = Screen.DEFAULT_VERTICAL_RESOLUTION
        self._device_pixel_ratio = 1.
        self._scan = Screen.SCAN_PROGRESSIVE
        self._update = Screen.UPDATE_NONE
        self._monochrome = 0
        self._color_gamut = Screen.COLOR_GAMUT_SRGB
        self._media = Screen.MEDIA_SCREEN

    def __repr__(self):
        return repr({'width': self._width,
                     'height': self._height,
                     'color_depth': self._color_depth,
                     'orientation': self._orientation,
                     'horizontal_resolution': self._horizontal_resolution,
                     'vertical_resolution': self._vertical_resolution,
                     'device_pixel_ratio': self._device_pixel_ratio,
                     'scan': self._scan,
                     'update': self._update,
                     'color_gamut': self._color_gamut,
                     'media': self._media,
                     })

    @property
    def color_depth(self):
        """int: The 'color' media feature describes the number of bits
        allocated to colors for a pixel in the output device, excluding the
        alpha channel.
        """
        return self._color_depth

    @color_depth.setter
    def color_depth(self, color_depth):
        self._color_depth = int(color_depth)

    @property
    def color_gamut(self):
        """str: The 'color-gamut' media feature."""
        return self._color_gamut

    @color_gamut.setter
    def color_gamut(self, color_gamut):
        self._color_gamut = color_gamut

    @property
    def device_pixel_ratio(self):
        return self._device_pixel_ratio

    @device_pixel_ratio.setter
    def device_pixel_ratio(self, ratio):
        self._device_pixel_ratio = float(ratio)

    @property
    def height(self):
        """int: The height of the screen area."""
        return self._height

    @height.setter
    def height(self, height):
        self._height = int(height)

    @property
    def horizontal_resolution(self):
        return self._horizontal_resolution

    @horizontal_resolution.setter
    def horizontal_resolution(self, resolution):
        self._horizontal_resolution = int(resolution)

    @property
    def media(self):
        """str: The media type."""
        return self._media

    @media.setter
    def media(self, media):
        self._media = media

    @property
    def monochrome(self):
        """int: The 'monochrome' media feature."""
        return self._monochrome

    @monochrome.setter
    def monochrome(self, monochrome):
        self._monochrome = int(monochrome)

    @property
    def orientation(self):
        """str: The 'orientation' media feature."""
        return self._orientation

    @orientation.setter
    def orientation(self, orientation):
        self._orientation = orientation

    @property
    def pixel_depth(self):
        """int: Same as the color_depth."""
        return self.color_depth

    @property
    def scan(self):
        """str: The 'scan' media feature."""
        return self._scan

    @scan.setter
    def scan(self, scan):
        self._scan = scan

    @property
    def update(self):
        """str: The 'update' media feature."""
        return self._update

    @update.setter
    def update(self, update):
        self._update = update

    @property
    def vertical_resolution(self):
        return self._vertical_resolution

    @vertical_resolution.setter
    def vertical_resolution(self, resolution):
        self._vertical_resolution = int(resolution)

    @property
    def width(self):
        """int: The width of the screen area."""
        return self._width

    @width.setter
    def width(self, width):
        self._width = int(width)
