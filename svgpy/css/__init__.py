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


import logging
import re
from abc import ABC, abstractmethod
from urllib.error import URLError
from urllib.request import urlopen

import tinycss2
from collections.abc import MutableMapping, MutableSequence

from ..utils import CaseInsensitiveMapping, normalize_url

_RE_COLLAPSIBLE_WHITESPACE = re.compile(r'(\x20){2,}')


def normalize_text(text):
    out_text = text.strip().replace(
        '\r\n', ' ').replace('\r', ' ').replace('\n', ' ')
    out_text = _RE_COLLAPSIBLE_WHITESPACE.sub(' ', out_text)
    return out_text


class CSSRule(object):
    """Represents an abstract, base CSS style rule."""

    UNKNOWN_RULE = 0
    STYLE_RULE = 1
    CHARSET_RULE = 2  # historical
    IMPORT_RULE = 3
    MEDIA_RULE = 4
    FONT_FACE_RULE = 5
    PAGE_RULE = 6
    MARGIN_RULE = 9
    NAMESPACE_RULE = 10
    SUPPORTS_RULE = 12
    FONT_FEATURE_VALUES_RULE = 14

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        self._type = rule_type
        self._parent_style_sheet = parent_style_sheet
        self._parent_rule = parent_rule
        self._css_text = None
        if rule is not None:
            self._css_text = normalize_text(rule.serialize())

    @property
    def css_text(self):
        return self._css_text

    @property
    def parent_rule(self):
        return self._parent_rule

    @property
    def parent_style_sheet(self):
        return self._parent_style_sheet

    @property
    def type(self):
        return self._type


