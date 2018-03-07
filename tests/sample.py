#!/usr/bin/env python3

import sys
from io import StringIO

sys.path.extend(['.', '..'])

from svgpy import Node, SVGGeometryElement, SVGGraphicsElement, SVGParser


# from https://dev.w3.org/SVG/tools/svgweb/samples/svg-files/python.svg
PYTHON_SVG = '''
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
  <defs>
    <linearGradient id="pyYellow" gradientTransform="rotate(45)">
      <stop stop-color="#fe5" offset="0.6"/>
      <stop stop-color="#da1" offset="1"/>
    </linearGradient>
    <linearGradient id="pyBlue" gradientTransform="rotate(45)">
      <stop stop-color="#69f" offset="0.4"/>
      <stop stop-color="#468" offset="1"/>
    </linearGradient>
  </defs>

  <path d="M27,16c0-7,9-13,24-13c15,0,23,6,23,13l0,22c0,7-5,12-11,12l-24,0c-8,0-14,6-14,15l0,10l-9,0c-8,0-13-9-13-24c0-14,5-23,13-23l35,0l0-3l-24,0l0-9l0,0z M88,50v1" fill="url(#pyBlue)"/>
  <path d="M74,87c0,7-8,13-23,13c-15,0-24-6-24-13l0-22c0-7,6-12,12-12l24,0c8,0,14-7,14-15l0-10l9,0c7,0,13,9,13,23c0,15-6,24-13,24l-35,0l0,3l23,0l0,9l0,0z M140,50v1" fill="url(#pyYellow)"/>

  <circle r="4" cx="64" cy="88" fill="#FFF"/>
  <circle r="4" cx="37" cy="15" fill="#FFF"/>
</svg>
'''


def main():
    """Usage: python3 sample.py filename
    """
    if len(sys.argv) >= 2:
        source = sys.argv[1]
        print('"{}"'.format(source))
    else:
        source = StringIO(PYTHON_SVG)

    parser = SVGParser()
    tree = parser.parse(source)
    root = tree.getroot()
    for element in root.iter():
        print('node type: {}, node name: \'{}\''.format(
            element.node_type, element.node_name))
        print('- class:', type(element))
        if element.node_type == Node.COMMENT_NODE:
            continue

        print('- tag: \'{}\', tag name: \'{}\''.format(
            element.tag, element.tag_name))
        print('- id: {}'.format(
            None if element.id is None else '\'{}\''.format(element.id)))
        print('- attributes: ' + repr(element.attributes))
        if element.local_name == 'svg':
            vpx, vpy, vpw, vph = element.get_viewport_size()
            print('- viewport: x: {}, y: {}, width: {}, height: {}'.format(
                vpx.value(), vpy.value(), vpw.value(), vph.value()))

        if isinstance(element, SVGGraphicsElement):
            ctm = element.get_ctm()
            print('- ctm: {}'.format(ctm.toarray()))
            bbox = element.get_bbox()
            print('- bbox: x: {}, y: {}, width: {}, height: {}'.format(
                bbox.x, bbox.y, bbox.width, bbox.height))

        if isinstance(element, SVGGeometryElement):
            print('- geometry: {}'.format(element.get_computed_geometry()))
            print('- total length: {:g}'.format(element.get_total_length()))


if __name__ == '__main__':
    main()
