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
    """Returns a 2d (4x4) matrix.

    Arguments:
        a (float): The a component of the matrix.
        b (float): The b component of the matrix.
        c (float): The c component of the matrix.
        d (float): The d component of the matrix.
        e (float): The e component of the matrix.
        f (float): The f component of the matrix.
    Returns:
        numpy.matrix: A 4x4 matrix object.
    """
    return np.matrix([[float(a), float(c), float(0), float(e)],
                      [float(b), float(d), float(0), float(f)],
                      [float(0), float(0), float(1), float(0)],
                      [float(0), float(0), float(0), float(1)]])


def matrix3d(m11, m12, m13, m14,
             m21, m22, m23, m24,
             m31, m32, m33, m34,
             m41, m42, m43, m44):
    """Returns a 3d (4x4) matrix.

    Arguments:
        m11 (float): The m11 component of the matrix.
        m12 (float): The m12 component of the matrix.
        m13 (float): The m13 component of the matrix.
        m14 (float): The m14 component of the matrix.
        m21 (float): The m21 component of the matrix.
        m22 (float): The m22 component of the matrix.
        m23 (float): The m23 component of the matrix.
        m24 (float): The m24 component of the matrix.
        m31 (float): The m31 component of the matrix.
        m32 (float): The m32 component of the matrix.
        m33 (float): The m33 component of the matrix.
        m34 (float): The m34 component of the matrix.
        m41 (float): The m41 component of the matrix.
        m42 (float): The m42 component of the matrix.
        m43 (float): The m43 component of the matrix.
        m44 (float): The m44 component of the matrix.
    Returns:
        numpy.matrix: A 4x4 matrix object.
    """
    return np.matrix([[float(m11), float(m21), float(m31), float(m41)],
                      [float(m12), float(m22), float(m32), float(m42)],
                      [float(m13), float(m23), float(m33), float(m43)],
                      [float(m14), float(m24), float(m34), float(m44)]])


