#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

version = '0.1.2'


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

with open('README.txt', 'rb') as f:
    readme = f.read().decode('utf-8')

setup(
    name="sun_oss",
    version=version,
    packages=['sun_oss'],

    author="pinkong",
    author_email="alain.swun@gmail.com",
    description="A Simple OSS SDK Integration. Include Aliyun, Qiniu, Qcloud, Maybe more",
    long_description=readme,

    install_requires=['qiniu==7.2.0',
                      'oss2==2.4.0',
                      'cos-python-sdk-v5==1.4.0'],
    include_package_data=True,

    license="PSF",
    keywords="OSS Integration Aliyun Qiniu Qcloud",
    url="https://github.com/PINKONG/sun-oss-python",
)