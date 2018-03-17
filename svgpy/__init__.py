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


import svgpy.formatter as formatter
from svgpy.__version__ import __version__
from svgpy.base import \
    HTMLElement, SVGBoundingBoxOptions, \
    SVGElement, SVGGeometryElement, SVGGradientElement, SVGGraphicsElement, \
    SVGPathData, SVGPathDataSettings, SVGPreserveAspectRatio, \
    SVGURIReference, SVGZoomAndPan
from svgpy.core import Element, Font, Matrix, Node, SVGLength, Window
from svgpy.element import Comment, SVGElementClassLookup, SVGParser
from svgpy.path import PathParser, SVGPathSegment
from svgpy.rect import Rect
from svgpy.text import SVGTextContentElement, SVGTextPositioningElement
from svgpy.transform import SVGTransform, SVGTransformList
