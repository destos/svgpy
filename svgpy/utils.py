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
from pathlib import Path
from urllib.parse import urlparse, unquote
from urllib.request import urlopen


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
