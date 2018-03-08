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
from abc import abstractmethod

from .core import CSSUtils, Element, Font, Matrix, Node, SVGLength, Window
from .formatter import format_coordinate_pair_sequence, \
    to_coordinate_pair_sequence
from .freetype import FreeType
from .harfbuzz import HBBuffer, HBDirection, HBFeature, HBFTFont, HBLanguage, \
    HBScript
from .opentype import features_from_style, iso639_codes_from_language_tag
from .path import PathParser
from .rect import Rect
from .transform import SVGTransformList


class CharacterData(Node):
    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError

    @data.setter
    @abstractmethod
    def data(self, data):
        raise NotImplementedError

    @property
    def node_value(self):
        raise NotImplementedError

    @node_value.setter
    def node_value(self, text):
        raise NotImplementedError

    @property
    def text_content(self):
        raise NotImplementedError

    @text_content.setter
    def text_content(self, text):
        raise NotImplementedError


# See https://www.w3.org/TR/html51/dom.html#htmlelement-htmlelement
# See https://drafts.csswg.org/cssom-view/#extensions-to-the-htmlelement-interface
class HTMLElement(Element):
    pass


class HTMLHyperlinkElementUtils(object):
    # TODO: implement the HTMLHyperlinkElementUtils.
    pass


# See https://www.w3.org/TR/html51/semantics-embedded-content.html#htmlmediaelement-htmlmediaelement
class HTMLMediaElement(HTMLElement):
    pass


class SVGAnimatedPoints(Element):
    @property
    def points(self):
        """list[tuple[float, float]]: A list of coordinates pair.

        Examples:
            >>> parser = SVGParser()
            >>> polygon = parser.make_element('polygon')
            >>> polygon.attributes.set('points', '100,300 300,300 200,100')
            >>> polygon.points
            [(100.0, 300.0), (300.0, 300.0), (200.0, 100.0)]
            >>> polygon.points = [(100, 100), (300, 100), (200, 300)]
            >>> polygon.tostring()
            b'<polygon points="100,100 300,100 200,300"/>'
        """
        # 'points' property
        # Value: <points>
        # <points> = [ <number>+ ]#
        # Initial value: (none)
        points = self.attributes.get('points')
        if points is None:
            return []
        number_sequence = list()
        for it in PathParser.RE_NUMBER_SEQUENCE.finditer(points.strip()):
            number = it.group('number')
            number_sequence.append(float(number))
        if len(number_sequence) % 2 != 0:
            return []  # an odd number of coordinates
        return to_coordinate_pair_sequence(number_sequence)

    @points.setter
    def points(self, points):
        value = format_coordinate_pair_sequence(points)
        self.attributes.set('points', value)


# See https://svgwg.org/svg2-draft/types.html#InterfaceSVGGraphicsElement
class SVGBoundingBoxOptions(object):
    def __init__(self):
        self.fill = True
        self.stroke = False
        self.markers = False
        self.clipped = False


