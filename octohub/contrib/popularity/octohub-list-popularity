#!/usr/bin/env python
# Copyright (c) 2016 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of octohub/contrib.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

"""
OctoHub: List repositories based on popularity for a given owner

Arguments:
    owner                       Owner := github organization or username

Options:
    -s --sort=<value>           Value := forks, watchers (default)
    -n --noauth                 Perform actions as an anonymous user

Environment:
    OCTOHUB_TOKEN               GitHub personal access token
    OCTOHUB_LOGLEVEL            Log level debugging sent to stderr

"""

import os
import sys
import getopt

from octohub.connection import Connection, Pager
from octohub.exceptions import ResponseError

def fatal(e):
    print('Error: ' + str(e), file=sys.stderr)
    sys.exit(1)

def usage(e=None):
    if e:
        print('Error: ' + str(e), file=sys.stderr)

    cmd = os.path.basename(sys.argv[0])
    print('Syntax: %s [-options] owner' % cmd, file=sys.stderr)
    print(__doc__.lstrip(), file=sys.stderr)

    sys.exit(1)

def get_repos(conn, uri):
    repos = []
    pager = Pager(conn, uri, params={}, max_pages=0)
    for response in pager:
        for repo in response.parsed:
            repos.append(repo)

    return repos

def main():
    try:
        l_opts = ['help', 'noauth', 'sort=']
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'hns:', l_opts)
    except getopt.GetoptError as e:
        usage(e)

    auth = True
    sort_by = 'watchers'
    for opt, val in opts:
        if opt in ('-h', '--help'):
            usage()

        elif opt in ('-n', '--noauth'):
            auth = False

        elif opt in ('-s', '--sort'):
            sort_by = val

    if not len(args) == 1:
        usage()

    owner = args[0]

    token = os.environ.get('OCTOHUB_TOKEN', None)
    if not token and auth:
        fatal('OCTOHUB_TOKEN is required, override with --noauth')

    if not auth:
        token = None

    if not sort_by in ('watchers', 'forks'):
        fatal('sort value not supported: %s' % sort_by)

    conn = Connection(token)

    try:
        repos = get_repos(conn, '/orgs/%s/repos' % owner)
    except ResponseError as e:
        repos = get_repos(conn, '/users/%s/repos' % owner)


    print("# repo                         watchers forks")
    for repo in sorted(repos, key=lambda repo: repo[sort_by], reverse=True):
        print("%-30s %-8d %d" % (
            repo["name"], repo["watchers"], repo["forks"]))


if __name__ == '__main__':
   main()
