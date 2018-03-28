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


import re
from abc import ABC, abstractmethod
from collections.abc import MutableMapping

from lxml import etree

from .core import CSSUtils, Font, SVGLength


def dict_to_style(d):
    if d is None:
        return ''
    items = ['{}: {};'.format(x, d[x]) for x in iter(d.keys())]
    return ' '.join(sorted(items))


def style_to_dict(text):
    if text is None:
        return {}
    items = [x.split(':') for x in iter(text.strip().split(';'))]
    if [''] in items:
        items.remove([''])
    return {key.strip(): value.strip() for key, value in iter(items)}


class Attrib(MutableMapping):
    """A wrapper class for lxml.etree._Attrib."""

    def __init__(self, attrib):
        """Constructs a Attrib object.

        Arguments:
            attrib (lxml.etree._Attrib): An attribute object.
        """
        self._attrib = attrib  # type: dict

    def __delitem__(self, name):
        """Removes an element attribute with the specified name.

        Arguments:
            name (str): The name of the attribute.
        """
        if name in self._attrib:
            del self._attrib[name]
            return
        style = self.get_style({})
        del style[name]
        if len(style) > 0:
            self.set_style(style)
        else:
            del self._attrib['style']

    def __getitem__(self, name):
        """Gets an element attribute with the specified name.

        Arguments:
            name (str): The name of the attribute.
        Returns:
            str: Returns the value of the specified attribute.
                Raises a KeyError if the attribute doesn't exists.
        """
        value = self._attrib.get(name)
        if value is not None:
            return value.strip()
        style = self.get_style()
        if style is not None:
            return style[name]
        raise KeyError

    def __iter__(self):
        for x in self._attrib:
            yield x

    def __len__(self):
        return len(self._attrib)

    def __repr__(self):
        return repr(self._attrib)

    def __setitem__(self, name, value):
        """Sets an element attribute with the specified name.

        Arguments:
            name (str): The name of the attribute.
            value (str): The value of the attribute.
        """
        self.set(name, value)

    def get_ns(self, namespace, local_name, default=None):
        """Gets an element attribute with the specified namespace and name.

        Arguments:
            namespace (str): The namespace URI.
            local_name (str): The local name of the attribute.
            default (str, optional): The default value of the attribute.
        Returns:
            str: Returns the value of the specified attribute if the attribute
                exists, else default.
        """
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        return self.get(name, default)

    def get_style(self, default=None):
        """Returns the 'style' attribute.

        Arguments:
            default (dict, optional): The default value of the attribute.
        Returns:
            dict: Returns the value of the 'style' attribute if the attribute
                exists, else default.
        """
        style = self._attrib.get('style')
        if style is None:
            return default
        return style_to_dict(style)

    def has(self, name):
        """Returns True if an element attribute with the specified name exists;
        otherwise returns False.

        Arguments:
            name (str): The name of the attribute.
        Returns:
            bool: Returns True if the attribute exists, else False.
        """
        if name in self._attrib:
            return True
        style = self.get_style({})
        return name in style

    def has_ns(self, namespace, local_name):
        """Returns True if an element attribute with the specified namespace
        and name exists; otherwise returns False.

        Arguments:
            namespace (str): The namespace URI.
            local_name (str): The local name of the attribute.
        Returns:
            bool: Returns True if the attribute exists, else False.
        """
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        return self.has(name)

    def pop(self, name, default=None):
        """Removes an element attribute with the specified name and returns the
        value associated with it.

        Arguments:
            name (str): The name of the attribute.
            default (str, optional): The default value of the attribute.
        Returns:
            str: Returns the value of the specified attribute if the attribute
                exists, else default.
        """
        try:
            value = self.__getitem__(name)
            self.__delitem__(name)
            return value
        except KeyError:
            return default

    def pop_ns(self, namespace, local_name, default=None):
        """Removes an element attribute with the specified namespace and name,
        and returns the value associated with it.

        Arguments:
            namespace (str): The namespace URI.
            local_name (str): The local name of the attribute.
            default (str, optional): The default value of the attribute.
        Returns:
            str: Returns the value of the specified attribute if the attribute
                exists, else default.
        """
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        return self.pop(name, default)

    def set(self, name, value):
        """Sets an element attribute.

        Arguments:
            name (str): The name of the attribute.
            value (str): The value of the attribute.
        """
        if name in self._attrib:
            self._attrib[name] = value
            return
        style = self.get_style()
        if style is not None and name in style:
            style[name] = value
            self.set_style(style)
            return
        self._attrib[name] = value

    def set_ns(self, namespace, local_name, value):
        """Sets an element attribute with the specified namespace and name.

        Arguments:
            namespace (str): The namespace URI.
            local_name (str): The local name of the attribute.
            value (str): The value of the attribute.
        """
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        self.set(name, value)

    def setdefault(self, name, default=None):
        """If the specified attribute exists, returns its value. If not, sets
        an element attribute with a value of default and returns default.

        Arguments:
            name (str): The name of the attribute.
            default (str, optional): The default value of the attribute.
        Returns:
            str: Returns the value of the specified attribute if the attribute
                exists, else default.
        """
        # override
        value = self.get(name)
        if value is not None:
            return value
        self._attrib[name] = default
        return default

    def setdefault_ns(self, namespace, local_name, default):
        """If the specified attribute exists, returns its value. If not, sets
        an element attribute with a value of default and returns default.

        Arguments:
            namespace (str): The namespace URI.
            local_name (str): The local name of the attribute.
            default (str, optional): The default value of the attribute.
        Returns:
            str: Returns the value of the specified attribute if the attribute
                exists, else default.
        """
        if namespace is None:
            name = local_name
        else:
            name = '{{{0}}}{1}'.format(namespace, local_name)
        return self.setdefault(name, default)

    def set_style(self, d):
        """Sets the 'style' attribute.

        Arguments:
            d (dict): The value of the 'style' attribute.
        """
        style = dict_to_style(d)
        self._attrib['style'] = style

    def update_style(self, other):
        """Updates the 'style' attribute with the key/value pairs from other.

        Arguments:
            other (dict): The key/value pairs of the 'style' attribute to be
                updated.
        """
        style = self.get_style({})
        style.update(other)
        self.set_style(style)