# See https://svgwg.org/svg2-draft/types.html#InterfaceSVGElement
class SVGElement(Element):
    @property
    def owner_svg_element(self):
        """SVGSVGElement: The nearest ancestor 'svg' element. If the current
        element is outer most 'svg' element, then returns None.
        """
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) == hash(self):
            return None
        nearest = self.get_nearest_svg_element()
        return nearest

    @property
    def viewport_element(self):
        """SVGElement: The nearest ancestor element that establishes an SVG
        viewport. If the current element is outer most 'svg' element, then
        returns None.
        """
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) == hash(self):
            return None
        nearest = self.get_nearest_viewport_element()
        return nearest

    def get_farthest_svg_element(self):
        """Returns the outermost 'svg' element.

        Returns:
            SVGSVGElement: The outermost 'svg' element.
        """
        root = None
        element = self
        while element is not None:
            if element.local_name == 'svg':
                root = element
            element = element.getparent()
        return root

    def get_farthest_viewport_element(self):
        root = None
        element = self
        while element is not None:
            if element.local_name in ['svg', 'symbol']:
                root = element
            element = element.getparent()
        return root

    def get_nearest_svg_element(self):
        element = self
        while element is not None:
            if element.local_name == 'svg':
                return element
            element = element.getparent()
        return None

    def get_nearest_viewport_element(self):
        element = self
        while element is not None:
            if element.local_name in ['svg', 'symbol']:
                return element
            element = element.getparent()
        return None

    def get_view_box(self):
        """Gets values of the 'viewBox' and 'preserveAspectRatio' attributes
        from nearest ancestor element that establishes an SVG viewport.

        Returns:
            tuple[SVGLength, SVGLength, SVGLength, SVGLength,
            SVGPreserveAspectRatio]: Returns a tuple of four numbers <min-x>,
            <min-y>, <width>, <height> and <SVGPreserveAspectRatio>.
        """
        element = self
        while element is not None:
            root = element.get_nearest_viewport_element()
            if root is None:
                break
            assert isinstance(root, SVGFitToViewBox)
            view_box = root.view_box
            if view_box is not None:
                vbx, vby, vbw, vbh = view_box
                par = root.preserve_aspect_ratio
                return vbx, vby, vbw, vbh, par
            element = root.getparent()
        return None

    def get_viewport_size(self):
        """Gets the SVG viewport size from nearest ancestor element that
        establishes an SVG viewport.

        Returns:
            tuple[SVGLength, SVGLength, SVGLength, SVGLength]: Returns a tuple
            of four numbers <min-x>, <min-y>, <width>, and <height>.
        """
        # See https://svgwg.org/svg2-draft/coords.html#Units
        element = self
        roots = list()
        while element is not None:
            root = element.get_nearest_viewport_element()
            if root is None:
                break
            roots.insert(0, root)
            element = root.getparent()

        parent_vpw = vpw = SVGLength(Window.inner_width,
                                     direction=SVGLength.DIRECTION_HORIZONTAL)
        parent_vph = vph = SVGLength(Window.inner_height,
                                     direction=SVGLength.DIRECTION_VERTICAL)
        for root in roots:
            attributes = root.attributes

            _width = attributes.get('width', 'auto')
            if _width == 'auto':
                _width = '100%'
            if _width == 'inherit':
                vpw = parent_vpw
            else:
                vpw = SVGLength(_width,
                                context=root,
                                direction=SVGLength.DIRECTION_HORIZONTAL)
                unit = vpw.unit
                if unit in [SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VW]:
                    vpw = vpw.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vpw
                elif unit == SVGLength.TYPE_VH:
                    vpw = vpw.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vph
                elif unit == SVGLength.TYPE_VMAX:
                    vpw = max(parent_vpw, parent_vph)
                elif unit == SVGLength.TYPE_VMIN:
                    vpw = min(parent_vpw, parent_vph)
            parent_vpw = vpw

            _height = attributes.get('height', 'auto')
            if _height == 'auto':
                _height = '100%'
            if _height == 'inherit':
                vph = parent_vph
            else:
                vph = SVGLength(_height,
                                context=root,
                                direction=SVGLength.DIRECTION_VERTICAL)
                unit = vph.unit
                if unit in [SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VH]:
                    vph = vph.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vph
                elif unit == SVGLength.TYPE_VW:
                    vph = vph.value(SVGLength.TYPE_PERCENTAGE) / 100 \
                          * parent_vpw
                elif unit == SVGLength.TYPE_VMAX:
                    vph = max(parent_vpw, parent_vph)
                elif unit == SVGLength.TYPE_VMIN:
                    vph = min(parent_vpw, parent_vph)
            parent_vph = vph
        if len(roots) == 0:
            vpx = SVGLength(0)
            vpy = SVGLength(0)
        else:
            root = roots[-1]
            attributes = root.attributes

            vpx = SVGLength(attributes.get('x', '0'),
                            context=root,
                            direction=SVGLength.DIRECTION_HORIZONTAL)
            unit = vpx.unit
            if unit in [SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VW]:
                vpx = vpx.value(SVGLength.TYPE_PERCENTAGE) / 100 * vpw
            elif unit == SVGLength.TYPE_VH:
                vpx = vpx.value(SVGLength.TYPE_PERCENTAGE) / 100 * vph
            elif unit == SVGLength.TYPE_VMAX:
                vpx = max(vpw, vph)
            elif unit == SVGLength.TYPE_VMIN:
                vpx = min(vpw, vph)

            vpy = SVGLength(attributes.get('y', '0'),
                            context=root,
                            direction=SVGLength.DIRECTION_VERTICAL)
            unit = vpy.unit
            if unit in [SVGLength.TYPE_PERCENTAGE, SVGLength.TYPE_VH]:
                vpy = vpy.value(SVGLength.TYPE_PERCENTAGE) / 100 * vph
            elif unit == SVGLength.TYPE_VW:
                vpy = vpy.value(SVGLength.TYPE_PERCENTAGE) / 100 * vpw
            elif unit == SVGLength.TYPE_VMAX:
                vpy = max(vpw, vph)
            elif unit == SVGLength.TYPE_VMIN:
                vpy = min(vpw, vph)

        # TODO: check a range: max-width, max-height, min-width and min-height.
        return vpx, vpy, vpw, vph


