#!/usr/bin/python3
# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of octohub/contrib
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

"""
Parse local Github issues and generate directory listing

Arguments:
    issues.json             Path to json encoded issues
    outdir                  Path to create directory listing

Options:
    --noinit                Don't initialize directory listing (use with care)

Generated directory listing:
    all/:issue.number
    state/:issue.state/:issue.title|slug       -> ../../all/:issue.number
    labels/:issue.label/:issue.title|slug      -> ../../all/:issue.number
    assignee/:assignee.login/:issue.title|slug -> ../../all/:issue.number
"""

import re
import os
import sys
import getopt
import shutil
import unicodedata

import json

from octohub.response import parse_element


def fatal(e):
    print('Error: ' + str(e), file=sys.stderr)
    sys.exit(1)


def usage(e=None):
    if e:
        print('Error:', e, file=sys.stderr)

    print('Syntax: %s [-options] issues.json outdir' % sys.argv[0],
          file=sys.stderr)
    print(__doc__.strip(), file=sys.stderr)

    sys.exit(1)


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def symlink(target, link_name):
    if not os.path.exists(link_name):
        mkdir(os.path.dirname(link_name))
        os.symlink(target, link_name)


def slugify(value):
    """Normalizes string, converts to lowercase, removes non-alpha characters,
    and converts spaces to hyphens.
    """
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore')
    value = re.sub(rb'[^\w\s-]', b'', value).strip().lower()
    return re.sub(rb'[-\s]+', b'-', value).decode()


def output_issues(issues, outdir):
    """Parse issues and output directory listing"""
    for issue in issues:
        slug = slugify(issue.title)

        path = os.path.join(outdir, 'all', str(issue.number))
        path_symlink = '../../all/%s' % str(issue.number)
        mkdir(os.path.dirname(path))
        with open(path, 'w') as fob:
            json.dump(issue, fob, indent=1)
        path = os.path.join(outdir, 'state', issue.state, slug)
        symlink(path_symlink, path)

        for label in issue.labels:
            path = os.path.join(outdir, 'labels', label.name, slug)
            symlink(path_symlink, path)

        if issue.assignee:
            path = os.path.join(outdir, 'assignee', issue.assignee.login, slug)
            symlink(path_symlink, path)


def main():
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'h', ['help', 'noinit'])
    except getopt.GetoptError as e:
        usage(e)

    init = True
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        if opt == '--noinit':
            init = False

    if len(args) == 0:
        usage()

    if len(args) != 2:
        usage('incorrect number of arguments')

    infile = args[0]
    outdir = args[1]

    if not os.path.exists(infile):
        fatal('path does not exist: %s' % infile)

    if init:
        for dir in ('state', 'labels', 'assignee'):
            path = os.path.join(outdir, dir)
            if os.path.exists(path):
                shutil.rmtree(path)

    with open(infile, 'r') as fob:
        issues_dict = json.loads(fob)
    issues_parsed = parse_element(issues_dict)
    output_issues(issues_parsed, outdir)


if __name__ == "__main__":
    main()
