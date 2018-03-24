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
import re

from .formatter import format_number_sequence
from .matrix import Matrix


class SVGTransform(object):
    """Represents the transform function values."""

    TRANSFORM_UNKNOWN = None
    TRANSFORM_MATRIX = 'matrix'
    TRANSFORM_TRANSLATE = 'translate'
    TRANSFORM_SCALE = 'scale'
    TRANSFORM_ROTATE = 'rotate'
    TRANSFORM_SKEWX = 'skewX'
    TRANSFORM_SKEWY = 'skewY'

    def __init__(self, function_name=None, *values):
        """Constructs a SVGTransform object.

        Arguments:
            function_name (str, optional): The type of transform function.
            *values: The values of transform function.
        Examples:
            >>> t = SVGTransform('translate', 100, -200)
            >>> t.tostring()
            'translate(100 -200)'
            >>> t.matrix.tolist()
            [[1.0, 0.0, 100.0], [0.0, 1.0, -200.0], [0.0, 0.0, 1.0]]
        """
        self._transform_type = None
        self._values = None
        self._angle = 0
        if function_name is not None:
            self.set(function_name, *values)

    def __repr__(self):
        return '<{}.{} object at {} ({}{})>'.format(
            type(self).__module__, type(self).__name__, hex(id(self)),
            self._transform_type,
            self._values if self._values is not None else '')

    @property
    def angle(self):
        """float: A current angle of a rotate(), skewX() or skewY() function,
        in degrees.
        """
        return self._angle

    @property
    def matrix(self):
        """Matrix: The current matrix or None."""
        if self._transform_type is None or self._values is None:
            return None
        matrix = Matrix()
        if self._transform_type == SVGTransform.TRANSFORM_MATRIX:
            matrix.set_matrix(*self._values)
        elif self._transform_type == SVGTransform.TRANSFORM_ROTATE:
            matrix.rotate_self(*self._values)
        elif self._transform_type == SVGTransform.TRANSFORM_SCALE:
            matrix.scale_self(*self._values)
        elif self._transform_type == SVGTransform.TRANSFORM_SKEWX:
            matrix.skewx_self(*self._values)
        elif self._transform_type == SVGTransform.TRANSFORM_SKEWY:
            matrix.skewy_self(*self._values)
        elif self._transform_type == SVGTransform.TRANSFORM_TRANSLATE:
            matrix.translate_self(*self._values)
        else:
            raise NotImplementedError(
                'Unknown transform type: {}'.format(self._transform_type))
        return matrix

    @property
    def type(self):
        """str: The type of the transform function."""
        return self._transform_type

    @property
    def values(self):
        """tuple[float, ...]: The values of the transform function."""
        return self._values

    @staticmethod
    def frommatrix(matrix):
        """Constructs a new SVGTransform initialized with the Matrix matrix.

        Arguments:
            matrix (Matrix): A Matrix object.
        Returns:
            SVGTransform: A new SVGTransform object.
        """
        if matrix is None or (not isinstance(matrix, Matrix)):
            raise TypeError('Expected Matrix, got {}'.format(type(matrix)))
        m = matrix.matrix
        transform = SVGTransform()
        transform.set_matrix(m[0, 0], m[1, 0], m[0, 1],
                             m[1, 1], m[0, 2], m[1, 2])
        return transform

    def set(self, function_name, *values):
        if function_name == 'matrix':
            self.set_matrix(*values)
        elif function_name == 'rotate':
            self.set_rotate(*values)
        elif function_name == 'scale':
            self.set_scale(*values)
        elif function_name == 'skewX':
            self.set_skewx(*values)
        elif function_name == 'skewY':
            self.set_skewy(*values)
        elif function_name == 'translate':
            self.set_translate(*values)
        else:
            raise NotImplementedError(
                'Unknown transform type: {}'.format(function_name))

    def set_matrix(self, a, b, c, d, e, f):
        """Sets the transform function value is matrix(a b c d e f).

        Arguments:
            a (float): The a component of the matrix.
            b (float): The b component of the matrix.
            c (float): The c component of the matrix.
            d (float): The d component of the matrix.
            e (float): The e component of the matrix.
            f (float): The f component of the matrix.
        """
        self._transform_type = SVGTransform.TRANSFORM_MATRIX
        self._values = (a, b, c, d, e, f)
        self._angle = 0

    def set_rotate(self, angle, cx=0, cy=0):
        """Sets the transform function value is rotate(angle cx cy).

        Arguments:
            angle (float): The rotation angle in degrees.
            cx (float): The x-coordinate of center of rotation.
            cy (float): The y-coordinate of center of rotation.
        """
        self._transform_type = SVGTransform.TRANSFORM_ROTATE
        self._values = (angle, cx, cy)
        self._angle = angle

    def set_scale(self, sx, sy=None):
        """Sets the transform function value is scale(sx sy).

        Arguments:
            sx (float): The scale amount in X.
            sy (float): The scale amount in Y.
        """
        if sy is None:
            sy = sx
        self._transform_type = SVGTransform.TRANSFORM_SCALE
        self._values = (sx, sy)
        self._angle = 0

    def set_skewx(self, angle):
        """Sets the transform function value is skewX(angle).

        Arguments:
            angle (float): The skew angle in degrees.
        """
        self._transform_type = SVGTransform.TRANSFORM_SKEWX
        self._values = (angle,)
        self._angle = angle

    def set_skewy(self, angle):
        """Sets the transform function value is skewY(angle).

        Arguments:
            angle (float): The skew angle in degrees.
        """
        self._transform_type = SVGTransform.TRANSFORM_SKEWY
        self._values = (angle,)
        self._angle = angle

    def set_translate(self, tx, ty=0):
        """Sets the transform function value is translate(tx ty).

        Arguments:
            tx (float): The translation amount in X.
            ty (float): The translation amount in Y.
        """
        self._transform_type = SVGTransform.TRANSFORM_TRANSLATE
        self._values = (tx, ty)
        self._angle = 0

    def tostring(self, delimiter=None):
        if self._transform_type is None or self._values is None:
            return ''
        number_sequence = format_number_sequence(self._values)
        if self._transform_type == SVGTransform.TRANSFORM_ROTATE:
            # "rotate(a 0 0)" -> "rotate(a)"
            if number_sequence[1] == '0' and number_sequence[2] == '0':
                del number_sequence[1:]
        elif self._transform_type == SVGTransform.TRANSFORM_SCALE:
            # "scale(a a)" -> "scale(a)"
            if number_sequence[0] == number_sequence[1]:
                del number_sequence[1]
        elif self._transform_type == SVGTransform.TRANSFORM_TRANSLATE:
            # "translate(a 0)" -> "translate(a)"
            if number_sequence[1] == '0':
                del number_sequence[1]
        if delimiter is None or len(delimiter) == 0:
            delimiter = ' '
        return '{0}({1})'.format(self._transform_type,
                                 delimiter.join(number_sequence))


