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


from lxml import etree, cssselect

from .core import window
from .css import CSSParser, CSSRule, normalize_url


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


def flatten_css_rules(element, css_rules):
    window.document = element
    flattened_css_rules = list()
    for css_rule in css_rules:
        if css_rule.type == CSSRule.IMPORT_RULE:
            # '@import' at-rule
            media = css_rule.media.media_text
            if media not in ['', 'all']:
                mql = window.match_media(media)
                if not mql.matches:
                    continue
            flattened_css_rules.extend(
                flatten_css_rules(element, css_rule.style_sheet.css_rules))
        elif css_rule.type == CSSRule.MEDIA_RULE:
            # '@media' at-rule
            media = css_rule.media.media_text
            if media not in ['', 'all']:
                mql = window.match_media(media)
                if not mql.matches:
                    continue
            flattened_css_rules.extend(
                flatten_css_rules(element, css_rule.css_rules))
        else:
            flattened_css_rules.append(css_rule)
    return flattened_css_rules


def get_css_rules(element):
    css_rules = CSSParser.fromstring(_SVG_UA_CSS_STYLESHEET)
    css_rules.extend(get_css_rules_from_xml_stylesheet(element))
    css_rules.extend(get_css_rules_from_svg_document(element))
    flattened = flatten_css_rules(element, css_rules)
    return flattened


def get_css_rules_from_svg_document(element):
    css_rules = list()
    window.document = element
    root = element.getroottree().getroot()
    for target in root.iter(tag=('{*}style', '{*}link')):
        local_name = target.local_name
        if local_name == 'style':
            if target.type != 'text/css' or target.text is None:
                continue
            media = target.media
            if media != 'all':
                mql = window.match_media(media)
                if not mql.matches:
                    continue
            rules = CSSParser.fromstring(target.text)
            css_rules.extend(rules)
        elif local_name == 'link':
            rel_list = target.rel_list
            if 'stylesheet' not in rel_list or 'alternate' in rel_list:
                continue  # TODO: support alternative style sheet.
            href = target.href
            if href is None or href[0] == '#':
                continue
            media = target.media
            if media != 'all':
                mql = window.match_media(media)
                if not mql.matches:
                    continue
            css_style_sheet = CSSParser.parse(normalize_url(href),
                                              owner_node=target)
            css_rules.extend(css_style_sheet.css_rules)
    return css_rules


def get_css_rules_from_xml_stylesheet(element):
    css_rules = list()
    window.document = element
    root = element.getroottree().getroot()
    # 'lxml.etree.SiblingsIterator' object is not reversible
    siblings = root.itersiblings(preceding=True)
    elements = [it for it in siblings]
    elements.reverse()
    for target in elements:
        tag = etree.tostring(target).decode()
        if tag.split()[0] != '<?xml-stylesheet':
            continue
        href = target.get('href')
        if (href is None
                or href[0] == '#'
                or target.get('alternate', '') == 'yes'):
            continue  # TODO: support alternative style sheet.
        media = target.get('media', 'all')
        if media != 'all':
            mql = window.match_media(media)
            if not mql.matches:
                continue
        encoding = target.get('charset')
        css_style_sheet = CSSParser.parse(normalize_url(href),
                                          owner_node=target,
                                          encoding=encoding)
        css_rules.extend(css_style_sheet.css_rules)
    return css_rules


def get_css_style(element, css_rules):
    window.document = element
    style = dict()
    style_important = dict()
    namespaces = None
    for css_rule in css_rules:
        if css_rule.type == CSSRule.STYLE_RULE:
            try:
                selector = cssselect.CSSSelector(css_rule.selector_text,
                                                 namespaces=namespaces)
                matched = selector(element)
                if len(matched) > 0 and element in matched:
                    for key, (value, priority) in css_rule.style.items():
                        style[key] = value
                        if priority == 'important':
                            style_important[key] = value
            except cssselect.ExpressionError:
                pass
        elif css_rule.type == CSSRule.FONT_FACE_RULE:
            # TODO: support CSS @font-face at-rule.
            pass
        elif css_rule.type == CSSRule.FONT_FEATURE_VALUES_RULE:
            # TODO: support CSS @font-feature-values at-rule.
            pass
        elif css_rule.type == CSSRule.NAMESPACE_RULE:
            if len(css_rule.prefix) > 0:
                if namespaces is None:
                    namespaces = dict()
                namespaces[css_rule.prefix] = css_rule.namespace_uri
    return style, style_important
