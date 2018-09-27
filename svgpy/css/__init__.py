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
from collections.abc import MutableMapping, MutableSequence
from logging import getLogger
from urllib.error import URLError

import tinycss2

from ..utils import CaseInsensitiveMapping, dict_to_style, get_content_type, \
    load, normalize_url, style_to_dict

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
        """Constructs a CSSRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            rule_type (int): The CSS rule type.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        self._type = rule_type
        self._parent_style_sheet = parent_style_sheet
        self._parent_rule = parent_rule
        self._css_text = None
        if rule is not None:
            self._css_text = normalize_text(rule.serialize())

    @property
    def css_text(self):
        """str: A serialization of the CSS rule."""
        # TODO: implement CSSRule.cssText.
        return self._css_text

    @property
    def parent_rule(self):
        """CSSRule: The parent CSS rule."""
        return self._parent_rule

    @property
    def parent_style_sheet(self):
        """CSSStyleSheet: The parent CSS style sheet."""
        return self._parent_style_sheet

    @property
    def type(self):
        """int: The CSS rule type."""
        return self._type


class CSSGroupingRule(CSSRule):
    """Represents an at-rule that contains other rules nested inside itself.
    """

    def __init__(self, rule, rule_type, parent_style_sheet=None,
                 parent_rule=None):
        """Constructs a CSSGroupingRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            rule_type (int): The CSS rule type.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         rule_type,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._css_rules = list()

    @property
    def css_rules(self):
        """list[CSSRule]: A list of the child CSS rules."""
        return self._css_rules

    def delete_rule(self, index):
        """Removes a CSS rule from a list of the child CSS rules at index.

        Arguments:
            index (int): An index position of the child CSS rules to be
                removed.
        """
        del self._css_rules[index]

    def insert_rule(self, rule, index):
        """Inserts a CSS rule into a list of the child CSS rules at index.

        Arguments:
            rule (str): A CSS rule.
            index (int): An index position of the child CSS rules to be
                inserted.
        Returns:
            int: An index position of the child CSS rules.
        """
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
        """Constructs a CSSConditionRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            rule_type (int): The CSS rule type.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         rule_type,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)

    @property
    @abstractmethod
    def condition_text(self):
        """str: The condition of the rule."""
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
        """int: The number of media queries."""
        return self.__len__()

    @property
    def media_text(self):
        """str: A serialization of the collection of media queries."""
        return ', '.join(self._items)

    @media_text.setter
    def media_text(self, value):
        media_text = normalize_text(value)
        if len(media_text) == 0:
            self._items.clear()
            return
        self._items = [x.strip() for x in media_text.split(',')]

    def append(self, item):
        """Adds the media query to the collection of media queries.
        Same as append_medium().

        Arguments:
            item (str): The media query to be added.
        """
        self.append_medium(item)

    def append_medium(self, item):
        """Adds the media query to the collection of media queries.

        Arguments:
            item (str): The media query to be added.
        """
        self._items.append(item.strip())

    def delete_medium(self, item):
        """Removes the media query in the collection of media queries.

        Arguments:
            item (str): The media query to be removed.
        """
        self._items.remove(item.strip())

    def insert(self, index, item):
        """Inserts the media query into the collection of media queries at
        index.

        Arguments:
            index (int): An index position of the collection of media queries.
            item (str): The media query to be added.
        """
        self._items.insert(index, item.strip())

    def item(self, index):
        """Returns a serialization of the media query in the collection of
        media queries given by index.

        Arguments:
            index (int): An index position of the collection of media queries.
        Returns:
            str: The media query.
        """
        return self.__getitem__(index)


class StyleSheet(object):
    """Represents an abstract, base style sheet."""

    def __init__(self, type_=None, href=None, owner_node=None,
                 parent_style_sheet=None, title=None, media=None,
                 disabled=False):
        """Constructs a StyleSheet object.

        Arguments:
            type_ (str, optional): The type of the style sheet.
            href (str, optional): The location of the style sheet.
            owner_node (Element, optional): The owner node of the style sheet.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            title (str, optional): The title of the style sheet.
            media (str, optional): The media queries of the style sheet.
            disabled (bool, optional): The disabled flag of the style sheet.
        """
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
        """bool: The disabled flag of the style sheet."""
        return self._disabled

    @disabled.setter
    def disabled(self, value):
        self._disabled = value

    @property
    def href(self):
        """str: The location of the style sheet."""
        return self._href

    @property
    def media(self):
        """MediaList: The media queries of the style sheet."""
        return self._media

    @property
    def owner_node(self):
        """Element: The owner node of the style sheet."""
        return self._owner_node

    @property
    def parent_style_sheet(self):
        """CSSStyleSheet: The parent CSS style sheet."""
        return self._parent_style_sheet

    @property
    def title(self):
        """str: The title of the style sheet."""
        return self._title

    @property
    def type(self):
        """str: The type of the style sheet."""
        return self._type


class CSSFontFaceRule(CSSRule):
    """Represents the '@font-face' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSFontFaceRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.FONT_FACE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._style = CSSStyleDeclaration(rule, parent_rule=self)

    def __repr__(self):
        return repr((type(self).__name__, self.style))

    @property
    def style(self):
        """CSSStyleDeclaration: A CSS declaration block associated with the
        at-rule.
        """
        return self._style


