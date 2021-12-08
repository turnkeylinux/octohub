OctoHub: Low level Python and CLI interface to GitHub
=====================================================

OctoHub is a Python package that provides a low level interface to the
full GitHub REST API:

* `Activity`_
* `Gists`_
* `Git Data`_
* `Issues`_
* `Orgs`_
* `Pull Requests`_
* `Repositories`_
* `Users`_
* `Search`_

OctoHub was developed out of a need to have a one-to-one interface to
the GitHub API based on the excellent `online documentation`_, with the
least amount of abstraction.

OctoHub does do its part by parsing raw json responses into Pythonic
attribute dictionaries, as well providing an optional iterative Pager
for handling pagination.

Also included is a command line interface for quick interaction with
GitHub's API.

Speaking of development, it's really easy to leverage the base code to
develop higher level tools, see `contrib`_ for some examples. We also
love pull requests, see our `gitflow`_ for guidelines and walk through.

Installation
------------

On TurnKey Linux (v17+)::

    # as root
    apt update
    apt install octohub

On Debian (11/Buster+)::

    # check http://archive.turnkeylinux.org/debian/pool/bullseye/main/o/octohub/ for latest version
    $ wget http://archive.turnkeylinux.org/debian/pool/bullseye/main/o/octohub/octohub_#VERSION#_amd64.deb
    $ sudo apt install ./octohub_#VERSION#_amd64.deb

::

    $ git clone https://github.com/turnkeylinux/octohub.git
    $ cd octohub
    $ sudo python3 setup.py install

Dependencies
''''''''''''

* `python-requests`_

GitHub Token
------------

OctoHub can be used anonymously, but is much more useful when authenticated.
You can create a revokable access token under `Personal access tokens`_ in your
`Account settings`_.

Usage examples (API)
--------------------

::

    >>> from octohub.connection import Connection
    >>> conn = Connection(token)
    >>> uri = '/repos/turnkeylinux/tracker/issues'

    >>> response = conn.send('GET', uri, params={'labels': 'bug'})
    >>> for issue in response.parsed:
    ...:    print(issue.title)

    >>> from octohub.connection import Pager
    >>> pager = Pager(conn, uri, params={'labels': 'bug'})
    >>> for issues in pager:
    ...:    for issue in issues:
    ...:        print(issue.title)

Usage examples (CLI)
--------------------

::

    # A Personal Access Token from your GitHub account:
    #   Account Settings > Developer settings > Personal access tokens > Generate new token

    $ export OCTOHUB_TOKEN=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
    $ export OCTOHUB_LOGLEVEL=INFO
    $ octohub GET /repos/turnkeylinux/tracker/issues labels=feature,core per_page=100

    INFO [response]: status: 200 OK
    INFO [response]: x-ratelimit-limit: 5000
    INFO [response]: x-ratelimit-remaining: 4997
    [
     {
      "body": "...
      "title": "...
      ...
    
    
    $ cat repo.json
    {
      "name": "test",
      "description": "My test project",
      "homepage": "http://www.turnkeylinux.org",
    }
    $ octohub POST /user/repos --input=repo.json

    INFO [response]: status: 201 Created
    INFO [response]: x-ratelimit-limit: 5000
    INFO [response]: x-ratelimit-remaining: 4996
    ...

For more example usage::

    $ octohub --help


.. _Activity: https://docs.github.com/en/rest/reference/activity
.. _Gists: https://docs.github.com/en/rest/reference/gists
.. _Git Data: https://docs.github.com/en/rest/reference/git
.. _Issues: https://docs.github.com/en/rest/reference/issues
.. _Orgs: https://docs.github.com/en/rest/reference/orgs
.. _Pull Requests: https://docs.github.com/en/rest/reference/pulls
.. _Repositories: https://docs.github.com/en/rest/reference/repos
.. _Users: https://docs.github.com/en/rest/reference/users
.. _Search: https://docs.github.com/en/rest/reference/search
.. _online documentation: https://docs.github.com/en/rest
.. _contrib: https://github.com/turnkeylinux/octohub/tree/master/contrib/
.. _gitflow: https://github.com/turnkeylinux/tracker/blob/master/GITFLOW.rst
.. _python-requests: https://docs.python-requests.org/en/latest/
.. _Account settings: https://github.com/settings
.. _Personal access token: https://github.com/settings/tokens
