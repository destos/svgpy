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


from lxml import etree

from .base import HTMLElement, \
    HTMLHyperlinkElementUtils, HTMLMediaElement, \
    SVGAnimatedPoints, SVGElement, SVGFitToViewBox, \
    SVGGeometryElement, SVGGraphicsElement, SVGGradientElement, \
    SVGPathData, SVGPathDataSettings, SVGURIReference, SVGZoomAndPan
from .core import CSSUtils, SVGLength
from .dom import Comment, Element, LinkStyle, ProcessingInstruction
from .path import PathParser, SVGPathSegment
from .text import SVGTextContentElement, SVGTextPositioningElement
from .transform import SVGTransform, SVGTransformList
from .utils import get_element_by_id, get_elements_by_class_name, \
    get_elements_by_tag_name, get_elements_by_tag_name_ns


class HTMLAudioElement(HTMLMediaElement):
    """Represents the HTML <audio> element."""
    pass


class HTMLCanvasElement(HTMLElement):
    """Represents the HTML <canvas> element."""
    pass


class HTMLIFrameElement(HTMLElement):
    """Represents the HTML <iframe> element."""
    pass


class HTMLLinkElement(HTMLElement, LinkStyle):
    """Represents the HTML <link> element."""

    @property
    def as_(self):
        return self.attributes.get('as', '')

    @as_.setter
    def as_(self, value):
        self.attributes.set('as', value)

    @property
    def color(self):
        return self.attributes.get('color')

    @color.setter
    def color(self, value):
        self.attributes.set('color', value)

    @property
    def cross_origin(self):
        return self.attributes.get('crossorigin')

    @cross_origin.setter
    def cross_origin(self, value):
        self.attributes.set('crossorigin', value)

    @property
    def href(self):
        return self.attributes.get('href')

    @href.setter
    def href(self, value):
        self.attributes.set('href', value)

    @property
    def hreflang(self):
        return self.attributes.get('hreflang')

    @hreflang.setter
    def hreflang(self, value):
        self.attributes.set('hreflang', value)

    @property
    def integrity(self):
        return self.attributes.get('integrity')

    @integrity.setter
    def integrity(self, value):
        self.attributes.set('integrity', value)

    @property
    def media(self):
        return self.attributes.get('media', 'all')

    @media.setter
    def media(self, value):
        self.attributes.set('media', value)

    @property
    def referrer_policy(self):
        return self.attributes.get('referrerpolicy')

    @referrer_policy.setter
    def referrer_policy(self, value):
        self.attributes.set('referrerpolicy', value)

    @property
    def rel(self):
        return self.attributes.get('rel')

    @rel.setter
    def rel(self, value):
        self.attributes.set('rel', value)

    @property
    def rel_list(self):
        rel = self.rel
        if rel is None:
            return []
        return rel.split()

    @property
    def sizes(self):
        sizes = self.attributes.get('sizes')
        if sizes is None:
            return []
        return sizes.split()

    @property
    def title(self):
        return self.attributes.get('title')

    @title.setter
    def title(self, value):
        self.attributes.set('title', value)

    @property
    def type(self):
        return self.attributes.get('type')

    @type.setter
    def type(self, value):
        self.attributes.set('type', value)


class HTMLVideoElement(HTMLMediaElement):
    """Represents the HTML <video> element."""
    pass


class SVGAElement(SVGGraphicsElement,
                  SVGURIReference, HTMLHyperlinkElementUtils):
    # TODO: implement the SVGAElement.
    """Represents the SVG <a> element."""

    def get_path_data(self, settings=None):
        return []