class Matrix(object):
    """Represents a 3d (4x4) matrix."""

    def __init__(self, *values, is2d=True):
        self._matrix = None
        self._is2d = None
        if len(values) > 0:
            self.set_matrix(*values)
        else:
            self.set_matrix(1, 0, 0, 1, 0, 0)
            self._is2d = is2d

    def __deepcopy__(self, memodict={}):
        x = Matrix()
        if self._matrix is not None:
            x._matrix = np.matrix.copy(self._matrix)
            x._is2d = self._is2d
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
        return self._matrix[0, 3]

    @e.setter
    def e(self, value):
        self._matrix[0, 3] = float(value)

    @property
    def f(self):
        """float: The f component of the matrix."""
        return self._matrix[1, 3]

    @f.setter
    def f(self, value):
        self._matrix[1, 3] = float(value)

    @property
    def is2d(self):
        return self._is2d

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
    def m13(self):
        """float: The m13 component of the matrix."""
        return self._matrix[2, 0]

    @m13.setter
    def m13(self, value):
        self._matrix[2, 0] = float(value)

    @property
    def m14(self):
        """float: The m14 component of the matrix."""
        return self._matrix[3, 0]

    @m14.setter
    def m14(self, value):
        self._matrix[3, 0] = float(value)

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
    def m23(self):
        """float: The m23 component of the matrix."""
        return self._matrix[2, 1]

    @m23.setter
    def m23(self, value):
        self._matrix[2, 1] = float(value)

    @property
    def m24(self):
        """float: The m24 component of the matrix."""
        return self._matrix[3, 1]

    @m24.setter
    def m24(self, value):
        self._matrix[3, 1] = float(value)

    @property
    def m31(self):
        """float: The m31 component of the matrix."""
        return self._matrix[0, 2]

    @m31.setter
    def m31(self, value):
        self._matrix[0, 2] = float(value)

    @property
    def m32(self):
        """float: The m32 component of the matrix."""
        return self._matrix[1, 2]

    @m32.setter
    def m32(self, value):
        self._matrix[1, 2] = float(value)

    @property
    def m33(self):
        """float: The m33 component of the matrix."""
        return self._matrix[2, 2]

    @m33.setter
    def m33(self, value):
        self._matrix[2, 2] = float(value)

    @property
    def m34(self):
        """float: The m34 component of the matrix."""
        return self._matrix[3, 2]

    @m34.setter
    def m34(self, value):
        self._matrix[3, 2] = float(value)

    @property
    def m41(self):
        """float: The m41 component of the matrix."""
        return self._matrix[0, 3]

    @m41.setter
    def m41(self, value):
        self._matrix[0, 3] = float(value)

    @property
    def m42(self):
        """float: The m42 component of the matrix."""
        return self._matrix[1, 3]

    @m42.setter
    def m42(self, value):
        self._matrix[1, 3] = float(value)

    @property
    def m43(self):
        """float: The m43 component of the matrix."""
        return self._matrix[2, 3]

    @m43.setter
    def m43(self, value):
        self._matrix[2, 3] = float(value)

    @property
    def m44(self):
        return self._matrix[3, 3]

    @m44.setter
    def m44(self, value):
        self._matrix[3, 3] = float(value)

    @property
    def matrix(self):
        """numpy.matrix: The current matrix."""
        return self._matrix

    def clear(self, is2d=True):
        """Sets the matrix [1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1].

        Returns:
            Matrix: Returns itself.
        """
        self.set_matrix(1, 0, 0, 0,
                        0, 1, 0, 0,
                        0, 0, 1, 0,
                        0, 0, 0, 1)
        self._is2d = is2d
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
        import ast
        fields = ast.literal_eval(text)
        if fields['Is2D']:
            matrix = Matrix(fields['M11'], fields['M12'],
                            fields['M21'], fields['M22'],
                            fields['M41'], fields['M42'])
        else:
            matrix = Matrix(
                fields['M11'], fields['M12'], fields['M13'], fields['M14'],
                fields['M21'], fields['M22'], fields['M23'], fields['M24'],
                fields['M31'], fields['M32'], fields['M33'], fields['M34'],
                fields['M41'], fields['M42'], fields['M43'], fields['M44'])
        return matrix

    @staticmethod
    def frommatrix(matrix):
        """Constructs a new Matrix initialized with the numpy.matrix matrix.

        Arguments:
            matrix (numpy.matrix): A 4x4 matrix object.
        Returns:
            Matrix: A new Matrix object.
        """
        if matrix is None or (not isinstance(matrix, np.matrix)):
            raise TypeError('Expected numpy.matrix, got {}'.format(
                type(matrix)))
        elif matrix.shape != (4, 4):
            raise ValueError('Expected 4x4 matrix, got {}'.format(
                matrix.tolist()))
        x = Matrix()
        x._matrix = np.matrix.copy(matrix)
        if ((x.m13 or x.m14 or x.m23 or x.m24 or x.m31 or x.m32
             or x.m34 or x.m43)
                or (x.m33 != 1 or x.m44 != 1)):
            x._is2d = False
        else:
            x._is2d = True
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
        rot_z = math.atan2(self.m12, self.m11)
        if degrees:
            rot_z = math.degrees(rot_z)
        if self._is2d:
            return rot_z
        rot_y = math.atan2(-self.m13,
                           math.sqrt(self.m23 ** 2 + self.m33 ** 2))
        rot_x = math.atan2(self.m23, self.m33)
        if degrees:
            rot_y = math.degrees(rot_y)
            rot_x = math.degrees(rot_x)
        return rot_x, rot_y, rot_z

    def get_scale(self):
        """Returns the scale amounts.

        Returns:
             tuple[float, float]: The scale amounts.
        """
        m11 = self.m11
        m12 = self.m12
        m13 = self.m13
        m21 = self.m21
        m22 = self.m22
        m23 = self.m23
        sx = math.sqrt(m11 ** 2 + m12 ** 2 + m13 ** 2)
        sy = math.sqrt(m21 ** 2 + m22 ** 2 + m23 ** 2)
        if self._is2d:
            return sx, sy
        m31 = self.m31
        m32 = self.m32
        m33 = self.m33
        sz = math.sqrt(m31 ** 2 + m32 ** 2 + m33 ** 2)
        return sx, sy, sz

    def get_translate(self):
        """Returns the translation amounts.

        Returns:
             tuple[float, float]: The translation amounts.
        """
        tx = self.m41
        ty = self.m42
        if self._is2d:
            return tx, ty
        tz = self.m43
        return tx, ty, tz

    def inverse(self):
        """Returns the inverse matrix.
        The current matrix is not modified.

        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.invert_self()
        return x

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
        self._matrix *= other._matrix
        if not other._is2d:
            self._is2d = False
        return self

    def point(self, x, y, z=0, w=1):
        """Post-multiplies the transformation [x y z w] and returns the
        resulting point.

        Arguments:
            x (float): The x-coordinate to transform.
            y (float): The y-coordinate to transform.
            z (float, optional): The z-coordinate to transform.
            w (float, optional): The w-coordinate to transform.
        Returns:
             tuple[float, float]: The resulting coordinates.
        """
        pt = np.matrix([[float(x)], [float(y)], [float(z)], [float(w)]])
        pt = self._matrix * pt
        if self._is2d and z == 0 and w == 1:
            return pt.item(0), pt.item(1)
        return pt.item(0), pt.item(1), pt.item(2), pt.item(3)

    def rotate(self, rot_x=0, rot_y=0, rot_z=0):
        """Post-multiplies a rotation transformation on the current matrix and
        returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            rot_x (float, optional): The x-axis rotation angle in degrees.
            rot_y (float, optional): The y-axis rotation angle in degrees.
            rot_z (float, optional): The z-axis rotation angle in degrees.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.rotate_self(rot_x, rot_y, rot_z)
        return x

    def rotate_axis_angle(self, x=0, y=0, z=0, angle=0):
        m = copy.deepcopy(self)
        m.rotate_axis_angle_self(x, y, z, angle)
        return m

    def rotate_axis_angle_self(self, x=0, y=0, z=0, angle=0):
        length = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        if length == 0:
            return self
        elif length != 1:
            x /= length
            y /= length
            z /= length

        t = math.radians(angle)
        sin = math.sin(t)
        cos = math.cos(t)
        if x == 0 and y == 0 and z == 1:
            # [0, 0, 1, rot_z]
            r = np.matrix([[cos, -sin, 0, 0],
                           [sin, cos, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]])
        elif x == 0 and y == 1 and z == 0:
            # [0, 1, 0, rot_y]
            r = np.matrix([[cos, 0, sin, 0],
                           [0, 1, 0, 0],
                           [-sin, 0, cos, 0],
                           [0, 0, 0, 1]])
        elif x == 1 and y == 0 and z == 0:
            # [1, 0, 0, rot_x]
            r = np.matrix([[1, 0, 0, 0],
                           [0, cos, -sin, 0],
                           [0, sin, cos, 0],
                           [0, 0, 0, 1]])
        else:
            r = np.matrix([[cos + x ** 2 * (1 - cos),
                            x * y * (1 - cos) - z * sin,
                            x * z * (1 - cos) - y * sin,
                            0],
                           [y * x * (1 - cos) + z * sin,
                            cos + y ** 2 * (1 - cos),
                            y * z * (1 - cos) + x * sin,
                            0],
                           [z * x * (1 - cos) - y * sin,
                            z * y * (1 - cos) + x * sin,
                            cos + z ** 2 * (1 - cos),
                            0],
                           [0, 0, 0, 1]])
        self._matrix *= r
        return self

    def rotate_self(self, rot_x=0, rot_y=0, rot_z=0):
        """Post-multiplies a rotation transformation on the current matrix.

        Arguments:
            rot_x (float, optional): The x-axis rotation angle in degrees.
            rot_y (float, optional): The y-axis rotation angle in degrees.
            rot_z (float, optional): The z-axis rotation angle in degrees.
        Returns:
            Matrix: Returns itself.
        """
        if rot_z != 0:
            self.rotate_axis_angle_self(0, 0, 1, rot_z)

        if rot_y != 0:
            self.rotate_axis_angle_self(0, 1, 0, rot_y)
            self._is2d = False

        if rot_x != 0:
            self.rotate_axis_angle_self(1, 0, 0, rot_x)
            self._is2d = False

        return self

    def scale(self, scale_x=1, scale_y=None, scale_z=1,
              origin_x=0, origin_y=0, origin_z=0):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            scale_x (float, optional): The scale amount in X.
            scale_y (float, optional): The scale amount in Y.
            scale_z (float, optional): The scale amount in Z.
            origin_x (float, optional): The translation amount in X.
            origin_y (float, optional): The translation amount in Y.
            origin_z (float, optional): The translation amount in Z.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.scale_self(scale_x, scale_y, scale_z, origin_x, origin_y, origin_z)
        return x

    def scale_self(self, scale_x=1, scale_y=None, scale_z=1,
                   origin_x=0, origin_y=0, origin_z=0):
        """Post-multiplies a non-uniform scale transformation on the current
        matrix.

        Arguments:
            scale_x (float, optional): The scale amount in X.
            scale_y (float, optional): The scale amount in Y.
            scale_z (float, optional): The scale amount in Z.
            origin_x (float, optional): The translation amount in X.
            origin_y (float, optional): The translation amount in Y.
            origin_z (float, optional): The translation amount in Z.
      Returns:
            Matrix: Returns itself.
        """
        if scale_y is None:
            scale_y = scale_x
        if scale_x == 1 and scale_y == 1 and scale_z == 1:
            return self
        if origin_x != 0 or origin_y != 0 or origin_z != 0:
            self.translate_self(origin_x, origin_y, origin_z)
        m = np.matrix([[scale_x, 0, 0, 0],
                       [0, scale_y, 0, 0],
                       [0, 0, scale_z, 0],
                       [0, 0, 0, 1]])
        self._matrix *= m
        if scale_z != 1:
            self._is2d = False
        if origin_x != 0 or origin_y != 0 or origin_z != 0:
            self.translate_self(-origin_x, -origin_y, -origin_z)
        return self

    def scale3d(self, scale=1, origin_x=0, origin_y=0, origin_z=0):
        return self.scale(scale, scale, scale, origin_x, origin_y, origin_z)

    def scale3d_self(self, scale=1, origin_x=0, origin_y=0, origin_z=0):
        return self.scale_self(scale, scale, scale,
                               origin_x, origin_y, origin_z)

    def set_matrix(self, *values):
        """Sets the matrix.

        Arguments:
            *values:
        """
        if len(values) == 6:
            self._matrix = matrix2d(*values)
            self._is2d = True
        else:
            self._matrix = matrix3d(*values)
            self._is2d = False

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
        if self._is2d:
            serialized = {
                'M11': self.m11,
                'M12': self.m12,
                'M21': self.m21,
                'M22': self.m22,
                'M41': self.m41,
                'M42': self.m42,
                'Is2D': 1,
            }
        else:
            serialized = {
                'M11': self.m11,
                'M12': self.m12,
                'M13': self.m13,
                'M14': self.m14,
                'M21': self.m21,
                'M22': self.m22,
                'M23': self.m23,
                'M24': self.m24,
                'M31': self.m31,
                'M32': self.m32,
                'M33': self.m33,
                'M34': self.m34,
                'M41': self.m41,
                'M42': self.m42,
                'M43': self.m43,
                'M44': self.m44,
                'Is2D': 0,
            }
        return repr(serialized)

    def toarray(self):
        return [self.m11, self.m12, self.m13, self.m14,
                self.m21, self.m22, self.m23, self.m24,
                self.m31, self.m32, self.m33, self.m34,
                self.m41, self.m42, self.m43, self.m44]

    def tolist(self):
        return self._matrix.tolist()

    def tostring(self, delimiter=None):
        if self._is2d:
            name = 'matrix'
            elements = [self.m11, self.m12,
                        self.m21, self.m22,
                        self.m41, self.m42]
        else:
            name = 'matrix3d'
            elements = [self.m11, self.m12, self.m13, self.m14,
                        self.m21, self.m22, self.m23, self.m24,
                        self.m31, self.m32, self.m33, self.m34,
                        self.m41, self.m42, self.m43, self.m44]
        number_sequence = format_number_sequence(elements)
        if delimiter is None or len(delimiter) == 0:
            delimiter = ' '
        return '{}({})'.format(name, delimiter.join(number_sequence))

    def translate(self, tx=0, ty=0, tz=0):
        """Post-multiplies a translation transformation on the current matrix
        and returns the resulting matrix.
        The current matrix is not modified.

        Arguments:
            tx (float, optional): The translation amount in X.
            ty (float, optional): The translation amount in Y.
            tz (float, optional): The translation amount in Z.
        Returns:
            Matrix: The resulting matrix.
        """
        x = copy.deepcopy(self)
        x.translate_self(tx, ty, tz)
        return x

    def translate_self(self, tx=0, ty=0, tz=0):
        """Post-multiplies a translation transformation on the current
        matrix.

        Arguments:
            tx (float, optional): The translation amount in X.
            ty (float, optional): The translation amount in Y.
            tz (float, optional): The translation amount in Z.
        Returns:
            Matrix: Returns itself.
        """
        if tx == 0 and ty == 0 and tz == 0:
            return self
        m = np.matrix([[1, 0, 0, tx],
                       [0, 1, 0, ty],
                       [0, 0, 1, tz],
                       [0, 0, 0, 1]])
        self._matrix *= m
        if tz:
            self._is2d = False
        return self
