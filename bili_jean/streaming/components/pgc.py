"""
Manipulate PGC resources
"""
from typing import Any, List, Optional

from ...proxy_service import ProxyService
from ...schemes import GetPGCViewResponse, Page


class PGCComponent:

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
        result = cls.parse_raw_view(view_response, req_ep_id)
        return result

    @classmethod
    def parse_raw_view(
        cls,
        view_response: GetPGCViewResponse,
        ep_id: Optional[int] = None
    ) -> Optional[List[Page]]:
        result = view_response.result
        if result is None:
            return None

        view_owner_id, view_owner_name, view_owner_avatar_url = None, None, None
        if result.up_info is not None:
            view_owner_id = result.up_info.mid
            view_owner_name = result.up_info.uname
            view_owner_avatar_url = result.up_info.avatar

        series_id = result.series.series_id if result.series.series_id != 0 else None
        series_title = result.series.series_title if result.series.series_title else None

        parsed_result = []
        for idx, episode in enumerate(result.episodes):
            item = Page(
                cid=episode.cid,
                title=episode.title,
                duration=episode.duration // 1000,
                view_aid=episode.aid,
                view_bvid=episode.bvid,
                view_ep_id=episode.ep_id,
                view_season_id=result.season_id,
                view_title=episode.long_title,
                view_desc='',
                view_cover_url=episode.cover,
                view_pub_time=episode.pub_time,
                view_duration=episode.duration // 1000,
                view_owner_id=view_owner_id,
                view_owner_name=view_owner_name,
                view_owner_avatar_url=view_owner_avatar_url,
                coll_szn_id=series_id,
                coll_szn_title=series_title,
                coll_szn_desc=None,
                coll_szn_cover_url=None,
                coll_szn_owner_id=view_owner_id,
                coll_szn_owner_name=view_owner_name,
                coll_szn_owner_avatar_url=view_owner_avatar_url,
                coll_sect_id=result.season_id,
                coll_sect_title=result.season_title,
                coll_ep_id=episode.ep_id,
                coll_ep_title=episode.title,
                coll_ep_cover_url=episode.cover,
                coll_ep_pub_time=episode.pub_time,
                coll_ep_duration=episode.duration // 1000,
                is_relevant_page=False
            )
            if (ep_id is None and idx == 0) or item.view_ep_id == ep_id:
                item.is_relevant_page = True
            parsed_result.append(item)
        if result.section is not None:
            for section in result.section:
                for episode in section.episodes:
                    is_pgc = episode.link_type is None
                    item = Page(
                        cid=episode.cid if is_pgc else None,
                        title=episode.title,
                        duration=episode.duration // 1000 if is_pgc else None,
                        view_aid=episode.aid,
                        view_bvid=episode.bvid if is_pgc else None,
                        view_ep_id=episode.ep_id if is_pgc else None,
                        view_season_id=result.season_id if is_pgc else None,
                        view_title=episode.long_title if is_pgc else '',
                        view_desc='',
                        view_cover_url=episode.cover,
                        view_pub_time=episode.pub_time if is_pgc else None,
                        view_duration=episode.duration // 1000 if is_pgc else None,
                        view_owner_id=view_owner_id if is_pgc else None,
                        view_owner_name=view_owner_name if is_pgc else None,
                        view_owner_avatar_url=view_owner_avatar_url if is_pgc else None,
                        coll_szn_id=series_id if is_pgc else None,
                        coll_szn_title=series_title if is_pgc else None,
                        coll_szn_desc=None,
                        coll_szn_cover_url=None,
                        coll_szn_owner_id=view_owner_id if is_pgc else None,
                        coll_szn_owner_name=view_owner_name if is_pgc else None,
                        coll_szn_owner_avatar_url=view_owner_avatar_url if is_pgc else None,
                        coll_sect_id=result.season_id if is_pgc else None,
                        coll_sect_title=result.season_title if is_pgc else None,
                        coll_ep_id=episode.ep_id if is_pgc else None,
                        coll_ep_title=episode.title if is_pgc else None,
                        coll_ep_cover_url=episode.cover if is_pgc else None,
                        coll_ep_pub_time=episode.pub_time if is_pgc else None,
                        coll_ep_duration=episode.duration // 1000 if is_pgc else None,
                        is_relevant_page=False
                    )
                    if ep_id is not None and ep_id == item.view_ep_id:
                        item.is_relevant_page = True
                    parsed_result.append(item)
        return parsed_result
