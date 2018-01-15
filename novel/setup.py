# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('README.rst') as f:
    README = f.read()

setup(
    name='novel',
    version='0.0.1',
    description='小说爬虫爬虫',
    long_description=README,
    author='Mervyn Zhang',
    author_email='zmy@foreverz.cn',
    padkages=find_packages(exclude=('tests', 'docs')))
