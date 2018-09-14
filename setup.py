#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import sys
from shutil import rmtree
from setuptools import find_packages, setup, Command

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="k911pythonalertsserver_pkg",
    version="0.0.1",
    author="Nyiema Bayfield",
    author_email="ntmbayfield@gmail.com",
    description="A python server for k911 app package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ntmbayfield/python-api.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
