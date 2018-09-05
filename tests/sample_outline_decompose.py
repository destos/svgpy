#!/usr/bin/env python3

import sys

sys.path.extend(['.', '..'])

from svgpy import Element, SVGPathSegment, SVGTransform, SVGTransformList, \
    formatter, window
from svgpy.fontconfig import FontConfig
from svgpy.freetype import FTFace, FTMatrix


# See also PathParser.from_glyph()
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


def _add_group(document, tx, ty, text_content, transform, path_data,
               font_family, font_size):
    root = document.document_element

    group = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'g')
    root.append(group)
    css_style = group.style
    css_style['font-family'] = font_family
    css_style['font-size'] = str(font_size)
    transform_list = SVGTransformList([
        SVGTransform(SVGTransform.SVG_TRANSFORM_TRANSLATE, tx, ty),
    ])
    group.transform = transform_list

    rect = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'rect')
    group.append(rect)
    css_style = rect.style
    css_style['fill'] = 'none'
    css_style['stroke'] = 'red'
    css_style['stroke-width'] = '1'
    css_style['stroke-dasharray'] = '2'

    circle = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'circle')
    group.append(circle)
    css_style = circle.style
    css_style['fill'] = 'red'
    circle.attributes['r'] = '2'

    text = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'text')
    group.append(text)
    css_style = text.style
    css_style['fill'] = 'skyblue'
    text.text_content = text_content
    if len(transform) > 0:
        text.attributes['transform'] = transform

    legend = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'text')
    group.append(legend)
    css_style = legend.style
    css_style['font-size'] = str(font_size // 3)
    legend.text_content = 'transform: "{}"'.format(transform)

    path = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'path')
    group.append(path)
    css_style = path.style
    css_style['fill'] = 'none'
    css_style['stroke'] = 'blue'
    css_style['stroke-width'] = '1'
    path.set_path_data(path_data)

    bbox = path.get_bbox()
    rect.attributes['x'] = str(bbox.x)
    rect.attributes['y'] = str(bbox.y)
    rect.attributes['width'] = str(bbox.width)
    rect.attributes['height'] = str(bbox.height)
    legend.attributes['x'] = str(bbox.right + 10)

    return bbox


def main():
    font_family = 'DejaVu Sans'
    result = FontConfig.match(font_family,
                              '%{{{}}}'.format(FontConfig.FC_FILE))
    if len(result) == 0:
        print('font file not found: "{}"'.format(font_family))
        sys.exit(1)
    face = FTFace.new_face(result[0])
    font_size = 36
    dpi = 96
    face.set_char_size(0, int(font_size * 3 / 4 * 64), dpi, dpi)
    outline = face.glyph.outline

    formatter.precision = 2
    document = window.document

    view_box_width = 800
    tx = 30
    ty = 50
    gap_height = 10
    text_content = 'M'

    transform = ''
    face.load_char(text_content[0])
    matrix = FTMatrix().flip_y()
    outline.transform(matrix)
    path_data = list()
    outline.decompose(_move_to, _line_to, _conic_to, _cubic_to,
                      user=path_data)
    bbox = _add_group(document, tx, ty, text_content, transform, path_data,
                      font_family, font_size)
    ty += int(bbox.height) + gap_height

    transform = 'scale(1.5, 0.8)'
    face.load_char(text_content[0])
    matrix = FTMatrix().flip_y()
    matrix.scale_self(1.5, 0.8)
    outline.transform(matrix)
    path_data = list()
    outline.decompose(_move_to, _line_to, _conic_to, _cubic_to,
                      user=path_data)
    bbox = _add_group(document, tx, ty, text_content, transform, path_data,
                      font_family, font_size)
    ty += int(bbox.height) + gap_height

    transform = 'rotate(30)'
    face.load_char(text_content[0])
    matrix = FTMatrix().flip_y()
    matrix.rotate_self(30)
    outline.transform(matrix)
    path_data = list()
    outline.decompose(_move_to, _line_to, _conic_to, _cubic_to,
                      user=path_data)
    bbox = _add_group(document, tx, ty, text_content, transform, path_data,
                      font_family, font_size)
    ty += int(bbox.height) + gap_height

    transform = 'skewX(45)'
    face.load_char(text_content[0])
    matrix = FTMatrix().flip_y()
    matrix.skew_x_self(45)
    outline.transform(matrix)
    path_data = list()
    outline.decompose(_move_to, _line_to, _conic_to, _cubic_to,
                      user=path_data)
    bbox = _add_group(document, tx, ty, text_content, transform, path_data,
                      font_family, font_size)
    ty += int(bbox.height) + gap_height

    transform = 'skewY(45)'
    face.load_char(text_content[0])
    matrix = FTMatrix().flip_y()
    matrix.skew_y_self(45)
    outline.transform(matrix)
    path_data = list()
    outline.decompose(_move_to, _line_to, _conic_to, _cubic_to,
                      user=path_data)
    bbox = _add_group(document, tx, ty, text_content, transform, path_data,
                      font_family, font_size)
    ty += int(bbox.height) + gap_height

    transform = 'scale(1.5, 0.8) rotate(30) skewX(45) skewY(45)'
    face.load_char(text_content[0])
    matrix = FTMatrix().flip_y()
    matrix.scale_self(1.5, 0.8)
    matrix.rotate_self(30)
    matrix.skew_x_self(45)
    matrix.skew_y_self(45)
    outline.transform(matrix)
    path_data = list()
    outline.decompose(_move_to, _line_to, _conic_to, _cubic_to,
                      user=path_data)
    bbox = _add_group(document, tx, ty, text_content, transform, path_data,
                      font_family, font_size)
    ty += int(bbox.height) + gap_height

    view_box_height = ty

    root = document.document_element
    root.attributes['width'] = str(view_box_width)
    root.attributes['height'] = str(view_box_height)
    root.attributes['viewBox'] = '0 0 {} {}'.format(view_box_width,
                                                    view_box_height)

    print(document.tostring(pretty_print=True).decode())


if __name__ == '__main__':
    main()
