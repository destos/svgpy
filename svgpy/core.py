# Copyright (C) 2017 Tetsuya Miura <miute.dev@gmail.com>
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


import copy
import html
import math
import re
import shlex
import unicodedata
from abc import ABC, abstractmethod
from collections.abc import MutableMapping
from decimal import Decimal

import numpy as np
from lxml import etree

from .fontconfig import FontConfig
from .formatter import format_number_sequence
from .freetype import FreeType, FTFace


def dict_to_style(d):
    if d is None:
        return ''
    items = ['{}: {};'.format(x, d[x]) for x in iter(d.keys())]
    return ' '.join(sorted(items))


def style_to_dict(text):
    if text is None:
        return {}
    items = [x.split(':') for x in iter(text.strip().split(';'))]
    if [''] in items:
        items.remove([''])
    return {key.strip(): value.strip() for key, value in iter(items)}


def matrix2d(a, b, c, d, e, f):
    """Returns a 2d (3x3) matrix.

    Arguments:
        a (float): The a component of the matrix.
        b (float): The b component of the matrix.
        c (float): The c component of the matrix.
        d (float): The d component of the matrix.
        e (float): The e component of the matrix.
        f (float): The f component of the matrix.
    Returns:
        numpy.matrix: A 3x3 matrix object.
    """
    return np.matrix([[float(a), float(c), float(e)],
                      [float(b), float(d), float(f)],
                      [float(0), float(0), float(1)]])


class Attrib(MutableMapping):
    """A wrapper class for lxml.etree._Attrib."""

    def __init__(self, attrib):
        """Constructs a Attrib object.

        Arguments:
            attrib (lxml.etree._Attrib): An attribute object.
        """
        self._attrib = attrib  # type: dict

    def __delitem__(self, name):
        """Removes an element attribute with the name."""
        if name in self._attrib:
            del self._attrib[name]
            return
        style = self.get_style({})
        del style[name]
        if len(style) > 0:
            self.set_style(style)
        else:
            del self._attrib['style']

    def __getitem__(self, name):
        """Gets an element attribute."""
        value = self._attrib.get(name)
        if value is not None:
            return value.strip()
        style = self.get_style()
        if style is not None:
            return style[name]
        raise KeyError

    def __iter__(self):
        for x in self._attrib:
            yield x

    def __len__(self):
        return len(self._attrib)

    def __repr__(self):
        return repr(self._attrib)

    def __setitem__(self, key, value):
        self.set(key, value)

    def get_ns(self, namespace, local_name, default=None):
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        return self._attrib.get(name, default)

    def get_style(self, default=None):
        """Returns the 'style' attribute."""
        style = self._attrib.get('style')
        if style is None:
            return default
        return style_to_dict(style)

    def pop(self, name, default=None):
        """Removes an element attribute with the name and returns the value
        associated with it.
        """
        try:
            value = self.__getitem__(name)
            self.__delitem__(name)
            return value
        except KeyError:
            return default

    def pop_ns(self, namespace, local_name, default=None):
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        return self._attrib.pop(name, default)

    def set(self, name, value):
        """Sets an element attribute."""
        if name in self._attrib:
            self._attrib[name] = value
            return
        style = self.get_style()
        if style is not None and name in style:
            style[name] = value
            self.set_style(style)
            return
        self._attrib[name] = value

    def set_ns(self, namespace, local_name, value):
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        self._attrib[name] = value

    def setdefault_ns(self, namespace, local_name, default):
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        value = self._attrib.get(name, default)
        if name not in self._attrib:
            self._attrib[name] = value
        return value

    def set_style(self, d):
        """Sets the 'style' attribute."""
        style = dict_to_style(d)
        self._attrib['style'] = style


