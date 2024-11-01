"""
Service component as the proxy of Bilibili official APIs
"""
from typing import Dict, Optional

from requests import Response, session


__all__ = ['ProxyService']


HEADERS = {
    'origin': 'https://www.bilibili.com',
    'referer': 'https://www.bilibili.com/',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'accept': 'application/json, text/plain, */*',
    'Sec-Ch-Ua': '"Chromium";v="124", "Google Chrome";v="124", "Not-A.Brand";v="99"',
    'Sec-Ch-Ua-Mobile': '?0',
    'Sec-Ch-Ua-Platform': '"macOS"',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site'
}
TIMEOUT = 5


URL_WEB_VIEW = 'https://api.bilibili.com/x/web-interface/view'


class ProxyService:

    @classmethod
    def _get(cls, url: str, params: Optional[Dict] = None) -> Response:
        s = session()
        return s.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)

    @classmethod
    def _get_view_response(cls, bvid: Optional[str] = None, aid: Optional[int] = None) -> Response:
        params: Dict = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': aid})
        response: Response = cls._get(URL_WEB_VIEW, params=params)
        return response