class SVGCircleElement(SVGGeometryElement):
    """Represents the SVG <circle> element."""

    def get_computed_geometry(self):
        geometry = dict()
        attributes = self.attributes

        # 'cx' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        cx = SVGLength(attributes.get('cx', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['cx'] = cx

        # 'cy' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        cy = SVGLength(attributes.get('cy', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['cy'] = cy

        # 'r' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        r = SVGLength(attributes.get('r', '0'),
                      context=self,
                      direction=SVGLength.DIRECTION_UNSPECIFIED).value()
        geometry['r'] = r

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        geometry = self.get_computed_geometry()
        path_data = list()

        # 'r' property
        r = geometry['r']
        if r <= 0:
            return path_data

        # 'cx', 'cy' properties
        cx = geometry['cx']
        cy = geometry['cy']

        path_data.append(SVGPathSegment('M', cx + r, cy))
        path_data.append(SVGPathSegment('A', r, r, 0, 0, 1, cx, cy + r))
        path_data.append(SVGPathSegment('A', r, r, 0, 0, 1, cx - r, cy))
        path_data.append(SVGPathSegment('A', r, r, 0, 0, 1, cx, cy - r))
        path_data.append(SVGPathSegment('A', r, r, 0, 0, 1, cx + r, cy))
        path_data.append(SVGPathSegment('Z'))
        if settings is not None:
            if not isinstance(settings, SVGPathDataSettings):
                raise TypeError('Expected SVGPathDataSettings, got {}'.format(
                    type(settings)))
            if settings.normalize:
                path_data = PathParser.normalize(path_data)
        return path_data


class SVGClipPathElement(SVGElement):
    # TODO: implement the SVGClipPathElement.
    """Represents the SVG <clipPath> element."""
    pass


class SVGDefsElement(SVGGraphicsElement):
    """Represents the SVG <defs> element."""

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        return []


class SVGDescElement(SVGElement):
    """Represents the SVG <desc> element."""
    pass


