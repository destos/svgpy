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

from lxml import cssselect, etree

from .core import CSSUtils, Font, SVGLength
from .css import CSSStyleDeclaration
from .style import get_css_rules, get_css_style, \
    get_css_style_sheet_from_element
from .utils import get_elements_by_class_name, get_elements_by_tag_name, \
    get_elements_by_tag_name_ns


_ASCII_WHITESPACE = '\t\n\f\r\x20'

_RE_ATTR_QUALIFIED_NAME = re.compile(
    r'{(?P<namespace>[^}]+)}(?P<local_name>.+)')


def dict_to_style(d):
    if d is None:
        return ''
    items = ['{}: {};'.format(key, value) for key, value in iter(d.items())]
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
        """Constructs an Attrib object.

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
            namespace (str, None): The namespace URI.
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
            namespace (str, None): The namespace URI.
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
            namespace (str, None): The namespace URI.
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
        if len(value) == 0:
            self.__delitem__(name)
            return
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
            namespace (str, None): The namespace URI.
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
            namespace (str, None): The namespace URI.
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


class DOMTokenList(MutableSequence):
    # FIXME: implement DOMTokenList.supports().
    """Represents the [DOM] DOMTokenList."""

    def __init__(self, owner_element, local_name):
        """Constructs a DOMTokenList object.

        Arguments:
            owner_element (Element): The element that is associated with the
                attribute.
            local_name (str): The local name of the attribute.
        """
        self._owner_element = owner_element
        self._local_name = local_name
        value = owner_element.get(local_name, '')
        tokens = value.split()
        self._tokens = list(tokens)

    def __delitem__(self, index):
        del self._tokens[index]
        self._update_attribute()

    def __getitem__(self, index):
        return self._tokens[index]

    def __len__(self):
        return len(self._tokens)

    def __repr__(self):
        return repr(self._tokens)

    def __setitem__(self, index, value):
        if isinstance(value, str):
            if value in self._tokens:
                return
        elif isinstance(value, list):
            for token in list(value):
                if token in self._tokens:
                    value.remove(token)
            if len(value) == 0:
                return
        else:
            raise TypeError('Expected str or list[str], got {}'.format(
                type(value)))
        self._tokens[index] = value
        self._update_attribute()

    @property
    def length(self):
        """int: The token set's size."""
        return self.__len__()

    @property
    def value(self):
        """str: The attribute's value."""
        return ' '.join(self._tokens)

    def _update_attribute(self):
        value = self.value
        if (len(value) == 0
                and self._local_name in self._owner_element.attrib):
            del self._owner_element.attrib[self._local_name]
        else:
            self._owner_element.set(self._local_name, value)

    def _validate_token(self, token):
        _ = self
        if len(token) == 0:
            raise ValueError('Unexpected empty string')
        elif any(ch in token for ch in _ASCII_WHITESPACE):
            raise ValueError('Invalid token: ' + repr(token))
        return True

    def _validate_tokens(self, tokens):
        for token in tokens:
            self._validate_token(token)
        return True

    def add(self, *tokens):
        """Adds tokens to the end of this token set.

        Arguments:
            *tokens (str, ...): The tokens to be added.
        """
        self._validate_tokens(tokens)
        self.extend(tokens)

    def contains(self, token):
        """Returns True if this token set contains token `token`, and False
        otherwise.

        Arguments:
            token (str): The token.
        Returns:
            bool: Returns True if this token set contains token, and False
                otherwise.
        """
        return token in self._tokens

    def insert(self, index, token):
        """Inserts `token` at the given position `index` in this token set.

        Arguments:
            index (int): An index position of the token set.
            token (str): The token to be inserted.
        """
        self._validate_token(token)
        self[index:index] = [token]

    def item(self, index):
        """Returns the token at index position `index` in the token set.

        Arguments:
            index (int): An index position of the token set.
        Returns:
            str: The token.
        """
        return self.__getitem__(index)

    def remove(self, *tokens):
        """Removes tokens in this token set.

        Arguments:
            *tokens (str, ...): The tokens to be removed.
        """
        self._validate_tokens(tokens)
        for token in tokens:
            if token not in self._tokens:
                continue
            super().remove(token)

    def replace(self, token, new_token):
        """Replaces `token` with `new_token`.

        Arguments:
            token (str): The token to be replaced.
            new_token (str): The new token.
        Returns:
            bool: Returns True if `token` was replaced with `new_token`, and
                False otherwise.
        """
        self._validate_tokens([token, new_token])
        if token not in self._tokens or new_token in self._tokens:
            return False
        index = self._tokens.index(token)
        self.__setitem__(index, new_token)
        return True

    def toggle(self, token, force=None):
        """If `force` is not given, "toggles" `token`, removing it if it’s
        present and adding it if it’s not present. If `force` is True, adds
        token (same as add()). If `force` is False, removes token (same as
        remove()).

        Arguments:
            token (str): The token to be added or removed.
            force (bool, optional): The toggle flag.
        Returns:
            bool: Returns True if `token` is now present, and False otherwise.
        """
        if token in self._tokens:
            if force in [None, False]:
                self.remove(token)
                return False
            return True
        elif force in [None, True]:
            self.add(token)
            return True
        return False