# See https://svgwg.org/svg2-draft/types.html#InterfaceSVGGraphicsElement
class SVGGraphicsElement(SVGElement):
    @property
    def transform(self):
        """SVGTransformList: The computed value of the 'transform' property.
        """
        # 'transform' property
        # Value: none | <transform-list>
        # <transform-list> = <transform-function>+
        # Initial: none
        # Inherited: no
        transform = self.attributes.get('transform')
        if transform is None or transform == 'none':
            return None
        return SVGTransformList.parse(transform)

    @transform.setter
    def transform(self, transform):
        value = SVGTransformList.tostring(transform)
        self.attributes.set('transform', value)

    def get_bbox(self, options=None, _depth=0):
        """Returns the bounding box of the current element.

        Arguments:
            options (SVGBoundingBoxOptions, optional): Reserved.
            _depth (int, optional): For internal use only.
        Returns:
            Rect: The bounding box of the current element.
        """
        # TODO: implement SVGBoundingBoxOptions option.
        _depth += 1
        bbox = Rect()
        if self.local_name in ['defs', 'symbol']:
            return bbox  # not rendered directly
        if self.iscontainer():
            for child in iter(self):
                if isinstance(child, SVGGraphicsElement):
                    display = child.attributes.get('display', 'inline')
                    if display == 'none':
                        continue
                    bbox |= child.get_bbox(options, _depth)
            if _depth > 1:
                transform_list = self.transform  # type: SVGTransformList
                if transform_list is not None:
                    matrix = transform_list.tomatrix()
                    bbox.transform(matrix)
        else:
            settings = SVGPathDataSettings()
            settings.normalize = True
            path_data = self.get_transformed_path_data(settings)
            if len(path_data) > 0:
                bbox = PathParser.get_bbox(path_data, options)
        return bbox

    def get_ctm(self):
        """Returns the current transformation matrix (CTM).

        Returns:
            Matrix: The current transformation matrix (CTM).
        """
        ctm = Matrix()
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) == hash(self):
            if farthest.zoom_and_pan == SVGZoomAndPan.ZOOMANDPAN_MAGNIFY:
                scale = self.current_scale
                tx, ty = self.current_translate
                ctm *= Matrix(scale, 0, 0, scale, tx, ty)

        vtm = self.get_viewport_transform_matrix()
        ctm *= vtm

        transform_list = SVGTransformList()
        element = self
        while element is not None:
            if element.istransformable():
                transform = element.transform
                if transform is not None:
                    transform_list[0:0] = transform
            if element.local_name in ['svg', 'symbol']:
                break
            element = element.getparent()
        if len(transform_list) > 0:
            matrix = transform_list.tomatrix()
            ctm *= matrix
        return ctm

    def get_descendant_path_data(self, settings=None):
        path_data = list()
        for child in iter(self):
            if isinstance(child, SVGGraphicsElement):
                path_data += child.get_path_data(settings)
        return path_data

    @abstractmethod
    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        raise NotImplementedError

    def get_transformed_path_data(self, settings=None):
        path_data = self.get_path_data(settings)
        if len(path_data) == 0:
            return path_data
        if self.local_name == 'use':
            transform_list = self.instance_root.transform
            if transform_list is not None:
                matrix = transform_list.tomatrix()
                path_data = PathParser.transform(path_data, matrix)
        transform_list = self.transform  # type: SVGTransformList
        if transform_list is not None:
            matrix = transform_list.tomatrix()
            path_data = PathParser.transform(path_data, matrix)
        return path_data

    def get_viewport_transform_matrix(self):
        """Returns the transformation matrix of an SVG viewport.

        Returns:
            Matrix: The transformation matrix.
        """
        # See https://svgwg.org/svg2-draft/coords.html#ComputingAViewportsTransform
        ctm = Matrix()
        ex, ey, ew, eh = self.get_viewport_size()
        view_box = self.get_view_box()
        if view_box is None:
            if ex is not None and ey is not None:
                ctm.translate_self(ex.value(), ey.value())
            return ctm
        if ew is None or eh is None:
            return ctm
        vbx, vby, vbw, vbh, par = view_box
        align = SVGPreserveAspectRatio.ALIGN_XMIDYMID \
            if par.align is None else par.align
        meet_or_slice = SVGPreserveAspectRatio.MEETORSLICE_MEET \
            if par.meet_or_slice is None \
            else par.meet_or_slice
        sx = ew / vbw
        sy = eh / vbh
        if align != SVGPreserveAspectRatio.ALIGN_NONE:
            if meet_or_slice == SVGPreserveAspectRatio.MEETORSLICE_MEET:
                if sx < sy:
                    sy = sx
                elif sx > sy:
                    sx = sy
            elif meet_or_slice == SVGPreserveAspectRatio.MEETORSLICE_SLICE:
                if sx > sy:
                    sy = sx
                elif sx < sy:
                    sx = sy
        tx = ex - vbx * sx
        ty = ey - vby * sy
        if 'xMid' in align:
            tx += (ew - vbw * sx) / 2
        if 'xMax' in align:
            tx += ew - vbw * sx
        if 'YMid' in align:
            ty += (eh - vbh * sy) / 2
        if 'YMax' in align:
            ty += eh - vbh * sy
        ctm.translate_self(tx.value(tx.unit), ty.value(tx.unit))
        ctm.scale_self(sx.value(tx.unit), sy.value(tx.unit))
        return ctm