class CSSUtils(object):
    # See https://www.w3.org/TR/css-fonts-3/#font-size-prop
    # See https://drafts.csswg.org/css-fonts-3/#font-size-prop
    _ABSOLUTE_FONT_SIZE_MAP = {
        # <absolute-size> keyword: (row, scale size factor)
        'xx-small': (0, 3 / 5),
        'x-small': (1, 3 / 4),
        'small': (2, 8 / 9),
        'medium': (3, 1),
        'large': (4, 6 / 5),
        'x-large': (5, 3 / 2),
        'xx-large': (6, 2 / 1),
    }
    """dict: The scale size factor for the absolute font size."""

    _QUIRKS_FONT_SIZE_TABLE = [
        [9, 9, 9, 9, 11, 14, 18, 28],
        [9, 9, 9, 10, 11, 14, 18, 31],  # (10px) fixed
        [9, 9, 9, 11, 13, 17, 22, 34],
        [9, 9, 10, 12, 14, 18, 24, 37],  # (12px)
        [9, 9, 10, 13, 16, 20, 26, 40],  # fixed font default (13px)
        [9, 9, 11, 14, 17, 21, 28, 42],
        [9, 10, 12, 15, 17, 23, 30, 45],
        [9, 10, 13, 16, 18, 24, 32, 48],  # proportional font default (16px)
    ]

    _STRICT_FONT_SIZE_TABLE = [
        [9, 9, 9, 9, 11, 14, 18, 27],
        [9, 9, 9, 10, 12, 15, 20, 30],
        [9, 9, 10, 11, 13, 17, 22, 33],
        [9, 9, 10, 12, 14, 18, 24, 36],
        [9, 10, 12, 13, 16, 20, 26, 39],
        [9, 10, 12, 14, 17, 21, 28, 42],
        [9, 10, 13, 15, 18, 23, 30, 45],
        [9, 10, 13, 16, 18, 24, 32, 48],  # proportional font default (16px)
    ]
    # See https://dom.spec.whatwg.org/#concept-document-mode
    """list: The table of the font size for the absolute font size."""

    _FONT_SIZE_TABLE_MAX = 16
    _FONT_SIZE_TABLE_MIN = 9
    _MINIMUM_FONT_SIZE = 10

    # See https://www.w3.org/TR/css-fonts-3/#font-weight-prop
    # See https://drafts.csswg.org/css-fonts-3/#font-weight-prop
    _FONT_WEIGHT_MAP = {
        'normal': 400,
        'bold': 700,
    }

    _INHERITED_WEIGHT_LIST = [100, 200, 300, 400, 500, 600, 700, 800, 900]
    _BOLDER_WEIGHT_LIST = [400, 400, 400, 700, 700, 900, 900, 900, 900]
    _LIGHTER_WEIGHT_LIST = [100, 100, 100, 100, 100, 400, 400, 700, 700]

    _RE_COLLAPSIBLE_WHITESPACE = re.compile(r'(\x20){2,}', re.MULTILINE)
    _RE_SEGMENT_BREAKS = re.compile(r'(\r\n|\r|\n)+', re.MULTILINE)
    _RE_PRECEDING_TAB_WHITESPACE = re.compile(r'^(\x20|\t)+', re.MULTILINE)
    _RE_FOLLOWING_TAB_WHITESPACE = re.compile(r'(\x20|\t)+$', re.MULTILINE)

    @staticmethod
    def compute_font_size(element, inherited_size=None, inherited_style=None):
        # See https://www.w3.org/TR/css-fonts-3/#font-size-prop
        # See https://drafts.csswg.org/css-fonts-3/#font-size-prop
        if inherited_style is None:
            inherited_style = element.get_inherited_style()

        # 'font-size' property
        # Value: <absolute-size> | <relative-size> | <length> | <percentage>
        # Initial: medium
        # Inherited: yes
        # Percentages: refer to parent element's font size
        font_size = inherited_style['font-size']
        if font_size in CSSUtils._ABSOLUTE_FONT_SIZE_MAP:
            # <absolute-size>
            # Value: xx-small | x-small | small | medium | large | x-large
            #  | xx-large
            column, scale_factor = CSSUtils._ABSOLUTE_FONT_SIZE_MAP[
                font_size]
            medium_size = Font.default_font_size
            if CSSUtils._FONT_SIZE_TABLE_MIN <= medium_size \
                    <= CSSUtils._FONT_SIZE_TABLE_MAX:
                row = int(medium_size - CSSUtils._FONT_SIZE_TABLE_MIN)
                px = CSSUtils._QUIRKS_FONT_SIZE_TABLE[row][column]
            else:
                px = scale_factor * medium_size
        elif font_size in ['larger', 'smaller']:
            # <relative-size>
            # Value: larger | smaller
            if inherited_size is None:
                inherited_size = Font.default_font_size
            parent_sequence = list()
            parent = element.getparent()
            while parent is not None:
                parent_sequence.insert(0, parent)
                parent = parent.getparent()
            for parent in iter(parent_sequence):
                value = parent.attributes.get('font-size')
                if value is None:
                    continue
                elif value in ['larger', 'smaller']:
                    scale_factor = 1.2 if font_size == 'larger' else 1 / 1.2
                    inherited_size *= scale_factor
                else:
                    inherited_size = CSSUtils.compute_font_size(
                        parent,
                        inherited_size,
                        {'font-size': value})
            px = inherited_size
        else:
            # <length> or <percentage>
            # See https://drafts.csswg.org/css-values-3/#lengths
            fs = SVGLength(font_size, context=element)
            px = fs.value()

        if px < CSSUtils._MINIMUM_FONT_SIZE:
            px = CSSUtils._MINIMUM_FONT_SIZE
        return float(px)

    @staticmethod
    def compute_font_size_adjust(style):
        # 'font-size-adjust' property
        # Value: 'none' | <number>
        # Initial: none
        # Inherited: yes
        # Percentages: N/A
        # See https://www.w3.org/TR/css-fonts-3/#font-size-adjust-prop
        # See https://drafts.csswg.org/css-fonts-3/#font-size-adjust-prop
        font_size_adjust = style['font-size-adjust']
        if font_size_adjust != 'none':
            font_size_adjust = SVGLength(font_size_adjust).value()
        return font_size_adjust

    @staticmethod
    def compute_font_weight(element,
                            inherited_weight=None, inherited_style=None):
        # See https://www.w3.org/TR/css-fonts-3/#font-weight-prop
        # See https://drafts.csswg.org/css-fonts/#font-weight-prop
        if inherited_style is None:
            inherited_style = element.get_inherited_style()

        # 'font-weight' property
        # Value: normal | bold | bolder | lighter
        #  | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900
        # Initial: normal
        # Inherited: yes
        # Percentages: N/A
        font_weight = inherited_style['font-weight']
        if font_weight in ['bolder', 'lighter']:
            # <relative-weight>
            # Value: bolder | lighter
            if inherited_weight is None:
                inherited_weight = Font.default_font_weight
            parent_sequence = list()
            parent = element.getparent()
            while parent is not None:
                parent_sequence.insert(0, parent)
                parent = parent.getparent()
            for parent in iter(parent_sequence):
                value = parent.attributes.get('font-weight')
                if value is None:
                    continue
                elif value in ['bolder', 'lighter']:
                    xp = CSSUtils._INHERITED_WEIGHT_LIST
                    fp = CSSUtils._BOLDER_WEIGHT_LIST if value == 'bolder' \
                        else CSSUtils._LIGHTER_WEIGHT_LIST
                    inherited_weight = np.interp(inherited_weight, xp, fp)
                else:
                    inherited_weight = CSSUtils.compute_font_weight(
                        parent,
                        inherited_weight,
                        {'font-weight': value})
            weight = inherited_weight
        else:
            # <absolute-weight>
            weight = CSSUtils._FONT_WEIGHT_MAP.get(font_weight, font_weight)

        return int(weight)

    @staticmethod
    def compute_line_height(element, computed_style=None):
        if computed_style is None:
            computed_style = element.get_computed_style()

        # 'line-height' property
        # Value: normal | <number> | <length> | <percentage> | inherit
        # Initial: normal
        # Inherited: yes
        # Percentages: refer to the font size of the element itself
        # See https://www.w3.org/TR/CSS22/visudet.html#line-height
        # See https://drafts.csswg.org/css2/visudet.html#propdef-line-height
        value = computed_style['line-height']
        font_size = computed_style['font-size']
        if value == 'normal':
            line_height = 1.2 * font_size
        else:
            h = SVGLength(value, context=element)
            if h.unit == SVGLength.TYPE_PERCENTAGE:
                # <percentage>
                line_height = (h.value(SVGLength.TYPE_PERCENTAGE) / 100
                               * font_size)
            else:
                # <length> or <number>
                line_height = h.value()
        return line_height

    @staticmethod
    def get_value(element, key, default=None):
        context = element
        while context is not None:
            value = context.attributes.get(key, default)
            if value == 'auto' and key in ['width', 'height']:
                # See https://drafts.csswg.org/css2/visudet.html#the-width-property
                local_name = context.local_name
                if local_name == 'svg':
                    return '100%', context
                elif local_name == 'image':
                    # TODO: compute width/height for 'image' element.
                    raise NotImplementedError
                else:
                    return '0', context
            elif value is not None and value != 'inherit':
                return value, context
            context = context.getparent()
        return None, element

    @staticmethod
    def normalize_text_content(element, text, style, prev_text=None,
                               first=False, tail=False):
        """Apply white-space processing to a text."""
        _ = element  # reserved

        def _is_hangul(ch):
            return (('\uAC00' <= ch <= '\uD7AF')
                    or ('\u1100' <= ch <= '\u11FF')
                    or ('\u3130' <= ch <= '\u318F')
                    or ('\uA960' <= ch <= '\uA97F')
                    or ('\uD7B0' <= ch <= '\uD7FF'))

        def _transform_segment_break(_text, _style):
            # See https://drafts.csswg.org/css-text-3/#line-break-transform
            _white_space = _style['white-space']
            if _white_space in ['pre', 'pre-wrap', 'pre-line']:
                _out_text = _text.replace('\r\n', '\n').replace('\r', '\n')
                return _out_text

            # white-space: normal | nowrap
            _break_positions = list()
            for _it in CSSUtils._RE_SEGMENT_BREAKS.finditer(_text):
                _break_positions.append(_it.span(0))
            if len(_break_positions) == 0:
                return _text

            _out_text = ''
            _last = 0
            _max_length = len(_text)
            for _start, _end in _break_positions:
                _out_text += _text[_last:_start]
                if ((_start > 0 and _text[_start - 1] == '\u200B')
                        or (_end < _max_length
                            and _text[_end] == '\u200B')):
                    pass  # remove segment breaks
                elif (_start > 0 and _end < _max_length
                      and unicodedata.east_asian_width(
                            _text[_start - 1]) in 'FWH'
                      and not _is_hangul(_text[_start - 1])
                      and unicodedata.east_asian_width(
                            _text[_end]) in 'FWH'
                      and not _is_hangul(_text[_end])):
                    pass  # remove segment breaks
                else:
                    _out_text += ' '  # convert to a space (U+0020)
                _last = _end
            else:
                _out_text += _text[_last:]
            return _out_text

        # See https://drafts.csswg.org/css-text-3/#white-space-property
        # 'white-space' property
        # Value: normal | pre | nowrap | pre-wrap | pre-line
        # Initial: normal
        # Inherited: yes
        # Percentages: N/A
        white_space = style['white-space']
        out_text = html.unescape(text)

        # FIXME: fix white-space processing.
        # See https://drafts.csswg.org/css-text-3/#white-space-rules
        if white_space in ['normal', 'nowrap', 'pre-line']:
            out_text = CSSUtils._RE_PRECEDING_TAB_WHITESPACE.sub(
                '', out_text)
            out_text = CSSUtils._RE_FOLLOWING_TAB_WHITESPACE.sub(
                '', out_text)
            out_text = _transform_segment_break(out_text, style)
            out_text = out_text.replace('\t', ' ')
            out_text = CSSUtils._RE_COLLAPSIBLE_WHITESPACE.sub(
                ' ', out_text)
        if white_space in ['pre', 'pre-wrap']:
            out_text = _transform_segment_break(out_text, style)

        if prev_text is not None:
            if prev_text.endswith(' ') and out_text.startswith(' '):
                out_text = out_text.lstrip()
            elif not prev_text.endswith(' ') and not out_text.startswith(' '):
                out_text = ' ' + out_text
        if first:
            out_text = out_text.lstrip(' ')
        # if len(element) == 0:
        if tail:
            out_text = out_text.rstrip(' ')

        return out_text

    @staticmethod
    def parse_font(value):
        """Parses a value of the shorthand 'font' property.

        Arguments:
            value (str):
        Returns:
            dict:
        """
        # See https://drafts.csswg.org/css-fonts-3/#font-prop
        # 'font' property
        # Value: [ [ <font-style> || <font-variant-css21>
        #  || <font-weight> || <font-stretch> ]? <font-size>
        #  [ / <line-height> ]? <font-family> ]
        #  | caption | icon | menu | message-box | small-caption | status-bar
        items = shlex.split(value)
        if len(items) == 0:
            return {}
        for item in iter(items):
            # system font
            if item in ['caption', 'icon', 'menu', 'message-box',
                        'small-caption', 'status-bar']:
                return {}

        style = dict({
            'font-family': [],
            'font-kerning': Font.CSS_DEFAULT_FONT_KERNING,
            'font-language-override': Font.CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE,
            'font-size': Font.CSS_DEFAULT_FONT_SIZE,
            'font-size-adjust': Font.CSS_DEFAULT_FONT_SIZE_ADJUST,
            'font-stretch': Font.CSS_DEFAULT_FONT_STRETCH,
            'font-style': Font.CSS_DEFAULT_FONT_STYLE,
            'font-variant': Font.CSS_DEFAULT_FONT_VARIANT,
            'font-weight': Font.CSS_DEFAULT_FONT_WEIGHT,
            'line-height': Font.CSS_DEFAULT_LINE_HEIGHT,
        })

        # 'font-family' property
        font_family = list([items.pop()])
        delimiter = False
        while len(items) > 0:
            item = items[-1]
            if item == ',':
                # 'a_,_b' -> ['a', ',', 'b']
                delimiter = True
            elif delimiter or item.endswith(','):
                font_family.insert(0, item)
                delimiter = False
            else:
                break
            items.pop()
        style['font-family'] = CSSUtils.parse_font_family(font_family)

        # 'font-size' and 'line-height' properties
        try:
            item = items.pop()
        except IndexError:
            return {}
        if item.find('/') != -1:
            # 'font-size' [/ 'line-height']
            parts = item.split('/')
            style['font-size'] = parts[0]
            style['line-height'] = parts[1]
        else:
            style['font-size'] = item

        while len(items) > 0:
            item = items[0]
            if item == 'normal':
                pass
            elif item in ['italic', 'oblique']:
                # 'font-style' property
                style['font-style'] = item
            elif item in ['small-caps']:
                # 'font-variant-css21' property
                style['font-variant'] = item
            elif item in ['bold', 'bolder', 'lighter', '100', '200', '300',
                          '400', '500', '600', '700', '800', '900']:
                # 'font-weight' property
                style['font-weight'] = item
            elif item in ['ultra-condensed', 'extra-condensed',
                          'condensed', 'semi-condensed', 'semi-expanded',
                          'expanded', 'extra-expanded', 'ultra-expanded']:
                # 'font-stretch' property
                style['font-stretch'] = item
            else:
                break
            items.pop(0)

        return style

    @staticmethod
    def parse_font_family(value):
        """Parses a value of the 'font-family' property.

        Arguments:
            value (str, list[str]):
        Returns:
            list[str]:
        """
        # See https://drafts.csswg.org/css-fonts-3/#font-family-prop
        # See https://drafts.csswg.org/css2/fonts.html#font-family-prop
        # 'font-family' property
        # Value: [[ <family-name> | <generic-family> ]
        #  [, [ <family-name>| <generic-family>] ]* ] | inherit
        # Initial: depends on user agent
        # Inherited: yes
        # Percentages: N/A
        if isinstance(value, list):
            items = value
        elif isinstance(value, str):
            if '"' in value or '\'' in value:
                items = shlex.split(value)
            else:
                items = [value]
        else:
            raise TypeError('Expected str or list, got {}'.format(
                type(value)))
        font_family = list()
        for item in iter(items):
            for name in iter(item.split(',')):
                name = name.strip()
                if len(name) > 0:
                    font_family.append(name)
        return font_family

    @staticmethod
    def parse_font_feature_settings(value):
        # 'font-feature-settings' property
        # Value: normal | <feature-tag-value>#
        # <feature-tag-value> = <string> [ <integer> | on | off ]?
        # Initial: normal
        # https://drafts.csswg.org/css-fonts-3/#propdef-font-feature-settings
        features = dict()
        if value == 'normal':
            return features
        tags = value.split(',')
        for tag_value in tags:
            items = tag_value.split()
            tag = items[0]
            if tag[0] == tag[-1] and tag[0] in '"\'':
                tag = tag[1:-1]
            if len(tag) != 4:
                continue  # invalid tag
            invalid_tag = False
            for ch in tag:
                if not (0x20 <= ord(ch) <= 0x7e):
                    invalid_tag = True
                    break
            if invalid_tag:
                continue
            if len(items) >= 2:
                if items[1].isdigit():
                    sw = int(items[1])
                elif items[1] == 'on':
                    sw = 1
                elif items[1] == 'off':
                    sw = 0
                else:
                    continue  # invalid value
            else:
                sw = 1
            features[tag] = sw

        return features

    @staticmethod
    def parse_font_variant(value):
        """Parses a value of the shorthand 'font-variant' property.

        Arguments:
            value (str):
        Returns:
            dict:
        """
        # 'font-variant' property
        # Value: normal | none
        #  | [ <common-lig-values> || <discretionary-lig-values>
        #  || <historical-lig-values> || <contextual-alt-values>
        #  || stylistic(<feature-value-name>) || historical-forms
        #  || styleset(<feature-value-name> #)
        #  || character-variant(<feature-value-name> #)
        #  || swash(<feature-value-name>) || ornaments(<feature-value-name>)
        #  || annotation(<feature-value-name>)
        #  || [ small-caps | all-small-caps | petite-caps | all-petite-caps
        #  | unicase | titling-caps ]
        #  || <numeric-figure-values> || <numeric-spacing-values>
        #  || <numeric-fraction-values> || ordinal || slashed-zero
        #  || <east-asian-variant-values> || <east-asian-width-values>
        #  || ruby || [ sub | super ] ]
        # https://drafts.csswg.org/css-fonts-3/#font-variant-prop
        # https://drafts.csswg.org/css-fonts-3/#propdef-font-variant
        # https://drafts.csswg.org/css-fonts-3/#font-rend-desc
        style = dict({
            'font-variant-alternates': None,
            'font-variant-caps': 'normal',
            'font-variant-east-asian': None,
            'font-variant-ligatures': None,
            'font-variant-numeric': None,
            'font-variant-position': 'normal',
        })
        if value == 'normal':
            style['font-variant-alternates'] = ['normal']
            style['font-variant-east-asian'] = ['normal']
            style['font-variant-ligatures'] = ['normal']
            style['font-variant-numeric'] = ['normal']
            return style
        elif value == 'none':
            style['font-variant-alternates'] = ['normal']
            style['font-variant-east-asian'] = ['normal']
            style['font-variant-ligatures'] = ['none']
            style['font-variant-numeric'] = ['normal']
            return style

        font_variant_alternates = list()
        font_variant_east_asian = list()
        font_variant_ligatures = list()
        font_variant_numeric = list()
        items = value.split()
        while len(items) > 0:
            item = items.pop(0)
            if item in ['common-ligatures', 'no-common-ligatures',
                        'discretionary-ligatures',
                        'no-discretionary-ligatures',
                        'historical-ligatures', 'no-historical-ligatures',
                        'contextual', 'no-contextual']:
                # https://drafts.csswg.org/css-fonts-3/#font-variant-ligatures-prop
                font_variant_ligatures.append(item)
            elif (item in ['historical-forms']
                  or item.startswith('stylistic(')
                  or item.startswith('styleset(')
                  or item.startswith('character-variant(')
                  or item.startswith('swash(')
                  or item.startswith('ornaments(')
                  or item.startswith('annotation(')):
                # https://drafts.csswg.org/css-fonts-3/#font-variant-alternates-prop
                font_variant_alternates.append(item)
            elif item in ['small-caps', 'all-small-caps', 'petite-caps',
                          'all-petite-caps', 'unicase', 'titling-caps']:
                # https://drafts.csswg.org/css-fonts-3/#font-variant-caps-prop
                style['font-variant-caps'] = item
            elif item in ['jis78', 'jis83', 'jis90', 'jis04', 'simplified',
                          'traditional',
                          'full-width', 'proportional-width', 'ruby']:
                # https://drafts.csswg.org/css-fonts-3/#font-variant-east-asian-prop
                font_variant_east_asian.append(item)
            elif item in ['lining-nums', 'oldstyle-nums',
                          'proportional-nums', 'tabular-nums',
                          'diagonal-fractions', 'stacked-fractions',
                          'ordinal', 'slashed-zero']:
                # https://drafts.csswg.org/css-fonts-3/#font-variant-numeric-prop
                font_variant_numeric.append(item)
            elif item in ['sub', 'super']:
                # https://drafts.csswg.org/css-fonts-3/#font-variant-position-prop
                style['font-variant-position'] = item

        if len(font_variant_alternates) == 0:
            font_variant_alternates.append('normal')
        style['font-variant-alternates'] = font_variant_alternates

        if len(font_variant_east_asian) == 0:
            font_variant_east_asian.append('normal')
        style['font-variant-east-asian'] = font_variant_east_asian

        if len(font_variant_ligatures) == 0:
            font_variant_ligatures.append('normal')
        style['font-variant-ligatures'] = font_variant_ligatures

        if len(font_variant_numeric) == 0:
            font_variant_numeric.append('normal')
        style['font-variant-numeric'] = font_variant_numeric

        return style