class ParentNode(ABC):
    """Represents the [DOM] ParentNode."""

    @property
    def child_element_count(self):
        """int: The number of the child elements."""
        return len(self.children)

    @property
    @abstractmethod
    def children(self):
        """list[Element]: A list of the child elements, in document order."""
        raise NotImplementedError

    @property
    def first_element_child(self):
        """Element: The first child element or None."""
        children = self.children
        return children[0] if len(children) > 0 else None

    @property
    def last_element_child(self):
        """Element: The last child element or None."""
        children = self.children
        return children[-1] if len(children) > 0 else None

    @abstractmethod
    def append(self, node):
        """Inserts a sub-node after the last child node.

        Arguments:
            node (Node): A node to be added.
        """
        raise NotImplementedError

    @abstractmethod
    def prepend(self, node):
        """Inserts a sub-node before the first child node.

        Arguments:
            node (Node): A node to be added.
        """
        raise NotImplementedError

    def query_selector(self, selectors):
        elements = self.query_selector_all(selectors)
        return elements[0] if len(elements) > 0 else None

    @abstractmethod
    def query_selector_all(self, selectors):
        raise NotImplementedError


class NonDocumentTypeChildNode(ABC):
    """Represents the [DOM] NonDocumentTypeChildNode."""

    @property
    @abstractmethod
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        raise NotImplementedError

    @property
    @abstractmethod
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        raise NotImplementedError


