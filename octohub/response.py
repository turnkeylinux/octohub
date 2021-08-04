# Copyright (c) 2013 Alon Swartz <alon@turnkeylinux.org>
#
# This file is part of OctoHub.
#
# OctoHub is free software; you can redistribute it and/or modify it under the
# terms of the GNU General Public License as published by the Free Software
# Foundation; either version 3 of the License, or (at your option) any later
# version.

from typing import Optional, cast
import re

from octohub.utils import AttrDict, OctoResponse, get_logger
from octohub.exceptions import ResponseError, OctoHubError

import requests

log = get_logger('response')


def _get_content_type(response: requests.Response) -> Optional[str]:
    """Parse response and return content-type"""
    try:
        content_type = response.headers['Content-Type']
        return content_type.split(';', 1)[0]
    except KeyError:
        return None


def _parse_link(header_link: str) -> AttrDict:
    """Parse header link and return AttrDict[rel].uri|params"""
    links = AttrDict()
    for s in header_link.split(','):
        link = AttrDict()

        m = re.match(r'<(.*)\?(.*)>', s.split(';')[0].strip())
        if m is None:
            raise OctoHubError("failed to match link uri")
        link.uri = m.groups()[0]
        link.params = {}
        for kv in m.groups()[1].split('&'):
            key, value = kv.split('=')
            link.params[key] = value

        m = re.match('rel="(.*)"', s.split(';')[1].strip())
        if m is None:
            raise OctoHubError("failed to match link rel")
        rel = m.groups()[0]

        links[rel] = link
        log.debug('link-%s-page: %s' % (rel, link.params['page']))

    return links


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


def parse_response(response: requests.Response) -> OctoResponse:
    """Parse request response object and raise exception on response error code
        response (requests.Response object):

        returns: requests.Response object, including:
            response.parsed (AttrDict)
            response.parsed_link (AttrDict)
            http://docs.python-requests.org/en/latest/api/#requests.Response
    """
    # I would prefer to change this return type to some new composed type which
    # embeds the requests.Request type. But to avoid breaking changes this
    # should provide the correct typing information to mypy.
    response = cast(OctoResponse, response)
    response.parsed = AttrDict()
    response.parsed_link = AttrDict()

    if 'link' in response.headers.keys():
        response.parsed_link = _parse_link(response.headers['link'])

    headers = ['status', 'x-ratelimit-limit', 'x-ratelimit-remaining']
    for header in headers:
        if header in response.headers.keys():
            log.info('%s: %s' % (header, response.headers[header]))

    content_type = _get_content_type(response)

    if content_type == 'application/json':
        json = response.json
        if callable(json):
            json = json()
        response.parsed = parse_element(json)
    else:
        if not response.status_code == 204:
            raise OctoHubError('unhandled content_type: %s' % content_type)

    if response.status_code not in (200, 201, 204):
        raise ResponseError(response.parsed)

    return response
