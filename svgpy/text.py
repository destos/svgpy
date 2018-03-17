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


import copy

from .base import SVGElement, SVGGraphicsElement, SVGPathDataSettings
from .core import CSSUtils, Element, Font, Matrix, Node, SVGLength
from .freetype import FreeType
from .harfbuzz import HBBuffer, HBDirection, HBFeature, HBFTFont, HBLanguage, \
    HBScript
from .opentype import features_from_style, iso639_codes_from_language_tag
from .path import PathParser
from .rect import Rect


# See https://svgwg.org/svg2-draft/text.html#InterfaceSVGTextContentElement
class SVGTextContentElement(SVGGraphicsElement):
    _CHARS_ID = 0
    _CHARS_TEXT = 1
    _CHARS_STYLE = 2
    _CHARS_PATH_DATA = 3
    _CHARS_ADVANCE_LIST = 4
    _CHARS_BBOX = 5
    _CHARS_ELEMENT = 6

    def _get_chars_info(self):
        root = self.get_nearest_text_element()
        if root is None:
            return []

        chars_info = SVGTextContentElement._get_descendant_chars_info(
            root, first=True, is_display=True, is_render=True)
        return chars_info

    @staticmethod
    def _get_descendant_chars(element, style_map=None,
                              prev_text=None, first=False, **kwargs):
        """Returns the addressable characters.

        Arguments:
            element (SVGElement):
            style_map (dict, optional):
            prev_text (str, optional):
            first (bool, optional):
            **kwargs: See below.
        Keyword Arguments:
            is_display (bool, optional):
        Returns:
            list[list[int, str, dict, list[SVGPathSegment], list[float], Rect,
                SVGElement]]:
                Returns a list of seven numbers <hash value of an element>,
                <text for rendering>, <computed presentation properties>,
                <list of path segments>, <list of advance measure>,
                <bbox> and <element object>.
            str: previous text for rendering.
        """
        is_display = kwargs.get('is_display', False)
        chars_info = list()
        if not element.istext() or (is_display
                                    and not element.isdisplay()):
            return chars_info, prev_text

        if style_map is None:
            style_map = dict()
        key = hash(element)
        style = style_map.get(key)
        if style is None:
            style = element.get_computed_style()
            style_map[key] = copy.deepcopy(style)
        if element.text is not None:
            out_text = CSSUtils.normalize_text_content(
                element,
                element.text,
                style,
                prev_text,
                first)
            if len(out_text) > 0:
                path_data = []
                advance_list = []
                bbox = None
                chars_info.append(
                    [key, out_text, style, path_data, advance_list, bbox,
                     element])
                prev_text = out_text
                first = False

        for child in iter(element):
            if (child.node_type == Node.ELEMENT_NODE
                    and child.istext()
                    and (not is_display
                         or (is_display and child.isdisplay()))):
                child_chars_info, out_text = \
                    SVGTextContentElement._get_descendant_chars(
                        child, style_map, prev_text, first, **kwargs)
                if len(out_text) > 0:
                    chars_info += child_chars_info
                    prev_text = out_text
                    first = False
            if (child.local_name in SVGElement.TEXT_CONTENT_CHILD_ELEMENTS
                    and child.tail is not None):
                out_text = CSSUtils.normalize_text_content(
                    child,
                    child.tail,
                    style,
                    prev_text,
                    first)
                if len(out_text) > 0:
                    path_data = []
                    advance_list = []
                    bbox = None
                    chars_info.append(
                        [key, out_text, style, path_data, advance_list, bbox,
                         element])
                    prev_text = out_text
                    first = False
        return chars_info, prev_text

    @staticmethod
    def _get_descendant_chars_info(root, first=False, **kwargs):
        """Returns the addressable characters.

        Arguments:
            root (SVGElement):
            first (bool, optional):
            **kwargs: See below.
        Keyword Arguments:
            is_display (bool, optional):
            is_render (bool, optional):
        Returns:
            list[list[int, str, dict, list[SVGPathSegment], list[float], Rect,
                SVGElement]]:
                Returns a list of seven numbers <hash value of an element>,
                <text for rendering>, <computed presentation properties>,
                <list of path segments>, <list of advance measure>,
                <bbox> and <element object>.
        """
        chars_info, _ = SVGTextContentElement._get_descendant_chars(
            root, first=first, **kwargs)
        if len(chars_info) > 0:
            item = chars_info[-1]
            text = item[SVGTextContentElement._CHARS_TEXT].rstrip()
            item[SVGTextContentElement._CHARS_TEXT] = text

            is_render = kwargs.get('is_render', False)
            if is_render:
                style = chars_info[0][SVGTextContentElement._CHARS_STYLE]
                x_list = style['x']
                if x_list is None:
                    x = 0
                else:
                    x = x_list[0]
                y_list = style['y']
                if y_list is None:
                    y = 0
                else:
                    y = y_list[0]

                style_map = dict()
                for info in iter(chars_info):
                    key = info[SVGTextContentElement._CHARS_ID]
                    style = info[SVGTextContentElement._CHARS_STYLE]
                    style_map[key] = copy.deepcopy(style)

                for info in iter(chars_info):
                    path_data, advance_list, bbox, (x, y) = \
                        SVGTextContentElement._get_text_path_data(
                            info[SVGTextContentElement._CHARS_ELEMENT],
                            style_map,
                            info[SVGTextContentElement._CHARS_TEXT],
                            x, y)
                    info[SVGTextContentElement._CHARS_PATH_DATA] = path_data
                    info[SVGTextContentElement._CHARS_ADVANCE_LIST] = \
                        advance_list
                    info[SVGTextContentElement._CHARS_BBOX] = bbox

        return chars_info

    @staticmethod
    def _get_text_path_data(element, style_map, out_text, start_x, start_y):
        """Returns the addressable characters.

        Arguments:
            element (SVGElement):
            style_map (dict):
            out_text (str): A text for rendering.
            start_x (float):
            start_y (float):
        Returns:
            list[SVGPathSegment]:
            list[float]:
            Rect:
            tuple[float, float]:
        """

        def _get_inherited_attribute(_element, _style_map, _key,
                                     _default=None):
            while _element is not None:
                if (_element.node_type == Node.ELEMENT_NODE
                        and _element.istext()
                        and _element.isdisplay()):
                    _style = _style_map.get(hash(_element))
                    if _style is None:
                        _style = _element.get_computed_style()
                        _style_map[hash(_element)] = _style
                    _value = _style.get(_key)
                    if _value is not None:
                        return _value
                _element = _element.getparent()
            return _default

        # TODO: support line-breaking and word-breaking.
        # TODO: support bidirectional text.
        x_list = _get_inherited_attribute(element, style_map, 'x', [])
        y_list = _get_inherited_attribute(element, style_map, 'y', [])
        dx_list = _get_inherited_attribute(element, style_map, 'dx', [])
        dy_list = _get_inherited_attribute(element, style_map, 'dy', [])
        rotate_list = _get_inherited_attribute(element, style_map, 'rotate',
                                               [])

        style = style_map.get(hash(element))  # computed style
        assert style is not None
        font = Font(element)
        face = font.face

        font_synthesis = style['font-synthesis']
        force_embolden = True if (style['font-weight'] > Font.WEIGHT_NORMAL
                                  and 'weight' in font_synthesis
                                  and (face.style_flags
                                       & FreeType.FT_STYLE_FLAG_BOLD) == 0
                                  ) else False
        force_oblique = True if (style['font-style'] != 'normal'
                                 and 'style' in font_synthesis
                                 and (face.style_flags
                                      & FreeType.FT_STYLE_FLAG_ITALIC) == 0
                                 ) else False

        # 'inline-size' property
        # See https://svgwg.org/svg2-draft/text.html#InlineSizeProperty
        inline_size = style['inline-size']

        # 'direction' property
        # Value: ltr | rtl
        # See https://drafts.csswg.org/css-writing-modes-4/#direction
        direction = style['direction']

        # 'writing-mode' property
        # Value: horizontal-tb | vertical-rl | vertical-lr | sideways-rl
        #  | sideways-lr
        # See https://drafts.csswg.org/css-writing-modes-3/#block-flow
        writing_mode = style['writing-mode']
        horizontal = True if writing_mode in [
            'horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb'] else False
        sideways = True if writing_mode.startswith('sideways') else False

        buf = HBBuffer.create()
        if horizontal:
            hb_dir_val = HBDirection.HB_DIRECTION_LTR if direction == 'ltr' \
                else HBDirection.HB_DIRECTION_RTL
        else:
            hb_dir_val = HBDirection.HB_DIRECTION_TTB
        buf.set_direction(HBDirection(hb_dir_val))

        # See https://www.microsoft.com/typography/otspec/featurelist.htm
        hb_features = list()
        features = features_from_style(style)
        for feature in features:
            hb_features.append(HBFeature.fromstring(feature))

        font_language_override = style['font-language-override']
        if font_language_override != 'normal':
            codes = iso639_codes_from_language_tag(font_language_override)
            if codes is not None:
                # FIXME: use correct language code.
                language = HBLanguage.fromstring(codes[0])
                buf.set_language(language)
        else:
            xml_lang = style.get(Element.XML_LANG)
            if xml_lang is None:
                xml_lang = style.get('lang')
            if xml_lang is None:
                xml_lang = HBLanguage.get_default().tostring()
            tags = xml_lang.split('-')  # language-script-region-variant-...
            if len(tags) >= 1:
                # ISO 639 2-letter codes
                language = HBLanguage.fromstring(tags[0])
                buf.set_language(language)
                if len(tags) >= 2 and len(tags[1]) == 4:
                    # ISO 15924 4-letter codes
                    script = HBScript.fromstring(tags[1])
                    buf.set_script(script)

        buf.add_utf8(out_text)
        buf.guess_segment_properties()
        hb_font = HBFTFont.create(face)
        buf.shape(hb_font, hb_features)
        infos = buf.get_glyph_infos()
        positions = buf.get_glyph_positions()

        # re-positioning
        glyph_index_list = list()
        for ch in out_text:
            index = face.get_char_index(ch)
            glyph_index_list.append(index)
        if direction == 'rtl':
            glyph_index_list.reverse()
        render_glyph_index_list = list()
        for info in infos:
            render_glyph_index_list.append(info.codepoint)
        if glyph_index_list != render_glyph_index_list:
            j = 0
            rotate = None if len(rotate_list) == 0 else rotate_list[-1]
            for i in range(len(render_glyph_index_list)):
                if render_glyph_index_list[i] == glyph_index_list[j]:
                    j += 1
                else:
                    for n in range(j + 1, len(glyph_index_list)):
                        if (len(render_glyph_index_list) > i + 1
                                and render_glyph_index_list[i + 1]
                                == glyph_index_list[n]):
                            j = n
                            break
                        try:
                            _ = x_list.pop(n)
                        except IndexError:
                            pass
                        try:
                            _ = y_list.pop(n)
                        except IndexError:
                            pass
                        try:
                            dx = dx_list.pop(n)
                            dx_list[n] += dx
                        except IndexError:
                            pass
                        try:
                            dy = dy_list.pop(n)
                            dy_list[n] += dy
                        except IndexError:
                            pass
                        try:
                            _ = rotate_list.pop(n)
                        except IndexError:
                            pass
                    else:
                        j = len(glyph_index_list) - 1
            if len(rotate_list) == 0 and rotate is not None:
                rotate_list.append(rotate)

        current_x = start_x
        current_y = start_y
        rotate = 0
        matrix = Matrix()
        path_data_list = list()
        advance_list = list()
        text_bbox = Rect()
        metrics = face.size.metrics
        x_ppem = metrics.x_ppem
        # y_ppem = metrics.y_ppem
        y_ppem = metrics.height / 64
        descender = metrics.descender / 64

        for info, position in zip(infos, positions):
            # 'x' attribute
            try:
                x = x_list.pop(0)
            except IndexError:
                x = current_x

            # 'y' attribute
            try:
                y = y_list.pop(0)
            except IndexError:
                y = current_y

            # 'dx' attribute
            try:
                dx = dx_list.pop(0)
            except IndexError:
                dx = 0

            # 'dy' attribute
            try:
                dy = dy_list.pop(0)
            except IndexError:
                dy = 0

            # 'rotate' attribute
            try:
                rotate = rotate_list.pop(0)
            except IndexError:
                pass

            # print(info, position)
            # print('index={} x={} y={} dx={} dy={} r={}'.format(
            #     info.codepoint, x, y, dx, dy, rotate))
            x_offset = position.x_offset / 64
            y_offset = position.y_offset / 64
            x += dx + x_offset
            y += dy - y_offset
            matrix.clear()
            if rotate:
                matrix.rotate_self(rotate)
            matrix.translate_self(x, -y)

            load_flags = FreeType.FT_LOAD_NO_BITMAP
            if not horizontal:
                load_flags |= FreeType.FT_LOAD_VERTICAL_LAYOUT
            face.load_glyph(info.codepoint, load_flags)
            glyph = face.glyph
            if force_embolden:
                glyph.embolden()
            if force_oblique:
                glyph.oblique()
            path_data = PathParser.fromglyph(face, matrix)
            if len(path_data) > 0:
                path_data_list += path_data

            if horizontal:
                advance = position.x_advance / 64
                glyph_bbox = Rect(x,
                                  y - y_ppem - descender,
                                  advance,
                                  y_ppem)
                x_advance = advance
                y_advance = 0
            else:
                # TODO: fix bbox for vertical text.
                advance = -position.y_advance / 64
                if sideways:
                    glyph_bbox = Rect(x, y, x_ppem, position.x_advance / 64)
                else:
                    glyph_bbox = Rect(x,
                                      y - advance + advance + y_offset,
                                      x_ppem,
                                      advance)
                x_advance = 0
                y_advance = advance
            advance_list.append(advance)
            if rotate:
                mtx = Matrix()
                mtx.rotate_self(rotate, x, y)
                glyph_bbox.transform(mtx)
            x += x_advance - x_offset
            y += y_advance + y_offset
            text_bbox |= glyph_bbox
            current_x = x
            current_y = y
        else:
            if len(rotate_list) == 0 and rotate != 0:
                rotate_list.append(rotate)

        return path_data_list, advance_list, text_bbox, (current_x, current_y)

    def get_bbox(self, options=None, _depth=0):
        """Returns the bounding box of the current element.

        Arguments:
            options (SVGBoundingBoxOptions, optional): Reserved.
            _depth (int, optional): For internal use only.
        Returns:
            Rect: The bounding box of the current element.
        """
        bbox = Rect()
        chars_info = self._get_chars_info()
        if len(chars_info) == 0:
            return bbox

        for info in iter(chars_info):
            bbox |= info[SVGTextContentElement._CHARS_BBOX]

        return bbox

    def get_computed_geometry(self):
        geometry = dict()
        attributes = self.attributes
        local_name = self.local_name

        # 'x' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: 0 <text>
        # Initial: (none) <tspan>
        default = '0' if local_name == 'text' else None
        _x = attributes.get('x', default)
        if _x is None:
            x = None
        else:
            x = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_x)
            ]
        geometry['x'] = x

        # 'y' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: 0 <text>
        # Initial: (none) <tspan>
        default = '0' if local_name == 'text' else None
        _y = attributes.get('y', default)
        if _y is None:
            y = None
        else:
            y = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_y)
            ]
        geometry['y'] = y

        # 'dx' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: (none)
        _dx = attributes.get('dx')
        if _dx is None:
            dx = None
        else:
            dx = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_dx)
            ]
        geometry['dx'] = dx

        # 'dy' attribute
        # Value: [ [ <length> | <percentage> | <number> ]+ ]#
        # Initial: (none)
        _dy = attributes.get('dy')
        if _dy is None:
            dy = None
        else:
            dy = [
                SVGLength(n,
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL).value()
                for n in Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_dy)
            ]
        geometry['dy'] = dy

        # 'rotate' attribute
        # Value: [ <number>+ ]#
        # Initial: (none)
        _rotate = attributes.get('rotate')
        if _rotate is None:
            rotate = None
        else:
            rotate = [
                float(x) for x in
                Element.RE_DIGIT_SEQUENCE_SPLITTER.split(_rotate)
            ]
        geometry['rotate'] = rotate

        return geometry

    def get_computed_text_length(self):
        return self.get_sub_string_length()

    def get_chars(self):
        """Returns the addressable characters available for rendering within
        the current element.

        Returns:
            str: The addressable characters or None.
        """
        root = self.get_nearest_text_element()
        if root is None:
            return None

        chars_info = SVGTextContentElement._get_descendant_chars_info(
            root, first=True, is_display=True)
        local_name = self.local_name
        if local_name == 'text':
            out = ''.join([x[SVGTextContentElement._CHARS_TEXT]
                           for x in chars_info])
            return out
        elif local_name in SVGElement.TEXT_CONTENT_CHILD_ELEMENTS:
            out = [x[SVGTextContentElement._CHARS_TEXT]
                   for x in chars_info
                   if x[SVGTextContentElement._CHARS_ID] == hash(self)]
            if len(out) == 0:
                return None
            return out[0]
        return None

    def get_nearest_text_element(self):
        element = self
        while element is not None:
            if element.local_name == 'text':
                return element
            element = element.getparent()
        return None

    def get_number_of_chars(self):
        """Returns the total number of addressable characters available for
        rendering within the current element.

        Returns:
            int: The total number of addressable characters.
        """
        # See https://svgwg.org/svg2-draft/text.html#__svg__SVGTextContentElement__getNumberOfChars
        chars = self.get_chars()
        if chars is None:
            return 0
        return len(chars)

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        path_data = list()
        chars_info = self._get_chars_info()
        if len(chars_info) == 0:
            return path_data

        for info in iter(chars_info):
            path_data += info[SVGTextContentElement._CHARS_PATH_DATA]

        if settings is not None:
            if not isinstance(settings, SVGPathDataSettings):
                raise TypeError('Expected SVGPathDataSettings, got {}'.format(
                    type(settings)))
            if settings.normalize:
                path_data = PathParser.normalize(path_data)
        return path_data

    def get_sub_string_length(self, char_num=0, nchars=-1):
        root = self.get_nearest_text_element()
        if root is None:
            return 0

        chars_info = SVGTextContentElement._get_descendant_chars_info(
            root, first=True, is_display=True, is_render=True)
        local_name = self.local_name
        advance_list = list()
        if local_name == 'text':
            for item in iter(chars_info):
                advance_list += item[SVGTextContentElement._CHARS_ADVANCE_LIST]
        elif local_name in SVGElement.TEXT_CONTENT_CHILD_ELEMENTS:
            out = [x[SVGTextContentElement._CHARS_ADVANCE_LIST]
                   for x in chars_info
                   if x[SVGTextContentElement._CHARS_ID] == hash(self)]
            if len(out) == 0:
                return 0
            advance_list = out[0]
        else:
            raise NotImplementedError

        if nchars == -1:
            last = len(advance_list)
        else:
            last = char_num + nchars
        return sum(advance_list[char_num:last])

    def get_total_length(self):
        """Returns the total length of the path.

        Returns:
            float: The total length of the path.
        """
        _ = self
        return 0


# See https://svgwg.org/svg2-draft/text.html#InterfaceSVGTextPositioningElement
class SVGTextPositioningElement(SVGTextContentElement):
    pass
