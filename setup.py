#!/usr/bin/env python
import octohub
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='octohub',
    version=octohub.__version__,
    install_requires=['simplejson', 'requests'],
    description='Low level Python and CLI interface to GitHub',
    long_description=open('README.rst').read(),
    author='Alon Swartz',
    author_email='alon@turnkeylinux.org',
    url='https://github.com/turnkeylinux/octohub',
    packages=[
        'octohub',
    ],
    entry_points={'console_scripts': ['octohub = octohub.cmd:main']}
)
