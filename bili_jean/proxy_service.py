"""
Service component as the proxy of Bilibili official APIs
"""
import json
from typing import Dict, Optional

from requests import Response, session

from .constants import FormatNumberValue
from .schemes import (
    GetPGCPlayResponse,
    GetPGCViewResponse,
    GetUGCPlayResponse,
    GetUGCViewResponse
)


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


URL_WEB_PGC_PLAY = 'https://api.bilibili.com/pgc/player/web/playurl'
URL_WEB_PGC_VIEW = 'https://api.bilibili.com/pgc/view/web/season'
URL_WEB_UGC_PLAY = 'https://api.bilibili.com/x/player/wbi/playurl'
URL_WEB_UGC_VIEW = 'https://api.bilibili.com/x/web-interface/view'


class ProxyService:

    @classmethod
    def _get(
        cls,
        url: str,
        params: Optional[Dict] = None,
        sess_data: Optional[str] = None
    ) -> Response:
        s = session()
        if sess_data is not None:
            s.cookies.set('SESSDATA', sess_data)
        return s.get(url, params=params, headers=HEADERS, timeout=TIMEOUT)

    @classmethod
    def get_ugc_view(
        cls,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        sess_data: Optional[str] = None
    ) -> GetUGCViewResponse:
        """
        get info of the UGC resource which is with '/video' namespace
        support fetching data by one of BV and AV ID
        BV ID has higher priority
        refer to https://www.bilibili.com/read/cv5167957/?spm_id_from=333.976.0.0)
        """
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

        response = cls._get_ugc_view_response(bvid, aid, sess_data)
        data = json.loads(response.content.decode('utf-8'))
        return GetUGCViewResponse.model_validate(data)

    @classmethod
    def _get_ugc_view_response(
        cls,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        sess_data: Optional[str] = None
    ) -> Response:
        params: Dict = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': aid})
        response: Response = cls._get(URL_WEB_UGC_VIEW, params=params, sess_data=sess_data)
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
        sess_data: Optional[str] = None
    ) -> GetUGCPlayResponse:
        """
        get UGC stream's info which is with '/video' namespace
        :param cid: Identifier of codec
        :type cid: int
        :param bvid: BV ID of video
        :type bvid: Optional[str]
        :param aid: AV ID of video
        :type aid: Optional[int]
        :param qn: Format quality number of streaming resource, refer to QualityNumber
        :type qn: Optional[int]
        :param fnval: integer type value of binary bitmap standing for multi-attribute combination
                      refer to FormatNumberValue
        :type fnval: int
        :param fourk: 4K or not
        :type fourk: int
        :param sess_data: cookie of Bilibili user, SESSDATA
        :type sess_data: str
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
            fourk,
            sess_data
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
        sess_data: Optional[str] = None
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

        response: Response = cls._get(URL_WEB_UGC_PLAY, params=params, sess_data=sess_data)
        return response

    @classmethod
    def get_pgc_view(
        cls,
        season_id: Optional[int] = None,
        ep_id: Optional[int] = None,
        sess_data: Optional[str] = None
    ) -> GetPGCViewResponse:
        """
        get info of the PGC resource which is with '/bangumi' namespace
        support fetching data by one of ssid (season_id) and epid (ep_id)
        season_id has higher priority
        """
        if all([id_val is None for id_val in (season_id, ep_id)]):
            raise ValueError("At least one of season_id and episode_id is necessary")

        response = cls._get_pgc_view_response(season_id, ep_id, sess_data)
        data = json.loads(response.content.decode('utf-8'))
        return GetPGCViewResponse.model_validate(data)

    @classmethod
    def _get_pgc_view_response(
        cls,
        season_id: Optional[int] = None,
        ep_id: Optional[int] = None,
        sess_data: Optional[str] = None
    ) -> Response:
        params: Dict = {}
        if season_id is not None:
            params.update({'season_id': season_id})
        else:
            params.update({'ep_id': ep_id})
        response: Response = cls._get(URL_WEB_PGC_VIEW, params=params, sess_data=sess_data)
        return response

    @classmethod
    def get_pgc_play(
        cls,
        cid: Optional[int] = None,
        ep_id: Optional[int] = None,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        qn: Optional[int] = None,
        fnval: int = FormatNumberValue.DASH.value,
        fourk: int = 1,
        sess_data: Optional[str] = None
    ) -> GetPGCPlayResponse:
        """
        get PGC stream's info which is with '/bangumi' namespace
        :param cid: Identifier of codec
        :type cid: Optional[int]
        :param ep_id: Identifier of episode
        :type ep_id: Optional[int]
        :param bvid: BV ID of video
        :type bvid: Optional[str]
        :param aid: AV ID of video
        :type aid: Optional[int]
        :param qn: Format quality number of streaming resource, refer to QualityNumber
        :type qn: Optional[int]
        :param fnval: integer type value of binary bitmap standing for multi-attribute combination
                      refer to FormatNumberValue
        :type fnval: int
        :param fourk: 4K or not
        :type fourk: int
        :param sess_data: cookie of Bilibili user, SESSDATA
        :type sess_data: str
        :return: GetPGCPlayResponse
        """
        if all([id_val is None for id_val in (cid, ep_id)]):
            raise ValueError("At least one of cid and ep_id is necessary")

        response = cls._get_pgc_play_response(
            cid,
            ep_id,
            bvid,
            aid,
            qn,
            fnval,
            fourk,
            sess_data
        )
        data = json.loads(response.content.decode('utf-8'))
        return GetPGCPlayResponse.model_validate(data)

    @classmethod
    def _get_pgc_play_response(
        cls,
        cid: Optional[int] = None,
        ep_id: Optional[int] = None,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        qn: Optional[int] = None,
        fnval: int = FormatNumberValue.DASH.value,
        fourk: int = 1,
        sess_data: Optional[str] = None
    ) -> Response:
        params: Dict = {}

        if cid is not None:
            params.update({'cid': cid})
        else:
            params.update({'ep_id': ep_id})

        if bvid is not None:
            params.update({'bvid': bvid})
        if aid is not None:
            params.update({'aid': aid})
        if qn is not None:
            params.update({'qn': qn})

        params.update({
            'fnval': fnval,
            'fourk': fourk
        })

        response: Response = cls._get(URL_WEB_PGC_PLAY, params=params, sess_data=sess_data)
        return response
