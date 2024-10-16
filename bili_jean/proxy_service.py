"""
Bilibili official API proxy
"""
import json
from typing import Dict, Optional

import requests
from requests import Response

from .models import (
    GetUserInfoResponse,
    GetVideoInfoResponse,
    GetVideoStreamResponse
)


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
SRC_VIDEO_STREAM_URL = 'https://api.bilibili.com/x/player/wbi/playurl'
USER_INFO_URL = 'https://api.bilibili.com/x/space/myinfo'


class ProxyService:

    @classmethod
    def _get(
        cls,
        url: str,
        params: Optional[Dict] = None,
        session_data: Optional[str] = None
    ) -> Response:
        session = requests.session()
        if session_data:
            session.cookies.set('SESSDATA', session_data)
        return session.get(
            url,
            params=params,
            headers=HEADERS,
            timeout=TIMEOUT
        )

    @classmethod
    def _get_video_info_response(
        cls,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        session_data: Optional[str] = None
    ) -> Response:
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

        params: Dict = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': aid})
        response: Response = cls._get(
            SRC_VIDEO_INFO_URL,
            params=params,
            session_data=session_data
        )
        return response

    @classmethod
    def get_video_info(
        cls,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        session_data: Optional[str] = None
    ) -> GetVideoInfoResponse:
        """
        get video info which is with /video/ namespace
        support fetching by BV or AV ID
        (reference: https://www.bilibili.com/read/cv5167957/?spm_id_from=333.976.0.0)
        """
        response = cls._get_video_info_response(bvid, aid, session_data)
        data = json.loads(response.content.decode('utf-8'))
        return GetVideoInfoResponse.model_validate(data)

    @classmethod
    def _get_video_stream_response(
        cls,
        cid: int,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        qn: Optional[int] = None,
        fnval: int = 16,
        fourk: int = 1,
        session_data: Optional[str] = None
    ) -> Response:
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

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
            SRC_VIDEO_STREAM_URL,
            params=params,
            session_data=session_data
        )
        return response

    @classmethod
    def get_video_stream(
        cls,
        cid: int,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        qn: Optional[int] = None,
        fnval: int = 1,
        fourk: int = 1,
        session_data: Optional[str] = None
    ) -> GetVideoStreamResponse:
        """
        get video stream's info which is with /video/ namespace
        :param cid: Identifier of codec
        :type cid: int
        :param bvid: BV ID of video
        :type bvid: Optional[str]
        :param aid: AV ID of video
        :type bvid: Optional[int]
        :param qn: Video stream's quality number, refer to VideoWorkQualityNumber
        :type qn: Optional[int]
        :param fnval: integer value of binary bitmap which stands for attributions
                      refer to VideoWorkFormatNumberValue
        :type fnval: int
        :param fourk: 4K or not
        :type fourk: int
        :param session_data: cookie of Bilibili user, SESSDATA
        :type session_data: str
        :return: GetVideoStreamResponse
        """
        response = cls._get_video_stream_response(
            cid,
            bvid,
            aid,
            qn,
            fnval,
            fourk,
            session_data
        )
        data = json.loads(response.content.decode('utf-8'))
        return GetVideoStreamResponse.model_validate(data)

    @classmethod
    def _get_user_info_response(
        cls,
        session_data: Optional[str] = None
    ) -> Response:
        response: Response = cls._get(
            USER_INFO_URL,
            session_data=session_data
        )
        return response

    @classmethod
    def get_user_info(
        cls,
        session_data: Optional[str] = None
    ) -> GetUserInfoResponse:
        """
        get login user info
        :param session_data: cookie of Bilibili user, SESSDATA
        :type session_data: str
        :return: GetUserInfoResponse
        """
        response = cls._get_user_info_response(session_data)
        data = json.loads(response.content.decode('utf-8'))
        return GetUserInfoResponse.model_validate(data)
