"""
Service component as the proxy of Bilibili official APIs
"""
import json
from typing import Dict, Optional

from requests import Response, session

from .schemes import GetUGCPlayResponse, GetUGCViewResponse


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


URL_WEB_UGC_PLAY = 'https://api.bilibili.com/x/player/wbi/playurl'
URL_WEB_UGC_VIEW = 'https://api.bilibili.com/x/web-interface/view'


class ProxyService:

    @classmethod
    def _get(cls, url: str, params: Optional[Dict] = None) -> Response:
        s = session()
        return s.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)

    @classmethod
    def get_ugc_view(cls, bvid: Optional[str] = None, aid: Optional[int] = None) -> GetUGCViewResponse:
        """
        get info of the UGC resource which is with '/video' namespace
        support fetching data by one of BV and AV ID
        BV ID has higher priority
        refer to https://www.bilibili.com/read/cv5167957/?spm_id_from=333.976.0.0)
        """
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

        response = cls._get_ugc_view_response(bvid, aid)
        data = json.loads(response.content.decode('utf-8'))
        return GetUGCViewResponse.model_validate(data)

    @classmethod
    def _get_ugc_view_response(cls, bvid: Optional[str] = None, aid: Optional[int] = None) -> Response:
        params: Dict = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': aid})
        response: Response = cls._get(URL_WEB_UGC_VIEW, params=params)
        return response

    @classmethod
    def get_ugc_play(
        cls,
        cid: int,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        qn: Optional[int] = None,
        fnval: int = 16,
        fourk: int = 1,
    ) -> GetUGCPlayResponse:
        """
        get UGC stream's info which is with '/video' namespace
        :param cid: Identifier of codec
        :type cid: int
        :param bvid: BV ID of video
        :type bvid: Optional[str]
        :param aid: AV ID of video
        :type bvid: Optional[int]
        :param qn: video's quality, which is noneffective for DASH format
                   | 6    | 240P    |                                                  |
                   | 16   | 360P    |                                                  |
                   | 32   | 480P    |                                                  |
                   | 64   | 720P    |                                                  |
                   | 74   | 720P60  |                                                  |
                   | 80   | 1080P   | login needed                                     |
                   | 112  | 1080P+  | VIP needed                                       |
                   | 116  | 1080P60 | VIP needed                                       |
                   | 120  | 4K      | VIP needed, `fnval&128=128` and `fourk=1`        |
                   | 125  | HDR     | VIP needed, only support DASH, `fnval&64=64`     |
                   | 126  | Dolby   | VIP needed, only support DASH, `fnval&512=512`   |
                   | 127  | 8K      | VIP needed, only support DASH, `fnval&1024=1024` |
        :type qn: Optional[int]
        :param fnval: binary which stands for attributions
                      | 1    | MP4                 | exclusive with DASH                                 |
                      | 16   | DASH                | exclusive with MP4                                  |
                      | 64   | HDR or not          | DASH is necessary, VIP needed, only H.265, `qn=125` |
                      | 128  | 4K or not           | VIP needed, `fourk=1` and `qn=120`                  |
                      | 256  | Dolby sound or not  | DASH is necessary, VIP needed                       |
                      | 512  | Dolby vision or not | DASH is necessary, VIP needed                       |
                      | 1024 | 8K or not           | DASH is necessary, VIP needed, `qn=127`             |
                      | 2048 | AV1 codec or not    | DASH is necessary                                   |
                      support 'or' for combination,
                      e.g. DASH format, and HDR, fnval = 16 | 64 = 80
        :type fnval: int
        :param fourk: 4K or not
        :type fourk: int
        :return: GetUGCPlayResponse
        """
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

        response = cls._get_ugc_play_response(
            cid,
            bvid,
            aid,
            qn,
            fnval,
            fourk
        )
        data = json.loads(response.content.decode('utf-8'))
        return GetUGCPlayResponse.model_validate(data)

    @classmethod
    def _get_ugc_play_response(
        cls,
        cid: int,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        qn: Optional[int] = None,
        fnval: int = 16,
        fourk: int = 1,
    ) -> Response:
        params: Dict = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'avid': aid})
        params.update({'cid': cid})

        if qn is not None:
            params.update({'qn': qn})

        params.update({
            'fnval': fnval,
            'fourk': fourk
        })

        response: Response = cls._get(
            URL_WEB_UGC_PLAY,
            params=params
        )
        return response
