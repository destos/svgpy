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
import math
import re

import numpy as np
from scipy.integrate import quad
from scipy.special import ellipeinc

from .core import SVGLength
from .formatter import format_number_sequence, to_coordinate_pair_sequence
from .freetype import FTMatrix
from .geometry.matrix import DOMMatrix
from .geometry.rect import DOMRect


def get_angle(y, x):
    """Returns the angle in degrees."""
    d = math.degrees(math.atan2(y, x))
    if y > 0:
        d = 360 - d
    elif y < 0:
        d = -d
    return d


class CubicBezierCurve(object):
    def __init__(self, p0, p1, p2, p3):
        """Constructs a CubicBezierCurve object.

        Arguments:
            p0 (numpy.array): The absolute coordinates of the starting point
                of the cubic bezier curve.
            p1 (numpy.array): The absolute coordinates of the control point
                at the beginning of the cubic bezier curve.
            p2 (numpy.array): The absolute coordinates of the control point
                at the end of the cubic bezier curve.
            p3 (numpy.array): The absolute coordinates of the end point of the
                cubic bezier curve.
        """
        self._p0 = p0
        self._p1 = p1
        self._p2 = p2
        self._p3 = p3

    @staticmethod
    def _get_length_integrand(t, c0, c1, c2, c3, c4):
        # use Hartmut Henkel method
        # See http://www.circuitwizard.de/metapost/arclength.pdf
        return math.sqrt(c4 * t ** 4 + c3 * t ** 3 + c2 * t ** 2 + c1 * t + c0)

    def get_bbox(self, options=None, **extra):
        """Returns the bounding box of the cubic bezier curve.

        Arguments:
            options (SVGBoundingBoxOptions, optional): Reserved.
            **extra: Reserved.
        Returns:
            DOMRect: The bounding box of the cubic bezier curve.
        """
        # TODO: implement the SVGBoundingBoxOptions option.
        x1, y1 = self._p0
        x2, y2 = self._p3
        points = list()
        points.append([x1, y1])
        points.append([x2, y2])

        roots = self.get_roots()
        for t in roots:
            x, y = self.point(t)
            points.append([x, y])

        a = np.array(points)
        x_sequence = a[:, 0]
        y_sequence = a[:, 1]
        x = min(x_sequence)
        y = min(y_sequence)
        width = max(x_sequence) - x
        height = max(y_sequence) - y
        return DOMRect(x, y, width, height)

    def get_coefficients(self):
        """Calculates the coefficients for a cubic polynomial equation."""
        a = -self._p0 + 3 * self._p1 - 3 * self._p2 + self._p3
        b = 3 * self._p0 - 6 * self._p1 + 3 * self._p2
        c = -3 * self._p0 + 3 * self._p1
        d = self._p0
        return a, b, c, d

    def get_length(self):
        """Returns the length of the bezier curve.

        Returns:
            float: The length of the bezier curve.
        """
        # use Hartmut Henkel method
        # See http://www.circuitwizard.de/metapost/arclength.pdf
        v3, v2, v1, _ = self.get_coefficients()
        # v3 = -p0 + 3 * p1 - 3 * p2 + p3
        # v2 = 3 * (p0 - 2 * p1 + p2)
        # v1 = 3 * (p1 - p0)
        a1, b1 = v1
        a2, b2 = v2
        a3, b3 = v3
        c4 = 9 * (a3 ** 2 + b3 ** 2)
        c3 = 12 * (a3 * a2 + b3 * b2)
        c2 = 6 * (a3 * a1 + b3 * b1) + 4 * (a2 ** 2 + b2 ** 2)
        c1 = 4 * (a2 * a1 + b2 * b1)
        c0 = a1 ** 2 + b1 ** 2
        result = quad(CubicBezierCurve._get_length_integrand,
                      0, 1,
                      args=(c0, c1, c2, c3, c4))
        return result[0]

    def get_roots(self):
        # See http://floris.briolas.nl/floris/2009/10/bounding-box-of-cubic-bezier/
        def _solve(_a, _b, _c, _s):
            # {-b + sqrt(b^2 - 4ac) / (2a)} or {-b - sqrt(b^2 - 4ac) / (2a)}
            s = 1 if _s else -1
            return (-_b + s * math.sqrt(_b ** 2 - 4 * _a * _c)) / (2 * _a)

        roots = list()
        coefficients = self.get_coefficients()
        a = 3 * coefficients[0]
        b = 2 * coefficients[1]
        c = coefficients[2]
        for i in range(0, 2):
            d = b[i] ** 2 - 4 * a[i] * c[i]
            if d < 0:
                continue
            if a[i] == 0 and b[i] != 0:
                roots.append(-c[i] / b[i])
            elif d == 0 and a[i] != 0:
                roots.append(_solve(a[i], b[i], c[i], True))
            elif a[i] != 0:
                roots.append(_solve(a[i], b[i], c[i], True))
                roots.append(_solve(a[i], b[i], c[i], False))
        return filter(lambda t: 0 <= t <= 1, roots)

    def point(self, t):
        a, b, c, d = self.get_coefficients()
        pt = a * t ** 3 + b * t ** 2 + c * t + d
        return pt.item(0), pt.item(1)


class Ellipse(object):
    def __init__(self, cx, cy, rx, ry, x_axis_rotation=0):
        """Constructs an Ellipse object.

        Arguments:
            cx (float): The absolute x-coordinate of the center of the ellipse.
            cy (float): The absolute y-coordinate of the center of the ellipse.
            rx (float): The horizontal radii of the ellipse.
            ry (float): The vertical radii of the ellipse.
            x_axis_rotation (float, optional): The angle from the x-axis of
                the ellipse in degrees.
        """
        self._cx = cx
        self._cy = cy
        self._rx = rx
        self._ry = ry
        self._x_axis_rotation = x_axis_rotation

    def get_length(self, start, delta):
        """Returns the arc length of the ellipse.

        Arguments:
            start (float): The start angle of the elliptical arc in degrees.
            delta (float): The difference between the start and the end angle
                of the arc in degrees.
        Returns:
            float: The arc length of the ellipse.
        """

        def _get_arc_length(_rx, _ry, _angle):
            """Returns the arc length of the ellipse.

            Arguments:
                _rx (float): The horizontal radii of the ellipse.
                _ry (float): The vertical radii of the ellipse.
                _angle (float): The angle is in the range of >=0 to <=90 in
                    degrees.
            Returns:
                float: The arc length of the ellipse.
            """
            if _rx == 0 or _ry == 0:
                return 0
            _t = math.radians(_angle)
            _phi = math.atan(_rx / _ry * math.tan(_t))
            _m = 1 - (_rx / _ry) ** 2
            _s = _ry * ellipeinc(_phi, _m)
            return _s

        if self._rx == 0 or self._ry == 0:
            return 0

        # 0 <= start <= 360
        while start > 360:
            start -= 360
        while start < 0:
            start += 360

        # 0 <= end <= 360
        end = start + delta
        while end > 360:
            end -= 360
        while end < 0:
            end += 360

        if start == end:
            return 0

        if delta < 0:
            start, end = end, start

        n1 = start // 90
        a1 = start % 90  # 0 <= a1 < 90
        n2 = end // 90
        a2 = end % 90  # 0 <= a2 < 90
        s0 = _get_arc_length(self._rx, self._ry, 90)
        s2 = n2 * s0
        if a2 > 0:
            if (90 < end <= 180) or (270 < end <= 360):
                s2 += s0 - _get_arc_length(self._rx, self._ry, 90 - a2)
            else:
                s2 += _get_arc_length(self._rx, self._ry, a2)
        s1 = n1 * s0
        if a1 > 0:
            if (90 < start <= 180) or (270 < start <= 360):
                s1 += s0 - _get_arc_length(self._rx, self._ry, 90 - a1)
            else:
                s1 += _get_arc_length(self._rx, self._ry, a1)
        if start < end:
            return s2 - s1
        return 4 * s0 - s1 + s2

    def point(self, angle):
        r = math.radians(self._x_axis_rotation)
        angle = angle % 360
        angle = -angle
        t = math.radians(angle)
        p = np.array([[math.cos(r), -math.sin(r)],
                      [math.sin(r), math.cos(r)]]).dot(
            np.array([[self._rx * math.cos(t)],
                      [self._ry * math.sin(t)]]))
        p += np.array([[self._cx],
                       [self._cy]])
        return p.item(0), p.item(1)


