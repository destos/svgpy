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

import numpy as np

from .formatter import format_number_sequence


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