class SVGTransformList(list):
    """Represents a list of SVGTransform objects."""

    RE_TRANSFORM_LIST = re.compile(
        r"(?P<transform>(?P<name>matrix|translate|scale|rotate|skewX|skewY)"
        r"\s*\((?P<values>[^)]+)\))($|\s+|\s*,\s*)")

    RE_NUMBER_SEQUENCE = re.compile(
        r"(?P<number>[+-]?"
        r"((\d+(\.\d*)?([Ee][+-]?\d+)?)|(\d*\.\d+([Ee][+-]?\d+)?)))"
        r"(\s*,\s*|\s+)?")

    def __add__(self, other):
        if not isinstance(other, SVGTransformList):
            return NotImplemented
        x = copy.deepcopy(self)
        x.extend(other)
        return x

    def __iadd__(self, other):
        if not isinstance(other, SVGTransformList):
            return NotImplemented
        self.extend(other)
        return self

    def __repr__(self):
        return '[{}]'.format(
            ', '.join(['\'{}\''.format(x.tostring()) for x in self]))

    def consolidate(self):
        """Converts the transform list into an equivalent transformation
        using a single transform function and returns it.

        Returns:
            SVGTransform: A SVGTransform object or None.
        """
        if len(self) == 0:
            return None
        transform = self.totransform()
        if transform is None:
            return None
        self.clear()
        self.append(transform)
        return transform

    @staticmethod
    def parse(text):
        """Parses text into a list of SVGTransform objects and returns it.

        Arguments:
            text (str): A text to parse.
        Returns:
            list[SVGTransform]: A list of SVGTransform objects.
        Examples:
            >>> t = SVGTransformList.parse('translate(50 30) rotate(30)')
            >>> len(t)
            2
            >>> for x in iter(t):
            ...     print(x.tostring())
            ...
            translate(50 30)
            rotate(30)
        """
        transform_list = SVGTransformList()
        for it in SVGTransformList.RE_TRANSFORM_LIST.finditer(text.strip()):
            function_name = it.group('name').strip()
            number_sequence = list()
            for it2 in SVGTransformList.RE_NUMBER_SEQUENCE.finditer(
                    it.group('values').strip()):
                number_sequence.append(float(it2.group('number')))
            transform_list.append(SVGTransform(function_name, *number_sequence))
        return transform_list

    def tomatrix(self):
        """Returns the matrix of this transformation.

        Returns:
            Matrix: A new Matrix object or None.
        """
        if len(self) == 0:
            return None
        matrix = Matrix()
        for transform in iter(self):
            if not isinstance(transform, SVGTransform):
                raise TypeError('Expected Transform, got {}'.format(
                    type(transform)))
            matrix *= transform.matrix
        return matrix

    def totransform(self):
        """Converts the transform list into an equivalent transformation
        using a single transform function and returns it.
        The current transform list is not modified.

        Returns:
            SVGTransform: A new SVGTransform object or None.
        """
        matrix = self.tomatrix()
        if matrix is None:
            return None
        transform = SVGTransform.frommatrix(matrix)
        return transform

    def tostring(self, delimiter=None):
        items = list()
        for transform in iter(self):
            if not isinstance(transform, SVGTransform):
                raise TypeError('Expected Transform, got {}'.format(
                    type(transform)))
            items.append(transform.tostring(delimiter=delimiter))
        return ' '.join(items)
