# -*- coding: utf-8 -*-
#
# This file is part of the calvin-hobbes-get project
#
# Copyright (c) 2017 Tiago Coutinho
# Distributed under the MIT license. See LICENSE for more info.

import os
import sys
from setuptools import setup

requirements = [
    'grequests',
    'bs4',
]

setup(
    name='calvin-hobbes-get',
    version='0.0.1',
    description="downloader of calvin and hobbes comics",
    author="Tiago Coutinho",
    author_email='coutinhotiago@gmail.com',
    url='https://github.com/tiagocoutinho/calvin-hobbes',
    py_modules=['calvinhobbes_get'],
    entry_points={
        'console_scripts': [
            'calvin-hobbes-get=calvinhobbes_get:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='calvin, hobbes',
    classifiers=[
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
