"""
Manipulate PUGV resources
"""
from typing import Any, List, Optional

from ...constants import StreamingCategory
from ...proxy_service import ProxyService
from ...schemes import GetPUGVViewResponse, Page
from .base import AbstractStreamingComponent
from .wrapper import register_component


@register_component(StreamingCategory.PUGV)
class PUGVComponent(AbstractStreamingComponent):

    @classmethod
    def get_views(cls, *args: Any, **kwargs: Any) -> Optional[List[Page]]:  # NOQA
        """
        get normalized views info
        :key season_id: ssid of a PUGV resource, type is str
        :key ep_id: ep_id of a PUGV resource, type is int
        :key sess_data: cookie of Bilibili user which key is SESSDATA, type is str
        """
        view_response = ProxyService.get_pugv_view(
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
        view_response: GetPUGVViewResponse,
        ep_id: Optional[int] = None
    ) -> Optional[List[Page]]:
        view_data = view_response.data
        if view_data is None:
            return None

        result = []
        for idx, episode in enumerate(view_data.episodes):
            normalized_page = Page(
                page_category=StreamingCategory.PUGV.value,
                page_cid=episode.cid,
                page_title=episode.title,
                page_duration=episode.duration,
                view_aid=episode.aid,
                view_ep_id=episode.id_field,
                view_season_id=view_data.season_id,
                view_title=episode.title,
                view_desc='',
                view_cover_url=episode.cover,
                view_pub_time=episode.release_date,
                view_duration=episode.duration,
                view_owner_id=view_data.up_info.mid,
                view_owner_name=view_data.up_info.uname,
                view_owner_avatar_url=view_data.up_info.avatar,
                coll_owner_id=view_data.up_info.mid,
                coll_owner_name=view_data.up_info.uname,
                coll_owner_avatar_url=view_data.up_info.avatar,
                coll_sect_id=view_data.season_id,
                coll_sect_title=view_data.title,
                is_selected_page=False
            )
            # 1. if request by season_id, choose first one as default selected episode
            # 2. if request by ep_id, choose the corresponding one
            if (ep_id is None and idx == 0) or (ep_id is not None and ep_id == normalized_page.view_ep_id):
                normalized_page.is_selected_page = True
            result.append(normalized_page)
        return result
