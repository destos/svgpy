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


import base64
import os
from collections.abc import MutableMapping
from pathlib import PurePath
from urllib.parse import unquote
from urllib.request import urlopen

from .url import Location, URL


def get_content_type(headers):
    _headers = CaseInsensitiveMapping(headers)
    # Content-Type := type "/" subtype *[";" parameter]
    # parameter := attribute "=" value
    content_type = _headers.get('Content-Type')
    if content_type is None:
        return None
    parameters = [x.strip() for x in content_type.split(';')]
    result = CaseInsensitiveMapping({None: parameters.pop(0)})
    for parameter in parameters:
        items = parameter.split('=')
        if len(items) == 2:
            result[items[0]] = items[1]
    return result


def get_element_by_id(element, element_id, namespaces=None):
    """Finds the first matching sub-element, by id.

    Arguments:
        element (Element): The root element.
        element_id (str): The id of the element.
        namespaces (dict, optional): The XPath prefixes in the path
            expression.
    Returns:
        Element: The first matching sub-element. Returns None if there is
            no such element.
    """
    elements = element.xpath('descendant-or-self::*[@id = $element_id]',
                             namespaces=namespaces,
                             element_id=element_id)
    return elements[0] if len(elements) > 0 else None


def get_elements_by_class_name(element, class_names, namespaces=None,
                               include_self=False):
    """Finds all matching sub-elements, by class names.

    Arguments:
        element (Element): The root element.
        class_names (str): A list of class names that are separated by
            whitespace.
        namespaces (dict, optional): The XPath prefixes in the path
            expression.
        include_self (bool, optional):
    Returns:
        list[Element]: A list of elements.
    """
    names = class_names.split()
    if len(names) == 0:
        return []
    if include_self:
        axis = 'descendant-or-self'
    else:
        axis = 'descendant'
    patterns = [r're:test(@class, "(^| ){}($| )")'.format(x) for x in names]
    expr = '{}::*[{}]'.format(axis, ' and '.join(patterns))
    if namespaces is None:
        namespaces = dict()
    namespaces['re'] = 'http://exslt.org/regular-expressions'
    return element.xpath(expr, namespaces=namespaces)


def get_elements_by_tag_name(element, qualified_name, namespaces=None,
                             include_self=False):
    """Finds all matching sub-elements, by the qualified name.

    Arguments:
        element (Element): The root element.
        qualified_name (str): The qualified name or '*'.
        namespaces (dict, optional): The XPath prefixes in the path
            expression.
        include_self (bool, optional):
    Returns:
        list[Element]: A list of elements.
    """
    if include_self:
        axis = 'descendant-or-self'
    else:
        axis = 'descendant'
    expr = '{}::*{}'.format(axis,
                            '' if qualified_name == '*'
                            else '[name() = $qualified_name]')
    return element.xpath(expr,
                         namespaces=namespaces,
                         qualified_name=qualified_name)


def get_elements_by_tag_name_ns(element, namespace, local_name,
                                namespaces=None, include_self=False):
    """Finds all matching sub-elements, by the namespace URI and the local
    name.

    Arguments:
        element (Element): The root element.
        namespace (str, None): The namespace URI, '*' or None.
        local_name (str): The local name or '*'.
        namespaces (dict, optional): The XPath prefixes in the path
            expression.
        include_self (bool, optional):
    Returns:
        list[Element]: A list of elements.
    """
    if include_self:
        axis = 'descendant-or-self'
    else:
        axis = 'descendant'
    patterns = list()
    if namespace is not None and namespace != '*':
        patterns.append('namespace-uri() = $namespace')
    if local_name != '*':
        patterns.append('local-name() = $local_name')
    expr = '{}::*{}'.format(axis,
                            '' if len(patterns) == 0
                            else '[{}]'.format(' and '.join(patterns)))
    return element.xpath(expr,
                         namespaces=namespaces,
                         namespace=namespace,
                         local_name=local_name)


def load(src, encoding=None, **kwargs):
    if isinstance(src, URL):
        url = src
    elif isinstance(src, str):
        url = URL(src)
    else:
        raise TypeError('Expected str or URL, got {}'.format(src))
    scheme = url.protocol
    headers = CaseInsensitiveMapping()
    if scheme == 'data:':
        # data:[<MIME-type>][;charset=<encoding>][;base64],<data>
        pathname = url.pathname
        end = pathname.find(',')
        if end < 0:
            return None, headers
        content_type = pathname[0:end].strip()
        if len(content_type) == 0:
            content_type = 'text/plain;charset=US-ASCII'
        data = unquote(pathname[end + 1:].strip())
        parameters = [x.strip() for x in content_type.split(';')]
        if 'base64' in parameters:
            parameters.remove('base64')
            data = base64.b64decode(data)
        headers['Content-Type'] = ';'.join(parameters)
        return data, headers

    with urlopen(url.href, **kwargs) as response:
        if hasattr(response, 'getheaders'):
            headers.update(response.getheaders())
        data = response.read()
        if encoding is not None:
            data = data.decode(encoding)
        return data, headers


def normalize_url(src, base=None):
    """Normalizes an URL.

    Arguments:
        src (str, Location): An entire URL or a relative-URL to be normalized.
        base (str, optional): A base URL for a relative-URL.
    Returns:
        URL: A new URL object.
    """
    if isinstance(src, str):
        _src = src
    elif isinstance(src, Location):
        _src = src.href
    else:
        raise TypeError('Expected str or Location, got ' + repr(type(src)))
    if base is None or base.startswith('about:'):
        base = PurePath(os.getcwd()).as_uri()
    return URL(_src, base=base)


def remove_quotes(src):
    if ((src.startswith('"') and src.endswith('"'))
            or (src.startswith('\'') and src.endswith('\''))):
        src = src[1:-1]
    return src


class CaseInsensitiveMapping(MutableMapping):
    def __init__(self, *args, **kwargs):
        self._data = dict()
        self._keys = dict()
        self.update(dict(*args, **kwargs))

    def __delitem__(self, key):
        del self._data[self._keys[CaseInsensitiveMapping._key(key)]]

    def __getitem__(self, key):
        return self._data[self._keys[CaseInsensitiveMapping._key(key)]]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def __setitem__(self, key, value):
        self._data[
            self._keys.setdefault(
                CaseInsensitiveMapping._key(key), key)
        ] = value

    @staticmethod
    def _key(key):
        return key.lower() if isinstance(key, str) else key
