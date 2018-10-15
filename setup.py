#!/usr/bin/env python3
# Copyright (c) 2018 Kevin Weiss, for HAW Hamburg  <kevin.weiss@haw-hamburg.de>
#
# This file is subject to the terms and conditions of the MIT License. See the
# file LICENSE in the top level directory for more details.
# SPDX-License-Identifier:    MIT
"""
    Setup file for bph_api.
"""
from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()


setup(
    name="bph_api",
    version="0.0.1",
    author="Kevin Weiss",
    author_email="kevin.weiss@haw-hamburg.de",
    license="MIT",
    description="API interface to Raspberry Pi Bluepill Hat (BPH)",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/riot-appstore/BPH",
    packages=find_packages(),
    platforms='any',
    python_requires='>=3.4.*',
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Linux",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers"
    ],
    setup_requires=["pytest-runner"],
    tests_require=["pytest", "pytest-regtest", "pprint"],
    install_requires=['wiringpi'],
    scripts=['bph_api']
)