class Node(ABC):
    """Represents the [DOM] Node."""

    ELEMENT_NODE = 1
    ATTRIBUTE_NODE = 2
    PROCESSING_INSTRUCTION_NODE = 7
    COMMENT_NODE = 8
    DOCUMENT_NODE = 9

    def __init__(self):
        self._owner_document = None

    @property
    @abstractmethod
    def node_name(self):
        """str: A string appropriate for the type of node."""
        raise NotImplementedError

    @property
    @abstractmethod
    def node_type(self):
        """int: The type of node."""
        raise NotImplementedError

    @property
    @abstractmethod
    def node_value(self):
        """str: The value of node."""
        raise NotImplementedError

    @node_value.setter
    @abstractmethod
    def node_value(self, value):
        raise NotImplementedError

    @property
    def owner_document(self):
        """Document: An associated document."""
        return (self._owner_document if self.node_type != Node.DOCUMENT_NODE
                else None)

    @property
    def parent_element(self):
        """Element: A parent element."""
        parent = self.parent_node
        if parent is not None and parent.node_type == Node.ELEMENT_NODE:
            return parent
        return None

    @property
    @abstractmethod
    def parent_node(self):
        """Node: A parent node."""
        raise NotImplementedError

    @property
    @abstractmethod
    def text_content(self):
        """str: The text content of node."""
        raise NotImplementedError

    @text_content.setter
    @abstractmethod
    def text_content(self, text):
        raise NotImplementedError

    @abstractmethod
    def append_child(self, node):
        """Adds a sub-node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        raise NotImplementedError

    @abstractmethod
    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        raise NotImplementedError

    @abstractmethod
    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        raise NotImplementedError

    @abstractmethod
    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        raise NotImplementedError

    @abstractmethod
    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be replaced.
        """
        raise NotImplementedError

    @abstractmethod
    def tostring(self, **kwargs):
        """Serializes a node to an encoded string representation of its XML
        tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        raise NotImplementedError


class Attr(Node):
    """Represents the [DOM] Attr."""

    def __init__(self, qualified_name, value=None, owner_element=None):
        """Constructs an Attr object.

        Arguments:
            qualified_name (str): The qualified name of the attribute.
            value (str, optional): The attribute's value.
            owner_element (Element, optional): The element that is associated
                with the attribute.
        """
        super().__init__()
        if value is None and owner_element is None:
            raise ValueError("Expected 'value' or 'owner_element'")
        self._qualified_name = self._local_name = qualified_name
        self._namespace_uri = None
        self._prefix = None
        self._value = value
        self._owner_element = owner_element
        matched = _RE_ATTR_QUALIFIED_NAME.match(qualified_name)
        if matched is not None:
            self._namespace_uri = matched.group('namespace')
            self._local_name = matched.group('local_name')
            if owner_element is not None:
                for prefix, namespace in owner_element.nsmap.items():
                    if namespace == self._namespace_uri:
                        self._prefix = prefix
                        break

    @property
    def local_name(self):
        """str: The local name of the attribute."""
        return self._local_name

    @property
    def name(self):
        """str: The qualified name of the attribute."""
        return self._qualified_name

    @property
    def namespace_uri(self):
        """str: The namespace URI of the attribute."""
        return self._namespace_uri

    @property
    def node_name(self):
        """str: The qualified name of the attribute.
        Same as Attr.name.
        """
        return self.name

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.ATTRIBUTE_NODE

    @property
    def node_value(self):
        """str: The attribute's value.
        Same sa Attr.value.
        """
        return self.value

    @node_value.setter
    def node_value(self, value):
        self.value = value

    @property
    def owner_element(self):
        """Element: The element that is associated with the attribute."""
        return self._owner_element

    @property
    def parent_node(self):
        """Node: A parent node."""
        return None

    @property
    def prefix(self):
        """str: The namespace prefix of the attribute."""
        return self._prefix

    @property
    def text_content(self):
        """str: The attribute's value.
        Same sa Attr.value.
        """
        return self.value

    @text_content.setter
    def text_content(self, value):
        self.value = value

    @property
    def value(self):
        """str: The attribute's value."""
        if self._owner_element is not None:
            return self._owner_element.get(self._qualified_name)
        return self._value

    @value.setter
    def value(self, value):
        if self._owner_element is not None:
            self._owner_element.set(self._qualified_name, value)
        else:
            self._value = value

    def append_child(self, node):
        """Adds a node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        return None

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be replaced.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def tostring(self, **kwargs):
        """Serializes the attribute's value to a string.

        Arguments:
            **kwargs: Reserved.
        Returns:
            bytes: An attribute.
        """
        return self.value.encode()


class CharacterData(Node, NonDocumentTypeChildNode):
    """Represents the [DOM] CharacterData."""

    @property
    @abstractmethod
    def data(self):
        """str: The value of node."""
        raise NotImplementedError

    @data.setter
    @abstractmethod
    def data(self, data):
        raise NotImplementedError

    @property
    def length(self):
        """int: A length of the data."""
        return len(self.data)


class Comment(etree.CommentBase, CharacterData):
    """Represents the [DOM] Comment."""

    def _init(self):
        Node.__init__(self)

    @property
    def data(self):
        """str: The value of node."""
        return self.text

    @data.setter
    def data(self, data):
        self.text = data

    @property
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        nodes = self.itersiblings()
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def node_name(self):
        """str: '#comment'."""
        return '#comment'

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.COMMENT_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return self.data

    @node_value.setter
    def node_value(self, value):
        self.data = value

    @property
    def parent_node(self):
        """Node: A parent node."""
        return self.getparent()

    @property
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        nodes = self.itersiblings(preceding=True)
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def text_content(self):
        """str: The text content of node."""
        return self.data

    @text_content.setter
    def text_content(self, text):
        self.data = text

    def _set_owner_document(self, node):
        for it in node.iter():
            if not isinstance(it, Node):
                raise TypeError('Expected Node, got {} {}'.format(
                    repr(type(it)), hex(id(it))))
            it._owner_document = self.owner_document

    def addnext(self, element):
        """Reimplemented from lxml.etree.CommentBase.addnext().

        Adds the element as a following sibling directly after this element.
        """
        self._set_owner_document(element)
        super().addnext(element)

    def addprevious(self, element):
        """Reimplemented from lxml.etree.CommentBase.addprevious().

        Adds the element as a preceding sibling directly before this element.
        """
        self._set_owner_document(element)
        super().addprevious(element)

    def append_child(self, node):
        """Adds a node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def extend(self, elements):
        """Reimplemented from lxml.etree.CommentBase.extend().

        Extends the current children by the elements in the iterable.
        """
        for element in elements:
            self._set_owner_document(element)
        super().extend(elements)

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        return self.getroottree().getroot()

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def remove(self, element):
        """Reimplemented from lxml.etree.CommentBase.remove().

        Removes a matching subelement. Unlike the find methods, this method
        compares elements based on identity, not on tag value or contents.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def replace(self, old_element, new_element):
        """Reimplemented from lxml.etree.CommentBase.replace().

        Replaces a subelement with the element passed as second argument.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be replaced.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def tostring(self, **kwargs):
        """Serializes a comment to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        return etree.tostring(self, **kwargs)


class Element(etree.ElementBase, Node, ParentNode, NonDocumentTypeChildNode):
    """Represents the [DOM] Element."""

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
        Node.__init__(self)
        self._attributes = Attrib(self.attrib)

    @property
    def attributes(self):
        """Attrib: A dictionary of an element attributes."""
        return self._attributes

    @property
    def children(self):
        """list[Element]: A list of the child elements, in document order."""
        elements = list()
        for node in iter(self):
            if node.node_type == Node.ELEMENT_NODE:
                elements.append(node)
        return elements

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
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        nodes = self.itersiblings()
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def node_name(self):
        """str: Same as Element.tag_name."""
        return self.tag_name

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.ELEMENT_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return None

    @node_value.setter
    def node_value(self, value):
        pass  # do nothing

    @property
    def parent_node(self):
        """Node: A parent node."""
        return self.getparent()

    @property
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        nodes = self.itersiblings(preceding=True)
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def qname(self):
        """lxml.etree.QName: The qualified XML name of an element."""
        qname = etree.QName(self)
        return qname

    @property
    def tag_name(self):
        """str: The qualified name of an element."""
        prefix = self.prefix
        local_name = self.local_name
        if prefix is not None:
            return prefix + ':' + local_name
        return local_name

    @property
    def text_content(self):
        """str: The text content of node."""
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

    def _set_owner_document(self, node, remove=False):
        owner_document = self.owner_document if not remove else None
        for it in node.iter():
            if not isinstance(it, Node):
                raise TypeError('Expected Node, got {} {}'.format(
                    repr(type(it)), hex(id(it))))
            it._owner_document = owner_document

    def addnext(self, element):
        """Reimplemented from lxml.etree.ElementBase.addnext().

        Adds the element as a following sibling directly after this element.
        """
        self._set_owner_document(element)
        super().addnext(element)


    def addprevious(self, element):
        """Reimplemented from lxml.etree.ElementBase.addprevious().

        Adds the element as a preceding sibling directly before this element.
        """
        self._set_owner_document(element)
        super().addprevious(element)

    def append(self, node):
        """Reimplemented from lxml.etree.ElementBase.append().

        Inserts a sub-node after the last child node.

        Arguments:
            node (Node): A node to be added.
        """
        self._set_owner_document(node)
        super().append(node)

    def append_child(self, node):
        """Adds a sub-node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        self.append(node)
        return node

    def create_sub_element(self, local_name, index=None, attrib=None,
                           nsmap=None, **_extra):
        """Creates a sub-element instance, and adds to the end of this element.
        See also Element.create_sub_element_ns(), Document.create_element(),
        Document.create_element_ns(), SVGParser.create_element() and
        SVGParser.create_element_ns().

        Arguments:
            local_name (str): A local name of an element to be created.
            index (int, optional): If specified, inserts a sub-element at the
                given position in this element.
            attrib (dict, optional): A dictionary of an element's attributes.
            nsmap (dict, optional): A map of a namespace prefix to the URI.
            **_extra: See lxml.etree._Element.makeelement() and
                lxml.etree._BaseParser.makeelement().
        Returns:
            Element: A new element.
        """
        element = self.makeelement(local_name,
                                   attrib=attrib,
                                   nsmap=nsmap,
                                   **_extra)
        if index is not None:
            self.insert(index, element)
        else:
            self.append(element)
        return element

    def create_sub_element_ns(self, namespace, local_name, index=None,
                              attrib=None, nsmap=None, **_extra):
        """Creates a sub-element instance with the specified namespace URI,
        and adds to the end of this element.
        See also Element.create_sub_element(), Document.create_element(),
        Document.create_element_ns(), SVGParser.create_element() and
        SVGParser.create_element_ns().

        Arguments:
            namespace (str, None): The namespace URI to associated with
                the element.
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
            >>> root = parser.create_element('svg', nsmap={'html': 'http://www.w3.org/1999/xhtml'})
            >>> video = root.create_sub_element_ns('http://www.w3.org/1999/xhtml', 'video')
            >>> print(root.tostring(pretty_print=True).decode())
            <svg xmlns:html="http://www.w3.org/1999/xhtml" xmlns="http://www.w3.org/2000/svg">
              <html:video/>
            </svg>
        """
        if namespace is not None:
            tag = '{{{0}}}{1}'.format(namespace, local_name)
        else:
            tag = local_name
        element = self.create_sub_element(tag,
                                          index=index,
                                          attrib=attrib,
                                          nsmap=nsmap,
                                          **_extra)
        return element

    def extend(self, elements):
        """Reimplemented from lxml.etree.ElementBase.extend().

        Extends the current children by the elements in the iterable.
        """
        for element in elements:
            self._set_owner_document(element)
        super().extend(elements)

    def get_attribute(self, qualified_name):
        """Returns an element attribute with the specified name.

        Arguments:
            qualified_name (str): The name of the attribute.
        Returns:
            str: Returns the value of the specified attribute or None.
        """
        return self.attributes.get(qualified_name)

    def get_attribute_names(self):
        """Returns a list of attribute names in order.

        Returns:
            list[str]: A list of attribute names.
        """
        return sorted(self.attributes.keys())

    def get_attribute_ns(self, namespace, local_name):
        """Returns an element attribute with the specified namespace and name.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
        Returns:
            str: Returns the value of the specified attribute or None.
        """
        return self.attributes.get_ns(namespace, local_name)

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
            context=self).value(direction=SVGLength.DIRECTION_UNSPECIFIED)

        # 'tab-size' property
        # Value: <percentage> | <length>
        # Initial: 8
        # See https://drafts.csswg.org/css-text-3/#tab-size-property
        tab_size = style['tab-size']
        style['tab-size'] = SVGLength(
            tab_size,
            context=self).value(direction=SVGLength.DIRECTION_UNSPECIFIED)

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
        css_rules = get_css_rules(self)
        element = self
        while element is not None:
            css_style, css_style_important = get_css_style(element, css_rules)
            css_style.update(element.attributes)
            _style = css_style.pop('style', None)
            if _style is not None:
                css_style.update(style_to_dict(_style))
            css_style.update(css_style_important)
            for key in iter(list(inherited_props.keys())):
                value = css_style.get(key)
                if value is not None and value not in ['inherit']:
                    if key == 'font':
                        # 'font' shorthand property
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
            display = css_style.get('display')
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

    def get_elements_by_class_name(self, class_names, namespaces=None):
        """Finds all matching sub-elements, by class names.

        Arguments:
            class_names (str): A list of class names that are separated by
                whitespace.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_class_name(self,
                                          class_names,
                                          namespaces=namespaces)

    def get_elements_by_local_name(self, local_name, namespaces=None):
        """Finds all matching sub-elements, by the local name.

        Arguments:
            local_name (str): The local name.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return self.xpath('.//*[local-name() = $local_name]',
                          namespaces=namespaces,
                          local_name=local_name)

    def get_elements_by_tag_name(self, qualified_name, namespaces=None):
        """Finds all matching sub-elements, by the qualified name.

        Arguments:
            qualified_name (str): The qualified name or '*'.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_tag_name(self,
                                        qualified_name,
                                        namespaces=namespaces)

    def get_elements_by_tag_name_ns(self, namespace, local_name,
                                    namespaces=None):
        """Finds all matching sub-elements, by the namespace URI and the local
        name.

        Arguments:
            namespace (str, None): The namespace URI, '*' or None.
            local_name (str): The local name or '*'.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            list[Element]: A list of elements.
        """
        return get_elements_by_tag_name_ns(self,
                                           namespace,
                                           local_name,
                                           namespaces=namespaces)

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        return self.getroottree().getroot()

    def has_attribute(self, qualified_name):
        """Returns True if an element attribute with the specified name
        exists; otherwise returns False.

        Arguments:
            qualified_name (str): The name of the attribute.
        Returns:
            bool: Returns True if the attribute exists, else False.
        """
        return self.attributes.has(qualified_name)

    def has_attribute_ns(self, namespace, local_name):
        """Returns True if an element attribute with the specified namespace
        and name exists; otherwise returns False.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
        Returns:
            bool: Returns True if the attribute exists, else False.
        """
        return self.attributes.has_ns(namespace, local_name)

    def insert(self, index, element):
        """Reimplemented from lxml.etree.ElementBase.insert().

        Inserts a subelement at the given position in this element.
        """
        self._set_owner_document(element)
        super().insert(index, element)

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        if child is None:
            return self.append_child(node)
        elif child not in self:
            raise ValueError('The object can not be found here')
        else:
            child.addprevious(node)
        return node

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

    def prepend(self, node):
        """Inserts a sub-node before the first child node.

        Arguments:
            node (Node): A node to be added.
        """
        self.insert(0, node)

    def query_selector_all(self, selectors):
        nsmap = self.nsmap.copy()
        uri = nsmap.pop(None, None)
        if uri is not None:
            nsmap['svg'] = uri
        sel = cssselect.CSSSelector(selectors, namespaces=nsmap)
        return sel(self)

    def remove(self, element):
        """Reimplemented from lxml.etree.ElementBase.remove().

        Removes a matching subelement. Unlike the find methods, this method
        compares elements based on identity, not on tag value or contents.
        """
        if element not in self:
            raise ValueError('The object can not be found here')
        self._set_owner_document(element, remove=True)
        super().remove(element)

    def remove_attribute(self, qualified_name):
        """Removes an element attribute with the specified name.

        Arguments:
            qualified_name (str): The name of the attribute.
        """
        self.attributes.pop(qualified_name, None)

    def remove_attribute_ns(self, namespace, local_name):
        """Removes an element attribute with the specified namespace and name.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
        """
        self.attributes.pop_ns(namespace, local_name, None)

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        self.remove(child)
        return child

    def replace(self, old_element, new_element):
        """Reimplemented from lxml.etree.ElementBase.replace().

        Replaces a subelement with the element passed as second argument.
        """
        if old_element not in self:
            raise ValueError('The object can not be found here')
        self._set_owner_document(new_element)
        self._set_owner_document(old_element, remove=True)
        super().replace(old_element, new_element)

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be replaced.
        """
        self.replace(child, node)
        return node

    def set_attribute(self, qualified_name, value):
        """Sets an element attribute.

        Arguments:
            qualified_name (str): The name of the attribute.
            value (str): The value of the attribute.
        """
        self.attributes.set(qualified_name, value)

    def set_attribute_ns(self, namespace, local_name, value):
        """Sets an element attribute with the specified namespace and name.

        Arguments:
            namespace (str, None): The namespace URI.
            local_name (str): The local name of the attribute.
            value (str): The value of the attribute.
        """
        self.attributes.set_ns(namespace, local_name, value)

    def tostring(self, **kwargs):
        """Serializes an element to an encoded string representation of its
        XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        return etree.tostring(self, **kwargs)


class ElementCSSInlineStyle(Element):
    """Represents the [cssom] ElementCSSInlineStyle."""

    @property
    def style(self):
        """CSSStyleDeclaration: A CSS declaration block object."""
        style = CSSStyleDeclaration(owner_node=self)
        return style


class LinkStyle(Element):
    """Represents the [cssom] LinkStyle."""

    @property
    def sheet(self):
        """StyleSheet: An associated CSS style sheet."""
        css_style_sheet = get_css_style_sheet_from_element(self)
        return css_style_sheet


class NonElementParentNode(ABC):
    """Represents the [DOM] NonElementParentNode."""

    @abstractmethod
    def get_element_by_id(self, element_id, namespaces=None):
        """Finds the first matching sub-element, by id.

        Arguments:
            element_id (str): The id of the element.
            namespaces (dict, optional): The XPath prefixes in the path
                expression.
        Returns:
            Element: The first matching sub-element. Returns None if there is
                no such element.
        """
        raise NotImplementedError


class ProcessingInstruction(etree.PIBase, CharacterData):
    """Represents the [DOM] ProcessingInstruction."""

    def _init(self):
        Node.__init__(self)

    @property
    def data(self):
        """str: The value of node."""
        return self.text

    @data.setter
    def data(self, data):
        self.text = data

    @property
    def next_element_sibling(self):
        """Element: The first following sibling element or None."""
        nodes = self.itersiblings()
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def node_name(self):
        """str: A string appropriate for the type of node."""
        return self.target

    @property
    def node_type(self):
        """int: The type of node."""
        return Node.PROCESSING_INSTRUCTION_NODE

    @property
    def node_value(self):
        """str: The value of node."""
        return self.data

    @node_value.setter
    def node_value(self, value):
        self.data = value

    @property
    def parent_node(self):
        """Node: A parent node."""
        return self.getparent()

    @property
    def previous_element_sibling(self):
        """Element: The first preceding sibling element or None."""
        nodes = self.itersiblings(preceding=True)
        for node in nodes:
            if node.node_type == Node.ELEMENT_NODE:
                return node
        return None

    @property
    def text_content(self):
        """str: The text content of node."""
        return self.data

    @text_content.setter
    def text_content(self, text):
        self.data = text

    def append_child(self, node):
        """Adds a node to the end of this node.

        Arguments:
            node (Node): A node to be added.
        Returns:
            Node: A node to be added.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def get_root_node(self):
        """Returns a root node of the document that contains this node.

        Returns:
            Node: A root node.
        """
        return self.getroottree().getroot()

    def insert_before(self, node, child):
        """Inserts a node into a parent before a child.

        Arguments:
            node (Node): A node to be inserted.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be inserted.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def remove_child(self, child):
        """Removes a child node from this node.

        Arguments:
            child (Node): A node to be removed.
        Returns:
            Node: A node to be removed.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def replace_child(self, node, child):
        """Replaces a child with node.

        Arguments:
            node (Node): A node to be replaced.
            child (Node, None): A reference child node.
        Returns:
            Node: A node to be replaced.
        """
        raise ValueError('The operation would yield an incorrect node tree')

    def tostring(self, **kwargs):
        """Serializes a processing instruction to an encoded string
        representation of its XML tree.

        Arguments:
            **kwargs: See lxml.etree.tostring().
        Returns:
            bytes: An XML document.
        """
        return etree.tostring(self, **kwargs)
