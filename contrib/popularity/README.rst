OctoHub Contrib: List repositories based on popularity
======================================================

Quick and easy way to list repositories of a user or organization and
sort the output based on either watchers (star) or forks.

Usage
-----

::

    Syntax: list.py [-options] owner
    OctoHub: List repositories based on popularity for a given owner

    Arguments:
        owner                       Owner := github organization or username

    Options:
        -s --sort=<value>           Value := forks, watchers (default)
        -n --noauth                 Perform actions as an anonymous user

    Environment:
        OCTOHUB_TOKEN               GitHub personal access token
        OCTOHUB_LOGLEVEL            Log level debugging sent to stderr