class CSSFontFeatureValuesRule(CSSRule):
    """Represents the '@font-feature-values' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSFontFeatureValuesRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
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
        return repr((type(self).__name__, {
            'font_family': self.font_family,
            'annotation': self.annotation,
            'character_variant': self.character_variant,
            'ornaments': self.ornaments,
            'styleset': self.styleset,
            'stylistic': self.stylistic,
            'swash': self.swash,
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
        """str: The list of one or more font families."""
        return self._font_family

    @property
    def annotation(self):
        """CaseInsensitiveMapping: The '@annotation' feature values."""
        return self._annotation

    @property
    def character_variant(self):
        """CaseInsensitiveMapping: The '@character-variant' feature values.
        """
        return self._character_variant

    @property
    def ornaments(self):
        """CaseInsensitiveMapping: The '@ornaments' feature values."""
        return self._ornaments

    @property
    def styleset(self):
        """CaseInsensitiveMapping: The '@styleset' feature values."""
        return self._styleset

    @property
    def stylistic(self):
        """CaseInsensitiveMapping: The '@stylistic' feature values."""
        return self._stylistic

    @property
    def swash(self):
        """CaseInsensitiveMapping: The '@swash' feature values."""
        return self._swash


class CSSImportRule(CSSRule):
    """Represents the '@import' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSImportRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.IMPORT_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._href = None
        self._media = MediaList()
        self._style_sheet = None
        self._parse_prelude(rule.prelude)

    def __repr__(self):
        return repr((type(self).__name__, {
            'href': self.href,
            'media': self.media,
            'style_sheet': self.style_sheet,
        }))

    def _parse_prelude(self, prelude):
        if self.parent_style_sheet is not None:
            owner_node = self.parent_style_sheet.owner_node
            base_url = self.parent_style_sheet.href
            if base_url is None and owner_node is not None:
                doc = owner_node.owner_document
                if doc is not None:
                    base_url = doc.location.href
        else:
            owner_node = None
            base_url = None
        mediums = list()
        for token in prelude:
            if self._href is None:
                if token.type in ['string', 'url']:
                    url = normalize_url(token.value, base_url)
                    self._href = url.href
            else:
                mediums.append(token)
        if len(mediums) > 0:
            self._media.media_text = tinycss2.serialize(mediums)
        if self._href is None:
            self._style_sheet = CSSStyleSheet(owner_node=owner_node,
                                              media=self._media.media_text,
                                              owner_rule=self)
        else:
            self._style_sheet = CSSParser.parse(self._href,
                                                owner_node=owner_node,
                                                parent_rule=self)

    @property
    def href(self):
        """str: The location of the style sheet."""
        return self._href

    @property
    def media(self):
        """MediaList: The media queries of the style sheet."""
        return self._media

    @property
    def style_sheet(self):
        """CSSStyleSheet: The associated CSS style sheet."""
        return self._style_sheet


