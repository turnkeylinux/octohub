#!/usr/bin/env python
import octohub
import setuptools

setuptools.setup(
    name='octohub',
    version=octohub.__version__,
    description='Low level Python and CLI interface to GitHub',
    long_description=open('README.rst').read(),
    author='Alon Swartz',
    author_email='alon@turnkeylinux.org',
    url='https://github.com/turnkeylinux/octohub',
    license='GPLv3+',
    install_requires=[
        'requests'
    ],
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
    ],
    packages=[
        'octohub',
    ],
    entry_points={
        'console_scripts': [
            'octohub=octohub.__main__:main',
        ],
    },
    scripts=[
        'octohub/contrib/gist/octohub-gist',
        'octohub/contrib/offline-issues/octohub-parse-issues',
        'octohub/contrib/offline-issues/octohub-update-issues',
        'octohub/contrib/popularity/octohub-list-popularity',
        'octohub/contrib/pull-requests/octohub-list-pullrequests',
    ],
)
