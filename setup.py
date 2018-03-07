#!/usr/bin/env python3

from setuptools import setup

setup(
    name='svgpy',
    version='0.1.1',
    author='Tetsuya Miura',
    author_email='miute.dev@gmail.com',
    description='SVG parser based on lxml',
    license='Apache License 2.0',
    keywords='svg parser',
    url='https://github.com/miute/svgpy',
    packages=['svgpy'],
    package_data={
    },
    python_requires='>=3.5',
    install_requires=[
        'cffi',
        'lxml',
        'numpy',
        'scipy',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
)