class SVGPathSegment(object):
    TYPE_UNKNOWN = None
    TYPE_BEARING_ABS = 'B'
    TYPE_BEARING_REL = 'b'
    TYPE_CLOSEPATH_ABS = 'Z'
    TYPE_CLOSEPATH_REL = 'z'
    TYPE_CURVETO_ABS = 'C'
    TYPE_CURVETO_REL = 'c'
    TYPE_CATMULL_ROM_ABS = 'R'
    TYPE_CATMULL_ROM_REL = 'r'
    TYPE_ELLIPTICAL_ARC_ABS = 'A'
    TYPE_ELLIPTICAL_ARC_REL = 'a'
    TYPE_HORIZONTAL_LINETO_ABS = 'H'
    TYPE_HORIZONTAL_LINETO_REL = 'h'
    TYPE_LINETO_ABS = 'L'
    TYPE_LINETO_REL = 'l'
    TYPE_MOVETO_ABS = 'M'
    TYPE_MOVETO_REL = 'm'
    TYPE_QUADRATIC_CURVETO_ABS = 'Q'
    TYPE_QUADRATIC_CURVETO_REL = 'q'
    TYPE_SMOOTH_CURVETO_ABS = 'S'
    TYPE_SMOOTH_CURVETO_REL = 's'
    TYPE_SMOOTH_QUADRATIC_CURVETO_ABS = 'T'
    TYPE_SMOOTH_QUADRATIC_CURVETO_REL = 't'
    TYPE_VERTICAL_LINETO_ABS = 'V'
    TYPE_VERTICAL_LINETO_REL = 'v'

    def __init__(self, path_type=None, *values):
        self._path_type = path_type
        self._values = values

    def __eq__(self, other):
        if not isinstance(other, SVGPathSegment):
            return NotImplemented
        return (self._path_type == other._path_type
                and self._values == other._values)

    def __repr__(self):
        return '<{} object at {} ({} {})>'.format(
            type(self).__name__, hex(id(self)),
            '\'{}\''.format(self._path_type) if self._path_type is not None
            else self._path_type,
            self._values)

    @property
    def end(self):
        """tuple[float, float]: The coordinates of the end point on the path
        segment.
        """
        if not self.isvalid():
            return None, None
        path_type = self._path_type
        if path_type in 'Aa':
            # 'A'|'a' (rx ry x-axis-rotation large-arc-flag sweep-flag x,y)+
            return tuple(self._values[5:])
        elif path_type in 'BbZz':
            return None, None
        elif path_type in 'Cc':
            # 'C'|'c' (x1,y1 x2,y2 x,y)+
            return tuple(self._values[4:])
        elif path_type == 'H':
            # 'H'|'h' x+
            return self._values[0], None
        elif path_type == 'h':
            # 'H'|'h' x+
            return self._values[0], 0
        elif path_type in 'LlMmTt':
            # 'L'|'l' (x,y)+
            # 'M'|'m' (x,y)+
            # 'T'|'t' (x,y)+
            return tuple(self._values)
        elif path_type in 'QqSs':
            # 'Q'|'q' (x1,y1 x,y)+
            # 'S'|'s' (x2,y2 x,y)+
            return tuple(self._values[2:])
        elif path_type == 'V':
            # 'V'|'v' y+
            return None, self._values[0]
        elif path_type == 'v':
            # 'V'|'v' y+
            return 0, self._values[0]
        raise NotImplementedError('Unsupported path type: ' + repr(path_type))

    @property
    def type(self):
        """str: The type of the path segment."""
        return self._path_type

    @property
    def values(self):
        """tuple[float, ...]: The values corresponding to the path segment."""
        return self._values

    def _tostring1(self):
        # command x+
        coordinate_sequence = format_number_sequence(self._values)
        return '{}{}'.format(self._path_type, ' '.join(coordinate_sequence))

    def _tostring2(self):
        # command (x,y)+
        coordinate_pair = format_number_sequence(self._values)
        return '{}{}'.format(self._path_type,
                             ','.join(coordinate_pair))

    def _tostring2n(self):
        # command (x,y ...)+
        coordinate_pair_sequence = list()
        for xy in to_coordinate_pair_sequence(self._values):
            coordinate_pair = format_number_sequence(xy)
            coordinate_pair_sequence.append(','.join(coordinate_pair))
        return '{}{}'.format(self._path_type,
                             ' '.join(coordinate_pair_sequence))

    def get_bearing(self, bearing):
        """Returns the current bearing.

        Arguments:
            bearing (float): The current bearing.
        Returns:
            float: The new bearing.
        """
        if not self.isvalid() or self._path_type not in 'Bb':
            return bearing
        elif self.isabsolute():
            return self._values[0]
        return bearing + self._values[0]

    def isabsolute(self):
        if self._path_type is None:
            return None
        return self._path_type.isupper()

    def isrelative(self):
        if self._path_type is None:
            return None
        return self._path_type.islower()

    def isvalid(self):
        return (self._path_type is not None
                and (self._path_type in 'Zz'
                     or (self._path_type in PathParser.PATH_SEGMENT_TYPES
                         and self._values is not None
                         and len(self._values) > 0)))

    def set_bearing_abs(self, angle):
        """Sets the absolute bearing.

        Arguments:
            angle (float): The current bearing.
        """
        self._path_type = 'B'
        self._values = (float(angle),)

    def set_bearing_rel(self, angle):
        """Sets the relative bearing.

        Arguments:
            angle (float): The current bearing.
        """
        self._path_type = 'b'
        self._values = (float(angle),)

    def set_curveto_abs(self, x1, y1, x2, y2, x, y):
        self._path_type = 'C'
        self._values = (float(x1), float(y1),
                        float(x2), float(y2),
                        float(x), float(y))

    def set_curveto_rel(self, x1, y1, x2, y2, x, y):
        self._path_type = 'c'
        self._values = (float(x1), float(y1),
                        float(x2), float(y2),
                        float(x), float(y))

    def set_elliptical_arc_abs(self, rx, ry, x_axis_rotation, large_arc_flag,
                               sweep_flag, x, y):
        self._path_type = 'A'
        self._values = (float(rx),
                        float(ry),
                        float(x_axis_rotation),
                        int(large_arc_flag),
                        int(sweep_flag),
                        float(x),
                        float(y))

    def set_elliptical_arc_rel(self, rx, ry, x_axis_rotation, large_arc_flag,
                               sweep_flag, x, y):
        self._path_type = 'a'
        self._values = (float(rx),
                        float(ry),
                        float(x_axis_rotation),
                        int(large_arc_flag),
                        int(sweep_flag),
                        float(x),
                        float(y))

    def set_horizontal_lineto_abs(self, x):
        self._path_type = 'H'
        self._values = (float(x),)

    def set_horizontal_lineto_rel(self, x):
        self._path_type = 'h'
        self._values = (float(x),)

    def set_lineto_abs(self, x, y):
        self._path_type = 'L'
        self._values = float(x), float(y)

    def set_lineto_rel(self, x, y):
        self._path_type = 'l'
        self._values = float(x), float(y)

    def set_moveto_abs(self, x, y):
        self._path_type = 'M'
        self._values = float(x), float(y)

    def set_moveto_rel(self, x, y):
        self._path_type = 'm'
        self._values = float(x), float(y)

    def set_quadratic_curveto_abs(self, x1, y1, x, y):
        self._path_type = 'Q'
        self._values = float(x1), float(y1), float(x), float(y)

    def set_quadratic_curveto_rel(self, x1, y1, x, y):
        self._path_type = 'q'
        self._values = float(x1), float(y1), float(x), float(y)

    def set_smooth_curveto_abs(self, x2, y2, x, y):
        self._path_type = 'S'
        self._values = float(x2), float(y2), float(x), float(y)

    def set_smooth_curveto_rel(self, x2, y2, x, y):
        self._path_type = 's'
        self._values = float(x2), float(y2), float(x), float(y)

    def set_smooth_quadratic_curveto_abs(self, x, y):
        self._path_type = 'T'
        self._values = float(x), float(y)

    def set_smooth_quadratic_curveto_rel(self, x, y):
        self._path_type = 't'
        self._values = float(x), float(y)

    def set_vertical_lineto_abs(self, y):
        self._path_type = 'V'
        self._values = (float(y),)

    def set_vertical_lineto_rel(self, y):
        self._path_type = 'v'
        self._values = (float(y),)

    def tostring(self):
        if not self.isvalid():
            return ''
        elif self._path_type in 'Aa':
            # 'A'|'a' (rx,ry x-axis-rotation large-arc-flag sweep-flag x,y)+
            number_sequence = format_number_sequence(self._values)
            if len(number_sequence) > 0:
                rx = number_sequence.pop(0)
                ry = number_sequence.pop(0)
                number_sequence[0:0] = [','.join([rx, ry])]
                y = number_sequence.pop()
                x = number_sequence.pop()
                number_sequence.append(','.join([x, y]))
            return '{}{}'.format(self.type, ' '.join(number_sequence))
        elif self._path_type in 'BbHhVv':
            # 'B'|'b' angle+
            # 'H'|'h' x+
            # 'V'|'v' y+
            return self._tostring1()
        elif self._path_type in 'CcQqSsTt':
            # 'C'|'c' (x1,y1 x2,y2 x,y)+
            # 'Q'|'q' (x1,y1 x,y)+
            # 'S'|'s' (x2,y2 x,y)+
            # 'T'|'t' (x,y)+
            return self._tostring2n()
        elif self._path_type in 'LlMm':
            # 'L'|'l' (x,y)+
            # 'M'|'m' (x,y)+
            return self._tostring2()
        elif self._path_type in 'Zz':
            # 'Z'|'z'
            return self._path_type
        raise NotImplementedError('Unsupported path type: ' + repr(
            self._path_type))


