"""
Manipulate UGC resources
"""
from collections import OrderedDict
from typing import Any, List, Optional

from ...proxy_service import ProxyService
from ...schemes import GetUGCViewResponse, Page


class UGCComponent:

    @classmethod
    def get_views(cls, *args: Any, **kwargs: Any) -> Optional[List[Page]]:  # NOQA
        """
        get normalized views info
        :key bvid: BV ID of a UGC resource, type is str
        :key aid: AV ID of a UGC resource, type is int
        :key sess_data: cookie of Bilibili user which key is SESSDATA, type is str
        """
        view_response = ProxyService.get_ugc_view(
            bvid=kwargs.get('bvid'),
            aid=kwargs.get('aid'),
            sess_data=kwargs.get('sess_data')
        )
        result = cls.parse_raw_view(view_response)
        return result

    @classmethod
    def parse_raw_view(cls, view_response: GetUGCViewResponse) -> Optional[List[Page]]:
        data = view_response.data
        if data is None:
            return None

        target_pages = OrderedDict()
        for page in data.pages:
            target_pages[page.cid] = Page(
                index=page.page,
                cid=page.cid,
                title=page.part,
                duration=page.duration,
                view_aid=data.aid,
                view_bvid=data.bvid,
                view_ep_id=None,
                view_season_id=None,
                view_title=data.title,
                view_desc=data.desc,
                view_cover_url=data.pic,
                view_pub_time=data.pubdate,
                view_duration=data.duration,
                view_owner_id=data.owner.mid,
                view_owner_name=data.owner.name,
                view_owner_avatar_url=data.owner.face,
                coll_szn_id=None,
                coll_szn_title=None,
                coll_szn_desc=None,
                coll_szn_cover_url=None,
                coll_szn_owner_id=None,
                coll_szn_owner_name=None,
                coll_szn_owner_avatar_url=None,
                coll_sect_id=None,
                coll_sect_title=None,
                coll_ep_id=None,
                coll_ep_title=None,
                coll_ep_cover_url=None,
                is_relevant_page=False
            )
        if not data.is_season_display:
            return [page for _, page in target_pages.items()]

        result = []
        ugc_season = data.ugc_season
        for section in ugc_season.sections:
            for episode in section.episodes:
                for page in episode.pages:
                    item = Page(
                        index=page.page,
                        cid=page.cid,
                        title=page.part,
                        duration=page.duration,
                        view_aid=episode.aid,
                        view_bvid=episode.bvid,
                        view_ep_id=None,
                        view_season_id=None,
                        view_title=None,
                        view_desc=None,
                        view_cover_url=None,
                        view_pub_time=None,
                        view_duration=None,
                        view_owner_id=None,
                        view_owner_name=None,
                        view_owner_avatar_url=None,
                        coll_szn_id=ugc_season.id_field,
                        coll_szn_title=ugc_season.title,
                        coll_szn_desc=ugc_season.intro,
                        coll_szn_cover_url=ugc_season.cover,
                        coll_szn_owner_id=ugc_season.mid,
                        coll_szn_owner_name=None,
                        coll_szn_owner_avatar_url=None,
                        coll_sect_id=section.id_field,
                        coll_sect_title=section.title,
                        coll_ep_id=episode.id_field,
                        coll_ep_title=episode.title,
                        coll_ep_desc=episode.arc.desc,
                        coll_ep_cover_url=episode.arc.pic,
                        coll_ep_pub_time=episode.arc.pubdate,
                        coll_ep_duration=episode.arc.duration,
                        is_relevant_page=True
                    )
                    target_page = target_pages.get(item.cid)
                    if target_page is not None:
                        item.view_title = target_page.view_title
                        item.view_desc = target_page.view_desc
                        item.view_cover_url = target_page.view_cover_url
                        item.view_pub_time = target_page.view_pub_time
                        item.view_duration = target_page.view_duration
                        item.view_owner_id = target_page.view_owner_id
                        item.view_owner_name = target_page.view_owner_name
                        item.view_owner_avatar_url = target_page.view_owner_avatar_url
                        item.is_relevant_page = target_page.is_relevant_page
                    result.append(item)
        return result
