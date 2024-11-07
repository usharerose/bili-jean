"""
Utilities for test case
"""
from typing import cast, Optional

from requests import Response
from requests.structures import CaseInsensitiveDict


__all__ = ['get_mocked_response']


class MockResponse(object):

    def __init__(self, status_code: int, content: bytes, headers: Optional[CaseInsensitiveDict] = None):
        self._status_code = status_code
        self._content = content
        self._headers = headers

    @property
    def status_code(self):
        return self._status_code

    @property
    def content(self):
        return self._content

    @property
    def headers(self):
        return self._headers


def get_mocked_response(
    status_code: int,
    content: bytes,
    headers: Optional[CaseInsensitiveDict] = None
) -> Response:
    mock_resp = cast(Response, MockResponse(status_code, content, headers))
    return mock_resp
