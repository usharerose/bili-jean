"""
Bilibili official API proxy
"""
import json
from typing import Dict, Optional

import requests
from requests import Response

from .models import GetVideoInfoResponse


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

SRC_VIDEO_INFO_URL = 'https://api.bilibili.com/x/web-interface/view'


class ProxyService:

    @classmethod
    def _get_video_info_response(cls, bvid: Optional[str] = None, aid: Optional[int] = None) -> Response:
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

        params: Dict = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': aid})
        response: Response = requests.get(
            SRC_VIDEO_INFO_URL,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT,
        )
        return response

    @classmethod
    def get_video_info(cls, bvid: Optional[str] = None, aid: Optional[int] = None) -> GetVideoInfoResponse:
        """
        get video info which is with /video/ namespace
        support fetching by BV or AV ID
        (reference: https://www.bilibili.com/read/cv5167957/?spm_id_from=333.976.0.0)
        """
        response = cls._get_video_info_response(bvid, aid)
        data = json.loads(response.content.decode('utf-8'))
        return GetVideoInfoResponse.model_validate(data)
