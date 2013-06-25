# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

import requests

from octohub import __useragent__
from octohub.response import parse_response

class Connection(object):
    def __init__(self, token=None):
        """OctoHub connection
            token (str): GitHub Token (anonymous if not provided)
        """
        self.endpoint = 'https://api.github.com'
        self.headers = {'User-Agent': __useragent__}

        if token:
            self.headers['Authorization'] = 'token %s' % token

    def send(self, method, uri, params={}, data=None):
        """Prepare and send request
            method (str): Request HTTP method (e.g., GET, POST, DELETE, ...)
            uri (str): Request URI (e.g., /user/issues)
            params (dict): Parameters to include in request
            data (str | file type object): data to include in request

            returns: requests.Response object, including:
                response.parsed (AttrDict): parsed response when applicable
                http://docs.python-requests.org/en/latest/api/#requests.Response
        """
        url = self.endpoint + uri
        kwargs = {'headers': self.headers, 'params': params, 'data': data}
        response = requests.request(method, url, **kwargs)

        return parse_response(response)

