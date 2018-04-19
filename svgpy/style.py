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


from urllib.error import URLError

import cssutils
from cssutils.css import CSSRule
from lxml import etree, cssselect

from .core import window
# from .harfbuzz import HBLanguage
from .utils import get_content_type, load

_SVG_UA_CSS_STYLESHEET = '''
@namespace url(http://www.w3.org/2000/svg);
@namespace xml url(http://www.w3.org/XML/1998/namespace);

svg:not(:root), hatch, image, marker, pattern, symbol { overflow: hidden; }

*:not(svg),
*:not(foreignObject) > svg {
  transform-origin: 0 0;
}

*[xml|space=preserve] {
  text-space-collapse: preserve-spaces;
}

defs, 
clipPath, mask, marker, 
desc, title, metadata, 
pattern, hatch,
linearGradient, radialGradient, meshGradient, 
script, style,
symbol {
  display: none !important;
}
:host(use) > symbol {
  display: inline !important;
}
'''

# _OPENTYPE_UA_CSS_STYLESHEET = '''
# @namespace svg url(http://www.w3.org/2000/svg);
#
# svg|text, svg|foreignObject {
#   display: none !important;
# }
# '''

cssutils.log.enabled = False


def get_css_rules(element):
    stylesheet_list = list()
    stylesheet_list.append(_SVG_UA_CSS_STYLESHEET)
    # stylesheet_list.append(_OPENTYPE_UA_CSS_STYLESHEET)
    stylesheet_list.extend(get_stylesheets_from_xml_stylesheet(element))
    stylesheet_list.extend(get_stylesheets_from_link_elements(element))
    stylesheet_list.extend(get_stylesheets_from_style_elements(element))

    def _parse_css_rules(_rules):
        _css_rules = list()
        for _rule in _rules:
            if _rule.type == CSSRule.IMPORT_RULE:
                _href = _rule.href
                if _href is None or _href[0] == '#':
                    continue
                _media = _rule.media.mediaText
                if _media != 'all':
                    _mql = window.match_media(_media)
                    if not _mql.matches:
                        continue
                _stylesheet = load_css_stylesheet(_href)
                if _stylesheet is not None:
                    _sheet = parser.parseString(_stylesheet)
                    _css_rules.extend(_parse_css_rules(_sheet.cssRules))
            elif _rule.type == CSSRule.MEDIA_RULE:
                _media = _rule.media.mediaText
                if _media != 'all':
                    _mql = window.match_media(_media)
                    if not _mql.matches:
                        continue
                _css_rules.extend(_parse_css_rules(_rule.cssRules))
            else:
                _css_rules.append(_rule)
        return _css_rules

    window.document = element
    parser = cssutils.CSSParser(parseComments=False)
    css_rules = list()
    for text in stylesheet_list:
        sheet = parser.parseString(text)
        css_rules.extend(_parse_css_rules(sheet.cssRules))
    return css_rules


def get_css_style(element, css_rules):
    window.document = element
    style = dict()
    style_important = dict()
    namespaces = None
    for rule in css_rules:
        if rule.type == CSSRule.STYLE_RULE:
            try:
                selector = cssselect.CSSSelector(rule.selectorText,
                                                 namespaces=namespaces)
                matched = selector(element)
                if len(matched) > 0 and element in matched:
                    rule_style = rule.style
                    for key in rule_style.keys():
                        value = rule_style.getPropertyValue(key)
                        style[key] = value
                        priority = rule_style.getPropertyPriority(key)
                        if priority == 'important':
                            style_important[key] = value
            except cssselect.ExpressionError:
                pass
        elif rule.type == CSSRule.FONT_FACE_RULE:
            # TODO: support CSS font face rule.
            pass
        elif rule.type == CSSRule.NAMESPACE_RULE:
            if len(rule.prefix) > 0:
                if namespaces is None:
                    namespaces = dict()
                namespaces[rule.prefix] = rule.namespaceURI
        else:
            import logging
            logging.getLogger(__name__).warning(
                'Not implemented CSS rule: ' + str(rule.type))
    return style, style_important


def get_stylesheets_from_link_elements(element):
    window.document = element
    stylesheet_list = list()
    root = element.getroottree().getroot()
    elements = root.get_elements_by_local_name('link')
    # TODO: support alternative stylesheet.
    alternates = list()
    for target in elements:
        if ('alternate' in target.rel_list
                and 'stylesheet' in target.rel_list
                and target.href is not None
                and target.hreflang is not None):
            alternates.append({
                'hreflang': target.hreflang,
                'title': target.title,
                'element': target,
            })
    # user_language = HBLanguage.get_default().tostring()
    for alternate in alternates:
        elements.remove(alternate['element'])
    for target in elements:
        href = target.href
        if ('stylesheet' not in target.rel_list
                or (target.type is not None and target.type != 'text/css')
                or href is None
                or href[0] == '#'):
            continue
        media = target.media
        if media != 'all':
            mql = window.match_media(media)
            if not mql.matches:
                continue
        try:
            stylesheet = load_css_stylesheet(href)
            if stylesheet is not None:
                stylesheet_list.append(stylesheet)
        except URLError:
            pass
    return stylesheet_list


def get_stylesheets_from_style_elements(element):
    window.document = element
    stylesheet_list = list()
    root = element.getroottree().getroot()
    elements = root.get_elements_by_local_name('style')
    for target in elements:
        if target.type != 'text/css' or target.text is None:
            continue
        media = target.media
        if media != 'all':
            mql = window.match_media(media)
            if not mql.matches:
                continue
        stylesheet_list.append(target.text)
    return stylesheet_list


def get_stylesheets_from_xml_stylesheet(element):
    window.document = element
    stylesheet_list = list()
    root = element.getroottree().getroot()
    elements = root.itersiblings(preceding=True)
    for target in elements:
        tag = etree.tostring(target).decode()
        href = target.get('href')
        if (tag.split()[0] != '<?xml-stylesheet'
                or target.get('type', 'text/css') != 'text/css'
                or href is None
                or href[0] == '#'):
            continue
        media = target.get('media', 'all')
        if media != 'all':
            mql = window.match_media(media)
            if not mql.matches:
                continue
        try:
            encoding = target.get('charset', 'utf-8')
            stylesheet = load_css_stylesheet(href, encoding)
            if stylesheet is not None:
                stylesheet_list.append(stylesheet)
        except URLError:
            pass
    return stylesheet_list


def load_css_stylesheet(path_or_url, encoding=None):
    if encoding is None:
        encoding = 'utf-8'
    data, headers = load(path_or_url)
    content_type = get_content_type(headers)
    if content_type is not None:
        if content_type.get(None) != 'text/css':
            return None
        encoding = content_type.get('charset', encoding)
    stylesheet = data.decode(encoding)
    return stylesheet
