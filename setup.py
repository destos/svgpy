#!/usr/bin/env python3


import os

from setuptools import find_packages, setup

NAME = 'svgpy'
AUTHOR = 'Tetsuya Miura'
AUTHOR_EMAIL = 'miute.dev@gmail.com'
DESCRIPTION = 'SVG parser based on lxml'
LICENSE = 'Apache License 2.0'
KEYWORDS = 'svg parser'
URL = 'https://github.com/miute/svgpy'
PACKAGES = find_packages()
PACKAGE_DATA = {}
PYTHON_REQUIRES = '>=3.6'
INSTALL_REQUIRES = [
    'cffi>=1.11',
    'cssselect',
    'lxml',
    'numpy',
    'scipy',
    'tinycss2',
]

here = os.path.abspath(os.path.dirname(__file__))

about = {}
with open(os.path.join(here, NAME, '__version__.py')) as f:
    exec(f.read(), about)

setup(
    name=NAME,
    version=about['__version__'],
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    description=DESCRIPTION,
    license=LICENSE,
    keywords=KEYWORDS,
    url=URL,
    packages=PACKAGES,
    package_data=PACKAGE_DATA,
    python_requires=PYTHON_REQUIRES,
    install_requires=INSTALL_REQUIRES,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
