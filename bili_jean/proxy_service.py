"""
Service component as the proxy of Bilibili official APIs
"""
import json
from typing import Dict, Optional

from requests import Response, session

from .constants import FormatNumberValue
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
        fnval: int = FormatNumberValue.DASH.value,
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
        :param qn: Format quality number of streaming resource, refer to QualityNumber
        :type qn: Optional[int]
        :param fnval: integer type value of binary bitmap standing for multi-attribute combination
                      refer to FormatNumberValue
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
        fnval: int = FormatNumberValue.DASH.value,
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
