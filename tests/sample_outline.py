#!/usr/bin/env python3

import sys

sys.path.extend(['.', '..'])

from svgpy import Element, PathParser, SVGTransform, SVGTransformList, \
    formatter, window


def add_group(document, tx, ty, text_content, transform=None, rotate=None):
    root = document.document_element

    group = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'g')
    root.append(group)
    css_style = group.style
    css_style['font-family'] = 'DejaVu Sans'
    css_style['font-size'] = '36'
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
    if transform is not None:
        text.attributes['transform'] = transform
    if rotate is not None:
        text.attributes['rotate'] = rotate

    legend = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'text')
    group.append(legend)
    css_style = legend.style
    css_style['font-size'] = '12'
    legend.text_content = 'transform: "{}", rotate: "{}"'.format(
        transform if transform is not None else '',
        rotate if rotate is not None else '')

    path = document.create_element_ns(Element.SVG_NAMESPACE_URI, 'path')
    group.append(path)
    css_style = path.style
    css_style['fill'] = 'none'
    css_style['stroke'] = 'blue'
    css_style['stroke-width'] = '1'
    path_data = text.get_path_data()
    if transform is not None:
        transform_list = SVGTransformList.parse(transform)
        matrix = transform_list.matrix
        path_data = PathParser.transform(path_data, matrix)
    path.set_path_data(path_data)

    bbox = path.get_bbox()
    rect.attributes['x'] = str(bbox.x)
    rect.attributes['y'] = str(bbox.y)
    rect.attributes['width'] = str(bbox.width)
    rect.attributes['height'] = str(bbox.height)
    legend.attributes['x'] = str(bbox.right + 10)

    return bbox


def main():
    formatter.precision = 1
    document = window.document

    view_box_width = 800
    view_box_height = 0
    tx = 30
    ty = 50
    gap_height = 10
    args = [
        # (text_content, transform, rotate)
        ('Hello World!', None, None),
        ('Hello World!', None, '-15, 0, 15, 30'),
        ('Hello World!', 'translate(-10, 10)', None),
        ('Hello World!', 'scale(1.5, 0.8)', None),
        ('Hello World!', 'matrix(0.866, 0.5, -0.5, 0.866, 0, 0)', None),
        ('Hello World!', 'rotate(30)', None),
        ('Hello World!', 'rotate(30)', '-15, 0, 15, 30'),
        ('Hello World!', 'skewX(30)', None),
        ('Hello World!', 'skewY(30)', None),
        ('Hello World!', 'skewX(30) skewY(30)', None),
    ]
    for text_content, transform, rotate in args:
        bbox = add_group(document, tx, ty, text_content, transform, rotate)
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