# See https://dom.spec.whatwg.org/#interface-node
# See https://www.w3.org/TR/2015/REC-dom-20151119/#interface-node
class Node(ABC):
    """Represents the DOM Node."""

    ELEMENT_NODE = 1
    COMMENT_NODE = 8

    @property
    @abstractmethod
    def node_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def node_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def node_value(self):
        raise NotImplementedError

    @node_value.setter
    @abstractmethod
    def node_value(self, text):
        raise NotImplementedError

    @property
    @abstractmethod
    def text_content(self):
        raise NotImplementedError

    @text_content.setter
    @abstractmethod
    def text_content(self, text):
        raise NotImplementedError


# See https://dom.spec.whatwg.org/#interface-element
# See https://www.w3.org/TR/2015/REC-dom-20151119/#interface-element
# Node > Element > SVGElement
class Element(etree.ElementBase, Node):
    """Represents the DOM Element."""

    SVG_NAMESPACE_URI = 'http://www.w3.org/2000/svg'
    XHTML_NAMESPACE_URI = 'http://www.w3.org/1999/xhtml'
    XLINK_NAMESPACE_URI = 'http://www.w3.org/1999/xlink'
    XML_NAMESPACE_URI = 'http://www.w3.org/XML/1998/namespace'

    XML_LANG = '{{{0}}}lang'.format(XML_NAMESPACE_URI)

    DESCRIPTIVE_ELEMENTS = ['desc', 'metadata', 'title']

    STRUCTURAL_ELEMENTS = ['defs', 'g', 'svg', 'symbol', 'use']

    STRUCTURALLY_EXTERNAL_ELEMENTS = \
        ['audio', 'foreignObject', 'iframe', 'image', 'script', 'use', 'video']

    CONTAINER_ELEMENTS = \
        ['a', 'clipPath', 'defs', 'g', 'marker', 'mask', 'pattern', 'svg',
         'switch', 'symbol', 'unknown']

    GRAPHICS_ELEMENTS = \
        ['audio', 'canvas', 'circle', 'ellipse', 'foreignObject', 'iframe',
         'image', 'line', 'mesh', 'path', 'polygon', 'polyline', 'rect',
         'text', 'textPath', 'tspan', 'video']

    GRAPHICS_REFERENCING_ELEMENTS = \
        ['audio', 'iframe', 'image', 'mesh', 'use', 'video']

    RENDERABLE_ELEMENTS = \
        ['a', 'audio', 'canvas', 'circle', 'ellipse', 'foreignObject', 'g',
         'iframe', 'image', 'line', 'mesh', 'path', 'polygon', 'polyline',
         'rect', 'svg', 'switch', 'text', 'textPath', 'tspan', 'unknown',
         'use', 'video']

    SHAPE_ELEMENTS = \
        ['circle', 'ellipse', 'line', 'mesh', 'path', 'polygon', 'polyline',
         'rect']

    TEXT_CONTENT_ELEMENTS = ['text', 'tspan']
    # TODO: add 'textPath' element to TEXT_CONTENT_ELEMENTS.

    TEXT_CONTENT_CHILD_ELEMENTS = ['textPath', 'tspan']

    TRANSFORMABLE_ELEMENTS = \
        ['a', 'defs', 'foreignObject', 'g', 'svg', 'switch',
         'use', ] + GRAPHICS_ELEMENTS
    # TODO: add 'clipPath' element to TRANSFORMABLE_ELEMENTS.

    RE_DIGIT_SEQUENCE_SPLITTER = re.compile(r'\s*,\s*|\s+')

    def _init(self):
        self._attributes = Attrib(self.attrib)

    @property
    def attributes(self):
        return self._attributes

    @property
    def class_name(self):
        return self.attributes.get('class')

    @class_name.setter
    def class_name(self, class_name):
        self.attributes.set('class', class_name)

    @property
    def id(self):
        return self.attributes.get('id')

    @id.setter
    def id(self, element_id):
        self.attributes.set('id', element_id)

    @property
    def local_name(self):
        """str: The local part of the qualified name of an element."""
        return self.qname.localname

    @property
    def namespace_uri(self):
        return self.nsmap.get(self.prefix)

    @property
    def node_name(self):
        return self.tag_name

    @property
    def node_type(self):
        return Node.ELEMENT_NODE

    @property
    def node_value(self):
        return None

    @node_value.setter
    def node_value(self, node_value):
        pass  # do nothing

    @property
    def qname(self):
        """lxml.etree.QName: The qualified XML name of an element."""
        qname = etree.QName(self)
        return qname

    @property
    def tag_name(self):
        prefix = self.prefix
        local_name = self.local_name
        if prefix is not None:
            return prefix + ':' + local_name
        return local_name

    @property
    def text_content(self):
        # See https://dom.spec.whatwg.org/#dom-node-textcontent
        local_name = self.local_name
        if local_name in Element.DESCRIPTIVE_ELEMENTS:
            return self.text
        elif local_name in Element.TEXT_CONTENT_ELEMENTS:
            chars = Element._get_text_content(self)
            return ''.join(chars)
        return None

    @text_content.setter
    def text_content(self, text):
        # TODO: implement Node.textContent.
        raise NotImplementedError

    @staticmethod
    def _get_text_content(element):
        # See https://dom.spec.whatwg.org/#dom-node-textcontent
        chars = list()
        if element.text is not None:
            chars.append(element.text)

        for child in iter(element):
            if child.node_type != Node.ELEMENT_NODE:
                continue
            local_name = child.local_name
            if local_name in Element.TEXT_CONTENT_ELEMENTS:
                contents = Element._get_text_content(child)
                chars.extend(contents)
                if (local_name in Element.TEXT_CONTENT_CHILD_ELEMENTS
                        and child.tail is not None):
                    chars.append(child.tail)
        return chars

    def get_computed_geometry(self):
        return {}  # override with a subclass

    def get_computed_style(self):
        """Gets the presentation attributes from ancestor elements."""
        style = self.get_inherited_style()

        # 'font-feature-settings' property
        style['font-feature-settings'] = CSSUtils.parse_font_feature_settings(
            style['font-feature-settings'])

        # 'font-size' property
        style['font-size'] = CSSUtils.compute_font_size(
            self,
            inherited_style=style)

        # 'font-size-adjust' property
        style['font-size-adjust'] = CSSUtils.compute_font_size_adjust(style)

        # 'font-synthesis' property
        # Value: none | [weight || style]
        items = style['font-synthesis'].split()
        items = [x for x in items if x in ['weight', 'style', 'none']]
        if 'none' in items and len(items) != 1:
            items = ['none']
        style['font-synthesis'] = items

        # 'font-weight' property
        style['font-weight'] = CSSUtils.compute_font_weight(
            self,
            inherited_style=style)

        # 'line-height' property
        style['line-height'] = CSSUtils.compute_line_height(self, style)

        # 'inline-size' property
        # Value: <length> | <percentage> | <number>
        # Initial: 0
        # Percentages: Refer to the width (for horizontal text) or height
        #  (for vertical text) of the current SVG viewport
        inline_size = style['inline-size']
        writing_mode = style['writing-mode']
        mode = SVGLength.DIRECTION_HORIZONTAL if writing_mode in [
            'horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb'
        ] else SVGLength.DIRECTION_VERTICAL
        style['inline-size'] = SVGLength(inline_size).value(direction=mode)

        # 'stroke-width' property
        # Value: <percentage> | <length>
        # Initial: 1
        # Percentages: refer to the size of the current SVG viewport
        stroke_width = style['stroke-width']
        style['stroke-width'] = SVGLength(
            stroke_width,
            context=self).value(direction=SVGLength.DIRECTION_OTHER)

        # 'tab-size' property
        # Value: <percentage> | <length>
        # Initial: 8
        # See https://drafts.csswg.org/css-text-3/#tab-size-property
        tab_size = style['tab-size']
        style['tab-size'] = SVGLength(
            tab_size,
            context=self).value(direction=SVGLength.DIRECTION_OTHER)

        # geometry properties
        geometry = self.get_computed_geometry()
        style.update(geometry)
        return style

    def get_inherited_style(self):
        def _update_font_prop(_value, _style, _inherited_style):
            _other = CSSUtils.parse_font(_value)
            for _key in _other:
                if _key not in _style:
                    _style[_key] = _other[_key]
                    if _key == 'font-variant':
                        _update_font_variant_prop(_other[_key],
                                                  _style,
                                                  _inherited_style)
            _inherited_style.pop('font-style', None)
            _inherited_style.pop('font-variant', None)
            _inherited_style.pop('font-weight', None)
            _inherited_style.pop('font-stretch', None)
            _inherited_style.pop('font-size', None)
            _inherited_style.pop('line-height', None)
            _inherited_style.pop('font-size-adjust', None)
            _inherited_style.pop('font-kerning', None)
            _inherited_style.pop('font-language-override', None)
            _inherited_style.pop('font-family', None)
            _inherited_style.pop('font', None)

        def _update_font_variant_prop(_value, _style, _inherited_style):
            _other = CSSUtils.parse_font_variant(_value)
            for _key in _other:
                if _key not in _style:
                    _style[_key] = _other[_key]
            _inherited_style.pop('font-variant-alternates', None)
            _inherited_style.pop('font-variant-caps', None)
            _inherited_style.pop('font-variant-east-asian', None)
            _inherited_style.pop('font-variant-ligatures', None)
            _inherited_style.pop('font-variant-numeric', None)
            _inherited_style.pop('font-variant-position', None)
            _inherited_style.pop('font-variant', None)

        # TODO: see CSS style sheet.
        # See https://svgwg.org/svg2-draft/propidx.html
        style = dict()
        non_inherited_props = \
            {'alignment-baseline': 'baseline',
             'baseline-shift': '0',
             'clip': 'auto',
             'clip-path': 'none',
             'display': 'inline',
             'dominant-baseline': 'auto',
             'filter': 'none',
             'flood-color': 'black',
             'flood-opacity': '1',
             'inline-size': '0',
             'lighting-color': 'white',
             'mask': 'no',
             'opacity': '1',
             'overflow': 'visible',
             'stop-color': 'black',
             'stop-opacity': '1',
             'text-decoration': 'none',
             'transform': 'none',
             'unicode-bidi': 'normal',
             'vector-effect': 'none',
             }
        attributes = self.attributes
        for key in iter(non_inherited_props.keys()):
            style.setdefault(key,
                             attributes.get(key, non_inherited_props[key]))

        inherited_props = \
            {'clip-rule': 'nonzero',
             'color': 'black',  # depends on user agent
             'color-interpolation': 'sRGB',
             'color-rendering': 'auto',
             'cursor': 'auto',
             'direction': 'ltr',
             'fill': 'black',
             'fill-opacity': '1',
             'fill-rule': 'nonzero',
             'font': None,
             'font-family': None,
             'font-feature-settings': 'normal',
             'font-kerning': Font.CSS_DEFAULT_FONT_KERNING,
             'font-language-override': Font.CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE,
             'font-size': Font.CSS_DEFAULT_FONT_SIZE,
             'font-size-adjust': Font.CSS_DEFAULT_FONT_SIZE_ADJUST,
             'font-stretch': Font.CSS_DEFAULT_FONT_STRETCH,
             'font-style': Font.CSS_DEFAULT_FONT_STYLE,
             'font-synthesis': 'weight style',
             'font-variant': Font.CSS_DEFAULT_FONT_VARIANT,
             'font-variant-alternates': ['normal'],
             'font-variant-caps': 'normal',
             'font-variant-east-asian': ['normal'],
             'font-variant-ligatures': ['normal'],
             'font-variant-numeric': ['normal'],
             'font-variant-position': 'normal',
             'font-weight': Font.CSS_DEFAULT_FONT_WEIGHT,
             # 'glyph-orientation-vertical': 'auto',  # deprecated
             'image-rendering': 'auto',
             'lang': None,
             'letter-spacing': 'normal',
             'line-height': Font.CSS_DEFAULT_LINE_HEIGHT,
             'marker': None,
             'marker-end': 'none',
             'marker-mid': 'none',
             'marker-start': 'none',
             'paint-order': 'normal',
             'pointer-events': 'visiblePainted',
             'shape-rendering': 'auto',
             'stroke': 'none',
             'stroke-dasharray': 'none',
             'stroke-dashoffset': '0',
             'stroke-linecap': 'butt',
             'stroke-linejoin': 'miter',
             'stroke-miterlimit': '4',
             'stroke-opacity': '1',
             'stroke-width': '1',
             'tab-size': '8',
             'text-anchor': 'start',
             'text-orientation': 'mixed',
             'text-rendering': 'auto',
             'visibility': 'visible',
             'white-space': 'normal',
             'word-spacing': 'normal',
             'writing-mode': 'horizontal-tb',
             Element.XML_LANG: None,
             }
        # 'color-interpolation-filters', 'font-feature-settings',
        # 'gradientTransform', 'glyph-orientation-horizontal',
        # 'isolation',
        # 'patternTransform',
        # 'solid-color', 'solid-opacity',
        # 'text-align', 'text-align-all', 'text-align-last',
        # 'text-decoration-color', 'text-decoration-line',
        # 'text-decoration-style', 'text-indent',
        # 'text-overflow',
        # 'transform', 'transform-box', 'transform-origin',
        # 'vertical-align',
        element = self
        while element is not None:
            attributes = element.attributes
            for key in iter(list(inherited_props.keys())):
                value = attributes.get(key)
                if value is not None and value not in ['inherit']:
                    if key == 'font':
                        # 'font' shorthand property
                        # See https://drafts.csswg.org/css-fonts-3/#font-prop
                        style[key] = value
                        _update_font_prop(value, style, inherited_props)
                    elif key == 'font-family':
                        # 'font-family' property
                        style[key] = CSSUtils.parse_font_family(value)
                        del inherited_props[key]
                    elif key == 'font-variant':
                        # 'font-variant' shorthand property
                        style[key] = value
                        _update_font_variant_prop(value, style,
                                                  inherited_props)
                    elif key == 'marker':
                        # TODO: parse the 'marker' shorthand property.
                        raise NotImplementedError
                    else:
                        if key in ['font-variant-alternates',
                                   'font-variant-east-asian',
                                   'font-variant-ligatures',
                                   'font-variant-numeric']:
                            style[key] = value.split()
                        else:
                            style[key] = value
                        inherited_props.pop(key, None)
            # 'display' property
            display = attributes.get('display')
            if display is not None and display == 'none':
                style['display'] = 'none'
            element = element.getparent()

        for key, value in iter(inherited_props.items()):
            if value is not None:
                style[key] = value

        font_family = style.get('font-family')
        if font_family is None:
            style['font-family'] = CSSUtils.parse_font_family(
                Font.default_font_family)

        return style

    def get_element_by_id(self, element_id, namespaces=None):
        """Finds the first matching sub-element, by id.

        Arguments:
            element_id (str): The id of the element.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            SVGElement: An element or None.
        """
        elements = self.xpath('//*[@id = $element_id]',
                              namespaces=namespaces,
                              element_id=element_id)
        return elements[0] if len(elements) > 0 else None

    def get_elements_by_class_name(self, class_names, namespaces=None):
        """Finds all matching sub-elements, by class names.

        Arguments:
            class_names (str): A list of class names that are separated by
                whitespace.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[SVGElement]: A list of elements.
        """
        names = class_names.split()
        pattern = [r're:test(@class, "(^| ){}($| )")'.format(x)
                   for x in names]
        # include itself
        expr = '//*[{}]'.format(' and '.join(pattern))
        if namespaces is None:
            namespaces = dict()
        namespaces['re'] = 'http://exslt.org/regular-expressions'
        return self.xpath(expr, namespaces=namespaces)

    def get_elements_by_local_name(self, local_name, namespaces=None):
        """Finds all matching sub-elements, by the local name.

        Arguments:
            local_name (str): The local name.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[SVGElement]: A list of elements.
        """
        return self.xpath('//*[local-name() = $local_name]',
                          namespaces=namespaces,
                          local_name=local_name)

    def get_elements_by_tag_name(self, tag, namespaces=None):
        # return self.findall(tag, namespaces)
        # include itself
        expr = '//*{}'.format('' if tag == '*' else '[name() = $tag_name]')
        return self.xpath(expr,
                          namespaces=namespaces,
                          tag_name=tag)

    def get_elements_by_tag_name_ns(self, namespace_uri, local_name):
        pattern = list()
        pattern.append('namespace-uri() = $namespace_uri')
        if local_name != '*':
            pattern.append('local-name() = $local_name')
        # include itself
        expr = '//*[{}]'.format(' and '.join(pattern))
        return self.xpath(expr,
                          namespace_uri=namespace_uri,
                          local_name=local_name)

    def iscontainer(self):
        """Returns True if this element is container element."""
        return self.local_name in Element.CONTAINER_ELEMENTS

    def isdisplay(self):
        style = self.get_inherited_style()
        return False if style['display'] == 'none' else True

    def isgraphics(self):
        """Returns True if this element is graphics element."""
        return self.local_name in Element.GRAPHICS_ELEMENTS

    def isrenderable(self):
        """Returns True if this element is renderable element."""
        return self.local_name in Element.RENDERABLE_ELEMENTS

    def isshape(self):
        """Returns True if this element is shape element."""
        return self.local_name in Element.SHAPE_ELEMENTS

    def istext(self):
        """Returns True if this element is text content element."""
        return self.local_name in Element.TEXT_CONTENT_ELEMENTS

    def istransformable(self):
        """Returns True if this element is transformable element."""
        return self.local_name in Element.TRANSFORMABLE_ELEMENTS

    def make_sub_element(self,
                         tag, index=None, attrib=None, nsmap=None, **_extra):
        """Creates a sub-element instance, and adds to the end of this element.
        See also SVGParser.make_element() and SVGParser.make_element_ns().

        Arguments:
            tag (str): A tag of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        element = self.makeelement(tag, attrib=attrib, nsmap=nsmap, **_extra)
        if index is None:
            self.append(element)
        else:
            self.insert(index, element)
        return element

    def make_sub_element_ns(self,
                            namespace_uri, local_name, index=None, attrib=None,
                            nsmap=None, **_extra):
        """Creates a sub-element instance with the specified namespace URI, 
        and adds to the end of this element.
        See also SVGParser.make_element() and SVGParser.make_element_ns().

        Arguments:
            namespace_uri (str, None): The namespace URI to associated with the
                element.
            local_name (str): A local name of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        Examples:
            >>> from svgpy import SVGParser
            >>> parser = SVGParser()
            >>> root = parser.make_element('svg', nsmap={'html': 'http://www.w3.org/1999/xhtml'})
            >>> video = root.make_sub_element_ns('http://www.w3.org/1999/xhtml', 'video')
            >>> print(root.tostring(pretty_print=True).decode())
            <svg xmlns:html="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/2000/svg">
              <html:video/>
            </svg>
        """
        if namespace_uri is None:
            tag = local_name
        else:
            tag = '{{{0}}}{1}'.format(namespace_uri, local_name)
        element = self.make_sub_element(tag, index, attrib, nsmap, **_extra)
        return element

    def tostring(self, **kwargs):
        """Serialize an element to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        """
        return etree.tostring(self, **kwargs)


class Font(object):
    CSS_DEFAULT_FONT_KERNING = 'auto'
    CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE = 'normal'
    CSS_DEFAULT_FONT_SIZE = 'medium'
    CSS_DEFAULT_FONT_SIZE_ADJUST = 'none'
    CSS_DEFAULT_FONT_STRETCH = 'normal'
    CSS_DEFAULT_FONT_STYLE = 'normal'
    CSS_DEFAULT_FONT_VARIANT = 'normal'
    CSS_DEFAULT_FONT_WEIGHT = 'normal'
    CSS_DEFAULT_LINE_HEIGHT = 'normal'

    WEIGHT_THIN = 100
    WEIGHT_EXTRA_LIGHT = 200
    WEIGHT_ULTRA_LIGHT = 200
    WEIGHT_LIGHT = 300
    WEIGHT_NORMAL = 400
    WEIGHT_MEDIUM = 500
    WEIGHT_DEMI_BOLD = 600
    WEIGHT_SEMI_BOLD = 600
    WEIGHT_BOLD = 700
    WEIGHT_EXTRA_BOLD = 800
    WEIGHT_ULTRA_BOLD = 800
    WEIGHT_BLACK = 900
    WEIGHT_HEAVY = 900

    default_font_family = 'sans-serif'
    default_font_size = 16
    default_font_weight = WEIGHT_NORMAL
    generic_font_family = [
        'serif', 'sans-serif', 'cursive', 'fantasy', 'monospace',
    ]

    def __init__(self, context):
        """Constructs a Font object.

        Arguments:
            context (SVGElement): An Element object.
        """
        self._context = context
        self._style = context.get_computed_style()
        self._face = FontManager.get_face(self._style, context.text_content)

    def __eq__(self, other):
        if not isinstance(other, Font):
            return NotImplemented
        style = self._style
        other_style = other._style
        return (style['font-family'] == other_style['font-family']
                and style['font-size'] == other_style['font-size']
                and style['font-size-adjust'] == other_style[
                    'font-size-adjust']
                and style['font-stretch'] == other_style['font-stretch']
                and style['font-style'] == other_style['font-style']
                and style['font-weight'] == other_style['font-weight'])

    def __repr__(self):
        return (
            "('family': '{}', 'ascent': {}, 'descent': {},"
            " 'cap_height': {}, 'ch_width': {}, 'height': {},"
            " 'ic_width': {}, 'line_height': {}, 'x_height': {})".format(
                self.family, self.ascent, self.descent,
                self.cap_height, self.ch_advance, self.height,
                self.ic_advance, self.line_height, self.x_height))

    @property
    def ascent(self):
        return self._face.ascender / 64

    @property
    def attributes(self):
        return self._style

    @property
    def cap_height(self):
        # See https://drafts.csswg.org/css-values/#cap
        # See https://drafts.csswg.org/css-values-4/#cap
        for ch in 'Hh':
            index = self._face.get_char_index(ch)
            if index != 0:
                self._face.load_char(ch, FreeType.FT_LOAD_NO_BITMAP)
                return self._face.glyph.metrics.vert_advance / 64
        return self._face.size.height / 64

    @property
    def ch_advance(self):
        """float: An advance measure of the '0' (ZERO, U+0030)."""
        # See https://drafts.csswg.org/css-values/#ch
        self._face.load_char('\u0030', FreeType.FT_LOAD_NO_BITMAP)
        writing_mode = self._style['writing-mode']
        if writing_mode in ['horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb']:
            # horizontal
            return self._face.glyph.metrics.hori_advance / 64
        else:
            # vertical
            text_orientation = self._style['text-orientation']
            if text_orientation in ['upright']:
                return 0  # 1em
            return self._face.glyph.metrics.vert_advance / 64

    @property
    def context(self):
        return self._context

    @property
    def descent(self):
        return self._face.descender / 64

    @property
    def face(self):
        """freetype.FTFace: A FreeType FTFace object."""
        return self._face

    @property
    def family(self):
        return self._face.family_name

    @property
    def height(self):
        return self._face.size.metrics.y_ppem

    @property
    def ic_advance(self):
        """float: An advance measure of the '水' (CJK water ideograph, U+6C34).
        """
        # See https://drafts.csswg.org/css-values/#ic
        index = self._face.get_char_index('\u6c34')
        if index == 0:
            return 0  # 1em
        self._face.load_glyph(index, FreeType.FT_LOAD_NO_BITMAP)
        writing_mode = self._style['writing-mode']
        if writing_mode in ['horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb']:
            # horizontal
            return self._face.glyph.metrics.hori_advance / 64
        else:
            # vertical
            text_orientation = self._style['text-orientation']
            if text_orientation in ['upright']:
                return 0  # 1em
            return self._face.glyph.metrics.vert_advance / 64

    @property
    def line_height(self):
        # See https://drafts.csswg.org/css2/visudet.html#propdef-line-height
        return self._face.size.metrics.height / 64

    @property
    def x_height(self):
        # See https://drafts.csswg.org/css-values/#ex
        self._face.load_char('x', FreeType.FT_LOAD_NO_BITMAP)
        return self._face.glyph.metrics.height / 64

    def set_point_size(self,
                       width, height,
                       hori_resolution=0, vert_resolution=0):
        self._face.request_size(FreeType.FT_SIZE_REQUEST_TYPE_NOMINAL,
                                width, height,
                                hori_resolution, vert_resolution)


class FontManager(object):
    @staticmethod
    def __debug_print(matched):
        # for style in matched:
        #     print(style)
        # print('----')
        pass

    @staticmethod
    def _find_face(style, text=None):
        font_family_names = list()
        for font_family_name in iter(style['font-family']):
            name = FontManager.match(font_family_name)
            if name is not None and name not in font_family_names:
                font_family_names.append(name)
        font_stretch = style['font-stretch']
        fc_width = FontConfig.FC_WIDTH_MAP.get(font_stretch)
        font_style = style['font-style']
        font_weight = style['font-weight']
        font_size = style['font-size']
        # font_size_adjust = style['font-size-adjust']

        for font_family_name in iter(font_family_names):
            # narrow down by font family name
            matched = FontManager.list(font_family_name)
            if len(matched) == 0:
                continue
            FontManager.__debug_print(matched)

            # narrow down by 'font-stretch' property (fontconfig width)
            # font-stretch : normal | ultra-condensed
            #  | extra-condensed | condensed | semi-condensed | semi-expanded
            #  | expanded | extra-expanded | ultra-expanded
            group = [x for x in iter(matched) if
                     fc_width == x[FontConfig.FC_WIDTH]]
            if len(group) == 0 and fc_width is not None:
                # narrow down by nearest font width
                fc_width_table = set(
                    [x[FontConfig.FC_WIDTH] for x in iter(matched)])
                if (font_stretch == 'normal'
                        or font_stretch.endswith('condensed')):
                    # 'normal' or '*condensed'
                    fc_width_table = sorted(fc_width_table)
                elif font_stretch.endswith('expanded'):
                    # '*expanded'
                    fc_width_table = sorted(fc_width_table, reverse=True)
                index = np.abs(
                    np.asarray(fc_width_table) - fc_width).argmin()
                group = [x for x in iter(matched) if
                         fc_width_table[index] == x[FontConfig.FC_WIDTH]]
            if len(group) == 0:
                continue
            else:
                matched = group
                FontManager.__debug_print(matched)

            # narrow down by 'font-style' property (fontconfig slant)
            # font-style: normal | italic | oblique
            if font_style == 'italic':
                order = ['italic', 'oblique', 'normal']
            elif font_style == 'oblique':
                order = ['oblique', 'italic', 'normal']
            else:
                order = ['normal', 'oblique', 'italic']
            for include_style in iter(order):
                fc_slant = FontConfig.FC_SLANT_MAP.get(include_style)
                group = [x for x in iter(matched) if
                         fc_slant == x[FontConfig.FC_SLANT]]
                if len(group) > 0:
                    matched = group
                    break
            FontManager.__debug_print(matched)

            # narrow down by 'font-weight' property
            # font-weight : normal | bold | bolder | lighter
            #  | 100 | 200 | 300 | 400 | 500 | 600 | 700 | 800 | 900
            group = [x for x in iter(matched) if
                     font_weight == x[FontConfig.FC_WEIGHT]]
            if len(group) == 0:
                # FIXME: narrow down by nearest font weight.
                fc_weight_table = set(
                    [x[FontConfig.FC_WEIGHT] for x in iter(matched)])
                if font_weight < Font.WEIGHT_NORMAL:  # <400
                    fc_weight_table = sorted(fc_weight_table, reverse=True)
                else:  # >=400
                    fc_weight_table = sorted(fc_weight_table)
                index = np.abs(
                    np.asarray(fc_weight_table) - font_weight).argmin()
                group = [x for x in iter(matched) if
                         fc_weight_table[index] == x[
                             FontConfig.FC_WEIGHT]]
            if len(group) == 0:
                continue
            else:
                matched = group
            FontManager.__debug_print(matched)

            # narrow down by 'font-size' property (fontconfig pixelsize)
            group = [x for x in iter(matched) if
                     font_size == x[FontConfig.FC_PIXEL_SIZE]]
            if len(group) == 0:
                pixel_size_table = sorted(set(
                    [x[FontConfig.FC_PIXEL_SIZE] for x in iter(matched)]
                ))
                index = np.abs(
                    np.asarray(pixel_size_table) - font_size).argmin()
                group = [x for x in iter(matched) if
                         pixel_size_table[index] == x[
                             FontConfig.FC_PIXEL_SIZE]]
            if len(group) == 0:
                continue
            else:
                matched = group
            if len(matched) > 1:
                # FIXME: narrow down to a single font face.
                # (e.g. 'Courier' / Windows)
                matched = sorted(matched,
                                 key=lambda x: x[FontConfig.FC_FILE])
            FontManager.__debug_print(matched)

            # check the glyph
            for fc in iter(matched):
                face = FTFace.new_face(fc[FontConfig.FC_FILE],
                                       fc[FontConfig.FC_INDEX])
                glyph_not_found = False
                if text is not None:
                    for ch in iter(text):
                        if ch in ['\t', '\r', '\n', '\x20']:
                            continue
                        index = face.get_char_index(ch)
                        if index == 0:
                            glyph_not_found = True
                            break
                        # for encoding in [FreeType.FT_ENCODING_MS_SYMBOL,
                        #                  FreeType.FT_ENCODING_ADOBE_CUSTOM,
                        #                  FreeType.FT_ENCODING_UNICODE]:
                        #     index = face.get_char_index(ch)
                        #     if index == 0:
                        #         face.select_charmap(encoding)
                        #     else:
                        #         if face.charmap.encoding \
                        #                 != FreeType.FT_ENCODING_UNICODE:
                        #             face.select_charmap(
                        #                 FreeType.FT_ENCODING_UNICODE)
                        #         break
                        # else:
                        #     glyph_not_found = True
                        # if glyph_not_found:
                        #     break
                if not glyph_not_found:
                    return face

        # fallback font
        filename = FontConfig.match(Font.default_font_family, '%{file}')[0]
        face = FTFace.new_face(filename)
        return face

    @staticmethod
    def get_face(style, text=None):
        face = FontManager._find_face(style, text)
        face.select_charmap(FreeType.FT_ENCODING_UNICODE)
        pixel_size = style['font-size']
        point_size = int(SVGLength(pixel_size).value(SVGLength.TYPE_PT) * 64)
        dpi = int(SVGLength.dpi)
        face.request_size(FreeType.FT_SIZE_REQUEST_TYPE_NOMINAL,
                          0, point_size, dpi, dpi)
        return face

    @staticmethod
    def list(family):
        fc_elements = [FontConfig.FC_FAMILY, FontConfig.FC_FILE,
                       FontConfig.FC_FONT_FORMAT, FontConfig.FC_INDEX,
                       FontConfig.FC_PIXEL_SIZE, FontConfig.FC_SLANT,
                       FontConfig.FC_WEIGHT, FontConfig.FC_WIDTH]
        fc_format = '\t'.join(['%{{{}}}'.format(x) for x in fc_elements])
        matched = FontConfig.list(family, fc_elements, fc_format)
        style_sequence = list()
        for line in iter(matched):
            items = line.split('\t')
            style = dict()
            style[FontConfig.FC_FAMILY] = items[0]
            style[FontConfig.FC_FILE] = items[1]
            style[FontConfig.FC_FONT_FORMAT] = items[2]
            style[FontConfig.FC_INDEX] = int(items[3])
            pixel_size = float(items[4]) if len(items[4]) > 0 else 0
            style[FontConfig.FC_PIXEL_SIZE] = pixel_size
            style[FontConfig.FC_SLANT] = int(items[5])
            style[FontConfig.FC_WEIGHT] = FontConfig.weight_to_open_type(
                int(items[6]))
            style[FontConfig.FC_WIDTH] = int(items[7])
            style_sequence.append(style)
        return style_sequence

    @staticmethod
    def match(family):
        matched = FontConfig.match(family, '%{family[0]}')
        if len(matched) == 0:
            return None
        return matched[0]


class LengthProperty(property):
    pass


class _LengthMeta(type):
    def __new__(mcs, *args, **kwargs):
        attrib = args[2]
        d = [(key, value) for key, value in iter(attrib.items()) if
             type(value) == LengthProperty]
        for key, value in iter(d):
            setattr(mcs, key, value)
            del attrib[key]
        return super().__new__(mcs, *args, **kwargs)


# See https://svgwg.org/svg2-draft/types.html#InterfaceSVGLength
class SVGLength(object, metaclass=_LengthMeta):
    # See https://drafts.csswg.org/css-values-3/#lengths
    TYPE_NUMBER = ''  # pixel
    TYPE_PERCENTAGE = '%'
    TYPE_EMS = 'em'
    TYPE_EXS = 'ex'
    TYPE_PX = 'px'
    TYPE_CM = 'cm'
    TYPE_MM = 'mm'
    TYPE_IN = 'in'
    TYPE_PT = 'pt'
    TYPE_PC = 'pc'
    TYPE_Q = 'Q'
    TYPE_CAPS = 'cap'
    TYPE_CHS = 'ch'
    TYPE_ICS = 'ic'
    TYPE_REMS = 'rem'
    TYPE_VW = 'vw'
    TYPE_VH = 'vh'
    TYPE_VMIN = 'vmin'
    TYPE_VMAX = 'vmax'

    DIRECTION_HORIZONTAL = 0
    DIRECTION_VERTICAL = 1
    DIRECTION_OTHER = 2

    RE_LENGTH = re.compile(
        r"(?P<number>[+-]?"
        r"((\d+(\.\d*)?([Ee][+-]?\d+)?)|(\d*\.\d+([Ee][+-]?\d+)?)))"
        r"(?P<unit>%|em|ex|px|cm|mm|in|pt|pc|Q|cap|ch|ic|rem|vw|vh|vmin|vmax)?"
    )

    rel_tol = 1e-9

    abs_tol = 1e-9

    _dpi = Decimal(96)

    # 1in = 2.54cm = 96px
    # 1cm = 1in/2.54 = 96px/2.54
    # 1mm = 1cm/10
    # 1q = 1cm/40
    # 1pt = 1in/72
    # 1pc = 1in/6
    _TO_PIXEL_SIZE_MAP = {
        TYPE_PX: 1.0,
        TYPE_IN: _dpi,
        TYPE_CM: _dpi / Decimal(2.54),
        TYPE_MM: _dpi / Decimal(25.4),
        TYPE_Q: _dpi / Decimal(2.54) / Decimal(40),
        TYPE_PT: _dpi / Decimal(72),
        TYPE_PC: _dpi / Decimal(6),
    }

    def __init__(self, value=None, unit=None, context=None, direction=None):
        """Constructs a SVGLength object.

        Arguments:
            value (str, float, optional): A number or a number with unit.
            unit (str, optional): The unit string.
            context (SVGElement, optional): The referencing element.
            direction (int, optional): The direction of this length value.
        Examples:
            >>> n = SVGLength()
            >>> n.tostring(), n.value(), n.unit
            ('0', 0, None)
            >>> n = SVGLength(math.pi)
            >>> n.tostring(), n.value(), n.unit
            ('3.141593', 3.141592653589793, None)
            >>> SVGLength.dpi
            Decimal('96')
            >>> n = SVGLength('1.0in')
            >>> n.tostring(), n.value(), n.unit
            ('1in', 96.0, 'in')
            >>> n.tostring(SVGLength.TYPE_MM), n.value(SVGLength.TYPE_MM)
            ('25.4mm', 25.4)
            >>> n = SVGLength('18.0pt')
            >>> n.tostring(), n.value(), n.unit
            ('18pt', 24.0, 'pt')  # 18(pt) * 4 / 3 = 24(px)
            >>> n /= 2
            >>> n.tostring(), n.value(), n.unit
            ('9pt', 12.0, 'pt')
        """
        if (context is not None
                and not isinstance(context, Element)):
            raise TypeError('Expected Element, got {}'.format(
                type(context)))
        self._context = context
        self._direction = direction
        if value is not None and unit is not None:
            self.new_value(value, unit)
        else:
            self._number, self._unit = SVGLength.parse(value)

    def __abs__(self):
        x = copy.deepcopy(self)
        x._number = abs(x._number)
        return x

    def __add__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        x = copy.deepcopy(self)
        if x._unit is None and other.unit is not None:
            x.convert(other.unit)
        x._number += Decimal(other.value(x._unit))
        return x

    def __eq__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        return math.isclose(self._number, o,
                            rel_tol=SVGLength.rel_tol,
                            abs_tol=SVGLength.abs_tol)

    def __ge__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return True
        return self._number >= o

    def __gt__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return False
        return self._number > o

    def __iadd__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        if self._unit is None and other.unit is not None:
            self.convert(other.unit)
        self._number += Decimal(other.value(self._unit))
        return self

    def __imul__(self, other):
        if isinstance(other, SVGLength):
            if self._unit is None and other.unit is not None:
                self.convert(other.unit)
            self._number *= Decimal(other.value(self._unit))
        elif isinstance(other, (int, float)):
            self._number *= Decimal(other)
        else:
            return NotImplemented
        return self

    def __isub__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        if self._unit is None and other.unit is not None:
            self.convert(other.unit)
        self._number -= Decimal(other.value(self._unit))
        return self

    def __itruediv__(self, other):
        if isinstance(other, SVGLength):
            if self._unit is None and other.unit is not None:
                self.convert(other.unit)
            self._number /= Decimal(other.value(self._unit))
        elif isinstance(other, (int, float)):
            self._number /= Decimal(other)
        else:
            return NotImplemented
        return self

    def __le__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return True
        return self._number <= o

    def __lt__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        o = Decimal(other.value(self._unit))
        if math.isclose(self._number, o,
                        rel_tol=SVGLength.rel_tol, abs_tol=SVGLength.abs_tol):
            return False
        return self._number < o

    def __mul__(self, other):
        x = copy.deepcopy(self)
        if isinstance(other, SVGLength):
            if x._unit is None and other.unit is not None:
                x.convert(other.unit)
            x._number *= Decimal(other.value(x._unit))
        elif isinstance(other, (int, float)):
            x._number *= Decimal(other)
        else:
            return NotImplemented
        return x

    def __neg__(self):
        x = copy.deepcopy(self)
        x._number = -x._number
        return x

    def __pos__(self):
        x = copy.deepcopy(self)
        return x

    def __pow__(self, power, modulo=None):
        x = copy.deepcopy(self)
        x._number = pow(x._number, power, modulo)
        return x

    def __repr__(self):
        return '<{}.{} object at {} ({:g} {})>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._number, self._unit)

    def __rmul__(self, other):
        return self.__mul__(other)

    def __str__(self):
        return '{:g}{}'.format(self._number,
                               self._unit if self._unit is not None else '')

    def __sub__(self, other):
        if not isinstance(other, SVGLength):
            return NotImplemented
        x = copy.deepcopy(self)
        if x._unit is None and other.unit is not None:
            x.convert(other.unit)
        x._number -= Decimal(other.value(x._unit))
        return x

    def __truediv__(self, other):
        x = copy.deepcopy(self)
        if isinstance(other, SVGLength):
            if x._unit is None and other.unit is not None:
                x.convert(other.unit)
            x._number /= Decimal(other.value(x._unit))
        elif isinstance(other, (int, float)):
            x._number /= Decimal(other)
        else:
            return NotImplemented
        return x

    @property
    def context(self):
        return self._context

    @LengthProperty
    def dpi(cls):
        """Decimal: The DPI value.

        Examples:
            >>> SVGLength.dpi
            Decimal('96')
            >>> n = SVGLength('1in')
            >>> n.tostring(SVGLength.TYPE_PX)
            '96px'
            >>> SVGLength.dpi = 300
            >>> SVGLength.dpi
            Decimal('300')
            >>> n.tostring(SVGLength.TYPE_PX)
            '300px'
            >>> n.tostring()
            '1in'
        """
        return cls._dpi

    @dpi.setter
    def dpi(cls, dpi):
        cls._dpi = Decimal(dpi)
        # 1in = 2.54cm = <dpi>
        # 1cm = 1in/2.54 = <dpi>/2.54
        # 1mm = 1cm/10
        # 1Q = 1cm/40
        # 1pt = 1in/72 = 4/3px
        # 1pc = 1in/6
        cls._TO_PIXEL_SIZE_MAP.update({
            cls.TYPE_IN: cls._dpi,
            cls.TYPE_CM: cls._dpi / Decimal(2.54),
            cls.TYPE_MM: cls._dpi / Decimal(25.4),
            cls.TYPE_Q: cls._dpi / Decimal(2.54) / Decimal(40),
            cls.TYPE_PT: cls._dpi / Decimal(72),
            cls.TYPE_PC: cls._dpi / Decimal(6),
        })

    @property
    def unit(self):
        """str: The unit string."""
        return self._unit if self._unit != SVGLength.TYPE_NUMBER else None

    def convert(self, unit):
        """Resets the stored unit.

        Arguments:
            unit (str): The unit string.
        """
        if unit == self._unit:
            return
        self._number = Decimal(self.value(unit))
        self._unit = unit

    def isabsolute(self):
        return self._unit in [
            None, SVGLength.TYPE_CM, SVGLength.TYPE_MM, SVGLength.TYPE_Q,
            SVGLength.TYPE_IN, SVGLength.TYPE_PT, SVGLength.TYPE_PC,
            SVGLength.TYPE_PX, SVGLength.TYPE_NUMBER]

    def isrelative(self):
        return self._unit in [
            SVGLength.TYPE_EMS, SVGLength.TYPE_EXS, SVGLength.TYPE_CHS,
            SVGLength.TYPE_ICS, SVGLength.TYPE_REMS,
            SVGLength.TYPE_PERCENTAGE,
            SVGLength.TYPE_VW, SVGLength.TYPE_VH,
            SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX]

    def new_value(self, number, unit):
        """Resets the value as a number with the unit.

        Arguments:
            number (float): The new value.
            unit (str): The unit string.
        """
        self._number = Decimal(number)
        self._unit = unit

    @staticmethod
    def parse(text):
        if text is None:
            return Decimal(0), None
        elif isinstance(text, str):
            match = SVGLength.RE_LENGTH.match(text.strip())
            if match is None:
                raise ValueError('Expected Number, got \'{}\''.format(text))
            return Decimal(match.group('number')), match.group('unit')
        return Decimal(text), None

    def tostring(self, unit=None, direction=None):
        """Returns a string with the unit, formatted according to the specified
        precision.

        Arguments:
            unit (str, optional): The unit string.
            direction (int, optional): The direction of this length value.
        Returns:
            str: The value in specified unit.
        Examples:
            >>> n = SVGLength('10cm')
            >>> n.tostring()
            '10cm'
            >>> n.tostring(SVGLength.TYPE_MM)
            '100mm'
            >>> from svgpy import formatter
            >>> formatter.precision
            6  # default precision for a floating point value
            >>> n /= 3
            >>> n.tostring()
            '3.333333cm'
            >>> formatter.precision = 3
            >>> n.tostring()
            '3.333cm'
        """
        if unit is None:
            unit = self._unit
        number = self.value(unit, direction=direction)
        value = format_number_sequence([number])[0]
        return '{0}{1}'.format(value, unit if unit is not None else '')

    def value(self, unit=None, direction=None):
        """Returns the value in specified unit, or in pixels if the unit is
        None or SVGLength.TYPE_NUMBER.

        Arguments:
            unit (str, optional): The unit string.
            direction (int, optional): The direction of this length value.
        Returns:
            float: The value in specified unit.
        Examples:
            >>> SVGLength.dpi = 72
            >>> SVGLength.dpi
            Decimal('72')
            >>> n = SVGLength('1in')
            >>> n.value(SVGLength.TYPE_IN)
            1.0  # 1.0(in)
            >>> n.value(SVGLength.TYPE_CM)
            2.54  # 2.54(cm)
            >>> n.value(SVGLength.TYPE_PX)
            72.0  # 72.0(px)
        """
        # See https://drafts.csswg.org/css-values/#lengths
        if unit == self._unit:
            return float(self._number)
        if direction is None:
            direction = self._direction
        element_font_size = None
        root_font_size = None
        vw = None
        vh = None
        vmin = None
        vmax = None
        font = None
        if self._unit == SVGLength.TYPE_REMS or unit == SVGLength.TYPE_REMS:
            # <font-relative lengths>: rem
            if self._context is None:
                root_font_size = Decimal(Font.default_font_size)
            else:
                root = self._context.getroottree().getroot()
                root_font_size = Decimal(CSSUtils.compute_font_size(root))

        if (self._unit in [SVGLength.TYPE_EMS, SVGLength.TYPE_PERCENTAGE,
                           SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                           SVGLength.TYPE_CHS,
                           SVGLength.TYPE_ICS]
                or unit in [SVGLength.TYPE_EMS, SVGLength.TYPE_PERCENTAGE,
                            SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                            SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]):
            # <font-relative lengths>: em
            # <font-percentage lengths>: %
            # falls back for 'ex' | 'cap' | 'ch' | 'ic' units
            if self._context is None:
                element_font_size = Decimal(Font.default_font_size)
            else:
                context = self._context.getparent()
                if context is None:
                    element_font_size = Decimal(Font.default_font_size)
                else:
                    element_font_size = Decimal(
                        CSSUtils.compute_font_size(context))

        if (self._unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                           SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX,
                           SVGLength.TYPE_PERCENTAGE]
                or unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                            SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX,
                            SVGLength.TYPE_PERCENTAGE]):
            # <viewport-percentage lengths>: % | vw | vh | vmin | vmax
            if self._context is None:
                vw = 100
                vh = 100
            else:
                view_box = self._context.get_view_box()
                if view_box is not None:
                    _, _, vbw, vbh, _ = view_box
                    vw = vbw.value()
                    vh = vbh.value()
                else:
                    _, _, vpw, vph = self._context.get_viewport_size()
                    vw = vpw.value()
                    vh = vph.value()
            vmin = min(vw, vh)
            vmax = max(vw, vh)

        if (self._unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                           SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]
                or unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                            SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]):
            # <font-relative lengths>: ex | cap | ch | ic
            if self._context is not None:
                font = Font(self._context)

        # convert to pixels
        if self._unit in [None, SVGLength.TYPE_NUMBER, SVGLength.TYPE_PX]:
            # pixels
            px = self._number
        elif self._unit == SVGLength.TYPE_REMS:
            # <font-relative lengths> 'rem' unit to pixels
            px = self._number * root_font_size
        elif self._unit in [SVGLength.TYPE_EMS]:
            # <font-relative lengths> 'em' unit to pixels
            px = self._number * element_font_size
        elif self._unit in [SVGLength.TYPE_PERCENTAGE]:
            # <viewport-percentage lengths> | <font-percentage lengths>:
            # percentage units to pixels
            if direction == SVGLength.DIRECTION_HORIZONTAL:
                px = self._number * Decimal(vw) / 100
            elif direction == SVGLength.DIRECTION_VERTICAL:
                px = self._number * Decimal(vh) / 100
            elif direction == SVGLength.DIRECTION_OTHER:
                k = math.sqrt(vw ** 2 + vh ** 2) / math.sqrt(2)
                px = self._number * Decimal(k) / 100
            else:
                px = self._number * element_font_size / 100
        elif self._unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                            SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]:
            # <font-relative lengths> 'ex' | 'cap' | 'ch' | 'ic' units to pixels
            if font is None:
                px = self._number * element_font_size / 2
            else:
                if self._unit == SVGLength.TYPE_EXS:
                    k = font.x_height
                elif self._unit == SVGLength.TYPE_CAPS:
                    k = font.cap_height
                elif self._unit == SVGLength.TYPE_CHS:
                    k = font.ch_advance
                elif self._unit == SVGLength.TYPE_ICS:
                    k = font.ic_advance
                else:
                    assert False
                val = Decimal(k)
                if val == 0:
                    val = element_font_size
                px = self._number * val
        elif self._unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                            SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX]:
            # <viewport-percentage lengths> 'vw' | 'vh' | 'vmin' | 'vmax' units
            # to pixels
            if self._unit == SVGLength.TYPE_VW:
                k = vw
            elif self._unit == SVGLength.TYPE_VH:
                k = vh
            elif self._unit == SVGLength.TYPE_VMIN:
                k = vmin
            elif self._unit == SVGLength.TYPE_VMAX:
                k = vmax
            else:
                assert False
            px = self._number * Decimal(k) / 100
        else:
            # <absolute lengths> units to pixels
            k = SVGLength._TO_PIXEL_SIZE_MAP.get(self._unit)
            if k is None:
                raise NotImplementedError(self._unit)
            px = self._number * k

        # convert to specified units
        if unit in [None, SVGLength.TYPE_NUMBER, SVGLength.TYPE_PX]:
            # to pixels
            return float(px)
        elif unit == SVGLength.TYPE_REMS:
            # to 'rem' unit
            px /= root_font_size
            return float(px)
        elif unit in [SVGLength.TYPE_EMS]:
            # to <font-relative lengths> 'em' unit
            px /= element_font_size
            return float(px)
        elif unit in [SVGLength.TYPE_PERCENTAGE]:
            # to <viewport-percentage lengths> | <font-percentage lengths>
            if direction == SVGLength.DIRECTION_HORIZONTAL:
                px /= Decimal(vw)
            elif direction == SVGLength.DIRECTION_VERTICAL:
                px /= Decimal(vh)
            elif direction == SVGLength.DIRECTION_OTHER:
                k = math.sqrt(vw ** 2 + vh ** 2) / math.sqrt(2)
                px /= Decimal(k)
            else:
                px /= element_font_size
            return float(px * 100)
        elif unit in [SVGLength.TYPE_EXS, SVGLength.TYPE_CAPS,
                      SVGLength.TYPE_CHS, SVGLength.TYPE_ICS]:
            # to <font-relative lengths> 'ex' | 'cap' | 'ch' | 'ic' units
            if font is None:
                px /= element_font_size / 2
            else:
                pt = int(px / SVGLength._TO_PIXEL_SIZE_MAP[SVGLength.TYPE_PT]
                         * 64)
                dpi = int(SVGLength.dpi)
                font.set_point_size(0, pt, dpi, dpi)
                if unit == SVGLength.TYPE_EXS:
                    k = font.x_height
                elif unit == SVGLength.TYPE_CAPS:
                    k = font.cap_height
                elif unit == SVGLength.TYPE_CHS:
                    k = font.ch_advance
                elif unit == SVGLength.TYPE_ICS:
                    k = font.ic_advance
                else:
                    assert False
                val = Decimal(k)
                if val == 0:
                    val = element_font_size
                px /= val
            return float(px)
        elif unit in [SVGLength.TYPE_VW, SVGLength.TYPE_VH,
                      SVGLength.TYPE_VMIN, SVGLength.TYPE_VMAX]:
            # to <viewport-percentage lengths>
            # 'vw' | 'vh' | 'vmin' | 'vmax' units
            if unit == SVGLength.TYPE_VW:
                k = vw
            elif unit == SVGLength.TYPE_VH:
                k = vh
            elif unit == SVGLength.TYPE_VMIN:
                k = vmin
            elif unit == SVGLength.TYPE_VMAX:
                k = vmax
            else:
                assert False
            return float(px / Decimal(k) * 100)

        # to <absolute lengths> units
        k = SVGLength._TO_PIXEL_SIZE_MAP.get(unit)
        if k is None:
            raise NotImplementedError(unit)
        return float(px / k)


# See https://drafts.fxtf.org/geometry/#DOMMatrix
class Matrix(object):
    # FIXME: implement the DOMMatrix?
    """Represents a 3x3 matrix."""

    def __init__(self, *values):
        self._matrix = None
        if len(values) > 0:
            self.set_matrix(*values)
        else:
            self.set_matrix(1, 0, 0, 1, 0, 0)

    def __deepcopy__(self, memodict={}):
        x = Matrix()
        if self._matrix is not None:
            x._matrix = np.matrix.copy(self._matrix)
        return x

    def __eq__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        return (self._matrix == other.matrix).all()

    def __imul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        self.multiply_self(other)
        return self

    def __mul__(self, other):
        if not isinstance(other, Matrix):
            return NotImplemented
        x = copy.deepcopy(self)
        x.multiply_self(other)
        return x

    def __repr__(self):
        return '<{}.{} object at {} {}>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._matrix.tolist())

    @property
    def a(self):
        """float: The a component of the matrix."""
        return self._matrix[0, 0]

    @a.setter
    def a(self, value):
        self._matrix[0, 0] = float(value)

    @property
    def b(self):
        """float: The b component of the matrix."""
        return self._matrix[1, 0]

    @b.setter
    def b(self, value):
        self._matrix[1, 0] = float(value)

    @property
    def c(self):
        """float: The c component of the matrix."""
        return self._matrix[0, 1]

    @c.setter
    def c(self, value):
        self._matrix[0, 1] = float(value)

    @property
    def d(self):
        """float: The d component of the matrix."""
        return self._matrix[1, 1]

    @d.setter
    def d(self, value):
        self._matrix[1, 1] = float(value)

    @property
    def e(self):
        """float: The e component of the matrix."""
        return self._matrix[0, 2]

    @e.setter
    def e(self, value):
        self._matrix[0, 2] = float(value)

    @property
    def f(self):
        """float: The f component of the matrix."""
        return self._matrix[1, 2]

    @f.setter
    def f(self, value):
        self._matrix[1, 2] = float(value)

    @property
    def m11(self):
        """float: The m11 component of the matrix."""
        return self._matrix[0, 0]

    @m11.setter
    def m11(self, value):
        self._matrix[0, 0] = float(value)

    @property
    def m12(self):
        """float: The m12 component of the matrix."""
        return self._matrix[1, 0]

    @m12.setter
    def m12(self, value):
        self._matrix[1, 0] = float(value)

    @property
    def m21(self):
        """float: The m21 component of the matrix."""
        return self._matrix[0, 1]

    @m21.setter
    def m21(self, value):
        self._matrix[0, 1] = float(value)

    @property
    def m22(self):
        """float: The m22 component of the matrix."""
        return self._matrix[1, 1]

    @m22.setter
    def m22(self, value):
        self._matrix[1, 1] = float(value)

    @property
    def m41(self):
        """float: The m41 component of the matrix."""
        return self._matrix[0, 2]

    @m41.setter
    def m41(self, value):
        self._matrix[0, 2] = float(value)

    @property
    def m42(self):
        """float: The m42 component of the matrix."""
        return self._matrix[1, 2]

    @m42.setter
    def m42(self, value):
        self._matrix[1, 2] = float(value)

    @property
    def matrix(self):
        """numpy.matrix: The current matrix."""
        return self._matrix

    def clear(self):
        """Sets the matrix [1 0 0 1 0 0].

        Returns:
            Matrix: Returns itself.
        """
        self.set_matrix(1, 0, 0, 1, 0, 0)
        return self

    def flipx(self):
        """Post-multiplies the transformation [-1 0 0 1 0 0] on the current
        matrix and returns the resulting matrix.
        The current matrix is not modified.

        Returns:
            Matrix: The resulting matrix.
        """
        x = self * Matrix(-1, 0, 0, 1, 0, 0)
        return x

    def flipy(self):
        """Post-multiplies the transformation [1 0 0 -1 0 0] on the current
        matrix.
        The current matrix is not modified.

        Returns:
            Matrix: The resulting matrix.
        """
        x = self * Matrix(1, 0, 0, -1, 0, 0)
        return x

    @staticmethod
    def fromjson(text):
        fields = eval(text)
        if not fields['Is2D']:
            return Matrix()
        matrix = Matrix(fields['M11'], fields['M12'],
                        fields['M21'], fields['M22'],
                        fields['M41'], fields['M42'])
        return matrix

    @staticmethod
    def frommatrix(matrix):
        """Constructs a new Matrix initialized with the numpy.matrix matrix.

        Arguments:
            matrix (numpy.matrix): A 3x3 matrix object.
        Returns:
            Matrix: A new Matrix object.
        """
        if matrix is None or (not isinstance(matrix, np.matrix)):
            raise TypeError('Expected numpy.matrix, got {}'.format(
                type(matrix)))
        elif matrix.shape != (3, 3):
            raise ValueError('Expected 3x3 matrix, got {}'.format(
                matrix.tolist()))
        x = Matrix()
        x._matrix = np.matrix.copy(matrix)
        return x

    def get_angle(self, degrees=True):
        """Returns the rotation angle.

        Arguments:
            degrees (bool, optional): If degrees is True, returns angle in
                degrees; otherwise returns angle in radians.
        Returns:
            float: The rotation angle is in the range of >-180 to <=180 in
                degrees.
        """
        a = self._matrix[0, 0]
        b = self._matrix[1, 0]
        t = math.atan2(b, a)  # Tz = atan2(r21, r11)
        if degrees:
            t = math.degrees(t)
        return t

    def get_scale(self):
        """Returns the scale amounts.

        Returns:
             tuple[float, float]: The scale amounts.
        """
        # 0 <= sx, 0 <= sy
        a = self._matrix[0, 0]  # 0
        c = self._matrix[0, 1]  # 2
        b = self._matrix[1, 0]  # 1
        d = self._matrix[1, 1]  # 3
        sx = math.sqrt(a ** 2 + c ** 2)
        sy = math.sqrt(b ** 2 + d ** 2)
        return sx, sy

    def get_translate(self):
        """Returns the translation amounts.

        Returns:
             tuple[float, float]: The translation amounts.
        """
        tx = self._matrix[0, 2]
        ty = self._matrix[1, 2]
        return tx, ty

    def inverse(self):
        """Returns the inverse matrix.
        The current matrix is not modified.

        Returns:
            Matrix: The resulting matrix.
        """
        m = self._matrix.getI()
        return Matrix.frommatrix(m)

    def invert_self(self):
        """Inverts the current matrix.

        Returns:
            Matrix: Returns itself.
        """
        self._matrix = self._matrix.getI()
        return self

    def multiply(self, other):
        """Post-multiplies the other matrix on the current matrix and returns
        the resulting matrix.
        The current matrix is not modified.

        Arguments:
            other (Matrix): A matrix to be multiplied.
        Returns:
            Matrix: The resulting matrix.
        """
        x = self * other
        return x

    def multiply_self(self, other):
        """Post-multiplies the other matrix on the current matrix.

        Arguments:
            other (Matrix): A matrix to be multiplied.
        Returns:
            Matrix: Returns itself.
        """
        self._matrix *= other.matrix
        return self

    def point(self, x, y):
        """Post-multiplies the transformation [x y 1] and returns the
        resulting point.

        Arguments:
            x (float): The x-coordinate to transform.
            y (float): The y-coordinate to transform.
        Returns:
             tuple[float, float]: The resulting coordinates.
        """
        pt = np.matrix([[float(x)], [float(y)], [1.0]])
        pt = self._matrix * pt
        return pt.item(0), pt.item(1)

    def rotate(self, angle, cx=0, cy=0):
        """Post-multiplies a rotation transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The rotation angle in degrees.
            cx (float, optional): The x-coordinate of center of rotation.
            cy (float, optional): The y-coordinate of center of rotation.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.rotate_self(angle, cx, cy)
        return x

    def rotate_self(self, angle, cx=0, cy=0):
        """Post-multiplies a rotation transformation on the current matrix.

        Arguments:
            angle (float): The rotation angle in degrees.
            cx (float, optional): The x-coordinate of center of rotation.
            cy (float, optional): The y-coordinate of center of rotation.
        Returns:
            Matrix: Returns itself.
        """
        # translate(cx cy) rotate(angle) translate(-cx -cy)
        if cx != 0 and cy != 0:
            self.translate_self(cx, cy)
        cosa = math.cos(math.radians(angle))
        sina = math.sin(math.radians(angle))
        m = matrix2d(cosa, sina, -sina, cosa, 0, 0)
        self._matrix *= m
        if cx != 0 and cy != 0:
            self.translate_self(-cx, -cy)
        return self

    def scale(self, sx, sy=None):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            sx (float): The scale amount in X.
            sy (float, optional): The scale amount in Y.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.scale_self(sx, sy)
        return x

    def scale_self(self, sx, sy=None):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix.

        Arguments:
            sx (float): The scale amount in X.
            sy (float, optional): The scale amount in Y.
        Returns:
            Matrix: Returns itself.
        """
        if sy is None:
            sy = sx
        m = matrix2d(sx, 0, 0, sy, 0, 0)
        self._matrix *= m
        return self

    def set_matrix(self, a, b, c, d, e, f):
        """Sets the matrix.

        Arguments:
            a (float): The a component of the matrix.
            b (float): The b component of the matrix.
            c (float): The c component of the matrix.
            d (float): The d component of the matrix.
            e (float): The e component of the matrix.
            f (float): The f component of the matrix.
        """
        self._matrix = matrix2d(a, b, c, d, e, f)

    def skewx(self, angle):
        """Post-multiplies a skewX transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.skewx_self(angle)
        return x

    def skewx_self(self, angle):
        """Post-multiplies a skewX transformation on the current matrix.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            Matrix: Returns itself.
        """
        m = matrix2d(1, 0, math.tan(math.radians(angle)), 1, 0, 0)
        self._matrix *= m
        return self

    def skewy(self, angle):
        """Post-multiplies a skewY transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.skewy_self(angle)
        return x

    def skewy_self(self, angle):
        """Post-multiplies a skewY transformation on the current matrix.

        Arguments:
            angle (float): The skew angle in degrees.
        Returns:
            Matrix: Returns itself.
        """
        m = matrix2d(1, math.tan(math.radians(angle)), 0, 1, 0, 0)
        self._matrix *= m
        return self

    def tojson(self):
        fields = {
            'M11': self.m11,
            'M12': self.m12,
            'M21': self.m21,
            'M22': self.m22,
            'M41': self.m41,
            'M42': self.m42,
            'Is2D': 1,
        }
        return repr(fields)

    def toarray(self):
        # [[a c e]
        #  [b d f]
        #  [0 0 1]]
        # -> [a b c d e f]
        # return self._matrix.A1.tolist()
        return [self._matrix[0, 0], self._matrix[1, 0], self._matrix[0, 1],
                self._matrix[1, 1], self._matrix[0, 2], self._matrix[1, 2]]

    def tolist(self):
        return self._matrix.tolist()

    def tostring(self, delimiter=None):
        number_sequence = format_number_sequence(self.toarray())
        if delimiter is None or len(delimiter) == 0:
            delimiter = ' '
        return 'matrix({})'.format(delimiter.join(number_sequence))

    def translate(self, tx, ty=0):
        """Post-multiplies a translation transformation on the current matrix
        and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            tx (float): The translation amount in X.
            ty (float, optional): The translation amount in Y.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.translate_self(tx, ty)
        return x

    def translate_self(self, tx, ty=0):
        """Post-multiplies a translation transformation on the current
        matrix.

        Arguments:
            tx (float): The translation amount in X.
            ty (float, optional): The translation amount in Y.
        Returns:
            Matrix: Returns itself.
        """
        m = matrix2d(1, 0, 0, 1, tx, ty)
        self._matrix *= m
        return self


class Window(object):
    inner_width = 1280
    inner_height = 720