# See https://dom.spec.whatwg.org/#interface-node
# See https://www.w3.org/TR/2015/REC-dom-20151119/#interface-node
class Node(ABC):
    """Represents the DOM Node."""

    ELEMENT_NODE = 1
    COMMENT_NODE = 8

    @property
    @abstractmethod
    def node_name(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def node_type(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def node_value(self):
        raise NotImplementedError

    @node_value.setter
    @abstractmethod
    def node_value(self, text):
        raise NotImplementedError

    @property
    @abstractmethod
    def text_content(self):
        raise NotImplementedError

    @text_content.setter
    @abstractmethod
    def text_content(self, text):
        raise NotImplementedError


class CharacterData(Node):
    @property
    @abstractmethod
    def data(self):
        raise NotImplementedError

    @data.setter
    @abstractmethod
    def data(self, data):
        raise NotImplementedError

    @property
    def node_value(self):
        raise NotImplementedError

    @node_value.setter
    def node_value(self, text):
        raise NotImplementedError

    @property
    def text_content(self):
        raise NotImplementedError

    @text_content.setter
    def text_content(self, text):
        raise NotImplementedError


# See https://dom.spec.whatwg.org/#interface-comment
# See https://www.w3.org/TR/2015/REC-dom-20151119/#interface-comment
# See https://www.w3.org/TR/2015/REC-dom-20151119/#interface-characterdata
# Node > CharacterData > Comment
class Comment(etree.CommentBase, CharacterData):
    """Represents the DOM Comment."""

    @property
    def data(self):
        return '' if self.text is None else self.text

    @data.setter
    def data(self, data):
        self.text = data

    @property
    def node_name(self):
        return '#comment'

    @property
    def node_type(self):
        return Node.COMMENT_NODE

    @property
    def node_value(self):
        return self.text

    @node_value.setter
    def node_value(self, text):
        self.text = text

    @property
    def text_content(self):
        return self.text

    @text_content.setter
    def text_content(self, text):
        self.text = text

    def tostring(self):
        return '' if self.text is None else '<!--{}-->'.format(self.text)


# See https://dom.spec.whatwg.org/#interface-element
# See https://www.w3.org/TR/2015/REC-dom-20151119/#interface-element
# Node > Element > SVGElement
class Element(etree.ElementBase, Node):
    """Represents the DOM Element."""

    SVG_NAMESPACE_URI = 'http://www.w3.org/2000/svg'
    XHTML_NAMESPACE_URI = 'http://www.w3.org/1999/xhtml'
    XLINK_NAMESPACE_URI = 'http://www.w3.org/1999/xlink'
    XML_NAMESPACE_URI = 'http://www.w3.org/XML/1998/namespace'

    XML_LANG = '{{{0}}}lang'.format(XML_NAMESPACE_URI)

    DESCRIPTIVE_ELEMENTS = ['desc', 'metadata', 'title']

    STRUCTURAL_ELEMENTS = ['defs', 'g', 'svg', 'symbol', 'use']

    STRUCTURALLY_EXTERNAL_ELEMENTS = \
        ['audio', 'foreignObject', 'iframe', 'image', 'script', 'use', 'video']

    CONTAINER_ELEMENTS = \
        ['a', 'clipPath', 'defs', 'g', 'marker', 'mask', 'pattern', 'svg',
         'switch', 'symbol', 'unknown']

    GRAPHICS_ELEMENTS = \
        ['audio', 'canvas', 'circle', 'ellipse', 'foreignObject', 'iframe',
         'image', 'line', 'mesh', 'path', 'polygon', 'polyline', 'rect',
         'text', 'textPath', 'tspan', 'video']

    GRAPHICS_REFERENCING_ELEMENTS = \
        ['audio', 'iframe', 'image', 'mesh', 'use', 'video']

    RENDERABLE_ELEMENTS = \
        ['a', 'audio', 'canvas', 'circle', 'ellipse', 'foreignObject', 'g',
         'iframe', 'image', 'line', 'mesh', 'path', 'polygon', 'polyline',
         'rect', 'svg', 'switch', 'text', 'textPath', 'tspan', 'unknown',
         'use', 'video']

    SHAPE_ELEMENTS = \
        ['circle', 'ellipse', 'line', 'mesh', 'path', 'polygon', 'polyline',
         'rect']

    TEXT_CONTENT_ELEMENTS = ['text', 'tspan']
    # TODO: add 'textPath' element to TEXT_CONTENT_ELEMENTS.

    TEXT_CONTENT_CHILD_ELEMENTS = ['textPath', 'tspan']

    TRANSFORMABLE_ELEMENTS = \
        ['a', 'defs', 'foreignObject', 'g', 'svg', 'switch',
         'use', ] + GRAPHICS_ELEMENTS
    # TODO: add 'clipPath' element to TRANSFORMABLE_ELEMENTS.

    RE_DIGIT_SEQUENCE_SPLITTER = re.compile(r'\s*,\s*|\s+')

    def _init(self):
        self._attributes = Attrib(self.attrib)

    @property
    def attributes(self):
        """Attrib: A dictionary of an element attributes."""
        return self._attributes

    @property
    def class_list(self):
        """list[str]: A list of classes."""
        classes = self.class_name
        if classes is None:
            return []
        return classes.split()

    @property
    def class_name(self):
        """str: Reflects the 'class' attribute."""
        return self.attributes.get('class')

    @class_name.setter
    def class_name(self, class_name):
        self.attributes.set('class', class_name)

    @property
    def id(self):
        """str: Reflects the 'id' attribute."""
        return self.attributes.get('id')

    @id.setter
    def id(self, element_id):
        self.attributes.set('id', element_id)

    @property
    def local_name(self):
        """str: The local part of the qualified name of an element."""
        return self.qname.localname

    @property
    def namespace_uri(self):
        return self.nsmap.get(self.prefix)

    @property
    def node_name(self):
        return self.tag_name

    @property
    def node_type(self):
        return Node.ELEMENT_NODE

    @property
    def node_value(self):
        return None

    @node_value.setter
    def node_value(self, node_value):
        pass  # do nothing

    @property
    def qname(self):
        """lxml.etree.QName: The qualified XML name of an element."""
        qname = etree.QName(self)
        return qname

    @property
    def tag_name(self):
        prefix = self.prefix
        local_name = self.local_name
        if prefix is not None:
            return prefix + ':' + local_name
        return local_name

    @property
    def text_content(self):
        """str: Implements Node#textContent."""
        # See https://dom.spec.whatwg.org/#dom-node-textcontent
        local_name = self.local_name
        if local_name in Element.DESCRIPTIVE_ELEMENTS:
            return self.text
        elif local_name in Element.TEXT_CONTENT_ELEMENTS:
            chars = Element._get_text_content(self)
            return ''.join(chars)
        return None

    @text_content.setter
    def text_content(self, text):
        for child in iter(self):
            self.remove(child)
        self.text = text

    @staticmethod
    def _get_text_content(element):
        # See https://dom.spec.whatwg.org/#dom-node-textcontent
        chars = list()
        if element.text is not None:
            chars.append(element.text)

        for child in iter(element):
            if child.node_type != Node.ELEMENT_NODE:
                continue
            local_name = child.local_name
            if local_name in Element.TEXT_CONTENT_ELEMENTS:
                contents = Element._get_text_content(child)
                chars.extend(contents)
                if (local_name in Element.TEXT_CONTENT_CHILD_ELEMENTS
                        and child.tail is not None):
                    chars.append(child.tail)
        return chars

    def get_computed_geometry(self):
        return {}  # override with a subclass

    def get_computed_style(self):
        """Gets the presentation attributes from ancestor elements."""
        style = self.get_inherited_style()

        # 'font-feature-settings' property
        style['font-feature-settings'] = CSSUtils.parse_font_feature_settings(
            style['font-feature-settings'])

        # 'font-size' property
        style['font-size'] = CSSUtils.compute_font_size(
            self,
            inherited_style=style)

        # 'font-size-adjust' property
        style['font-size-adjust'] = CSSUtils.compute_font_size_adjust(style)

        # 'font-synthesis' property
        # Value: none | [weight || style]
        items = style['font-synthesis'].split()
        items = [x for x in items if x in ['weight', 'style', 'none']]
        if 'none' in items and len(items) != 1:
            items = ['none']
        style['font-synthesis'] = items

        # 'font-weight' property
        style['font-weight'] = CSSUtils.compute_font_weight(
            self,
            inherited_style=style)

        # 'line-height' property
        style['line-height'] = CSSUtils.compute_line_height(self, style)

        # 'inline-size' property
        # Value: <length> | <percentage> | <number>
        # Initial: 0
        # Percentages: Refer to the width (for horizontal text) or height
        #  (for vertical text) of the current SVG viewport
        inline_size = style['inline-size']
        writing_mode = style['writing-mode']
        mode = SVGLength.DIRECTION_HORIZONTAL if writing_mode in [
            'horizontal-tb', 'lr', 'lr-tb', 'rl', 'rl-tb'
        ] else SVGLength.DIRECTION_VERTICAL
        style['inline-size'] = SVGLength(inline_size).value(direction=mode)

        # 'stroke-width' property
        # Value: <percentage> | <length>
        # Initial: 1
        # Percentages: refer to the size of the current SVG viewport
        stroke_width = style['stroke-width']
        style['stroke-width'] = SVGLength(
            stroke_width,
            context=self).value(direction=SVGLength.DIRECTION_OTHER)

        # 'tab-size' property
        # Value: <percentage> | <length>
        # Initial: 8
        # See https://drafts.csswg.org/css-text-3/#tab-size-property
        tab_size = style['tab-size']
        style['tab-size'] = SVGLength(
            tab_size,
            context=self).value(direction=SVGLength.DIRECTION_OTHER)

        # geometry properties
        geometry = self.get_computed_geometry()
        style.update(geometry)
        return style

    def get_inherited_style(self):
        def _update_font_prop(_value, _style, _inherited_style):
            _other = CSSUtils.parse_font(_value)
            for _key in _other:
                if _key not in _style:
                    _style[_key] = _other[_key]
                    if _key == 'font-variant':
                        _update_font_variant_prop(_other[_key],
                                                  _style,
                                                  _inherited_style)
            _inherited_style.pop('font-style', None)
            _inherited_style.pop('font-variant', None)
            _inherited_style.pop('font-weight', None)
            _inherited_style.pop('font-stretch', None)
            _inherited_style.pop('font-size', None)
            _inherited_style.pop('line-height', None)
            _inherited_style.pop('font-size-adjust', None)
            _inherited_style.pop('font-kerning', None)
            _inherited_style.pop('font-language-override', None)
            _inherited_style.pop('font-family', None)
            _inherited_style.pop('font', None)

        def _update_font_variant_prop(_value, _style, _inherited_style):
            _other = CSSUtils.parse_font_variant(_value)
            for _key in _other:
                if _key not in _style:
                    _style[_key] = _other[_key]
            _inherited_style.pop('font-variant-alternates', None)
            _inherited_style.pop('font-variant-caps', None)
            _inherited_style.pop('font-variant-east-asian', None)
            _inherited_style.pop('font-variant-ligatures', None)
            _inherited_style.pop('font-variant-numeric', None)
            _inherited_style.pop('font-variant-position', None)
            _inherited_style.pop('font-variant', None)

        # TODO: see CSS style sheet.
        # See https://svgwg.org/svg2-draft/propidx.html
        style = dict()
        non_inherited_props = \
            {'alignment-baseline': 'baseline',
             'baseline-shift': '0',
             'clip': 'auto',
             'clip-path': 'none',
             'display': 'inline',
             'dominant-baseline': 'auto',
             'filter': 'none',
             'flood-color': 'black',
             'flood-opacity': '1',
             'inline-size': '0',
             'lighting-color': 'white',
             'mask': 'no',
             'opacity': '1',
             'overflow': 'visible',
             'stop-color': 'black',
             'stop-opacity': '1',
             'text-decoration': 'none',
             'transform': 'none',
             'unicode-bidi': 'normal',
             'vector-effect': 'none',
             }
        attributes = self.attributes
        for key in iter(non_inherited_props.keys()):
            style.setdefault(key,
                             attributes.get(key, non_inherited_props[key]))

        inherited_props = \
            {'clip-rule': 'nonzero',
             'color': 'black',  # depends on user agent
             'color-interpolation': 'sRGB',
             'color-rendering': 'auto',
             'cursor': 'auto',
             'direction': 'ltr',
             'fill': 'black',
             'fill-opacity': '1',
             'fill-rule': 'nonzero',
             'font': None,
             'font-family': None,
             'font-feature-settings': 'normal',
             'font-kerning': Font.CSS_DEFAULT_FONT_KERNING,
             'font-language-override': Font.CSS_DEFAULT_FONT_LANGUAGE_OVERRIDE,
             'font-size': Font.CSS_DEFAULT_FONT_SIZE,
             'font-size-adjust': Font.CSS_DEFAULT_FONT_SIZE_ADJUST,
             'font-stretch': Font.CSS_DEFAULT_FONT_STRETCH,
             'font-style': Font.CSS_DEFAULT_FONT_STYLE,
             'font-synthesis': 'weight style',
             'font-variant': Font.CSS_DEFAULT_FONT_VARIANT,
             'font-variant-alternates': ['normal'],
             'font-variant-caps': 'normal',
             'font-variant-east-asian': ['normal'],
             'font-variant-ligatures': ['normal'],
             'font-variant-numeric': ['normal'],
             'font-variant-position': 'normal',
             'font-weight': Font.CSS_DEFAULT_FONT_WEIGHT,
             # 'glyph-orientation-vertical': 'auto',  # deprecated
             'image-rendering': 'auto',
             'lang': None,
             'letter-spacing': 'normal',
             'line-height': Font.CSS_DEFAULT_LINE_HEIGHT,
             'marker': None,
             'marker-end': 'none',
             'marker-mid': 'none',
             'marker-start': 'none',
             'paint-order': 'normal',
             'pointer-events': 'visiblePainted',
             'shape-rendering': 'auto',
             'stroke': 'none',
             'stroke-dasharray': 'none',
             'stroke-dashoffset': '0',
             'stroke-linecap': 'butt',
             'stroke-linejoin': 'miter',
             'stroke-miterlimit': '4',
             'stroke-opacity': '1',
             'stroke-width': '1',
             'tab-size': '8',
             'text-anchor': 'start',
             'text-orientation': 'mixed',
             'text-rendering': 'auto',
             'visibility': 'visible',
             'white-space': 'normal',
             'word-spacing': 'normal',
             'writing-mode': 'horizontal-tb',
             Element.XML_LANG: None,
             }
        # 'color-interpolation-filters', 'font-feature-settings',
        # 'gradientTransform', 'glyph-orientation-horizontal',
        # 'isolation',
        # 'patternTransform',
        # 'solid-color', 'solid-opacity',
        # 'text-align', 'text-align-all', 'text-align-last',
        # 'text-decoration-color', 'text-decoration-line',
        # 'text-decoration-style', 'text-indent',
        # 'text-overflow',
        # 'transform', 'transform-box', 'transform-origin',
        # 'vertical-align',
        element = self
        while element is not None:
            attributes = element.attributes
            for key in iter(list(inherited_props.keys())):
                value = attributes.get(key)
                if value is not None and value not in ['inherit']:
                    if key == 'font':
                        # 'font' shorthand property
                        # See https://drafts.csswg.org/css-fonts-3/#font-prop
                        style[key] = value
                        _update_font_prop(value, style, inherited_props)
                    elif key == 'font-family':
                        # 'font-family' property
                        style[key] = CSSUtils.parse_font_family(value)
                        del inherited_props[key]
                    elif key == 'font-variant':
                        # 'font-variant' shorthand property
                        style[key] = value
                        _update_font_variant_prop(value, style,
                                                  inherited_props)
                    elif key == 'marker':
                        # TODO: parse the 'marker' shorthand property.
                        raise NotImplementedError
                    else:
                        if key in ['font-variant-alternates',
                                   'font-variant-east-asian',
                                   'font-variant-ligatures',
                                   'font-variant-numeric']:
                            style[key] = value.split()
                        else:
                            style[key] = value
                        inherited_props.pop(key, None)
            # 'display' property
            display = attributes.get('display')
            if display is not None and display == 'none':
                style['display'] = 'none'
            element = element.getparent()

        for key, value in iter(inherited_props.items()):
            if value is not None:
                style[key] = value

        font_family = style.get('font-family')
        if font_family is None:
            style['font-family'] = CSSUtils.parse_font_family(
                Font.default_font_family)

        return style

    def get_element_by_id(self, element_id, namespaces=None):
        """Finds the first matching sub-element, by id.

        Arguments:
            element_id (str): The id of the element.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            SVGElement: An element or None.
        """
        elements = self.xpath('//*[@id = $element_id]',
                              namespaces=namespaces,
                              element_id=element_id)
        return elements[0] if len(elements) > 0 else None

    def get_elements_by_class_name(self, class_names, namespaces=None):
        """Finds all matching sub-elements, by class names.

        Arguments:
            class_names (str): A list of class names that are separated by
                whitespace.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[SVGElement]: A list of elements.
        """
        names = class_names.split()
        pattern = [r're:test(@class, "(^| ){}($| )")'.format(x)
                   for x in names]
        # include itself
        expr = '//*[{}]'.format(' and '.join(pattern))
        if namespaces is None:
            namespaces = dict()
        namespaces['re'] = 'http://exslt.org/regular-expressions'
        return self.xpath(expr, namespaces=namespaces)

    def get_elements_by_local_name(self, local_name, namespaces=None):
        """Finds all matching sub-elements, by the local name.

        Arguments:
            local_name (str): The local name.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[SVGElement]: A list of elements.
        """
        return self.xpath('//*[local-name() = $local_name]',
                          namespaces=namespaces,
                          local_name=local_name)

    def get_elements_by_tag_name(self, tag, namespaces=None):
        # return self.findall(tag, namespaces)
        # include itself
        expr = '//*{}'.format('' if tag == '*' else '[name() = $tag_name]')
        return self.xpath(expr,
                          namespaces=namespaces,
                          tag_name=tag)

    def get_elements_by_tag_name_ns(self, namespace_uri, local_name):
        pattern = list()
        pattern.append('namespace-uri() = $namespace_uri')
        if local_name != '*':
            pattern.append('local-name() = $local_name')
        # include itself
        expr = '//*[{}]'.format(' and '.join(pattern))
        return self.xpath(expr,
                          namespace_uri=namespace_uri,
                          local_name=local_name)

    def iscontainer(self):
        """Returns True if this element is container element."""
        return self.local_name in Element.CONTAINER_ELEMENTS

    def isdisplay(self):
        style = self.get_inherited_style()
        return False if style['display'] == 'none' else True

    def isgraphics(self):
        """Returns True if this element is graphics element."""
        return self.local_name in Element.GRAPHICS_ELEMENTS

    def isrenderable(self):
        """Returns True if this element is renderable element."""
        return self.local_name in Element.RENDERABLE_ELEMENTS

    def isshape(self):
        """Returns True if this element is shape element."""
        return self.local_name in Element.SHAPE_ELEMENTS

    def istext(self):
        """Returns True if this element is text content element."""
        return self.local_name in Element.TEXT_CONTENT_ELEMENTS

    def istransformable(self):
        """Returns True if this element is transformable element."""
        return self.local_name in Element.TRANSFORMABLE_ELEMENTS

    def make_sub_element(self,
                         tag, index=None, attrib=None, nsmap=None, **_extra):
        """Creates a sub-element instance, and adds to the end of this element.
        See also SVGParser.make_element() and SVGParser.make_element_ns().

        Arguments:
            tag (str): A tag of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        element = self.makeelement(tag, attrib=attrib, nsmap=nsmap, **_extra)
        if index is None:
            self.append(element)
        else:
            self.insert(index, element)
        return element

    def make_sub_element_ns(self,
                            namespace_uri, local_name, index=None, attrib=None,
                            nsmap=None, **_extra):
        """Creates a sub-element instance with the specified namespace URI,
        and adds to the end of this element.
        See also SVGParser.make_element() and SVGParser.make_element_ns().

        Arguments:
            namespace_uri (str, None): The namespace URI to associated with the
                element.
            local_name (str): A local name of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        Examples:
            >>> from svgpy import SVGParser
            >>> parser = SVGParser()
            >>> root = parser.make_element('svg', nsmap={'html': 'http://www.w3.org/1999/xhtml'})
            >>> video = root.make_sub_element_ns('http://www.w3.org/1999/xhtml', 'video')
            >>> print(root.tostring(pretty_print=True).decode())
            <svg xmlns:html="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/2000/svg">
              <html:video/>
            </svg>
        """
        if namespace_uri is None:
            tag = local_name
        else:
            tag = '{{{0}}}{1}'.format(namespace_uri, local_name)
        element = self.make_sub_element(tag, index, attrib, nsmap, **_extra)
        return element

    def tostring(self, **kwargs):
        """Serialize an element to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        """
        return etree.tostring(self, **kwargs)
