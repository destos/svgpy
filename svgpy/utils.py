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
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse, urlunparse, unquote
from urllib.request import urlopen

from .config import config


def get_content_type(headers):
    _headers = {k.lower(): v for k, v in headers.items()}
    content_type = _headers.get('content-type')
    if content_type is None:
        return None
    parameters = [x.strip() for x in content_type.split(';')]
    result = dict({None: parameters.pop(0)})
    for parameter in parameters:
        items = parameter.split('=')
        if len(items) == 2:
            result[items[0]] = items[1]
    return result


def load(path_or_url, encoding=None, **kwargs):
    scheme = urlparse(path_or_url).scheme
    headers = {}
    if scheme == 'data':
        # data:[<MIME-type>][;charset=<encoding>][;base64],<data>
        start = path_or_url.find(':')
        end = path_or_url.find(',')
        if start < 0 or end < 0:
            return None, headers
        content_type = path_or_url[start + 1:end].strip()
        if len(content_type) == 0:
            content_type = 'text/plain;charset=US-ASCII'
        data = unquote(path_or_url[end + 1:].strip())
        parameters = [x.strip() for x in content_type.split(';')]
        if 'base64' in parameters:
            parameters.remove('base64')
            data = base64.b64decode(data)
        headers = {'Content-Type': ';'.join(parameters)}
        return data, headers
    elif len(scheme) > 0:
        url = path_or_url
    else:
        url = Path(path_or_url).absolute().as_uri()
    with urlopen(url, **kwargs) as response:
        if hasattr(response, 'getheaders'):
            headers = dict(response.getheaders())
        data = response.read()
        if encoding is not None:
            data = data.decode(encoding)
        return data, headers


def normalize_path(path):
    path_obj = Path(path).absolute()
    return Path(os.path.normpath(path_obj)).as_uri()


def normalize_url(path_or_url):
    def _url_normalize(_parts):
        _scheme = _parts.scheme.lower()
        _netloc = _parts.netloc.lower().split(':')
        _path = _parts.path
        _params = _parts.params
        _query = _parts.query
        _fragment = _parts.fragment
        if len(_scheme) > 0 and len(_netloc) == 2:
            if ((_scheme == 'http' and int(_netloc[1]) == 80)
                    or (_scheme == 'https' and int(_netloc[1]) == 443)):
                del _netloc[1]
        if _scheme != 'data':
            _path = unquote(_path)
            _path = os.path.normpath(_path)
            _path = quote(_path, safe='/~')
        return urlunparse(
            (_scheme, ':'.join(_netloc), _path, _params, _query, _fragment))

    if path_or_url.startswith('local(') and path_or_url.endswith(')'):
        # local(...)
        src = remove_quotes(path_or_url[6:-1])
        url = normalize_path(src)
        return url
    elif path_or_url.startswith('url(') and path_or_url.endswith(')'):
        # url(...)
        src = remove_quotes(path_or_url[4:-1])
        parts = urlparse(src)
        if len(parts.scheme) > 0:
            url = _url_normalize(parts)
            return url
        for proxy_pass_path, base_url in config.proxy_pass.items():
            if proxy_pass_path != '/' and src.startswith(proxy_pass_path):
                url = urljoin(base_url, src[len(proxy_pass_path) + 1:])
                url = _url_normalize(urlparse(url))
                return url
        url = urljoin(config.proxy_pass['/'], src)
        url = _url_normalize(urlparse(url))
        return url

    parts = urlparse(remove_quotes(path_or_url))
    if len(parts.scheme) > 0:
        url = _url_normalize(parts)
    else:
        url = normalize_path(path_or_url)
    return url


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
        del self._data[self._keys[key.lower()]]

    def __getitem__(self, key):
        return self._data[self._keys[key.lower()]]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        return repr(self._data)

    def __setitem__(self, key, value):
        self._data[self._keys.setdefault(key.lower(), key)] = value