class CSSGroupingRule(CSSRule):
    """Represents an at-rule that contains other rules nested inside itself.
    """

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        super().__init__(rule,
                         rule_type,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._css_rules = list()

    @property
    def css_rules(self):
        return self._css_rules

    def delete_rule(self, index):
        del self._css_rules[index]

    def insert_rule(self, rule, index):
        # str -> list[CSSRule]
        css_rules = CSSParser.fromstring(
            rule,
            parent_style_sheet=self.parent_style_sheet,
            parent_rule=self)
        self._css_rules[index:index] = css_rules
        return index


class CSSConditionRule(CSSGroupingRule, ABC):
    """Represents all the 'conditional' at-rules, which consist of a condition
    and a statement block.
    """

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        super().__init__(rule,
                         rule_type,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)

    @property
    @abstractmethod
    def condition_text(self):
        raise NotImplementedError


class MediaList(MutableSequence):
    """Represents a collection of media queries."""

    def __init__(self):
        self._items = list()

    def __delitem__(self, index):
        del self._items[index]

    def __getitem__(self, index):
        return self._items[index]

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return repr(self._items)

    def __setitem__(self, index, item):
        self._items[index] = item.strip()

    @property
    def length(self):
        return self.__len__()

    @property
    def media_text(self):
        return ', '.join(self._items)

    @media_text.setter
    def media_text(self, value):
        media_text = normalize_text(value)
        if len(media_text) == 0:
            self._items.clear()
            return
        self._items = [x.strip() for x in media_text.split(',')]

    def append(self, item):
        self.append_medium(item)

    def append_medium(self, item):
        self._items.append(item.strip())

    def delete_medium(self, item):
        self._items.remove(item.strip())

    def insert(self, index, item):
        self._items.insert(index, item.strip())

    def item(self, index):
        return self.__getitem__(index)


class StyleSheet(object):
    """Represents an abstract, base style sheet."""

    def __init__(self, type_=None, href=None, owner_node=None,
                 parent_style_sheet=None, title=None, media=None,
                 disabled=False):
        self._type = type_ if type_ is not None else 'text/css'
        self._media = MediaList()
        if media is not None:
            self._media.media_text = media
        self._href = href
        self._owner_node = owner_node
        self._parent_style_sheet = parent_style_sheet
        self._title = title
        self._disabled = disabled

    @property
    def disabled(self):
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value

    @property
    def href(self):
        return self._href

    @property
    def media(self):
        return self._media

    @property
    def owner_node(self):
        return self._owner_node

    @property
    def parent_style_sheet(self):
        return self._parent_style_sheet

    @property
    def title(self):
        return self._title

    @property
    def type(self):
        return self._type


class CSSFontFaceRule(CSSRule):
    """Represents the '@font-face' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        super().__init__(rule,
                         CSSRule.FONT_FACE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._style = CSSStyleDeclaration(rule, parent_rule=self)

    def __repr__(self):
        return repr(('CSSFontFaceRule', self.style))

    @property
    def style(self):
        return self._style


class CSSFontFeatureValuesRule(CSSRule):
    """Represents the '@font-feature-values' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        super().__init__(rule,
                         CSSRule.FONT_FEATURE_VALUES_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._font_family = normalize_text(tinycss2.serialize(rule.prelude))
        self._annotation = CaseInsensitiveMapping()
        self._character_variant = CaseInsensitiveMapping()
        self._ornaments = CaseInsensitiveMapping()
        self._styleset = CaseInsensitiveMapping()
        self._stylistic = CaseInsensitiveMapping()
        self._swash = CaseInsensitiveMapping()
        self._parse_content(rule.content)

    def __repr__(self):
        return repr(('CSSFontFeatureValuesRule', {
            'font-family': self.font_family,
            '@annotation': self.annotation,
            '@character-variant': self.character_variant,
            '@ornaments': self.ornaments,
            '@styleset': self.styleset,
            '@stylistic': self.stylistic,
            '@swash': self.swash,
        }))

    def _parse_content(self, content):
        nodes = tinycss2.parse_rule_list(content,
                                         skip_comments=True,
                                         skip_whitespace=True)
        for node in nodes:
            if node.type == 'at-rule':
                # tinycss2.parse_one_component_value() returns ParseError
                feature_type = node.lower_at_keyword
                name = None
                feature_values = None
                for token in node.content:
                    if token.type == 'ident':
                        name = token.value
                    elif token.type == 'literal' and token.value == ':':
                        if name is not None:
                            feature_values = list()
                    elif token.type == 'number' and token.is_integer:
                        if feature_values is not None and token.int_value >= 0:
                            feature_values.append(token.int_value)
                    elif token.type == 'literal' and token.value == ';':
                        if (name is not None
                                and feature_values is not None
                                and len(feature_values) > 0):
                            if feature_type == 'annotation':
                                self._annotation[name] = feature_values
                            elif feature_type == 'character-variant':
                                self._character_variant[name] = feature_values
                            elif feature_type == 'ornaments':
                                self._ornaments[name] = feature_values
                            elif feature_type == 'styleset':
                                self._styleset[name] = feature_values
                            elif feature_type == 'stylistic':
                                self._stylistic[name] = feature_values
                            elif feature_type == 'swash':
                                self._swash[name] = feature_values
                        name = None
                        feature_values = None

    @property
    def font_family(self):
        return self._font_family

    @property
    def annotation(self):
        return self._annotation

    @property
    def character_variant(self):
        return self._character_variant

    @property
    def ornaments(self):
        return self._ornaments

    @property
    def styleset(self):
        return self._styleset

    @property
    def stylistic(self):
        return self._stylistic

    @property
    def swash(self):
        return self._swash


class CSSImportRule(CSSRule):
    """Represents the '@import' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        super().__init__(rule,
                         CSSRule.IMPORT_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._href = None
        self._media = MediaList()
        self._style_sheet = None
        self._parse_prelude(rule.prelude)

    def __repr__(self):
        return repr(('CSSImportRule', {
            'href': self.href,
            'media': self.media,
            'styleSheet': self._style_sheet,
        }))

    def _parse_prelude(self, prelude):
        mediums = list()
        for token in prelude:
            if self._href is None:
                if token.type == 'url':
                    self._href = normalize_url('url({})'.format(token.value))
                elif token.type == 'string':
                    self._href = normalize_url(token.value)
            else:
                mediums.append(token)
        if len(mediums) > 0:
            self._media.media_text = tinycss2.serialize(mediums)
        if self._href is None:
            self._style_sheet = CSSStyleSheet(owner_rule=self)
            return
        self._style_sheet = CSSParser.parse(self._href, parent_rule=self)

    @property
    def href(self):
        return self._href

    @property
    def media(self):
        return self._media

    @property
    def style_sheet(self):
        return self._style_sheet


class CSSMediaRule(CSSConditionRule):
    """Represents the '@media' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        super().__init__(rule,
                         CSSRule.MEDIA_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._media = MediaList()
        self._media.media_text = tinycss2.serialize(rule.prelude)
        rules = tinycss2.parse_rule_list(rule.content,
                                         skip_comments=True,
                                         skip_whitespace=True)
        css_rules = CSSParser.parse_rules(
            rules,
            parent_style_sheet=parent_style_sheet,
            parent_rule=self)
        self.css_rules.extend(css_rules)

    def __repr__(self):
        return repr(('CSSMediaRule', {
            'media': self.media,
            'cssRules': self.css_rules,
        }))

    @property
    def condition_text(self):
        return self._media.media_text

    @condition_text.setter
    def condition_text(self, value):
        self._media.media_text = value

    @property
    def media(self):
        return self._media


class CSSNamespaceRule(CSSRule):
    """Represents the '@namespace' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        super().__init__(rule,
                         CSSRule.NAMESPACE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._namespace_uri = None
        self._prefix = ''
        self._parse_prelude(rule.prelude)

    def __repr__(self):
        return repr(('CSSNamespaceRule', {
            'namespaceURI': self.namespace_uri,
            'prefix': self.prefix,
        }))

    def _parse_prelude(self, prelude):
        for token in prelude:
            if token.type == 'url':
                self._namespace_uri = token.value
            elif token.type == 'ident':
                self._prefix = token.value

    @property
    def namespace_uri(self):
        return self._namespace_uri

    @property
    def prefix(self):
        return self._prefix


class CSSStyleDeclaration(MutableMapping):
    """Represents a CSS declaration block."""

    def __init__(self, rule=None, parent_rule=None):
        self._parent_rule = parent_rule
        self._css_text = None
        self._properties = CaseInsensitiveMapping()
        self._owner_attributes = None
        if rule is not None:
            self._css_text = normalize_text(tinycss2.serialize(rule.content))
            self._parse_content(rule.content)
        else:
            owner_node = self.get_owner_node()
            if owner_node is not None:
                self._owner_attributes = owner_node.attributes

    def __delitem__(self, name):
        if self._owner_attributes is not None:
            del self._owner_attributes[name]
        else:
            del self._properties[name]

    def __getitem__(self, name):
        # TODO: support shorthand property.
        if self._owner_attributes is not None:
            style = self._owner_attributes.get_style({})
            return style[name], ''
        return self._properties[name]

    def __iter__(self):
        if self._owner_attributes is not None:
            style = self._owner_attributes.get_style({})
            return iter(style)
        return iter(self._properties)

    def __len__(self):
        if self._owner_attributes is not None:
            style = self._owner_attributes.get_style({})
            return len(style)
        return len(self._properties)

    def __repr__(self):
        if self._owner_attributes is not None:
            style = self._owner_attributes.get_style({})
        else:
            style = self._properties
        return repr(('CSSStyleDeclaration', style))

    def __setitem__(self, name, value_and_priority):
        # TODO: support shorthand property.
        if isinstance(value_and_priority, str):
            value = value_and_priority
            priority = ''
        elif (isinstance(value_and_priority, (tuple, list))
              and len(value_and_priority) == 2):
            value, priority = value_and_priority
            priority = priority.lower()
        else:
            raise ValueError(
                'Expected a tuple of two numbers <str> and <str>, got '
                + repr(value_and_priority))
        value = normalize_text(value)
        value = value.replace('("', '(').replace('")', ')')
        value = value.replace('(\'', '(').replace('\')', ')')
        if len(value) == 0:
            self.__delitem__(name)
            return
        if self._owner_attributes is not None:
            self._owner_attributes.update_style({name: value})
        else:
            self._properties[name] = value, priority

    def _parse_content(self, content):
        nodes = tinycss2.parse_declaration_list(content,
                                                skip_comments=True,
                                                skip_whitespace=True)
        for node in nodes:
            if node.type == 'declaration':
                name = node.lower_name
                value = tinycss2.serialize(node.value)
                self.__setitem__(
                    name,
                    (value, 'important' if node.important else ''))

    @property
    def css_text(self):
        return self._css_text

    @property
    def length(self):
        return self.__len__()

    @property
    def parent_rule(self):
        return self._parent_rule

    def get_owner_node(self):
        if self._parent_rule is None:
            return None
        sheet = self._parent_rule.parent_style_sheet
        if sheet is None:
            return None
        return sheet.owner_node

    def get_property_priority(self, name):
        _, priority = self.__getitem__(name)
        return priority

    def get_property_value(self, name):
        value, _ = self.__getitem__(name)
        return value

    def remove_property(self, name):
        self.__delitem__(name)

    def set_property(self, name, value, priority=''):
        self.__setitem__(name, (value, priority))


class CSSStyleRule(CSSRule):
    """Represents a style rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        super().__init__(rule,
                         CSSRule.STYLE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._selector_text = normalize_text(tinycss2.serialize(rule.prelude))
        self._style = CSSStyleDeclaration(rule, parent_rule=self)

    def __repr__(self):
        return repr(('CSSStyleRule', self.selector_text, self.style))

    @property
    def selector_text(self):
        return self._selector_text

    @property
    def style(self):
        return self._style


class CSSStyleSheet(StyleSheet):
    """Represents a CSS style sheet."""

    def __init__(self, owner_rule=None, **extra):
        super().__init__(**extra)
        self._owner_rule = owner_rule
        self._css_rules = list()

    def __repr__(self):
        return repr(('CSSStyleSheet', {
            'href': self.href,
            'media': self.media,
            'title': self.title,
            'cssRules': self.css_rules,
        }))

    @property
    def owner_rule(self):
        return self._owner_rule

    @property
    def css_rules(self):
        return self._css_rules

    def delete_rule(self, index):
        del self._css_rules[index]

    def insert_rule(self, rule, index=0):
        # str -> list[CSSRule]
        css_rules = CSSParser.fromstring(
            rule,
            parent_style_sheet=self,
            parent_rule=self._owner_rule)
        self._css_rules[index:index] = css_rules
        return index


class CSSParser(object):
    @staticmethod
    def fromstring(stylesheet, parent_style_sheet=None, parent_rule=None):
        try:
            rules = tinycss2.parse_stylesheet(
                stylesheet,
                skip_comments=True,
                skip_whitespace=True)
            css_rules = CSSParser.parse_rules(
                rules,
                parent_style_sheet=parent_style_sheet,
                parent_rule=parent_rule)
            return css_rules
        except URLError as exp:
            logging.getLogger(__name__).info(
                'CSSParser#fromstring() error: ' + str(exp),
                stack_info=True)
            return []

    @staticmethod
    def parse(url, owner_node=None, parent_style_sheet=None,
              parent_rule=None, encoding=None):
        extra = dict({
            'type_': None,
            'href': None,
            'owner_node': owner_node,
            'parent_style_sheet': parent_style_sheet,
            'title': None,
            'media': None,
        })
        if owner_node is not None:
            extra.update({
                'type_': owner_node.get('type'),
                'href': owner_node.get('href'),
                'title': owner_node.get('title'),
                'media': owner_node.get('media'),
            })
        css_stylesheet = CSSStyleSheet(owner_rule=parent_rule, **extra)
        try:
            response = urlopen(url)
            css_bytes = response.read()
            if encoding is None:
                encoding = response.info().get_charset()
            rules, encoding = tinycss2.parse_stylesheet_bytes(
                css_bytes=css_bytes,
                protocol_encoding=encoding,
                skip_comments=True,
                skip_whitespace=True)
            css_rules = CSSParser.parse_rules(
                rules,
                parent_style_sheet=parent_style_sheet,
                parent_rule=parent_rule)
            css_stylesheet.css_rules.extend(css_rules)
        except URLError as exp:
            logging.getLogger(__name__).info(
                'CSSParser#parse() error: ' + str(exp),
                stack_info=True)
        return css_stylesheet

    @staticmethod
    def parse_rules(rules, parent_style_sheet=None, parent_rule=None):
        css_rules = list()
        for rule in rules:
            if rule.type == 'at-rule':
                if rule.lower_at_keyword == 'font-face':
                    # @font-face at-rule
                    css_rule = CSSFontFaceRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'font-feature-values':
                    # @font-feature-values at-rule
                    css_rule = CSSFontFeatureValuesRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'import':
                    # @import at-rule
                    css_rule = CSSImportRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'media':
                    # @media at-rule
                    css_rule = CSSMediaRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
                elif rule.lower_at_keyword == 'namespace':
                    # @namespace at-rule
                    css_rule = CSSNamespaceRule(
                        rule,
                        parent_style_sheet=parent_style_sheet,
                        parent_rule=parent_rule)
                    css_rules.append(css_rule)
            elif rule.type == 'qualified-rule':
                css_rule = CSSStyleRule(
                    rule,
                    parent_style_sheet=parent_style_sheet,
                    parent_rule=parent_rule)
                css_rules.append(css_rule)
        return css_rules