class SVGFitToViewBox(Element):
    @property
    def preserve_aspect_ratio(self):
        """SVGPreserveAspectRatio: The value of the 'preserveAspectRatio'
        attribute.
        """
        # 'preserveAspectRatio' attribute
        # Value: <align> <meetOrSlice>?
        # Initial: xMidYMid meet
        par = SVGPreserveAspectRatio(
            self.attributes.get('preserveAspectRatio', 'xMidYMid meet'))
        return par

    @property
    def view_box(self):
        """tuple[SVGLength, SVGLength, SVGLength, SVGLength]: The value of the
        'viewBox' attribute is a tuple of four numbers <min-x>, <min-y>,
        <width> and <height>.
        """
        # 'viewBox' attribute
        # Value: [<min-x>,? <min-y>,? <width>,? <height>]
        # <min-x>, <min-x>, <width>, <height> = <number>
        view_box = self.attributes.get('viewBox')
        if view_box is None:
            return None
        vb = Element.RE_DIGIT_SEQUENCE_SPLITTER.split(view_box)
        return (SVGLength(vb[0],
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL),
                SVGLength(vb[1],
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL),
                SVGLength(vb[2],
                          context=self,
                          direction=SVGLength.DIRECTION_HORIZONTAL),
                SVGLength(vb[3],
                          context=self,
                          direction=SVGLength.DIRECTION_VERTICAL))


# See https://svgwg.org/svg2-draft/types.html#InterfaceSVGGeometryElement
class SVGGeometryElement(SVGGraphicsElement):
    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        raise NotImplementedError  # implement in a subclass

    def get_point_at_length(self, distance):
        # TODO: implement SVGGeometryElement.getPointAtLength().
        # See https://svgwg.org/svg2-draft/types.html#__svg__SVGGeometryElement__getPointAtLength
        pass

    def get_total_length(self):
        """Returns the total length of the path.

        Returns:
            float: The total length of the path.
        """
        path_data = self.get_path_data()
        if len(path_data) == 0:
            return 0
        return PathParser.get_total_length(path_data)


class SVGPathData(Element):
    def set_path_data(self, path_data):
        if path_data is None or len(path_data) == 0:
            d = 'none'
        else:
            d = PathParser.tostring(path_data)
        self.attributes.set('d', d)


# See https://www.w3.org/TR/svg-paths/#InterfaceSVGPathData
# See https://svgwg.org/specs/paths/#InterfaceSVGPathData
class SVGPathDataSettings(object):
    def __init__(self):
        self.normalize = False


