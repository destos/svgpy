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


from abc import abstractmethod

from .core import SVGLength
from .dom import Element, ElementCSSInlineStyle
from .formatter import format_coordinate_pair_sequence, \
    to_coordinate_pair_sequence
from .geometry.matrix import DOMMatrix
from .geometry.rect import DOMRect
from .path import PathParser
from .screen import Screen
from .transform import SVGTransformList


class HTMLElement(ElementCSSInlineStyle):
    pass


class HTMLHyperlinkElementUtils(object):
    # TODO: implement the HTMLHyperlinkElementUtils.
    pass


class HTMLMediaElement(HTMLElement):
    pass


class SVGAnimatedPoints(Element):
    @property
    def points(self):
        """list[tuple[float, float]]: A list of coordinates pair.

        Examples:
            >>> parser = SVGParser()
            >>> polygon = parser.create_element('polygon')
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


class SVGBoundingBoxOptions(object):
    def __init__(self):
        self.fill = True
        self.stroke = False
        self.markers = False
        self.clipped = False


class SVGElement(ElementCSSInlineStyle):
    NEAREST_VIEWPORT = 0
    FARTHEST_VIEWPORT = 1

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

    def get_view_box(self, recursive=True):
        """Gets values of the 'viewBox' and 'preserveAspectRatio' attributes
        from nearest ancestor element that establishes an SVG viewport.

        Returns:
            tuple[SVGLength, SVGLength, SVGLength, SVGLength,
            SVGPreserveAspectRatio]: Returns a tuple of four numbers <min-x>,
            <min-y>, <width>, <height> and <preserveAspectRatio>.
        """
        element = self
        while element is not None:
            root = element.get_nearest_viewport_element()
            if root is None:
                return None
            assert isinstance(root, SVGFitToViewBox)
            view_box = root.view_box
            if view_box is not None:
                vbx, vby, vbw, vbh = view_box
                par = root.preserve_aspect_ratio
                return vbx, vby, vbw, vbh, par
            if not recursive:
                return None
            element = root.getparent()
        return None

    def get_viewport_size(self, recursive=True):
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
            if not recursive:
                break
            element = root.getparent()

        win = (self.owner_document.default_view
               if self.owner_document is not None
               else None)
        if win is None:
            initial_viewport_width = Screen.DEFAULT_SCREEN_WIDTH
            initial_viewport_height = Screen.DEFAULT_SCREEN_HEIGHT
        else:
            initial_viewport_width = win.inner_width
            initial_viewport_height = win.inner_height
        parent_vpw = vpw = SVGLength(initial_viewport_width,
                                     direction=SVGLength.DIRECTION_HORIZONTAL)
        parent_vph = vph = SVGLength(initial_viewport_height,
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

    def _get_ctm(self, viewport_type):
        """Returns the current transformation matrix (CTM).

        Returns:
            DOMMatrix: The current transformation matrix (CTM).
        """
        roots = list()
        ctm = DOMMatrix()
        farthest = self.get_farthest_svg_element()
        if farthest is None:
            return ctm
        elif hash(farthest) == hash(self):
            roots.append(farthest)
        else:
            element = self
            while element is not None:
                root = element.get_nearest_viewport_element()
                if root is None or root in roots:
                    break
                roots.insert(0, root)
                if viewport_type == SVGElement.NEAREST_VIEWPORT:
                    if (self.local_name not in ['svg', 'symbol']
                            or len(roots) >= 2):
                        break
                element = root.getparent()
        if len(roots) == 0:
            return ctm

        if viewport_type == SVGElement.FARTHEST_VIEWPORT:
            scale = farthest.current_scale
            tx, ty = farthest.current_translate
            ctm *= DOMMatrix([scale, 0, 0, scale, tx, ty])
        for root in roots:
            vtm = root.get_viewport_transformation_matrix(recursive=False)
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

    def get_bbox(self, options=None, _depth=0):
        """Returns the bounding box of the current element.

        Arguments:
            options (SVGBoundingBoxOptions, optional): Reserved.
            _depth (int, optional): For internal use only.
        Returns:
            DOMRect: The bounding box of the current element.
        """
        # TODO: implement SVGBoundingBoxOptions option.
        _depth += 1
        bbox = DOMRect()
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
                    bbox.transform_self(matrix)
        else:
            settings = SVGPathDataSettings()
            settings.normalize = True
            path_data = self.get_transformed_path_data(settings)
            if len(path_data) > 0:
                bbox = PathParser.get_bbox(path_data, options)
        return bbox

    def get_ctm(self):
        """Returns the current transformation matrix (CTM). The matrix that
        transforms the current element's coordinate system to its SVG
        viewport's coordinate system.

        Returns:
            DOMMatrix: The current transformation matrix (CTM).
        """
        ctm = self._get_ctm(SVGElement.NEAREST_VIEWPORT)
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

    def get_screen_ctm(self):
        """Returns the current transformation matrix (CTM). The matrix that
        transforms the current element's coordinate system to the coordinate
        system of the SVG viewport for the SVG document fragment.

        Returns:
            DOMMatrix: The current transformation matrix (CTM).
        """
        ctm = self._get_ctm(SVGElement.FARTHEST_VIEWPORT)
        return ctm

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

    def get_viewport_transformation_matrix(self, recursive=True):
        """Returns the transformation matrix of an SVG viewport.

        Returns:
            DOMMatrix: The transformation matrix.
        """
        ctm = DOMMatrix()
        ex, ey, ew, eh = self.get_viewport_size(recursive)
        view_box = self.get_view_box(recursive)
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
        ctm.translate_self(tx.value(), ty.value())
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