class SVGEllipseElement(SVGGeometryElement):
    """Represents the SVG <ellipse> element."""

    def get_computed_geometry(self):
        geometry = dict()
        attributes = self.attributes

        # 'rx' property
        # Value: <length> | <percentage> | auto
        # Initial: auto
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        _rx = attributes.get('rx', 'auto')

        # 'ry' property
        # Value: <length> | <percentage> | auto
        # Initial: auto
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        _ry = attributes.get('ry', 'auto')

        if _rx != 'auto' and _ry == 'auto':
            _ry = _rx
        elif _rx == 'auto' and _ry != 'auto':
            _rx = _ry

        if _rx == 'auto' and _ry == 'auto':
            rx = 0
            ry = 0
        else:
            rx = SVGLength(_rx,
                           context=self,
                           direction=SVGLength.DIRECTION_HORIZONTAL).value()
            ry = SVGLength(_ry,
                           context=self,
                           direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['rx'] = rx
        geometry['ry'] = ry

        # 'cx' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        cx = SVGLength(attributes.get('cx', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['cx'] = cx

        # 'cy' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        cy = SVGLength(attributes.get('cy', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['cy'] = cy

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        style = self.get_computed_geometry()
        path_data = list()

        # 'rx', 'ry' properties
        rx = style['rx']
        ry = style['ry']
        if rx <= 0 or ry <= 0:
            return path_data

        # 'cx', 'cy' properties
        cx = style['cx']
        cy = style['cy']

        path_data.append(SVGPathSegment('M', cx + rx, cy))
        path_data.append(SVGPathSegment('A', rx, ry, 0, 0, 1, cx, cy + ry))
        path_data.append(SVGPathSegment('A', rx, ry, 0, 0, 1, cx - rx, cy))
        path_data.append(SVGPathSegment('A', rx, ry, 0, 0, 1, cx, cy - ry))
        path_data.append(SVGPathSegment('A', rx, ry, 0, 0, 1, cx + rx, cy))
        path_data.append(SVGPathSegment('Z'))
        if settings is not None:
            if not isinstance(settings, SVGPathDataSettings):
                raise TypeError('Expected SVGPathDataSettings, got {}'.format(
                    type(settings)))
            if settings.normalize:
                path_data = PathParser.normalize(path_data)
        return path_data


class SVGForeignObjectElement(SVGGraphicsElement):
    # TODO: implement the SVGForeignObjectElement.
    """Represents the SVG <foreignObject> element."""
    pass


class SVGGElement(SVGGraphicsElement):
    """Represents the SVG <g> element."""

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list(SVGPathSegment): A list of path segments.
        """
        return self.get_descendant_path_data(settings)


class SVGHatchElement(SVGElement):
    """Represents the SVG <hatch> element."""
    pass


class SVGHatchpathElement(SVGElement):
    """Represents the SVG <hatchpath> element."""
    pass


class SVGImageElement(SVGGraphicsElement, SVGURIReference):
    # TODO: implement the SVGImageElement.
    """Represents the SVG <image> element."""
    pass


class SVGLinearGradientElement(SVGGradientElement):
    """Represents the SVG <linearGradient> element."""
    pass


class SVGLineElement(SVGGeometryElement):
    """Represents the SVG <line> element."""

    def get_computed_geometry(self):
        geometry = dict()
        attributes = self.attributes

        # 'x1', 'y1' properties
        # Value: <length> | <percentage> | <number>
        # Initial: 0
        x1 = SVGLength(attributes.get('x1', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['x1'] = x1

        y1 = SVGLength(attributes.get('y1', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['y1'] = y1

        # 'x2', 'y2' properties
        # Value: <length> | <percentage> | <number>
        # Initial: 0
        x2 = SVGLength(attributes.get('x2', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['x2'] = x2

        y2 = SVGLength(attributes.get('y2', '0'),
                       context=self,
                       direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['y2'] = y2

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        geometry = self.get_computed_geometry()
        path_data = list()

        # 'x1', 'y1', 'x2', 'y2' properties
        x1 = geometry['x1']
        y1 = geometry['y1']
        x2 = geometry['x2']
        y2 = geometry['y2']
        if (SVGLength(x2 - x1) == SVGLength(0)
                and SVGLength(y2 - y1) == SVGLength(0)):
            return path_data

        path_data.append(SVGPathSegment('M', x1, y1))
        path_data.append(SVGPathSegment('L', x2, y2))
        return path_data


class SVGMarkerElement(SVGGraphicsElement):
    # TODO: implement the SVGMarkerElement.
    """Represents the SVG <marker> element."""
    pass


class SVGMeshElement(SVGGeometryElement):
    # TODO: implement the SVGMeshElement.
    """Represents the SVG <mesh> element."""

    def get_path_data(self, settings=None):
        return []


class SVGMeshGradientElement(SVGGradientElement):
    """Represents the SVG <mesh> element."""
    pass


class SVGMeshpatchElement(SVGElement):
    """Represents the SVG <meshpatch> element."""
    pass


class SVGMeshrowElement(SVGElement):
    """Represents the SVG <meshrow> element."""
    pass


class SVGMetadataElement(SVGElement):
    """Represents the SVG <metadata> element."""
    pass


class SVGPathElement(SVGGeometryElement, SVGPathData):
    """Represents the SVG <path> element."""

    def get_computed_geometry(self):
        geometry = dict()

        # 'd' property
        # Value: none | <string>
        # Initial: none
        # Inherited: no
        # Percentages: N/A
        d = self.attributes.get('d', 'none')
        if d == 'none' or len(d) == 0:
            d = None
        geometry['d'] = d

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        geometry = self.get_computed_geometry()
        d = geometry['d']
        if d is None:
            return []
        path_data = PathParser.parse(d)
        if settings is not None:
            if not isinstance(settings, SVGPathDataSettings):
                raise TypeError('Expected SVGPathDataSettings, got {}'.format(
                    type(settings)))
            if settings.normalize:
                path_data = PathParser.normalize(path_data)
        return path_data


class SVGPatternElement(SVGGraphicsElement, SVGFitToViewBox, SVGURIReference):
    # TODO: implement the SVGPatternElement.
    """Represents the SVG <pattern> element."""

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        return []


class SVGPolygonElement(SVGGeometryElement, SVGAnimatedPoints):
    """Represents the SVG <polygon> element."""

    def get_computed_geometry(self):
        geometry = dict()

        # 'points' property
        geometry['points'] = self.points

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        geometry = self.get_computed_geometry()
        path_data = list()

        points = geometry['points']
        if len(points) == 0:
            return path_data

        x, y = points.pop(0)
        path_data.append(SVGPathSegment('M', x, y))
        if len(points) > 0:
            for x, y in iter(points):
                path_data.append(SVGPathSegment('L', x, y))
            path_data.append(SVGPathSegment('Z'))
        return path_data


class SVGPolylineElement(SVGGeometryElement, SVGAnimatedPoints):
    """Represents the SVG <polyline> element."""

    def get_computed_geometry(self):
        geometry = dict()

        # 'points' property
        geometry['points'] = self.points

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        geometry = self.get_computed_geometry()
        path_data = list()

        points = geometry['points']
        if len(points) == 0:
            return path_data

        x, y = points.pop(0)
        path_data.append(SVGPathSegment('M', x, y))
        if len(points) > 0:
            for x, y in iter(points):
                path_data.append(SVGPathSegment('L', x, y))
        return path_data


class SVGRadialGradientElement(SVGGradientElement):
    """Represents the SVG <radialGradient> element."""
    pass


class SVGRectElement(SVGGeometryElement):
    """Represents the SVG <rect> element."""

    def get_computed_geometry(self):
        geometry = dict()
        attributes = self.attributes

        # 'width' property
        # Value: <length> | <percentage> | auto | inherit
        # Initial: auto => 0
        # Inherited: no
        # Percentages: refer to width of containing block
        _width, context = CSSUtils.get_value(self, 'width', 'auto')
        width = SVGLength(_width,
                          context=context,
                          direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['width'] = width

        # 'height' property
        # Value: <length> | <percentage> | auto | inherit
        # Initial: auto => 0
        # Inherited: no
        # Percentages: refer to height of containing block
        _height, context = CSSUtils.get_value(self, 'height', 'auto')
        height = SVGLength(_height,
                           context=context,
                           direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['height'] = height

        # 'rx' property
        # Value: <length> | <percentage> | auto
        # Initial: auto
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        _rx = attributes.get('rx', 'auto')

        # 'ry' property
        # Value: <length> | <percentage> | auto
        # Initial: auto
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        _ry = attributes.get('ry', 'auto')

        if _rx == 'auto' and _ry == 'auto':
            rx = 0
            ry = 0
        else:
            if _rx == 'auto':
                rx = 0
            else:
                rx = SVGLength(
                    _rx,
                    context=self,
                    direction=SVGLength.DIRECTION_HORIZONTAL).value()

            if _ry == 'auto':
                ry = 0
            else:
                ry = SVGLength(
                    _ry,
                    context=self,
                    direction=SVGLength.DIRECTION_VERTICAL).value()

            if _rx != 'auto' and _ry == 'auto':
                ry = rx
            elif _rx == 'auto' and _ry != 'auto':
                rx = ry

            if rx > width / 2:
                rx = width / 2
            if ry > height / 2:
                ry = height / 2

        geometry['rx'] = rx
        geometry['ry'] = ry

        # 'x' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        x = SVGLength(attributes.get('x', '0'),
                      context=self,
                      direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['x'] = x

        # 'y' property
        # Value: <length> | <percentage>
        # Initial: 0
        # Inherited: no
        # Percentages: refer to the size of the current SVG viewport
        y = SVGLength(attributes.get('y', '0'),
                      context=self,
                      direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['y'] = y

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        geometry = self.get_computed_geometry()
        path_data = list()

        w = geometry['width']
        h = geometry['height']
        if w <= 0 or h <= 0:
            return path_data

        x = geometry['x']
        y = geometry['y']
        square_corners = False
        rx = geometry['rx']
        ry = geometry['ry']
        if rx <= 0 or ry <= 0:
            square_corners = True
            rx = 0
            ry = 0

        path_data.append(SVGPathSegment('M', x + rx, y))
        path_data.append(SVGPathSegment('H', x + w - rx))
        if not square_corners:
            path_data.append(SVGPathSegment('A',
                                            rx, ry, 0, 0, 1, x + w, y + ry))
        path_data.append(SVGPathSegment('V', y + h - ry))
        if not square_corners:
            path_data.append(SVGPathSegment(
                'A',
                rx, ry, 0, 0, 1, x + w - rx, y + h))
        path_data.append(SVGPathSegment('H', x + rx))
        if not square_corners:
            path_data.append(SVGPathSegment('A',
                                            rx, ry, 0, 0, 1, x, y + h - ry))
        path_data.append(SVGPathSegment('V', y + ry))
        if not square_corners:
            path_data.append(SVGPathSegment('A', rx, ry, 0, 0, 1, x + rx, y))
        path_data.append(SVGPathSegment('Z'))
        if settings is not None:
            if not isinstance(settings, SVGPathDataSettings):
                raise TypeError('Expected SVGPathDataSettings, got {}'.format(
                    type(settings)))
            if settings.normalize:
                path_data = PathParser.normalize(path_data)
        return path_data


class SVGScriptElement(SVGElement, SVGURIReference):
    """Represents the SVG <script> element."""
    pass


class SVGSolidcolorElement(SVGElement):
    """Represents the SVG <solidcolor> element."""
    pass


class SVGStopElement(SVGElement):
    """Represents the SVG <stop> element."""
    pass


class SVGStyleElement(SVGElement, LinkStyle):
    """Represents the SVG <style> element."""

    @property
    def media(self):
        return self.attributes.get('media', 'all')

    @media.setter
    def media(self, value):
        self.attributes.set('media', value)

    @property
    def title(self):
        return self.attributes.get('title')

    @title.setter
    def title(self, value):
        self.attributes.set('title', value)

    @property
    def type(self):
        return self.attributes.get('type', 'text/css')

    @type.setter
    def type(self, value):
        self.attributes.set('type', value)


class SVGSVGElement(SVGGraphicsElement, SVGFitToViewBox, SVGZoomAndPan):
    """Represents the SVG <svg> element."""

    def _init(self):
        super()._init()
        self._current_scale = 1
        self._current_translate = 0, 0

    @property
    def current_scale(self):
        """float: The current scale for the 'svg' element."""
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) != hash(self):
            return 1
        return self._current_scale

    @current_scale.setter
    def current_scale(self, scale):
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) != hash(self):
            return
        self._current_scale = scale

    @property
    def current_translate(self):
        """tuple[float, float]: The current translation for the 'svg' element.
        """
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) != hash(self):
            return 0, 0
        return self._current_translate

    @current_translate.setter
    def current_translate(self, translate):
        farthest = self.get_farthest_svg_element()
        if farthest is not None and hash(farthest) != hash(self):
            return
        self._current_translate = translate

    def get_computed_geometry(self):
        geometry = dict()

        vpx, vpy, vpw, vph = self.get_viewport_size()
        geometry['x'] = vpx.value()
        geometry['y'] = vpy.value()
        geometry['width'] = vpw.value()
        geometry['height'] = vph.value()

        return geometry

    def get_element_by_id(self, element_id, namespaces=None):
        """Finds the first matching sub-element, by id.

        Arguments:
            element_id (str): The id of the element.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            Element: The first matching sub-element. Returns None if there is
                no such element.
        """
        return get_element_by_id(self, element_id, namespaces=namespaces)

    def get_elements_by_class_name(self, class_names, namespaces=None):
        """Reimplemented from Element.get_elements_by_class_name().

        Finds all matching sub-elements, by class names.

        Arguments:
            class_names (str): A list of class names that are separated by
                whitespace.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_class_name(self,
                                          class_names,
                                          namespaces=namespaces,
                                          include_self=True)

    def get_elements_by_tag_name(self, qualified_name, namespaces=None):
        """Reimplemented from Element.get_elements_by_tag_name().

        Finds all matching sub-elements, by the qualified name.

        Arguments:
            qualified_name (str): The qualified name or '*'.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_tag_name(self,
                                        qualified_name,
                                        namespaces=namespaces,
                                        include_self=True)

    def get_elements_by_tag_name_ns(self,
                                    namespace, local_name, namespaces=None):
        """Reimplemented from Element.get_elements_by_tag_name_ns().

        Finds all matching sub-elements, by the namespace URI and the local
        name.

        Arguments:
            namespace (str, None): The namespace URI, '*' or None.
            local_name (str): The local name or '*'.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_tag_name_ns(self,
                                           namespace,
                                           local_name,
                                           namespaces=namespaces,
                                           include_self=True)

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        return self.get_descendant_path_data(settings)


class SVGSwitchElement(SVGGraphicsElement):
    # TODO: implement the SVGSwitchElement.
    """Represents the SVG <switch> element."""
    pass


class SVGSymbolElement(SVGGraphicsElement, SVGFitToViewBox):
    # TODO: implement the SVGSymbolElement.
    """Represents the SVG <symbol> element."""

    def get_computed_geometry(self):
        geometry = dict()

        vpx, vpy, vpw, vph = self.get_viewport_size()
        geometry['x'] = vpx.value()
        geometry['y'] = vpy.value()
        geometry['width'] = vpw.value()
        geometry['height'] = vph.value()

        attributes = self.attributes
        ref_x = attributes.get('refX')
        if ref_x is not None and ref_x not in ['left', 'center', 'right']:
            ref_x = SVGLength(ref_x,
                              context=self,
                              direction=SVGLength.DIRECTION_HORIZONTAL).value()
        geometry['refX'] = ref_x

        ref_y = attributes.get('refY')
        if ref_y is not None and ref_y not in ['top', 'center', 'bottom']:
            ref_y = SVGLength(ref_y,
                              context=self,
                              direction=SVGLength.DIRECTION_VERTICAL).value()
        geometry['refY'] = ref_y

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        return []


class SVGTextElement(SVGTextPositioningElement):
    """Represents the SVG <text> element."""
    pass


class SVGTextPathElement(SVGTextContentElement):
    # TODO: implement the SVGTextPathElement.
    """Represents the SVG <textPath> element."""
    pass


class SVGTitleElement(SVGElement):
    """Represents the SVG <title> element."""
    pass


class SVGTSpanElement(SVGTextPositioningElement):
    """Represents the SVG <tspan> element."""
    pass


class SVGUseElement(SVGGraphicsElement, SVGURIReference):
    """Represents the SVG <use> element."""

    @property
    def instance_root(self):
        href = self.href
        if href is None or len(href) == 0:
            return None
        elif href[0] != '#':
            # TODO: support external link.
            raise NotImplementedError(href)
        root = self.getroottree().getroot()
        element = root.get_element_by_id(href[1:])
        return element

    def get_computed_geometry(self):
        geometry = dict()
        attributes = self.attributes

        geometry['x'] = SVGLength(
            attributes.get('x', '0'),
            context=self,
            direction=SVGLength.DIRECTION_HORIZONTAL).value()

        geometry['y'] = SVGLength(
            attributes.get('y', '0'),
            context=self,
            direction=SVGLength.DIRECTION_VERTICAL).value()

        # 'width' property
        # Value: <length> | <percentage> | auto | inherit
        # Initial: auto => 0
        # Inherited: no
        # Percentages: refer to width of containing block
        _width, context = CSSUtils.get_value(self, 'width', 'auto')
        geometry['width'] = SVGLength(
            _width,
            context=context,
            direction=SVGLength.DIRECTION_HORIZONTAL).value()

        # 'height' property
        # Value: <length> | <percentage> | auto | inherit
        # Initial: auto => 0
        # Inherited: no
        # Percentages: refer to height of containing block
        _height, context = CSSUtils.get_value(self, 'height', 'auto')
        geometry['height'] = SVGLength(
            _height,
            context=context,
            direction=SVGLength.DIRECTION_VERTICAL).value()

        return geometry

    def get_path_data(self, settings=None):
        """Returns a list of path segments that corresponds to the path data.

        Arguments:
            settings (SVGPathDataSettings, optional): If normalize is set to
                True then the returned list of path segments is converted to
                the base set of absolute commands ('M', 'L', 'C' and 'Z').
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        root = self.instance_root
        if root is None or not isinstance(root, SVGGraphicsElement):
            return []
        path_data = root.get_path_data(settings)

        transform_list = self.transform
        if transform_list is None:
            transform_list = SVGTransformList()

        geometry = self.get_computed_geometry()
        x = geometry['x']
        y = geometry['y']
        if x != 0 or y != 0:
            transform = SVGTransform()
            transform.set_translate(x, y)
            transform_list.append(transform)
        if root.local_name in ['svg', 'symbol']:
            # TODO: test 'width' and 'height' properties on the 'use' element.
            width = geometry['width']
            height = geometry['height']
            if width > 0 or height > 0:
                bbox = PathParser.get_bbox(path_data)
                sx = width / bbox.width
                if sx == 0:
                    sx = 1
                sy = height / bbox.height
                if sy == 0:
                    sy = 1
                transform = SVGTransform()
                transform.set_scale(sx, sy)
                transform_list.append(transform)
        if len(transform_list) > 0:
            matrix = transform_list.matrix
            path_data = PathParser.transform(path_data, matrix)
        return path_data


class SVGViewElement(SVGGraphicsElement, SVGFitToViewBox, SVGZoomAndPan):
    # TODO: implement the SVGViewElement.
    """Represents the SVG <view> element."""
    pass


class SVGElementClassLookup(etree.CustomElementClassLookup):
    ELEMENT_CLASS_MAP = {
        'a': SVGAElement,
        'audio': HTMLAudioElement,
        'canvas': HTMLCanvasElement,
        'circle': SVGCircleElement,
        # 'clipPath': SVGClipPathElement,
        'defs': SVGDefsElement,
        'desc': SVGDescElement,
        'ellipse': SVGEllipseElement,
        # 'foreignObject': SVGForeignObjectElement,
        'g': SVGGElement,
        'hatch': SVGHatchElement,
        'hatchpath': SVGHatchpathElement,
        'iframe': HTMLIFrameElement,
        'line': SVGLineElement,
        'linearGradient': SVGLinearGradientElement,
        'link': HTMLLinkElement,
        'marker': SVGMarkerElement,
        # 'mesh': SVGMeshElement,
        'meshgradient': SVGMeshGradientElement,
        'meshpatch': SVGMeshpatchElement,
        'meshrow': SVGMeshrowElement,
        'metadata': SVGMetadataElement,
        'path': SVGPathElement,
        'pattern': SVGPatternElement,
        'polygon': SVGPolygonElement,
        'polyline': SVGPolylineElement,
        'radialGradient': SVGRadialGradientElement,
        'rect': SVGRectElement,
        'script': SVGScriptElement,
        'solidcolor': SVGSolidcolorElement,
        'stop': SVGStopElement,
        'style': SVGStyleElement,
        'svg': SVGSVGElement,
        # 'switch': SVGSwitchElement,
        'symbol': SVGSymbolElement,
        'text': SVGTextElement,
        'textPath': SVGTextPathElement,
        'title': SVGTitleElement,
        'tspan': SVGTSpanElement,
        'use': SVGUseElement,
        'video': HTMLVideoElement,
        'view': SVGViewElement,
    }

    def lookup(self, node_type, document, namespace, name):
        _ = document
        if node_type == 'element':
            default = (HTMLElement if namespace == Element.XHTML_NAMESPACE_URI
                       else SVGElement)
            return SVGElementClassLookup.ELEMENT_CLASS_MAP.get(name, default)
        elif node_type == 'comment':
            return Comment
        elif node_type == 'PI':
            return ProcessingInstruction
        return None  # pass on to (default) fallback

    @staticmethod
    def update(other):
        SVGElementClassLookup.ELEMENT_CLASS_MAP.update(other)


class SVGParser(object):
    def __init__(self, **kwargs):
        """Constructs an SVGParser object.

        Arguments:
            **kwargs: See lxml.etree.XMLParser.__init__().
        """
        self._parser = etree.XMLParser(**kwargs)
        self._parser.set_element_class_lookup(SVGElementClassLookup())
        etree.set_default_parser(self._parser)

    @property
    def parser(self):
        """lxml.etree.XMLParser: The XML parser."""
        return self._parser

    def create_comment(self, data):
        """Creates a new comment instance, and returns it.
        See also Document.create_comment().

        Arguments:
            data (str): A string of the comment.
        Returns:
            Comment: A new comment.
        """
        _ = self
        comment = etree.Comment(data)
        return comment

    def create_element(self, local_name, attrib=None, nsmap=None, **_extra):
        """Creates a new element instance, and returns it.
        See also SVGParser.create_element_ns(), Document.create_element(),
        Document.create_element_ns(), Element.create_sub_element() and
        Element.create_sub_element_ns().

        Arguments:
            local_name (str): A local name of an element to be created.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        if local_name == 'svg' or local_name.endswith('}svg'):
            if nsmap is None:
                nsmap = dict()
            if None not in nsmap:
                nsmap[None] = Element.SVG_NAMESPACE_URI
        element = self._parser.makeelement(local_name,
                                           attrib=attrib,
                                           nsmap=nsmap,
                                           **_extra)
        return element

    def create_element_ns(self,
                          namespace, qualified_name, attrib=None, nsmap=None,
                          **_extra):
        """Creates a new element instance with the specified namespace URI,
        and returns it.
        See also SVGParser.create_element(), Document.create_element(),
        Document.create_element_ns(), Element.create_sub_element() and
        Element.create_sub_element_ns().

        Arguments:
            namespace (str, None): The namespace URI to associated with the
                element or None.
            qualified_name (str): A qualified name of an element to be created.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        Examples:
            >>> from svgpy import SVGParser
            >>> parser = SVGParser()
            >>> element = parser.create_element_ns('http://www.w3.org/1999/xhtml', 'source')
            >>> element.tag
            '{http://www.w3.org/1999/xhtml}source'
            >>> element.node_name
            'html:source'
            >>> element.tag_name
            'html:source'
            >>> element.local_name
            'source'
        """
        if namespace is not None:
            tag = '{{{0}}}{1}'.format(namespace, qualified_name)
        else:
            tag = qualified_name
        element = self.create_element(tag,
                                      attrib=attrib,
                                      nsmap=nsmap,
                                      **_extra)
        return element

    def create_processing_instruction(self, target, data=None):
        """Creates a new ProcessingInstruction node, and returns it.

        Arguments:
            target (str): The target of this processing instruction.
            data (str, optional): The content of this processing instruction.
        Returns:
            ProcessingInstruction: A new ProcessingInstruction node.
        Examples:
            >>> from svgpy import SVGParser
            >>> parser = SVGParser()
            >>> pi = parser.create_processing_instruction('xml-stylesheet', 'href="style.css" media="print"')
            >>> pi.tostring()
            b'<?xml-stylesheet href="style.css" media="print"?>'
        """
        _ = self
        pi = etree.ProcessingInstruction(target, data)
        return pi

    def fromstring(self, text):
        """Parses an SVG document or fragment from a string, and returns the
        root node.

        Arguments:
            text (str): An SVG document.
        Returns:
            Element: A root node of the ElementTree.
        """
        root = etree.fromstring(text, parser=self._parser)
        return root

    def parse(self, source):
        """Parses the source into an ElementTree object, and returns it.
        To parse from a string, use the fromstring() method instead.

        Arguments:
            source (file, str): A filename or a file object of an SVG document.
        Returns:
            lxml.etree._ElementTree: An ElementTree object.
        """
        tree = etree.parse(source, parser=self._parser)
        return tree
