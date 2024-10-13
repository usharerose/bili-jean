"""
Components on Bilibili videos manipulations
"""
from typing import List, Optional, TypedDict, Union
from urllib.parse import urlencode, urlparse, urlunparse

from .models import (
    GetVideoInfoDataOwner,
    GetVideoInfoDataStaffItem,
    GetVideoInfoResponse,
    Work,
    WorkPagesItem,
    WorkStaffItem
)
from .proxy_service import ProxyService
from .utils import parse_aid, parse_bvid


VIDEO_URL_PATTERN = 'https://www.bilibili.com/video/{video_id}'
DEFAULT_STAFF_TITLE = 'UP主'


class WorkService:

    @classmethod
    def get_work_meta(cls, url: str) -> Optional[Work]:
        video_info = cls._get_work_info_by_url(url)

        if video_info.code == 0:
            data = video_info.data
            assert data is not None
            return Work(
                url=VIDEO_URL_PATTERN.format(video_id=data.bvid),
                title=data.title,
                description=data.desc,
                cover_url=data.pic,
                staff=cls._parse_work_staff(video_info),
                pages=cls._parse_work_pages(video_info)
            )
        return None

    @classmethod
    def _get_work_info_by_url(cls, url: str) -> GetVideoInfoResponse:
        class GetVideoInfoParamsType(TypedDict):
            aid: Optional[int]
            bvid: Optional[str]

        params: GetVideoInfoParamsType = {
            'aid': None,
            'bvid': None
        }
        try:
            bvid = parse_bvid(url)
            params.update({'bvid': bvid})
        except ValueError:
            try:
                aid = parse_aid(url)
                params.update({'aid': aid})
            except ValueError:
                pass

        return ProxyService.get_video_info(**params)

    @classmethod
    def _parse_work_staff(cls, dm: GetVideoInfoResponse) -> List[WorkStaffItem]:
        assert dm.data is not None
        work_staff: List[Union[GetVideoInfoDataStaffItem, GetVideoInfoDataOwner]] = [dm.data.owner]
        if dm.data.staff is not None:
            work_staff = [item for item in dm.data.staff]
        return [
            WorkStaffItem(
                account_id=item.mid,
                name=item.name,
                title=item.title if hasattr(item, 'title') else DEFAULT_STAFF_TITLE,
                avatar_url=item.face
            ) for item in work_staff
        ]

    @classmethod
    def _parse_work_pages(cls, dm: GetVideoInfoResponse) -> List[WorkPagesItem]:
        assert dm.data is not None
        work_pages = dm.data.pages

        base_url = VIDEO_URL_PATTERN.format(video_id=dm.data.bvid)
        url_parts = urlparse(base_url)

        return [
            WorkPagesItem(
                url=urlunparse((
                    url_parts.scheme,
                    url_parts.netloc,
                    url_parts.path,
                    url_parts.params,
                    urlencode({'p': item.page}, doseq=True),
                    url_parts.fragment
                )),
                aid=dm.data.aid,
                bvid=dm.data.bvid,
                cid=item.cid,
                title=item.part,
                duration=item.duration
            ) for item in work_pages
        ]