class PathSegment(object):
    """Utility class for SVG path segment."""

    @staticmethod
    def get_bbox(path_segment, cpx, cpy, bearing, options=None, **extra):
        """Returns the bounding box of the path segment.

        Arguments:
            path_segment (SVGPathSegment):
            cpx (float): The absolute x-coordinate of the current point on the
                path.
            cpy (float): The absolute y-coordinate of the current point on the
                path.
            bearing (float): The current bearing.
            options (SVGBoundingBoxOptions, optional): Reserved.
            **extra: See below.
        Keyword Arguments:
            x1 (float): The absolute x-coordinate of the control point at the
                beginning of the curve for S/s/T/t commands.
            y1 (float): The absolute y-coordinate of the control point at the
                beginning of the curve for S/s/T/t commands.
        Returns:
            DOMRect: The bounding box of the path segment.
        """
        # TODO: add the Catmull-Rom command ("R"|"r").
        if not path_segment.isvalid() or path_segment.type in 'BbZz':
            return DOMRect()
        normalized = PathSegment.normalize(path_segment,
                                           cpx, cpy, bearing, **extra)
        bbox = DOMRect()
        for segment in normalized:
            path_type = segment.type
            if path_type == 'C':
                # 'C'|'c' (x1,y1 x2,y2 x,y)+
                if cpx is None:
                    cpx = 0
                if cpy is None:
                    cpy = 0
                x1, y1, x2, y2, x, y = segment.values
                p0 = np.array([cpx, cpy])
                p1 = np.array([x1, y1])
                p2 = np.array([x2, y2])
                p3 = np.array([x, y])
                curve = CubicBezierCurve(p0, p1, p2, p3)
                bbox |= curve.get_bbox(options, **extra)
                cpx, cpy = x, y
            elif path_type == 'L':
                # 'L'|'l' (x,y)+
                if cpx is None:
                    cpx = 0
                if cpy is None:
                    cpy = 0
                x, y = segment.values
                bbox |= DOMRect(cpx, cpy, x - cpx, y - cpy).normalize()
                cpx, cpy = x, y
            elif path_type == 'M':
                # 'M'|'m' (x,y)+
                x, y = segment.values
                if cpx is None or cpy is None:
                    if bbox.isvalid():
                        bbox |= DOMRect(x, y)
                    else:
                        bbox = DOMRect(x, y)
                else:
                    bbox |= DOMRect(cpx, cpy, x - cpx, y - cpy).normalize()
                cpx, cpy = x, y
        return bbox

    @staticmethod
    def get_center_of_arc(path_segment, cpx, cpy, bearing):
        """Returns the absolute coordinates of the center of the ellipse.

        Arguments:
            path_segment (SVGPathSegment):
            cpx (float): The absolute x-coordinate of the current point on the
                path.
            cpy (float): The absolute y-coordinate of the current point on the
                path.
            bearing (float): The current bearing.
        Returns:
            tuple[float, float]: The absolute coordinates of the center of the
                ellipse.
            tuple[float, float]: The computed radii of the ellipse (also known
                as its semi-major and semi-minor axes).
            tuple[float, float, float]: The start angle of the elliptical arc,
                the end angle of the elliptical arc, and the difference between
                these two angles.
        """
        path_type = path_segment.type
        if path_type not in 'Aa':
            raise ValueError('Unexpected path type: ' + repr(path_type))
        cx = None
        cy = None
        rx = 0
        ry = 0
        d1 = None
        d2 = None
        delta = None
        if not path_segment.isvalid():
            return (cx, cy), (rx, ry), (d1, d2, delta)
        if path_type == 'a':
            abs_path_segment = PathSegment.toabsolute(path_segment,
                                                      cpx, cpy, bearing)
        else:
            abs_path_segment = path_segment

        # See https://www.w3.org/TR/SVG11/implnote.html#ArcImplementationNotes
        # See https://www.w3.org/TR/SVG2/implnote.html#ArcImplementationNotes
        rx, ry, x_axis_rotation, fa, fs, epx, epy = abs_path_segment.values
        rx = abs(rx)  # SVG1.1 F.6.6.1
        ry = abs(ry)  # SVG1.1 F.6.6.1
        fa = 0 if fa == 0 else 1
        fs = 0 if fs == 0 else 1

        if math.isclose(rx, 0,
                        rel_tol=SVGLength.rel_tol,
                        abs_tol=SVGLength.abs_tol):
            rx = 0
        if math.isclose(ry, 0,
                        rel_tol=SVGLength.rel_tol,
                        abs_tol=SVGLength.abs_tol):
            ry = 0
        if rx == 0 or ry == 0:
            # treat as a straight line from start point to end point
            return (cx, cy), (rx, ry), (d1, d2, delta)

        if math.isclose(cpx, epx,
                        rel_tol=SVGLength.rel_tol,
                        abs_tol=SVGLength.abs_tol) \
                and math.isclose(cpy, epy,
                                 rel_tol=SVGLength.rel_tol,
                                 abs_tol=SVGLength.abs_tol):
            # start point and end point of the arc are identical
            return (cx, cy), (rx, ry), (d1, d2, delta)

        r = math.radians(x_axis_rotation)

        # compute (x1',y1') [SVG1.1 F.6.5.1]
        p = np.array([[math.cos(r), math.sin(r)],
                      [-math.sin(r), math.cos(r)]]).dot(
            np.array([[(cpx - epx) / 2],
                      [(cpy - epy) / 2]]))
        x1p = p.item(0)
        y1p = p.item(1)

        # ensure radii are large enough [SVG1.1 F.6.6.2]
        a = (x1p ** 2) / (rx ** 2) + (y1p ** 2) / (ry ** 2)
        if a > 1:
            # SVG1.1 F.6.6.3
            k = math.sqrt(a)
            rx *= k
            ry *= k

        # compute (cx',cy') [SVG1.1 F.6.5.2]
        fp = (((rx ** 2) * (ry ** 2)
               - (rx ** 2) * (y1p ** 2)
               - (ry ** 2) * (x1p ** 2))
              / ((rx ** 2) * (y1p ** 2) + (ry ** 2) * (x1p ** 2)))
        f = math.sqrt(max(fp, 0))
        if fa == fs:
            f = -f
        cp = f * np.array([[rx * y1p / ry],
                           [-ry * x1p / rx]])
        cxp = cp.item(0)
        cyp = cp.item(1)

        # compute (cx,cy) from (cx',cy') [SVG1.1 F.6.5.3]
        c = np.array([[math.cos(r), -math.sin(r)],
                      [math.sin(r), math.cos(r)]]).dot(
            np.array([[cxp], [cyp]]))
        c += np.array([[(cpx + epx) / 2],
                       [(cpy + epy) / 2]])
        cx = c.item(0)
        cy = c.item(1)

        d1 = get_angle(cpy - cy, cpx - cx)
        d2 = get_angle(epy - cy, epx - cx)
        if x_axis_rotation:
            d1 += x_axis_rotation
            d2 += x_axis_rotation
        delta = abs(d2 - d1)
        if fa:
            # large arc
            if delta < 180:
                delta = 360 - delta
        else:
            # small arc
            if delta > 180:
                delta = 360 - delta
        if fs:
            # negative direction arc
            delta = -delta

        return (cx, cy), (rx, ry), (d1, d2, delta)

    @staticmethod
    def get_length(path_segment, cpx, cpy, bearing, **extra):
        """Returns the length of the path segment.

        Arguments:
            path_segment (SVGPathSegment):
            cpx (float): The absolute x-coordinate of the current point on the
                path.
            cpy (float): The absolute y-coordinate of the current point on the
                path.
            bearing (float): The current bearing.
            **extra: See below.
        Keyword Arguments:
            x1 (float): The absolute x-coordinate of the control point at the
                beginning of the curve for S/s/T/t commands.
            y1 (float): The absolute y-coordinate of the control point at the
                beginning of the curve for S/s/T/t commands.
        Returns:
            float: The length of the path segment.
            tuple[float, float]: The absolute coordinates of the new current
                point on the path.
        """
        # TODO: add the Catmull-Rom command ("R"|"r").
        if not path_segment.isvalid() or path_segment.type in 'BbZz':
            return 0, (cpx, cpy)
        if cpx is None:
            cpx = 0
        if cpy is None:
            cpy = 0
        if path_segment.isrelative():
            # relative path segment -> absolute path segment
            # h/v -> L
            abs_path_segment = PathSegment.toabsolute(path_segment,
                                                      cpx, cpy, bearing)
        else:
            abs_path_segment = path_segment
        if abs_path_segment.type in 'HQSTV':
            # H/V -> L
            # Q/S/T -> C
            abs_path_segment = PathSegment.normalize(abs_path_segment,
                                                     cpx, cpy, bearing,
                                                     **extra)[0]
        path_type = abs_path_segment.type
        if path_type == 'A':
            # 'A'|'a' (rx,ry x-axis-rotation large-arc-flag sweep-flag x,y)+
            _, _, x_axis_rotation, _, _, epx, epy = abs_path_segment.values
            (cx, cy), (rx, ry), (d1, d2, extent) = \
                PathSegment.get_center_of_arc(abs_path_segment, cpx, cpy,
                                              bearing)
            if cx is None or cy is None:
                if rx == 0 or ry == 0:
                    # treat as a straight line from start point to end point
                    return math.hypot(epx - cpx, epy - cpy), (epx, epy)
                else:
                    # start point and end point of the arc are identical
                    return 0, (epx, epy)
            ellipse = Ellipse(cx, cy, rx, ry, x_axis_rotation)
            length = ellipse.get_length(d1, extent)
            return length, (epx, epy)
        elif path_type == 'C':
            # 'C'|'c' (x1,y1 x2,y2 x,y)+
            x1, y1, x2, y2, x, y = abs_path_segment.values
            p0 = np.array([cpx, cpy])
            p1 = np.array([x1, y1])
            p2 = np.array([x2, y2])
            p3 = np.array([x, y])
            curve = CubicBezierCurve(p0, p1, p2, p3)
            length = curve.get_length()
            return length, (x, y)
        elif path_type in 'LM':
            # 'L'|'l' (x,y)+
            # 'M'|'m' (x,y)+
            x, y = abs_path_segment.values
            return math.hypot(x - cpx, y - cpy), (x, y)
        raise NotImplementedError('Unsupported path type: ' + repr(path_type))

    @staticmethod
    def get_next_control_point(path_segment, cpx, cpy, bearing, last_path_type,
                               **extra):
        if not path_segment.isvalid():
            return None, None
        elif path_segment.type not in 'CcQqSsTt':
            raise ValueError('Unexpected path type: '
                             + repr(path_segment.type))
        elif path_segment.isabsolute():
            abs_path_segment = path_segment
        else:
            abs_path_segment = PathSegment.toabsolute(path_segment,
                                                      cpx, cpy, bearing)
        path_type = abs_path_segment.type
        if path_type in 'CS':
            # cubic bezier curveto: 'C'|'c' (x1,y1 x2,y2 x,y)+
            # smooth cubic bezier curveto: 'S'|'s' (x2,y2 x,y)+
            if path_type == 'C':
                _, _, x2, y2, x, y = abs_path_segment.values
            elif (path_type == 'S'
                  and last_path_type is not None and last_path_type in 'CcSs'):
                x2, y2, x, y = abs_path_segment.values
            else:
                x2, y2 = cpx, cpy
                x, y = abs_path_segment.end
            next_x1 = 2 * x - x2
            next_y1 = 2 * y - y2
            return next_x1, next_y1
        else:
            # quadratic bezier curveto: 'Q'|'q' (x1,y1 x,y)+
            # smooth quadratic bezier curveto: 'T'|'t' (x,y)+
            if path_type == 'Q':
                x1, y1, x, y = abs_path_segment.values
            elif (path_type == 'T'
                  and last_path_type is not None and last_path_type in 'QqTt'):
                x1 = extra.get('x1', cpx)
                y1 = extra.get('y1', cpy)
                x, y = abs_path_segment.values
            else:
                x1, y1 = cpx, cpy
                x, y = abs_path_segment.end
            next_x1 = 2 * x - x1
            next_y1 = 2 * y - y1
            return next_x1, next_y1

    @staticmethod
    def normalize(path_segment, cpx, cpy, bearing, **extra):
        """Converts to the base set of absolute path segments ('M', 'L', 'C' or
        'Z'), and returns it.

        Arguments:
            path_segment (SVGPathSegment):
            cpx (float): The absolute x-coordinate of the current point on the
                path.
            cpy (float): The absolute y-coordinate of the current point on the
                path.
            bearing (float): The current bearing.
            **extra: See below.
        Keyword Arguments:
            x1 (float): The absolute x-coordinate of the control point at the
                beginning of the curve for S/s/T/t commands.
            y1 (float): The absolute y-coordinate of the control point at the
                beginning of the curve for S/s/T/t commands.
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        # TODO: add the Catmull-Rom command ("R"|"r").
        path_type = path_segment.type
        if not path_segment.isvalid() or path_type in 'Bb':
            return []
        elif path_type in 'CLMZ':
            return [copy.deepcopy(path_segment)]
        if cpx is None:
            cpx = 0
        if cpy is None:
            cpy = 0
        if path_segment.isrelative():
            # relative path segment -> absolute path segment
            # h/v -> L
            abs_path_segment = PathSegment.toabsolute(path_segment,
                                                      cpx, cpy, bearing)
        else:
            abs_path_segment = path_segment
        path_type = abs_path_segment.type
        if path_type == 'A':
            # 'A'|'a' (rx,ry x-axis-rotation large-arc-flag sweep-flag x,y)+
            rx, ry, x_axis_rotation, fa, fs, epx, epy = abs_path_segment.values
            (cx, cy), (rx, ry), (d1, d2, extent) = \
                PathSegment.get_center_of_arc(abs_path_segment, cpx, cpy,
                                              bearing)
            if cx is None or cy is None:
                if rx == 0 or ry == 0:
                    return [SVGPathSegment('L', epx, epy)]
                else:
                    return []

            # ripped from AndroidSVG (Apache 2.0 License)
            # androidsvg/src/main/java/com/caverock/androidsvg/SVGAndroidRenderer.java
            # SVGAndroidRenderer.arcTo() and SVGAndroidRenderer.arcToBeziers()
            # by Paul LeBeau, Cave Rock Software Ltd.
            # See https://github.com/BigBadaboom/androidsvg/blob/master/androidsvg/src/main/java/com/caverock/androidsvg/SVGAndroidRenderer.java
            segments = math.ceil(abs(extent) / 90)
            increment = math.radians(extent) / segments
            control_length = (4 / 3 * math.sin(increment / 2)
                              / (1 + math.cos(increment / 2)))

            matrix = DOMMatrix()
            matrix.translate_self(cx, -cy)
            matrix.rotate_self(rot_z=-x_axis_rotation)
            matrix.scale_self(rx, ry)

            path_data = list()
            start = math.radians(d1)
            for i in range(0, int(segments)):
                # control point at the beginning of the curve
                t = start + i * increment
                dx = math.cos(t)
                dy = math.sin(t)
                p1 = matrix.transform_point(dx - control_length * dy,
                                            dy + control_length * dx)

                # control point at the end of the curve
                t += increment
                dx = math.cos(t)
                dy = math.sin(t)
                p2 = matrix.transform_point(dx + control_length * dy,
                                            dy - control_length * dx)

                # end point of the curve
                if i == segments - 1:
                    p3 = epx, -epy
                else:
                    p3 = matrix.transform_point(dx, dy)

                path_data.append(SVGPathSegment('C',
                                                p1[0], -p1[1],
                                                p2[0], -p2[1],
                                                p3[0], -p3[1]))
            return path_data
        elif path_type in 'CLMZ':
            # 'C'|'c' (x1,y1 x2,y2 x,y)+
            # 'L'|'l' (x,y)+
            # 'M'|'m' (x,y)+
            # 'Z'|'z'
            return [abs_path_segment]
        elif path_type == 'H':
            # 'H'|'h' x+
            x, y = abs_path_segment.values[0], cpy
            return [SVGPathSegment('L', x, y)]
        elif path_type == 'Q':
            # 'Q'|'q' (x1,y1 x,y)+
            x1, y1, x, y = abs_path_segment.values
            qp0 = np.array([cpx, cpy])
            qp1 = np.array([x1, y1])
            qp2 = np.array([x, y])
            cp1 = qp0 + 2 / 3 * (qp1 - qp0)
            cp2 = qp2 + 2 / 3 * (qp1 - qp2)
            cp3 = qp2
            return [SVGPathSegment('C',
                                   cp1[0], cp1[1],
                                   cp2[0], cp2[1],
                                   cp3[0], cp3[1])]
        elif path_type == 'S':
            # 'S'|'s' (x2,y2 x,y)+
            x2, y2, x, y = abs_path_segment.values
            x1 = extra.get('x1', cpx)
            y1 = extra.get('y1', cpy)
            return [SVGPathSegment('C', x1, y1, x2, y2, x, y)]
        elif path_type == 'T':
            # 'T'|'t' (x,y)+
            x, y = abs_path_segment.values
            x1 = extra.get('x1', cpx)
            y1 = extra.get('y1', cpy)
            # T -> Q -> C
            path_data = PathSegment.normalize(
                SVGPathSegment('Q', x1, y1, x, y),
                cpx, cpy, bearing, **extra)
            return path_data
        elif path_type == 'V':
            # 'V'|'v' y+
            x, y = cpx, abs_path_segment.values[0]
            return [SVGPathSegment('L', x, y)]
        raise NotImplementedError('Unsupported path type: ' + repr(path_type))

    @staticmethod
    def toabsolute(path_segment, cpx, cpy, bearing):
        """Converts to absolute path segment and returns it.

        Arguments:
            path_segment (SVGPathSegment):
            cpx (float): The absolute x-coordinate of the current point on the
                path.
            cpy (float): The absolute y-coordinate of the current point on the
                path.
            bearing (float): The current bearing.
        Returns:
            SVGPathSegment: A new SVGPathSegment object.
        """
        # TODO: add the Catmull-Rom command ("R"|"r").
        if not path_segment.isvalid() or path_segment.isabsolute():
            return copy.deepcopy(path_segment)
        if cpx is None:
            cpx = 0
        if cpy is None:
            cpy = 0
        path_type = path_segment.type.upper()
        values = path_segment.values
        if path_type == 'A':
            # 'A'|'a' (rx,ry x-axis-rotation large-arc-flag sweep-flag x,y)+
            rx, ry, x_axis_rotation, fa, fs, x, y = values
            if bearing != 0:
                matrix = DOMMatrix()
                matrix.rotate_self(rot_z=bearing)
                x, y = matrix.transform_point(x, y)
                x_axis_rotation += bearing
            x += cpx
            y += cpy
            return SVGPathSegment(path_type, rx, ry, x_axis_rotation, fa, fs,
                                  x, y)
        elif path_type == 'B':
            # 'B'|'b' angle+
            return SVGPathSegment(path_type, bearing + values[0])
        elif path_type == 'C':
            # 'C'|'c' (x1,y1 x2,y2 x,y)+
            x1, y1, x2, y2, x, y = values
            if bearing != 0:
                matrix = DOMMatrix()
                matrix.rotate_self(rot_z=bearing)
                x1, y1 = matrix.transform_point(x1, y1)
                x2, y2 = matrix.transform_point(x2, y2)
                x, y = matrix.transform_point(x, y)
            x1 += cpx
            y1 += cpy
            x2 += cpx
            y2 += cpy
            x += cpx
            y += cpy
            return SVGPathSegment(path_type, x1, y1, x2, y2, x, y)
        elif path_type == 'H':
            # 'H'|'h' x+
            x, y = values[0], 0
            if bearing != 0:
                matrix = DOMMatrix()
                matrix.rotate_self(rot_z=bearing)
                x, y = matrix.transform_point(x, y)
            x += cpx
            y += cpy
            return SVGPathSegment('L', x, y)
        elif path_type in 'LMT':
            # 'L'|'l' (x,y)+
            # 'M'|'m' (x,y)+
            # 'T'|'t' (x,y)+
            x, y = values
            if bearing != 0:
                matrix = DOMMatrix()
                matrix.rotate_self(rot_z=bearing)
                x, y = matrix.transform_point(x, y)
            x += cpx
            y += cpy
            return SVGPathSegment(path_type, x, y)
        elif path_type in 'QS':
            # 'Q'|'q' (x1,y1 x,y)+
            # 'S'|'s' (x2,y2 x,y)+
            x2, y2, x, y = values
            if bearing != 0:
                matrix = DOMMatrix()
                matrix.rotate_self(rot_z=bearing)
                x2, y2 = matrix.transform_point(x2, y2)
                x, y = matrix.transform_point(x, y)
            x2 += cpx
            y2 += cpy
            x += cpx
            y += cpy
            return SVGPathSegment(path_type, x2, y2, x, y)
        elif path_type == 'V':
            # 'V'|'v' y+
            x, y = 0, values[0]
            if bearing != 0:
                matrix = DOMMatrix()
                matrix.rotate_self(rot_z=bearing)
                x, y = matrix.transform_point(x, y)
            x += cpx
            y += cpy
            return SVGPathSegment('L', x, y)
        elif path_type == 'Z':
            # 'Z'|'z'
            return SVGPathSegment(path_type)
        raise NotImplementedError('Unsupported path type: ' + repr(path_type))

    @staticmethod
    def transform(path_segment, cpx, cpy, bearing, matrix):
        path_type = path_segment.type
        if not path_segment.isvalid() or path_type in 'Zz':
            return copy.deepcopy(path_segment)
        elif path_type in 'Bb':
            raise NotImplementedError('Unsupported path type: '
                                      + repr(path_type))
        if path_segment.isrelative():
            # relative path segment -> absolute path segment
            # h/v -> L
            abs_path_segment = PathSegment.toabsolute(path_segment,
                                                      cpx, cpy, bearing)
        else:
            abs_path_segment = path_segment
        path_type = abs_path_segment.type
        if path_type == 'A':
            # 'A'|'a' (rx,ry x-axis-rotation large-arc-flag sweep-flag x,y)+
            rx, ry, x_axis_rotation, fa, fs, x, y = abs_path_segment.values
            x, y = matrix.transform_point(x, y)
            # x_axis_rotation += matrix.get_angle()
            return SVGPathSegment('A', rx, ry, x_axis_rotation, fa, fs, x, y)
        elif path_type == 'C':
            # 'C'|'c' (x1,y1 x2,y2 x,y)+
            x1, y1, x2, y2, x, y = abs_path_segment.values
            x1, y1 = matrix.transform_point(x1, y1)
            x2, y2 = matrix.transform_point(x2, y2)
            x, y = matrix.transform_point(x, y)
            return SVGPathSegment('C', x1, y1, x2, y2, x, y)
        elif path_type == 'H':
            # 'H'|'h' x+
            x, y = abs_path_segment.values[0], cpy
            x, y = matrix.transform_point(x, y)
            return SVGPathSegment('L', x, y)
        elif path_type in 'LMT':
            # 'L'|'l' (x,y)+
            # 'M'|'m' (x,y)+
            # 'T'|'t' (x,y)+
            x, y = abs_path_segment.values
            x, y = matrix.transform_point(x, y)
            return SVGPathSegment(path_type, x, y)
        elif path_type in 'QS':
            # 'Q'|'q' (x1,y1 x,y)+
            # 'S'|'s' (x2,y2 x,y)+
            x2, y2, x, y = abs_path_segment.values
            x2, y2 = matrix.transform_point(x2, y2)
            x, y = matrix.transform_point(x, y)
            return SVGPathSegment(path_type, x2, y2, x, y)
        elif path_type == 'V':
            # 'V'|'v' y+
            x, y = cpx, abs_path_segment.values[0]
            x, y = matrix.transform_point(x, y)
            return SVGPathSegment('L', x, y)
        raise NotImplementedError('Unsupported path type: ' + repr(path_type))


class PathParser(object):
    """Utility class for SVG path data."""

    # TODO: add the Catmull-Rom curve commands ("R"|"r").
    # See https://svgwg.org/specs/paths/#PathDataCatmullRomCommand
    RE_PATH_SEGMENT_LIST = re.compile(
        r"((?P<type>[AaBbCcHhLlMmQqSsTtVvZz])\s*"
        r"(?P<values>([^AaBbCcHhLlMmQqSsTtVvZz]|$)+))")

    RE_NUMBER_SEQUENCE = re.compile(
        r"(?P<number>[+-]?"
        r"((\d+(\.\d*)?([Ee][+-]?\d+)?)|(\d*\.\d+([Ee][+-]?\d+)?)))"
        r"(\s*,\s*|\s+)?")

    PATH_SEGMENT_TYPES = 'AaBbCcHhLlMmQqSsTtVvZz'

    _PATH_SEGMENT_VALUES_LENGTH = {
        'A': 7,
        'B': 1,
        'C': 6,
        'H': 1,
        'L': 2,
        'M': 2,
        'Q': 4,
        'S': 4,
        'T': 2,
        'V': 1,
    }

    @staticmethod
    def from_glyph(face, matrix=None):
        """Creates a list of path segments from specified glyph outlines
        and returns it.

        Arguments:
            face (FTFace): The FTFace object.
            matrix (DOMMatrixReadOnly, optional): The transformation matrix.
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """

        def _move_to(x, y, user):
            x /= 64
            y /= 64
            user.append(SVGPathSegment('M', x, y))

        def _line_to(x, y, user):
            x /= 64
            y /= 64
            user.append(SVGPathSegment('L', x, y))

        def _conic_to(x1, y1, x, y, user):
            x1 /= 64
            y1 /= 64
            x /= 64
            y /= 64
            user.append(SVGPathSegment('Q', x1, y1, x, y))

        def _cubic_to(x1, y1, x2, y2, x, y, user):
            x1 /= 64
            y1 /= 64
            x2 /= 64
            y2 /= 64
            x /= 64
            y /= 64
            user.append(SVGPathSegment('C', x1, y1, x2, y2, x, y))

        path_data = list()
        outline = face.glyph.outline
        transform = FTMatrix()
        transform = transform.flip_y()
        if matrix is not None:
            # convert from DOMMatrixReadOnly to FTMatrix
            other = FTMatrix()
            other.a = matrix.a
            other.b = matrix.b
            other.c = matrix.c
            other.d = matrix.d
            transform *= other
            tx, ty = matrix.get_translate()
            outline.translate(int(tx * 64), int(ty * 64))
        outline.transform(transform)
        outline.decompose(_move_to,
                          _line_to,
                          _conic_to,
                          _cubic_to,
                          user=path_data)
        return path_data

    @staticmethod
    def get_bbox(path_data, options=None, **extra):
        """Returns the bounding box of the path.

        Arguments:
            path_data (list[SVGPathSegment]): A list of path segments. The path
                segments must be normalized.
            options (SVGBoundingBoxOptions, optional): Reserved.
            **extra: Reserved.
        Returns:
            DOMRect: The bounding box of the path.
        """
        bbox = DOMRect()
        start_x = None
        start_y = None
        cpx = None
        cpy = None
        bearing = 0  # current bearing
        last_command = None
        for path_segment in iter(path_data):
            if not isinstance(path_segment, SVGPathSegment):
                raise TypeError('Expected SVGPathSegment, got {}'.format(
                    type(path_segment)))
            if not path_segment.isvalid():
                continue
            command = path_segment.type
            if command in 'CLM':
                # cubic bezier curveto: 'C'|'c' (x1,y1 x2,y2 x,y)+
                # lineto: 'L'|'l' (x,y)+
                # moveto: 'M'|'m' (x,y)+
                rect = PathSegment.get_bbox(path_segment,
                                            cpx, cpy, bearing,
                                            options=options, **extra)
                cpx, cpy = path_segment.end
                if command == 'M':
                    if last_command is None:
                        bbox = rect
                    if last_command is not None and last_command == 'M':
                        # implicit "lineto" command
                        bbox |= rect
                    else:
                        start_x = cpx
                        start_y = cpy
                else:
                    bbox |= rect
                    if start_x is None or start_y is None:
                        start_x = cpx
                        start_y = cpy
            elif command == 'Z':
                # pathclose: 'Z'|'z'
                if (start_x is not None and start_y is not None
                        and cpx is not None and cpy is not None):
                    # line to the start point
                    line = SVGPathSegment('L', start_x, start_y)
                    rect = PathSegment.get_bbox(line,
                                                cpx, cpy, bearing,
                                                options=options, **extra)
                    bbox |= rect
                    cpx = start_x
                    cpy = start_y
            else:
                raise ValueError('Unexpected path type: ' + repr(command))
            last_command = command
        return bbox

    @staticmethod
    def get_total_length(path_data):
        """Returns the total length of the path.

        Arguments:
            path_data (list[SVGPathSegment]): A list of path segments.
        Returns:
            float: The total length of the path.
        """
        total_length = 0
        start_x = None
        start_y = None
        cpx = None
        cpy = None
        x1 = None
        y1 = None
        bearing = 0  # current bearing
        last_command = None
        for path_segment in iter(path_data):
            if not isinstance(path_segment, SVGPathSegment):
                raise TypeError('Expected SVGPathSegment, got {}'.format(
                    type(path_segment)))
            if not path_segment.isvalid():
                continue
            command = path_segment.type
            if command in 'AaCcHhLlMmQqSsTtVv':
                # elliptical arc: 'A'|'a' (rx ry r fa fs x,y)+
                # cubic bezier curveto: 'C'|'c' (x1,y1 x2,y2 x,y)+
                # horizontal lineto: 'H'|'h' x+
                # lineto: 'L'|'l' (x,y)+
                # moveto: 'M'|'m' (x,y)+
                # quadratic bezier curveto: 'Q'|'q' (x1,y1 x,y)+
                # vertical lineto: 'V'|'v' y+
                old_cpx, old_cpy = cpx, cpy
                length, (cpx, cpy) = PathSegment.get_length(path_segment,
                                                            cpx, cpy, bearing,
                                                            x1=x1, y1=y1)

                # control point for next shorthand/smooth curve
                if command in 'CcQqSsTt':
                    x1, y1 = PathSegment.get_next_control_point(
                        path_segment, old_cpx, old_cpy, bearing, last_command,
                        x1=x1, y1=y1)
                else:
                    x1, y1 = cpx, cpy

                if command in 'Mm':
                    if last_command is not None and last_command in 'Mm':
                        # implicit "lineto" command
                        total_length += length
                    else:
                        start_x = cpx
                        start_y = cpy
                else:
                    total_length += length
                    if start_x is None or start_y is None:
                        start_x = cpx
                        start_y = cpy
            elif command in 'Bb':
                # bearing: 'B'|'b' angle+
                bearing = path_segment.get_bearing(bearing)
            elif command in 'Zz':
                # pathclose: 'Z'|'z'
                if (start_x is not None and start_y is not None
                        and cpx is not None and cpy is not None):
                    # line to the start point
                    line = SVGPathSegment('L', start_x, start_y)
                    length, (cpx, cpy) = PathSegment.get_length(line,
                                                                cpx, cpy,
                                                                bearing)
                    total_length += length
                    cpx = start_x
                    cpy = start_y
            last_command = command
        return total_length

    @staticmethod
    def normalize(path_data):
        """Converts to the base set of absolute path segments ('M', 'L', 'C'
        and 'Z') and returns it.

        Arguments:
            path_data (list[SVGPathSegment]): A list of path segments.
        Returns:
            list[SVGPathSegment]: A new list of path segments.
        """
        normalized_path_data = list()
        start_x = None
        start_y = None
        cpx = None
        cpy = None
        x1 = None
        y1 = None
        bearing = 0  # current bearing
        last_command = None
        for path_segment in iter(path_data):
            if not isinstance(path_segment, SVGPathSegment):
                raise TypeError('Expected SVGPathSegment, got {}'.format(
                    type(path_segment)))
            if not path_segment.isvalid():
                continue
            command = path_segment.type
            if command in 'AaCcHhLlMmQqSsTtVvZz':
                # elliptical arc: 'A'|'a' (rx ry r fa fs x,y)+
                # cubic bezier curveto: 'C'|'c' (x1,y1 x2,y2 x,y)+
                # horizontal lineto: 'H'|'h' x+
                # lineto: 'L'|'l' (x,y)+
                # moveto: 'M'|'m' (x,y)+
                # quadratic bezier curveto: 'Q'|'q' (x1,y1 x,y)+
                # smooth cubic bezier curveto: 'S'|'s' (x2,y2 x,y)+
                # smooth quadratic bezier curveto: 'T'|'t' (x,y)+
                # vertical lineto: 'V'|'v' y+
                # pathclose: 'Z'|'z'
                normalized = PathSegment.normalize(path_segment,
                                                   cpx, cpy, bearing,
                                                   x1=x1, y1=y1)
                normalized_path_data.extend(normalized)

                # control point for next shorthand/smooth curve
                if command in 'CcQqSsTt':
                    x1, y1 = PathSegment.get_next_control_point(
                        path_segment, cpx, cpy, bearing, last_command,
                        x1=x1, y1=y1)
                else:
                    x1, y1 = normalized[-1].end

                if command in 'Zz':
                    if start_x is not None and start_y is not None:
                        cpx = start_x
                        cpy = start_y
                else:
                    cpx, cpy = normalized[-1].end
                    if ((command in 'Mm'
                         and (last_command is None
                              or last_command not in 'Mm'))
                            or (start_x is None or start_y is None)):
                        start_x = cpx
                        start_y = cpy
            elif command in 'Bb':
                # bearing: 'B'|'b' angle+
                bearing = path_segment.get_bearing(bearing)
            last_command = command
        return normalized_path_data

    @staticmethod
    def parse(text):
        """Parses text into a list of path segments and returns it.

        Arguments:
            text (str): A text to parse.
        Returns:
            list[SVGPathSegment]: A list of path segments.
        """
        path_data = list()
        if text is None:
            return path_data
        for it in PathParser.RE_PATH_SEGMENT_LIST.finditer(text.strip()):
            path_type = it.group('type').strip()
            if path_type in 'Zz':
                path_data.append(SVGPathSegment(path_type))
            elif path_type in PathParser.PATH_SEGMENT_TYPES:
                values = it.group('values').strip()
                args_sequence = list()
                if len(values) > 0:
                    number_sequence = list()
                    for it2 in PathParser.RE_NUMBER_SEQUENCE.finditer(values):
                        number = it2.group('number')
                        number_sequence.append(float(number))
                    argc = PathParser._PATH_SEGMENT_VALUES_LENGTH.get(
                        path_type.upper())
                    args_sequence = zip(*[iter(number_sequence)] * argc)
                for args in iter(args_sequence):
                    path_data.append(SVGPathSegment(path_type, *args))
        return path_data

    @staticmethod
    def tostring(path_data):
        # See https://svgwg.org/specs/paths/#PathDataBNF
        svg_path = list()
        last_path_type = None
        for path_segment in iter(path_data):
            if not isinstance(path_segment, SVGPathSegment):
                raise TypeError('Expected SVGPathSegment, got {}'.format(
                    type(path_segment)))
            drawto_command = path_segment.tostring()
            path_type = path_segment.type
            if last_path_type == path_type:
                drawto_command = drawto_command[1:]
            svg_path.append(drawto_command)
            last_path_type = path_type
        svg_path = [x for x in svg_path if x not in ['']]
        return ' '.join(svg_path)

    @staticmethod
    def transform(path_data, matrix):
        transformed_path_data = list()
        start_x = None
        start_y = None
        cpx = None
        cpy = None
        bearing = 0  # current bearing
        last_command = None
        for path_segment in iter(path_data):
            if not isinstance(path_segment, SVGPathSegment):
                raise TypeError('Expected SVGPathSegment, got {}'.format(
                    type(path_segment)))
            if not path_segment.isvalid():
                continue
            command = path_segment.type
            if command in 'AaCcHhLlMmQqSsTtVv':
                # elliptical arc: 'A'|'a' (rx ry r fa fs x,y)+
                # cubic bezier curveto: 'C'|'c' (x1,y1 x2,y2 x,y)+
                # horizontal lineto: 'H'|'h' x+
                # lineto: 'L'|'l' (x,y)+
                # moveto: 'M'|'m' (x,y)+
                # quadratic bezier curveto: 'Q'|'q' (x1,y1 x,y)+
                # smooth cubic bezier curveto: 'S'|'s' (x2,y2 x,y)+
                # smooth quadratic bezier curveto: 'T'|'t' (x,y)+
                # vertical lineto: 'V'|'v' y+
                transformed = PathSegment.transform(path_segment,
                                                    cpx, cpy, bearing, matrix)
                transformed_path_data.append(transformed)
                if command.islower():
                    abs_path_segment = PathSegment.toabsolute(path_segment,
                                                              cpx, cpy,
                                                              bearing)
                else:
                    abs_path_segment = path_segment
                cpx, cpy = abs_path_segment.end
                if ((command in 'Mm'
                     and (last_command is None or last_command not in 'Mm'))
                        or (start_x is None or start_y is None)):
                    start_x = cpx
                    start_y = cpy
            elif command in 'Bb':
                # bearing: 'B'|'b' angle+
                bearing = path_segment.get_bearing(bearing)
            elif command in 'Zz':
                # pathclose: 'Z'|'z'
                transformed_path_data.append(SVGPathSegment('Z'))
                if start_x is not None and start_y is not None:
                    cpx = start_x
                    cpy = start_y
            last_command = command
        return transformed_path_data
