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


class Longhand(object):

    @staticmethod
    def is_longhand(property_name):
        if property_name.startswith('--'):
            return False
        property_name = property_name.lower()
        return property_name in longhand_property_map

    @staticmethod
    def shorthands(property_name):
        property_name = property_name.lower()
        return longhand_property_map.get(property_name, ())


longhand_property_map = {
    # 'font'
    'font-style': ('font', 'font-variant'),
    'font-variant': ('font', 'font-variant'),  # <font-variant-css2>
    'font-weight': ('font', 'font-variant'),
    'font-stretch': ('font', 'font-variant'),  # <font-stretch-css3>
    'font-size': ('font', 'font-variant'),
    'line-height': ('font', 'font-variant'),
    'font-family': ('font', 'font-variant'),
    # 'font-variant'
    'font-variant-ligatures': ('font', 'font-variant'),
    'font-variant-caps': ('font', 'font-variant'),
    'font-variant-alternates': ('font', 'font-variant'),
    'font-variant-numeric': ('font', 'font-variant'),
    'font-variant-east-asian': ('font', 'font-variant'),
    'font-variant-position': ('font', 'font-variant'),
    # 'overflow'
    'overflow-x': ('overflow',),
    'overflow-y': ('overflow',),
}