#!/usr/bin/env python3


import os
import sys
import unittest

sys.path.extend(['.', '..'])

from svgpy.url import Location, URL, URLSearchParams

here = os.path.abspath(os.path.dirname(__file__))
os.chdir(here)


class LocationTestCase(unittest.TestCase):
    def test_location_attr_hash(self):
        location = Location()
        location.href = 'https://example.org/'
        location.hash = '#api'
        self.assertEqual('https://example.org/#api',
                         location.tostring())
        self.assertEqual('https://example.org/#api',
                         location.href)
        self.assertEqual('https://example.org', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('#api', location.hash)

        location.hash = 'url-class'
        self.assertEqual('https://example.org/#url-class',
                         location.tostring())
        self.assertEqual('https://example.org/#url-class',
                         location.href)
        self.assertEqual('https://example.org', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('#url-class', location.hash)

        location.hash = ''
        self.assertEqual('', location.hash)

    def test_location_attr_host(self):
        location = Location()
        location.href = 'https://example.org/'

        # ascii-domain with port
        location.host = 'example.org:8080'
        self.assertEqual('https://example.org:8080/', location.tostring())
        self.assertEqual('https://example.org:8080/', location.href)
        self.assertEqual('https://example.org:8080', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org:8080', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('8080', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # ascii-domain
        location.host = 'example.net'
        self.assertEqual('https://example.net/', location.tostring())
        self.assertEqual('https://example.net/', location.href)
        self.assertEqual('https://example.net', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.net', location.host)
        self.assertEqual('example.net', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IPv6 address without []
        location.host = '2001:db8::1'
        self.assertEqual('https://[2001:db8::1]/', location.tostring())
        self.assertEqual('https://[2001:db8::1]/', location.href)
        self.assertEqual('https://[2001:db8::1]', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('[2001:db8::1]', location.host)
        self.assertEqual('[2001:db8::1]', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IPv6 address with []
        location.host = '[2001:db8::2]'
        self.assertEqual('https://[2001:db8::2]/', location.tostring())
        self.assertEqual('https://[2001:db8::2]/', location.href)
        self.assertEqual('https://[2001:db8::2]', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('[2001:db8::2]', location.host)
        self.assertEqual('[2001:db8::2]', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IPv6 address with port
        location.host = '[2001:db8::3]:8000'
        self.assertEqual('https://[2001:db8::3]:8000/', location.tostring())
        self.assertEqual('https://[2001:db8::3]:8000/', location.href)
        self.assertEqual('https://[2001:db8::3]:8000', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('[2001:db8::3]:8000', location.host)
        self.assertEqual('[2001:db8::3]', location.hostname)
        self.assertEqual('8000', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IDN
        location.host = '日本語.example:444'
        self.assertEqual('https://xn--wgv71a119e.example:444/', location.href)
        self.assertEqual('https://xn--wgv71a119e.example:444', location.origin)
        self.assertEqual('xn--wgv71a119e.example:444', location.host)
        self.assertEqual('xn--wgv71a119e.example', location.hostname)
        self.assertEqual('444', location.port)

        # empty string
        location.host = ''
        self.assertEqual('', location.host)
        self.assertEqual('null', location.origin)
        self.assertEqual('', location.port)

    def test_location_attr_hostname(self):
        location = Location()
        location.href = 'https://example.org:8080/'

        # ascii-domain
        location.hostname = 'example.net'
        self.assertEqual('https://example.net:8080/', location.tostring())
        self.assertEqual('https://example.net:8080/', location.href)
        self.assertEqual('https://example.net:8080', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.net:8080', location.host)
        self.assertEqual('example.net', location.hostname)
        self.assertEqual('8080', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # ascii-domain with port
        location.hostname = 'example.com:444'
        self.assertEqual('https://example.com:444/', location.tostring())
        self.assertEqual('https://example.com:444/', location.href)
        self.assertEqual('https://example.com:444', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.com:444', location.host)
        self.assertEqual('example.com', location.hostname)
        self.assertEqual('444', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IPv6 address without []
        location.hostname = '2001:db8::1'
        self.assertEqual('https://[2001:db8::1]:444/', location.tostring())
        self.assertEqual('https://[2001:db8::1]:444/', location.href)
        self.assertEqual('https://[2001:db8::1]:444', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('[2001:db8::1]:444', location.host)
        self.assertEqual('[2001:db8::1]', location.hostname)
        self.assertEqual('444', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IPv6 address with []
        location.hostname = '2001:db8::2'
        self.assertEqual('https://[2001:db8::2]:444/', location.tostring())
        self.assertEqual('https://[2001:db8::2]:444/', location.href)
        self.assertEqual('https://[2001:db8::2]:444', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('[2001:db8::2]:444', location.host)
        self.assertEqual('[2001:db8::2]', location.hostname)
        self.assertEqual('444', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IPv6 address with port
        location.hostname = '[2001:db8::3]:445'
        self.assertEqual('https://[2001:db8::3]:445/', location.tostring())
        self.assertEqual('https://[2001:db8::3]:445/', location.href)
        self.assertEqual('https://[2001:db8::3]:445', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('[2001:db8::3]:445', location.host)
        self.assertEqual('[2001:db8::3]', location.hostname)
        self.assertEqual('445', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # IDN
        location.hostname = '日本語.example'
        self.assertEqual('https://xn--wgv71a119e.example:445/', location.href)
        self.assertEqual('https://xn--wgv71a119e.example:445',
                         location.origin)
        self.assertEqual('xn--wgv71a119e.example:445', location.host)
        self.assertEqual('xn--wgv71a119e.example', location.hostname)
        self.assertEqual('445', location.port)

        # contains forbidden host code point
        self.assertRaises(
            ValueError,
            lambda: setattr(location, 'hostname', 'example%20.test'))

        # empty string
        location.hostname = ''
        self.assertEqual('', location.host)
        self.assertEqual('', location.hostname)
        self.assertEqual('null', location.origin)
        self.assertEqual('445', location.port)

    def test_location_attr_pathname(self):
        location = Location()
        location.href = 'http://localhost/'
        location.pathname = '/svg/svg.svg'
        self.assertEqual('http://localhost/svg/svg.svg', location.tostring())
        self.assertEqual('http://localhost/svg/svg.svg', location.href)
        self.assertEqual('http://localhost', location.origin)
        self.assertEqual('http:', location.protocol)
        self.assertEqual('localhost', location.host)
        self.assertEqual('localhost', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/svg/svg.svg', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        location.pathname = '/wiki/Category:W3C勧告'
        self.assertEqual(
            'http://localhost/wiki/Category:W3C%E5%8B%A7%E5%91%8A',
            location.tostring())
        self.assertEqual(
            'http://localhost/wiki/Category:W3C%E5%8B%A7%E5%91%8A',
            location.href)
        self.assertEqual('http://localhost', location.origin)
        self.assertEqual('http:', location.protocol)
        self.assertEqual('localhost', location.host)
        self.assertEqual('localhost', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/wiki/Category:W3C%E5%8B%A7%E5%91%8A',
                         location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        location.pathname = '/path;param?a=0&b=1#hash'
        self.assertEqual('http://localhost/path;param%3Fa=0&b=1%23hash',
                         location.href)
        self.assertEqual('http://localhost', location.origin)
        self.assertEqual('http:', location.protocol)
        self.assertEqual('localhost', location.host)
        self.assertEqual('localhost', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/path;param%3Fa=0&b=1%23hash', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        location.pathname = ''
        self.assertEqual('/', location.pathname)

    def test_location_attr_port(self):
        location = Location()
        location.href = 'https://example.org:8080/'
        location.port = ''
        self.assertEqual('https://example.org/', location.tostring())
        self.assertEqual('https://example.org/', location.href)
        self.assertEqual('https://example.org', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        location.port = '8888'
        self.assertEqual('https://example.org:8888/', location.tostring())
        self.assertEqual('https://example.org:8888/', location.href)
        self.assertEqual('https://example.org:8888', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org:8888', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('8888', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        location.port = '443'
        self.assertEqual('https://example.org/', location.tostring())
        self.assertEqual('https://example.org/', location.href)
        self.assertEqual('https://example.org', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('443', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        location.port = '0'
        self.assertEqual('0', location.port)

        location.port = '65535'
        self.assertEqual('65535', location.port)

        # less than 2 ** 16
        self.assertRaises(ValueError,
                          lambda: setattr(location, 'port', '65536'))

        # ASCII-digits
        self.assertRaises(ValueError,
                          lambda: setattr(location, 'port', '0.1'))

        # empty string
        self.assertEqual('https://example.org:65535/', location.href)
        self.assertEqual('https://example.org:65535', location.origin)
        self.assertEqual('example.org:65535', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('65535', location.port)
        location.port = ''
        self.assertEqual('https://example.org/', location.href)
        self.assertEqual('https://example.org', location.origin)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('', location.port)

    def test_location_attr_protocol(self):
        location = Location()
        location.href = 'ssh://username@example.org/'
        location.protocol = 'ftp:'
        self.assertEqual('ftp://username@example.org/', location.tostring())
        self.assertEqual('ftp://username@example.org/', location.href)
        self.assertEqual('ftp://example.org', location.origin)
        self.assertEqual('ftp:', location.protocol)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        # starts with ASCII-alpha, followed by zero or more of
        # ASCII-alphanumeric, U+002B (+), U+002D (-), and U+002E (.).
        location.protocol = 'h323'
        self.assertEqual('h323:', location.protocol)

        # contains U+002B (+)
        location.protocol = 'CoAP+TCP'
        self.assertEqual('coap+tcp:', location.protocol)

        # contains U+002D (-)
        location.protocol = 'view-source'
        self.assertEqual('view-source:', location.protocol)

        # contains U+002E (.)
        location.protocol = 'xmlrpc.beep'
        self.assertEqual('xmlrpc.beep:', location.protocol)

        # starts with ASCII-alpha
        self.assertRaises(ValueError,
                          lambda: setattr(location, 'protocol', '0http:'))

        # starts with ASCII-alpha, followed by zero or more of
        # ASCII-alphanumeric, U+002B (+), U+002D (-), and U+002E (.).
        self.assertRaises(ValueError,
                          lambda: setattr(location, 'protocol', 'coap_tcp:'))

        # empty string
        location.protocol = ''
        self.assertEqual('', location.protocol)

    def test_location_attr_search(self):
        location = Location()
        location.href = 'https://example.org/'
        location.search = 'q=🏳️‍🌈&key=e1f7bc78'
        self.assertEqual(
            "https://example.org/"
            "?key=e1f7bc78&q=%F0%9F%8F%B3%EF%B8%8F%E2%80%8D%F0%9F%8C%88",
            location.tostring())
        self.assertEqual(
            "https://example.org/"
            "?key=e1f7bc78&q=%F0%9F%8F%B3%EF%B8%8F%E2%80%8D%F0%9F%8C%88",
            location.href)
        self.assertEqual('https://example.org', location.origin)
        self.assertEqual('https:', location.protocol)
        self.assertEqual('example.org', location.host)
        self.assertEqual('example.org', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/', location.pathname)
        self.assertEqual(
            '?key=e1f7bc78&q=%F0%9F%8F%B3%EF%B8%8F%E2%80%8D%F0%9F%8C%88',
            location.search)
        self.assertEqual('', location.hash)

        location.search = ''
        self.assertEqual('https://example.org/', location.tostring())
        self.assertEqual('', location.search)

    def test_location_init01(self):
        location = Location()
        self.assertEqual('about:blank', location.tostring())
        self.assertEqual('about:blank', location.href)
        self.assertEqual('null', location.origin)
        self.assertEqual('about:', location.protocol)
        self.assertEqual('', location.host)
        self.assertEqual('', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('blank', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

    def test_location_init02(self):
        location = Location()
        src = 'scheme://netloc/path;parameters?query=a#fragment'
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('null', location.origin)
        self.assertEqual('scheme:', location.protocol)
        self.assertEqual('netloc', location.host)
        self.assertEqual('netloc', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/path;parameters', location.pathname)
        self.assertEqual('?query=a', location.search)
        self.assertEqual('#fragment', location.hash)

        src = "scheme://user:password@netloc:88" \
              "/path;parameters?query=a#fragment"
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('null', location.origin)
        self.assertEqual('scheme:', location.protocol)
        self.assertEqual('netloc:88', location.host)
        self.assertEqual('netloc', location.hostname)
        self.assertEqual('88', location.port)
        self.assertEqual('/path;parameters', location.pathname)
        self.assertEqual('?query=a', location.search)
        self.assertEqual('#fragment', location.hash)

    def test_location_init03(self):
        location = Location()
        src = '/path;parameters?query=a#fragment'
        self.assertRaises(ValueError,
                          lambda: setattr(location, 'href', src))

        src = 'path;parameters?query=a#fragment'
        self.assertRaises(ValueError,
                          lambda: setattr(location, 'href', src))

        src = 'file:///path;parameters?query=a#fragment'
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('null', location.origin)
        self.assertEqual('file:', location.protocol)
        self.assertEqual('', location.host)
        self.assertEqual('', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/path;parameters', location.pathname)
        self.assertEqual('?query=a', location.search)
        self.assertEqual('#fragment', location.hash)

    def test_location_init_ipv4(self):
        location = Location()
        src = 'http://127.0.0.1:8000/svg/svg.svg'
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('http://127.0.0.1:8000', location.origin)
        self.assertEqual('http:', location.protocol)
        self.assertEqual('127.0.0.1:8000', location.host)
        self.assertEqual('127.0.0.1', location.hostname)
        self.assertEqual('8000', location.port)
        self.assertEqual('/svg/svg.svg', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

    def test_location_init_ipv6(self):
        location = Location()
        src = 'http://[::1]/svg/svg.svg'
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('http://[::1]', location.origin)
        self.assertEqual('http:', location.protocol)
        self.assertEqual('[::1]', location.host)
        self.assertEqual('[::1]', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('/svg/svg.svg', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

        src = 'http://[::1]:8000/svg/svg.svg'
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('http://[::1]:8000', location.origin)
        self.assertEqual('http:', location.protocol)
        self.assertEqual('[::1]:8000', location.host)
        self.assertEqual('[::1]', location.hostname)
        self.assertEqual('8000', location.port)
        self.assertEqual('/svg/svg.svg', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

    def test_location_init_about(self):
        location = Location()
        src = 'about:blank'
        location.href = src
        self.assertEqual(src, location.tostring())
        self.assertEqual(src, location.href)
        self.assertEqual('null', location.origin)
        self.assertEqual('about:', location.protocol)
        self.assertEqual('', location.host)
        self.assertEqual('', location.hostname)
        self.assertEqual('', location.port)
        self.assertEqual('blank', location.pathname)
        self.assertEqual('', location.search)
        self.assertEqual('', location.hash)

    def test_url_init01(self):
        # See https://url.spec.whatwg.org/#example-5434421b
        src = 'https://example.org/💩'
        url = URL(src)
        self.assertEqual('/%F0%9F%92%A9', url.pathname)

        src = '/🍣🍺'
        self.assertRaises(ValueError, lambda: URL(src))

        src = '/🍣🍺'
        base = 'https://example.org/#example'
        url = URL(src, base=base)
        self.assertEqual('https://example.org/%F0%9F%8D%A3%F0%9F%8D%BA',
                         url.href)

        src = '🏳️‍🌈'
        base = URL('https://pride.example/hello-world')
        url = URL(src, base=base)
        self.assertEqual('/%F0%9F%8F%B3%EF%B8%8F%E2%80%8D%F0%9F%8C%88',
                         url.pathname)

        self.assertRaises(ValueError, lambda: URL(''))

        self.assertRaises(ValueError, lambda: URL('', base=''))

        self.assertRaises(TypeError, lambda: URL('', base=0))

        url = URL('', base='https://example.org')
        self.assertEqual('https://example.org/', url.href)
        self.assertEqual('/', url.pathname)

        url = URL('hello/../world', base='https://example.org')
        self.assertEqual('https://example.org/world', url.href)
        self.assertEqual('/world', url.pathname)

        url = URL('about:blank', base='https://example.org/')
        self.assertEqual('about:blank', url.href)

    def test_url_init02(self):
        src = 'scheme://netloc/path;parameters?query=a#fragment'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('null', url.origin)
        self.assertEqual('scheme:', url.protocol)
        self.assertEqual('netloc', url.host)
        self.assertEqual('netloc', url.hostname)
        self.assertEqual('', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('/path;parameters', url.pathname)
        self.assertEqual('?query=a', url.search)
        self.assertEqual('#fragment', url.hash)

        src = "scheme://user:password@netloc:81" \
              "/path;parameters?query=a#fragment"
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('null', url.origin)
        self.assertEqual('scheme:', url.protocol)
        self.assertEqual('netloc:81', url.host)
        self.assertEqual('netloc', url.hostname)
        self.assertEqual('81', url.port)
        self.assertEqual('user', url.username)
        self.assertEqual('password', url.password)
        self.assertEqual('/path;parameters', url.pathname)
        self.assertEqual('?query=a', url.search)
        self.assertEqual('#fragment', url.hash)

    def test_url_init03(self):
        # see https://en.wikipedia.org/wiki/URL_normalization
        src = 'HTTP://WWW.EXAMPLE.COM:80/css/./style.css'
        url = URL(src)
        self.assertEqual('http://www.example.com/css/style.css', url.href)

        src = 'HTTPS://WWW.EXAMPLE.COM:443/css/./style.css'
        url = URL(src)
        self.assertEqual('https://www.example.com/css/style.css', url.href)

        src = 'HTTP://www.Example.com:80/~%c2%b1/'
        url = URL(src)
        self.assertEqual('http://www.example.com/~%C2%B1/', url.href)

        src = 'HTTP://www.Example.com:80/%7e%c2%b1/'
        url = URL(src)
        self.assertEqual('http://www.example.com/~%C2%B1/', url.href)

        src = 'http://www.example.com/../a/b/../c/./d.html'
        url = URL(src)
        self.assertEqual('http://www.example.com/a/c/d.html', url.href)

    def test_url_init04(self):
        src = 'ja'
        base = 'http://localhost:8000/docs/en-US;parameters?query=a#fragment'
        url = URL(src, base=base)
        self.assertEqual('http://localhost:8000/docs/ja', url.href)

        src = '/docs/ja'
        base = 'http://localhost:8000/docs/en-US;parameters?query=a#fragment'
        url = URL(src, base=base)
        self.assertEqual('http://localhost:8000/docs/ja', url.href)

        src = 'ja;parameters?query=a#fragment'
        base = 'http://example.com/docs/en-US#foo'
        url = URL(src, base=base)
        self.assertEqual(
            'http://example.com/docs/ja;parameters?query=a#fragment',
            url.href)
        self.assertEqual('/docs/ja;parameters', url.pathname)
        self.assertEqual('?query=a', url.search)
        self.assertEqual('#fragment', url.hash)

    def test_url_init_about_blank(self):
        src = 'about:blank'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('null', url.origin)
        self.assertEqual('about:', url.protocol)
        self.assertEqual('', url.host)
        self.assertEqual('', url.hostname)
        self.assertEqual('', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('blank', url.pathname)
        self.assertEqual('', url.search)
        self.assertEqual('', url.hash)

    def test_url_init_blob(self):
        # See https://url.spec.whatwg.org/#example-43b5cea5
        src = 'blob:https://whatwg.org/d0360e2f-caee-469f-9a2f-87d5b0456f6f'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('https://whatwg.org', url.origin)
        self.assertEqual('blob:', url.protocol)
        self.assertEqual('', url.host)
        self.assertEqual('', url.hostname)
        self.assertEqual('', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual(
            'https://whatwg.org/d0360e2f-caee-469f-9a2f-87d5b0456f6f',
            url.pathname)
        self.assertEqual('', url.search)
        self.assertEqual('', url.hash)

    def test_url_init_ipv4(self):
        src = 'http://127.0.0.1:8000/svg/svg.svg'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('http://127.0.0.1:8000', url.origin)
        self.assertEqual('http:', url.protocol)
        self.assertEqual('127.0.0.1:8000', url.host)
        self.assertEqual('127.0.0.1', url.hostname)
        self.assertEqual('8000', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('/svg/svg.svg', url.pathname)
        self.assertEqual('', url.search)
        self.assertEqual('', url.hash)

    def test_url_init_ipv6(self):
        src = 'http://[::1]/svg/svg.svg'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('http://[::1]', url.origin)
        self.assertEqual('http:', url.protocol)
        self.assertEqual('[::1]', url.host)
        self.assertEqual('[::1]', url.hostname)
        self.assertEqual('', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('/svg/svg.svg', url.pathname)
        self.assertEqual('', url.search)
        self.assertEqual('', url.hash)

        src = 'http://[::1]:8000/svg/svg.svg'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('http://[::1]:8000', url.origin)
        self.assertEqual('http:', url.protocol)
        self.assertEqual('[::1]:8000', url.host)
        self.assertEqual('[::1]', url.hostname)
        self.assertEqual('8000', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('/svg/svg.svg', url.pathname)
        self.assertEqual('', url.search)
        self.assertEqual('', url.hash)

    def test_url_init_data(self):
        # data scheme
        src = 'data:text/plain;base64,SGVsbG8sIFdvcmxkIQ%3D%3D'
        url = URL(src)
        self.assertEqual(src, url.tostring())
        self.assertEqual(src, url.href)
        self.assertEqual('null', url.origin)
        self.assertEqual('data:', url.protocol)
        self.assertEqual('', url.host)
        self.assertEqual('', url.hostname)
        self.assertEqual('', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('text/plain;base64,SGVsbG8sIFdvcmxkIQ%3D%3D',
                         url.pathname)
        self.assertEqual('', url.search)
        self.assertEqual('', url.hash)

    def test_url_search_params01(self):
        # See https://url.spec.whatwg.org/#example-searchparams-sort
        src = 'https://example.org/?q=🏳️‍🌈&key=e1f7bc78'
        expected = \
            "https://example.org" \
            "/?key=e1f7bc78&q=%F0%9F%8F%B3%EF%B8%8F%E2%80%8D%F0%9F%8C%88"
        url = URL(src)
        self.assertEqual(expected, url.tostring())
        self.assertEqual(expected, url.href)
        self.assertEqual('https://example.org', url.origin)
        self.assertEqual('https:', url.protocol)
        self.assertEqual('example.org', url.host)
        self.assertEqual('example.org', url.hostname)
        self.assertEqual('', url.port)
        self.assertEqual('', url.username)
        self.assertEqual('', url.password)
        self.assertEqual('/', url.pathname)
        self.assertEqual(
            '?key=e1f7bc78&q=%F0%9F%8F%B3%EF%B8%8F%E2%80%8D%F0%9F%8C%88',
            url.search)
        self.assertEqual('', url.hash)

        sp = url.search_params
        self.assertEqual(2, len(sp))
        self.assertEqual('e1f7bc78', sp['key'])
        self.assertEqual('🏳️‍🌈', sp['q'])

    def test_url_search_params02(self):
        sp = URLSearchParams()
        self.assertEqual('', sp.tostring())

        key = 'key'
        value = '730d67'
        sp = URLSearchParams({key: value})
        self.assertEqual(value, sp[key])
        self.assertEqual('key=730d67', sp.tostring())

        # value = '100%+20%'
        value = '100&#x0025;+20&#x0025;'
        sp[key] = value
        self.assertEqual(value, sp[key])
        self.assertEqual('key=100%26%23x0025%3B%2B20%26%23x0025%3B',
                         sp.tostring())

        url = URL('http://example.org')
        sp = url.search_params
        value = '100&#x0025;&20&#x0025;'
        sp[key] = value
        self.assertEqual(1, len(sp))
        self.assertEqual('100&#x0025;&20&#x0025;', sp['key'])
        self.assertEqual('?key=100%26%23x0025%3B%2620%26%23x0025%3B',
                         url.search)


if __name__ == '__main__':
    unittest.main()