class SVGPreserveAspectRatio(object):
    ALIGN_NONE = 'none'
    ALIGN_XMINYMIN = 'xMinYMin'
    ALIGN_XMIDYMIN = 'xMidYMin'
    ALIGN_XMAXYMIN = 'xMaxYMin'
    ALIGN_XMINYMID = 'XMinYMid'
    ALIGN_XMIDYMID = 'xMidYMid'
    ALIGN_XMAXYMID = 'xMaxYMid'
    ALIGN_XMINYMAX = 'xMinYMax'
    ALIGN_XMIDYMAX = 'xMidYMax'
    ALIGN_XMAXYMAX = 'xMaxYMax'

    MEETORSLICE_MEET = 'meet'
    MEETORSLICE_SLICE = 'slice'

    def __init__(self, text=None):
        # 'preserveAspectRatio' attribute
        # Value: <align> <meetOrSlice>?
        # Initial: xMidYMid meet
        self._align = SVGPreserveAspectRatio.ALIGN_XMIDYMID
        self._meet_or_slice = SVGPreserveAspectRatio.MEETORSLICE_MEET
        if text is not None:
            (self._align,
             self._meet_or_slice) = SVGPreserveAspectRatio.parse(text)

    def __eq__(self, other):
        if not isinstance(other, SVGPreserveAspectRatio):
            return NotImplemented
        return (self.align == other.align
                and self.meet_or_slice == other.meet_or_slice)

    @property
    def align(self):
        return self._align if self._align is not None else 'xMidYMid'

    @align.setter
    def align(self, align):
        self._align = align

    @property
    def meet_or_slice(self):
        if self._align == SVGPreserveAspectRatio.ALIGN_NONE:
            return None
        return self._meet_or_slice if self._meet_or_slice is not None \
            else 'meet'

    @meet_or_slice.setter
    def meet_or_slice(self, meet_or_slice):
        self._meet_or_slice = meet_or_slice

    @staticmethod
    def parse(text):
        align = SVGPreserveAspectRatio.ALIGN_XMIDYMID
        meet_or_slice = SVGPreserveAspectRatio.MEETORSLICE_MEET
        items = Element.RE_DIGIT_SEQUENCE_SPLITTER.split(text.strip())
        if (len(items) > 0
                and items[0] in [SVGPreserveAspectRatio.ALIGN_NONE,
                                 SVGPreserveAspectRatio.ALIGN_XMAXYMAX,
                                 SVGPreserveAspectRatio.ALIGN_XMAXYMID,
                                 SVGPreserveAspectRatio.ALIGN_XMAXYMIN,
                                 SVGPreserveAspectRatio.ALIGN_XMIDYMAX,
                                 SVGPreserveAspectRatio.ALIGN_XMIDYMID,
                                 SVGPreserveAspectRatio.ALIGN_XMIDYMIN,
                                 SVGPreserveAspectRatio.ALIGN_XMINYMAX,
                                 SVGPreserveAspectRatio.ALIGN_XMINYMID,
                                 SVGPreserveAspectRatio.ALIGN_XMINYMIN]):
            align = items[0]
            if (align != SVGPreserveAspectRatio.ALIGN_NONE and len(items) >= 2
                    and items[1] in [
                        SVGPreserveAspectRatio.MEETORSLICE_MEET,
                        SVGPreserveAspectRatio.MEETORSLICE_SLICE
                    ]):
                meet_or_slice = items[1]
        return align, meet_or_slice

    def tostring(self):
        return ' '.join([self.align,
                         self.meet_or_slice
                         if self.align != SVGPreserveAspectRatio.ALIGN_NONE
                         else '']).strip()


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


class SVGURIReference(Element):
    @property
    def href(self):
        attributes = self.attributes
        href = attributes.get('href')
        if href is None:
            href = attributes.get_ns(Element.XLINK_NAMESPACE_URI, 'href')
        return href


class SVGGradientElement(SVGElement, SVGURIReference):
    SPREADMETHOD_UNKNOWN = 0
    SPREADMETHOD_PAD = 1
    SPREADMETHOD_REFLECT = 2
    SPREADMETHOD_REPEAT = 3


class SVGZoomAndPan(Element):
    ZOOMANDPAN_UNKNOWN = 0
    ZOOMANDPAN_DISABLE = 1
    ZOOMANDPAN_MAGNIFY = 2

    _ZOOMANDPAN_MAP = {
        'disable': ZOOMANDPAN_DISABLE,
        'magnify': ZOOMANDPAN_MAGNIFY,
    }

    @property
    def zoom_and_pan(self):
        """int: The zoom and pan type."""
        zoom_and_pan = self.attributes.get('zoomAndPan', 'disable')
        zap_type = SVGZoomAndPan._ZOOMANDPAN_MAP.get(
            zoom_and_pan, SVGZoomAndPan.ZOOMANDPAN_UNKNOWN)
        return zap_type

    @zoom_and_pan.setter
    def zoom_and_pan(self, zoom_and_pan_type):
        if zoom_and_pan_type not in SVGZoomAndPan._ZOOMANDPAN_MAP.values():
            return
        zoom_and_pan = [key for key, value
                        in SVGZoomAndPan._ZOOMANDPAN_MAP.items()
                        if value == zoom_and_pan_type][0]
        self.attributes.set('zoomAndPan', zoom_and_pan)
