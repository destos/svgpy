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
from svgpy.core import Font, SVGLength
from svgpy.dom import Comment, Element, Node
from svgpy.element import SVGElementClassLookup, SVGParser
from svgpy.geometry.matrix import DOMMatrix, DOMMatrixReadOnly
from svgpy.geometry.rect import DOMRect
from svgpy.path import PathParser, SVGPathSegment
from svgpy.screen import Screen
from svgpy.text import SVGTextContentElement, SVGTextPositioningElement
from svgpy.transform import SVGTransform, SVGTransformList
from svgpy.url import Location, URL, URLSearchParams
from svgpy.window import Document, SVGDOMImplementation, Window, XMLDocument, \
    window