class CSSMediaRule(CSSConditionRule):
    """Represents the '@media' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSMediaRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
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
        return repr((type(self).__name__, {
            'media': self.media,
            'css_rules': self.css_rules,
        }))

    @property
    def condition_text(self):
        """str: A serialization of the collection of media queries.
        Same as media.media_text.
        """
        return self._media.media_text

    @condition_text.setter
    def condition_text(self, value):
        self._media.media_text = value

    @property
    def media(self):
        """MediaList: The media queries of the style sheet."""
        return self._media


class CSSNamespaceRule(CSSRule):
    """Represents the '@namespace' at-rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSNamespaceRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.NAMESPACE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._namespace_uri = None
        self._prefix = ''
        self._parse_prelude(rule.prelude)

    def __repr__(self):
        return repr((type(self).__name__, {
            'namespace_uri': self.namespace_uri,
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
        """str: The namespace of the '@namespace' at-rule."""
        return self._namespace_uri

    @property
    def prefix(self):
        """str: The prefix of the '@namespace' at-rule."""
        return self._prefix


class CSSStyleDeclaration(MutableMapping):
    """Represents a CSS declaration block."""

    def __init__(self, rule=None, parent_rule=None, owner_node=None):
        """Constructs a CSSStyleDeclaration object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_rule (CSSRule, optional): The parent CSS rule.
            owner_node (Element, optional): The owner node of the inline style
                properties.
        """
        self._parent_rule = parent_rule
        self._css_text = None
        self._values = dict()
        self._priorities = dict()
        self._owner_node = owner_node
        if rule is not None:
            self._css_text = normalize_text(tinycss2.serialize(rule.content))
            self._parse_content(rule.content)

    def __delitem__(self, name):
        self._remove_item(name)

    def __getitem__(self, name):
        return self._get_item(name)

    def __iter__(self):
        items = self._items()
        return iter(items)

    def __len__(self):
        items = self._items()
        return len(items)

    def __repr__(self):
        items = self._items()
        return repr((type(self).__name__, items))

    def __setitem__(self, name, value):
        """Sets a CSS declaration property with a value and an important flag
        in the declarations.

        Arguments:
            name (str): A property name of a CSS declaration.
            value (str, tuple[str, str], None): A CSS value of the
                declarations with or without an important flag.
        """
        if value is None or isinstance(value, str):
            priority = None
        elif (isinstance(value, (tuple, list))
              and len(value) == 2):
            value, priority = value
        else:
            raise TypeError('Expected str or tuple[str, str], got '
                            + repr(type(value)))
        self._set_item(name, value, priority)

    def _get_item(self, name):
        # TODO: support shorthand property.
        if self._owner_node is None:
            items = self._values
        else:
            items = self._items()
        return items[name]

    def _items(self):
        if self._owner_node is None:
            return self._values
        else:
            style = self._owner_node.get('style')
            if style is None:
                return {}
            items = style_to_dict(style)
            return items

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

    def _remove_item(self, name):
        items = self._items()
        del items[name]
        self._priorities.pop(name, None)
        if self._owner_node is not None:
            if len(items) == 0:
                del self._owner_node.attrib['style']
            else:
                style = dict_to_style(items)
                self._owner_node.set('style', style)

    def _set_item(self, name, value, priority=None):
        # TODO: support shorthand property.
        if value is not None:
            value = normalize_text(value)
            value = value.replace('("', '(').replace('")', ')')
            value = value.replace('(\'', '(').replace('\')', ')')
        if value is None or len(value) == 0:
            try:
                self._remove_item(name)
            except KeyError:
                pass
            return
        if priority is None and name not in self._priorities:
            priority = ''  # default
        elif priority is not None:
            priority = priority.lower()
            if len(priority) > 0 and priority != 'important':
                return
        items = self._items()
        items[name] = value
        if self._owner_node is not None:
            style = dict_to_style(items)
            self._owner_node.set('style', style)
        if priority is not None:
            self._priorities[name] = priority

    @property
    def css_text(self):
        """str: A serialization of the CSS rule."""
        # TODO: implement CSSStyleDeclaration.cssText.
        return self._css_text

    @property
    def length(self):
        """int: The number of CSS declarations in the declarations."""
        return self.__len__()

    @property
    def parent_rule(self):
        """CSSRule: The parent CSS rule."""
        return self._parent_rule

    def get_property_priority(self, name):
        """Returns the important flag of the first exact match of name in the
        declarations.

        Arguments:
            name (str): A property name of a CSS declaration.
        Returns:
            str: The important flag of the declarations.
        """
        items = self._items()
        if name not in items:
            raise KeyError(name)
        priority = self._priorities.setdefault(name, '')
        return priority

    def get_property_value(self, name):
        """Returns a CSS value of the first exact match of name in the
        declarations.

        Arguments:
            name (str): A property name of a CSS declaration.
        Returns:
            str: A CSS value of the declarations.
        """
        return self.__getitem__(name)

    def remove_property(self, name):
        """Removes a CSS declaration property of the first exact match of name
        in the declarations.

        Arguments:
            name (str): A property name of a CSS declaration.
        """
        self.__delitem__(name)

    def set_property(self, name, value, priority=None):
        """Sets a CSS declaration property with a value and an important flag
        in the declarations.

        Arguments:
            name (str): A property name of a CSS declaration.
            value (str, None): A CSS value of the declarations.
            priority (str, optional): An important flag of the
                declarations.
        """
        self.__setitem__(name, (value, priority))


class CSSStyleRule(CSSRule):
    """Represents a style rule."""

    def __init__(self, rule, parent_style_sheet=None, parent_rule=None):
        """Constructs a CSSStyleRule object.

        Arguments:
            rule: A parsed CSS at-rule object.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        """
        super().__init__(rule,
                         CSSRule.STYLE_RULE,
                         parent_style_sheet=parent_style_sheet,
                         parent_rule=parent_rule)
        self._selector_text = normalize_text(tinycss2.serialize(rule.prelude))
        self._style = CSSStyleDeclaration(rule, parent_rule=self)

    def __repr__(self):
        return repr((type(self).__name__, self.selector_text, self.style))

    @property
    def selector_text(self):
        """str: The associated group of selectors."""
        return self._selector_text

    @property
    def style(self):
        """CSSStyleDeclaration: A CSS declaration block associated with the
        at-rule.
        """
        return self._style


class CSSStyleSheet(StyleSheet):
    """Represents a CSS style sheet."""

    def __init__(self, owner_rule=None, **extra):
        """Constructs a CSSStyleSheet object.

        Arguments:
            owner_rule (CSSRule, optional): The owner CSS rule.
            **extra: See StyleSheet.__init__().
        """
        super().__init__(**extra)
        self._owner_rule = owner_rule
        self._css_rules = list()

    def __repr__(self):
        return repr((type(self).__name__, {
            'href': self.href,
            'media': self.media,
            'title': self.title,
            'css_rules': self.css_rules,
        }))

    @property
    def owner_rule(self):
        """CSSRule: The owner CSS rule."""
        return self._owner_rule

    @property
    def css_rules(self):
        """list[CSSRule]: A list of the child CSS rules."""
        return self._css_rules

    def delete_rule(self, index):
        """Removes a CSS rule from a list of the child CSS rules at index.

        Arguments:
            index (int): An index position of the child CSS rules to be
                removed.
        """
        del self._css_rules[index]

    def insert_rule(self, rule, index=0):
        """Inserts a CSS rule into a list of the child CSS rules at index.

        Arguments:
            rule (str): A CSS rule.
            index (int, optional): An index position of the child CSS rules to
            be inserted.
        Returns:
            int: An index position of the child CSS rules.
        """
        css_rules = CSSParser.fromstring(
            rule,
            parent_style_sheet=self,
            parent_rule=self._owner_rule)
        self._css_rules[index:index] = css_rules
        return index


class CSSParser(object):
    @classmethod
    def fromstring(cls, stylesheet, parent_style_sheet=None,
                   parent_rule=None):
        """Parses the CSS style sheet or fragment from a string.

        Arguments:
            stylesheet (str): The CSS style sheet to be parsed.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
        Returns:
            list[CSSRule]: A list of CSS rules.
       """
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
            logger = getLogger('{}.{}'.format(__name__, cls.__name__))
            logger.info('failed to parse: ' + repr(exp))
            return []

    @classmethod
    def parse(cls, url, owner_node=None, parent_style_sheet=None,
              parent_rule=None, encoding=None):
        """Parses the CSS style sheet.

        Arguments:
            url (str): The location of the style sheet.
            owner_node (Element, optional): The owner node of the style sheet.
            parent_style_sheet (CSSStyleSheet, optional): The parent CSS style
                sheet.
            parent_rule (CSSRule, optional): The parent CSS rule.
            encoding (str, optional): An advisory character encoding for the
                referenced style sheet.
        Returns:
            CSSStyleSheet: A new CSSStyleSheet object.
        """
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
        css_style_sheet = CSSStyleSheet(owner_rule=parent_rule, **extra)
        logger = getLogger('{}.{}'.format(__name__, cls.__name__))
        try:
            logger.debug('urlopen \'{}\''.format(url))
            data, headers = load(url)
            if encoding is None:
                content_type = get_content_type(headers)
                if content_type is None:
                    encoding = 'utf-8'
                else:
                    encoding = content_type.get('charset', 'utf-8')
            rules, encoding = tinycss2.parse_stylesheet_bytes(
                css_bytes=data,
                protocol_encoding=encoding,
                skip_comments=True,
                skip_whitespace=True)
            css_rules = CSSParser.parse_rules(
                rules,
                parent_style_sheet=css_style_sheet,
                parent_rule=parent_rule)
            css_style_sheet.css_rules.extend(css_rules)
        except URLError as exp:
            logger.info(
                'failed to parse: \'{}\': {}'.format(url, repr(exp)))
        return css_style_sheet

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
