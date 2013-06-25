# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

from octohub.utils import AttrDict
from octohub.exceptions import ResponseError, OctoHubError

def _get_content_type(response):
    """Parse response and return content-type"""
    try:
        content_type = response.headers['Content-Type']
        content_type = content_type.split(';', 1)[0]
    except KeyError:
        content_type = None

    return content_type

def parse_element(el):
    """Parse el recursively, replacing dicts with AttrDicts representation"""
    if type(el) == dict:
        el_dict = AttrDict()
        for key, val in el.items():
            el_dict[key] = parse_element(val)

        return el_dict

    elif type(el) == list:
        el_list = []
        for l in el:
            el_list.append(parse_element(l))

        return el_list

    else:
        return el

def parse_response(response):
    """Parse request response object and raise exception on response error code
        response (requests.Response object):

        returns: requests.Response object, including:
            response.parsed (AttrDict)
            http://docs.python-requests.org/en/latest/api/#requests.Response
    """
    response.parsed = AttrDict()
    content_type = _get_content_type(response)

    if content_type == 'application/json':
        response.parsed = parse_element(response.json())
    else:
        raise OctoHubError('unhandled content_type: %s' % content_type)

    if not response.status_code in (200, 201, 204):
        raise ResponseError(response.parsed)

    return response


