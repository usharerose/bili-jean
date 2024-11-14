"""
Manipulate PGC resources
"""
from typing import Any, List, Optional, Union

from ...constants import StreamingCategory
from ...proxy_service import ProxyService
from ...schemes import GetPGCViewResponse, Page
from ...schemes.proxy.pgc_view import (
    GetPGCViewResultEpisodesItem,
    GetPGCViewResultSectionEpisodesItem
)
from .base import AbstractStreamingComponent
from .wrapper import register_component


@register_component(StreamingCategory.PGC)
class PGCComponent(AbstractStreamingComponent):

    @classmethod
    def get_views(cls, *args: Any, **kwargs: Any) -> Optional[List[Page]]:  # NOQA
        """
        get normalized views info
        :key bvid: BV ID of a PGC resource, type is str
        :key aid: AV ID of a PGC resource, type is int
        :key sess_data: cookie of Bilibili user which key is SESSDATA, type is str
        """
        view_response = ProxyService.get_pgc_view(
            season_id=kwargs.get('season_id'),
            ep_id=kwargs.get('ep_id'),
            sess_data=kwargs.get('sess_data')
        )
        req_ep_id = kwargs.get('ep_id')
        result = cls._parse_raw_view(view_response, req_ep_id)
        return result

    @classmethod
    def _parse_raw_view(
        cls,
        view_response: GetPGCViewResponse,
        ep_id: Optional[int] = None
    ) -> Optional[List[Page]]:
        view_data = view_response.result
        if view_data is None:
            return None

        view_owner_id, view_owner_name, view_owner_avatar_url = None, None, None
        if view_data.up_info is not None:
            view_owner_id = view_data.up_info.mid
            view_owner_name = view_data.up_info.uname
            view_owner_avatar_url = view_data.up_info.avatar

        series_id = view_data.series.series_id if view_data.series.series_id != 0 else None
        series_title = view_data.series.series_title if view_data.series.series_title else None

        result = []
        for idx, episode in enumerate(view_data.episodes):
            normalized_page = Page(
                page_category=StreamingCategory.PGC.value,
                page_cid=episode.cid,
                page_title=cls._process_title(episode),
                page_duration=cls._process_duration(episode),
                view_aid=episode.aid,
                view_bvid=episode.bvid,
                view_ep_id=episode.ep_id,
                view_season_id=view_data.season_id,
                view_title=cls._process_title(episode),
                view_desc='',
                view_cover_url=episode.cover,
                view_pub_time=episode.pub_time,
                view_duration=cls._process_duration(episode),
                view_owner_id=view_owner_id,
                view_owner_name=view_owner_name,
                view_owner_avatar_url=view_owner_avatar_url,
                coll_id=series_id,
                coll_title=series_title,
                coll_owner_id=view_owner_id,
                coll_owner_name=view_owner_name,
                coll_owner_avatar_url=view_owner_avatar_url,
                coll_sect_id=view_data.season_id,
                coll_sect_title=view_data.season_title,
                is_selected_page=False
            )
            # 1. if request by season_id, choose first one as default selected episode
            # 2. if request by ep_id, choose the corresponding one
            if (ep_id is None and idx == 0) or (ep_id is not None and ep_id == normalized_page.view_ep_id):
                normalized_page.is_selected_page = True
            result.append(normalized_page)

        for section in (view_data.section or []):
            for episode_in_sect in section.episodes:
                # There could be UGC resources as sidelights
                # ignore them since it is just a pointer, not located here actually
                is_pgc = episode_in_sect.link_type is None
                if not is_pgc:
                    continue

                normalized_page = Page(
                    page_category=StreamingCategory.PGC.value,
                    page_cid=episode_in_sect.cid,
                    page_title=cls._process_title(episode_in_sect),
                    page_duration=cls._process_duration(episode_in_sect),
                    view_aid=episode_in_sect.aid,
                    view_bvid=episode_in_sect.bvid,
                    view_ep_id=episode_in_sect.ep_id,
                    view_season_id=view_data.season_id,
                    view_title=cls._process_title(episode_in_sect),
                    view_desc='',
                    view_pub_time=episode_in_sect.pub_time,
                    view_duration=cls._process_duration(episode_in_sect),
                    view_owner_id=view_owner_id,
                    view_owner_name=view_owner_name,
                    view_owner_avatar_url=view_owner_avatar_url,
                    coll_id=series_id,
                    coll_title=series_title,
                    coll_owner_id=view_owner_id,
                    coll_owner_name=view_owner_name,
                    coll_owner_avatar_url=view_owner_avatar_url,
                    coll_sect_id=view_data.season_id,
                    coll_sect_title=view_data.season_title,
                    is_selected_page=False
                )
                # if request by ep_id, choose the corresponding one
                if ep_id is not None and ep_id == normalized_page.view_ep_id:
                    normalized_page.is_selected_page = True
                result.append(normalized_page)
        return result

    @staticmethod
    def _process_duration(
        episode: Union[GetPGCViewResultEpisodesItem, GetPGCViewResultSectionEpisodesItem]
    ) -> int:
        """
        convert duration of PGC episode from millisecond to second
        """
        if episode.duration is None:
            raise ValueError('PGC episode should not be null')
        return int(round(episode.duration / 1000))

    @staticmethod
    def _process_title(
        episode: Union[GetPGCViewResultEpisodesItem, GetPGCViewResultSectionEpisodesItem]
    ) -> str:
        return ' '.join((episode.title or '', episode.long_title or '')).strip()
