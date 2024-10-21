"""
Components on Bilibili videos manipulations
"""
from typing import Dict, Iterator, List, Optional, Tuple, TypedDict, Union
from urllib.parse import urlencode, urlparse, urlunparse

from .models import (
    GetVideoInfoDataOwner,
    GetVideoInfoDataStaffItem,
    GetVideoInfoResponse,
    WorkPage,
    WorkPagesItem,
    WorkOwner,
    WorkStaffItem
)
from .proxy_service import ProxyService
from .utils import parse_aid, parse_bvid


VIDEO_URL_PATTERN = 'https://www.bilibili.com/video/{video_id}'
DEFAULT_STAFF_TITLE = 'UP主'


class WorkService:

    @classmethod
    def get_work_meta(cls, url: str, return_season: bool = False) -> Optional[List[WorkPage]]:
        video_info = cls._get_work_info_by_url(url)
        if video_info.code != 0:
            return None

        season_owner_name, season_owner_avatar_url = None, None
        assert video_info.data is not None
        if video_info.data.is_season_display:
            assert video_info.data.ugc_season is not None
            season_owner_id = video_info.data.ugc_season.mid
            season_owner_name, season_owner_avatar_url = cls._get_user_name_and_avatar_url(season_owner_id)

        if return_season:
            page_iter_func = cls._get_pages_from_episodes
        else:
            page_iter_func = cls._get_pages_from_pages
        result = []
        for page in page_iter_func(video_info):
            page.season_owner_name = season_owner_name
            page.season_owner_avatar_url = season_owner_avatar_url
            result.append(page)
        return result

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
    def _get_pages_from_pages(cls, dm: GetVideoInfoResponse) -> Iterator[WorkPage]:
        assert dm.data is not None

        work_base_url = VIDEO_URL_PATTERN.format(video_id=dm.data.bvid)
        work_base_url_parts = urlparse(work_base_url)

        season_id, season_name, season_cover_url, season_owner_id = None, None, None, None

        page_to_section_mapping: Dict = {}
        if dm.data.is_season_display:
            assert dm.data.ugc_season is not None
            season_id = dm.data.ugc_season.id_field
            season_name = dm.data.ugc_season.title
            season_cover_url = dm.data.ugc_season.cover
            season_owner_id = dm.data.ugc_season.mid
            for section in dm.data.ugc_season.sections:
                section_id = section.id_field
                section_name = section.title
                for episode in section.episodes:
                    page_to_section_mapping[episode.cid] = {
                        'section_id': section_id,
                        'section_name': section_name,
                        'episode_id': episode.id_field,
                        'episode_name': episode.title
                    }

        pages = dm.data.pages
        for page in pages:
            yield WorkPage(
                aid=dm.data.aid,
                bvid=dm.data.bvid,
                cid=page.cid,
                page_url=urlunparse((
                    work_base_url_parts.scheme,
                    work_base_url_parts.netloc,
                    work_base_url_parts.path,
                    work_base_url_parts.params,
                    urlencode({'p': page.page}, doseq=True),
                    work_base_url_parts.fragment
                )),
                page_title=page.part,
                duration=page.duration,
                season_id=season_id,
                season_name=season_name,
                season_cover_url=season_cover_url,
                season_owner_id=season_owner_id,
                season_owner_name=None,
                season_owner_avatar_url=None,
                section_id=page_to_section_mapping.get(page.cid, {}).get('section_id', None),
                section_name=page_to_section_mapping.get(page.cid, {}).get('section_name', None),
                episode_id=page_to_section_mapping.get(page.cid, {}).get('episode_id', None),
                episode_name=page_to_section_mapping.get(page.cid, {}).get('episode_name', None),
                work_url=work_base_url,
                work_title=dm.data.title,
                work_description=dm.data.desc,
                work_cover_url=dm.data.pic,
                work_owner_id=dm.data.owner.mid,
                work_owner_name=dm.data.owner.name,
                work_owner_avatar_url=dm.data.owner.face
            )

    @classmethod
    def _get_pages_from_episodes(cls, dm: GetVideoInfoResponse) -> Iterator[WorkPage]:
        assert dm.data is not None and dm.data.ugc_season is not None
        for section in dm.data.ugc_season.sections:
            for episode in section.episodes:
                work_base_url = VIDEO_URL_PATTERN.format(video_id=episode.bvid)
                work_base_url_parts = urlparse(work_base_url)

                for page in episode.pages:
                    yield WorkPage(
                        aid=episode.aid,
                        bvid=episode.bvid,
                        cid=episode.cid,
                        page_url=urlunparse((
                            work_base_url_parts.scheme,
                            work_base_url_parts.netloc,
                            work_base_url_parts.path,
                            work_base_url_parts.params,
                            urlencode({'p': page.page}, doseq=True),
                            work_base_url_parts.fragment
                        )),
                        page_title=page.part,
                        duration=page.duration,
                        season_id=dm.data.ugc_season.id_field,
                        season_name=dm.data.ugc_season.title,
                        season_cover_url=dm.data.ugc_season.cover,
                        season_owner_id=dm.data.ugc_season.mid,
                        season_owner_name=None,
                        season_owner_avatar_url=None,
                        section_id=section.id_field,
                        section_name=section.title,
                        episode_id=episode.id_field,
                        episode_name=episode.title,
                        work_url=work_base_url,
                        work_title=None,
                        work_description=None,
                        work_cover_url=episode.arc.pic,
                        work_owner_id=None,
                        work_owner_name=None,
                        work_owner_avatar_url=None
                    )

    @classmethod
    def _parse_work_owner(cls, dm: GetVideoInfoResponse) -> WorkOwner:
        assert dm.data is not None
        work_owner = dm.data.owner
        return WorkOwner(
            account_id=work_owner.mid,
            name=work_owner.name,
            avatar_url=work_owner.face
        )

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

    @classmethod
    def _get_user_name_and_avatar_url(cls, mid: int) -> Tuple[Optional[str], Optional[str]]:
        season_owner_name = None
        season_owner_avatar_url = None
        try:
            user_card_response = ProxyService.get_user_card(mid)
            if user_card_response.code == 0:
                assert user_card_response.data is not None
                season_owner_name = user_card_response.data.card.name
                season_owner_avatar_url = user_card_response.data.card.face
        except (ConnectionError, TimeoutError):
            pass
        return season_owner_name, season_owner_avatar_url
