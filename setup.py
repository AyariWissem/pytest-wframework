#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest_wframework',
    version='0.1.0',
    author='Ayari Wissem',
    author_email='ayariWissem96@gmail.com',
    maintainer='Ayari Wissem',
    maintainer_email='ayariWissem96@gmail.com',
    license='MIT',
    url='https://github.com/AyariWissem/pytest-wframework',
    description='WFrame is a custom framework that contains an beautiful API that can be used with the testing framework PyTest easily to automate Desktop and Mobile devices and generate both html and excel reports.',
    long_description=read('README.rst'),
    packages=['pytest_wframework'],
    python_requires='>=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*',
    install_requires=['pytest>=5.0.0','selenium>=3.14.0','Appium-Python-Client>=1.0.0','openpyxl>=3.0.0','pytest-json-report>=1.2.0','allure-pytest>=2.8.16'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
    entry_points={
        'pytest11': [
            'wframework = pytest_wframework.plugin',
        ],
    },
)
