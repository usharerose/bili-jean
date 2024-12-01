"""
Manipulate UGC resources
"""
from collections import OrderedDict
import logging
from typing import Any, List, Optional, Tuple

from ...constants import FormatNumberValue, StreamingCategory
from ...proxy_service import ProxyService
from ...schemes import (
    AudioStreamingSourceMeta,
    DashMediaItem,
    GetUGCPlayResponse,
    GetUGCViewResponse,
    Page,
    VideoStreamingSourceMeta
)
from ...schemes.proxy.card import GetCardDataCard
from .base import AbstractStreamingComponent
from .wrapper import register_component


logger = logging.getLogger(__name__)


@register_component(StreamingCategory.UGC)
class UGCComponent(AbstractStreamingComponent):

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
        result = cls._parse_raw_view(view_response)
        return result

    @classmethod
    def _parse_raw_view(cls, view_response: GetUGCViewResponse) -> Optional[List[Page]]:
        view_data = view_response.data
        if view_data is None:
            return None

        selected_pages = OrderedDict()
        for page in view_data.pages:
            normalized_page = Page(
                page_category=StreamingCategory.UGC.value,
                page_index=page.page,
                page_cid=page.cid,
                page_title=page.part,
                page_duration=page.duration,
                view_aid=view_data.aid,
                view_bvid=view_data.bvid,
                view_title=view_data.title,
                view_desc=view_data.desc,
                view_cover_url=view_data.pic,
                view_pub_time=view_data.pubdate,
                view_duration=view_data.duration,
                view_owner_id=view_data.owner.mid,
                view_owner_name=view_data.owner.name,
                view_owner_avatar_url=view_data.owner.face,
                is_selected_page=True
            )
            selected_pages[page.cid] = normalized_page

        if not view_data.is_season_display:
            return [page for _, page in selected_pages.items()]

        coll_owner_data: Optional[GetCardDataCard] = None
        try:
            coll_owner_data = ProxyService.get_card(mid=view_data.ugc_season.mid).data.card
        except Exception as e:
            logger.exception(e)
        coll_owner_name = coll_owner_data.name if coll_owner_data is not None else None
        coll_owner_avatar_url = coll_owner_data.face if coll_owner_data is not None else None

        result = []
        for section in view_data.ugc_season.sections:
            for episode in section.episodes:
                for page in episode.pages:
                    normalized_page = Page(
                        page_category=StreamingCategory.UGC.value,
                        page_index=page.page,
                        page_cid=page.cid,
                        page_title=page.part,
                        page_duration=page.duration,
                        view_aid=episode.aid,
                        view_bvid=episode.bvid,
                        view_title=episode.arc.title,
                        view_desc=episode.arc.desc,
                        view_cover_url=episode.arc.pic,
                        view_pub_time=episode.arc.pubdate,
                        view_duration=episode.arc.duration,
                        coll_id=view_data.ugc_season.id_field,
                        coll_title=view_data.ugc_season.title,
                        coll_desc=view_data.ugc_season.intro,
                        coll_cover_url=view_data.ugc_season.cover,
                        coll_owner_id=view_data.ugc_season.mid,
                        coll_owner_name=coll_owner_name,
                        coll_owner_avatar_url=coll_owner_avatar_url,
                        coll_sect_id=section.id_field,
                        coll_sect_title=section.title,
                        is_selected_page=False
                    )
                    selected_page = selected_pages.get(normalized_page.page_cid)
                    if selected_page is not None:
                        normalized_page.view_title = selected_page.view_title
                        normalized_page.view_desc = selected_page.view_desc
                        normalized_page.view_cover_url = selected_page.view_cover_url
                        normalized_page.view_pub_time = selected_page.view_pub_time
                        normalized_page.view_duration = selected_page.view_duration
                        normalized_page.view_owner_id = selected_page.view_owner_id
                        normalized_page.view_owner_name = selected_page.view_owner_name
                        normalized_page.view_owner_avatar_url = selected_page.view_owner_avatar_url
                        normalized_page.is_selected_page = True
                    result.append(normalized_page)
        return result

    @classmethod
    def get_page_streaming_src(
        cls,
        *args: Any,
        **kwargs: Any
    ) -> Tuple[VideoStreamingSourceMeta, AudioStreamingSourceMeta]:
        """
        :key cid: cid of a UGC resource, type is int
        :key bvid: BV ID of a UGC resource, type is str, optional
        :key aid: AV ID of a UGC resource, type is int, optional
        :key is_video_hq_preferred: prefer high quality video or not, type is bool, default is True
        :key video_qn: quality number, optional, prior to is_video_hq_preferred if declared
        :key is_video_codec_eff_preferred: prefer higher efficiency codec or not,
                                           type is bool, default is True
                                           which means AV1 > HEVC > AVC
        :key video_codec_number: codec number of video, optional, prior to is_video_codec_eff_preferred if declared
        :key is_audio_hq_preferred: prefer high quality audio or not, type is bool, default is True
        :key audio_qn: audio quality number, optional, prior to is_audio_hq_preferred if declared
        :key sess_data: cookie of Bilibili user which key is SESSDATA, type is str
        """
        return super().get_page_streaming_src(*args, **kwargs)

    @classmethod
    def _get_play(
        cls,
        *args: Any,
        **kwargs: Any
    ) -> GetUGCPlayResponse:
        cid = kwargs.get('cid')
        if cid is None:
            raise ValueError('cid is necessary')
        bvid = kwargs.get('bvid')
        aid = kwargs.get('aid')
        if all([id_val is None for id_val in (bvid, aid)]):
            raise ValueError("At least one of bvid and aid is necessary")

        params = {}
        if bvid is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': aid})
        params.update({
            'cid': cid,
            'fnval': FormatNumberValue.full_format(),
            'fourk': 1,
            'sess_data': kwargs.get('sess_data')
        })

        ugc_play = ProxyService.get_ugc_play(**params)
        return ugc_play

    @classmethod
    def _get_play_video_pool(cls, *args: Any, **kwargs: Any) -> List[DashMediaItem]:  # NOQA
        play_dm: GetUGCPlayResponse = kwargs['play_dm']
        return play_dm.data.dash.video

    @classmethod
    def _get_play_audio_pool(cls, *args: Any, **kwargs: Any) -> List[DashMediaItem]:  # NOQA
        play_dm: GetUGCPlayResponse = kwargs['play_dm']
        dash = play_dm.data.dash
        source_pool: List[DashMediaItem] = []
        if dash.dolby.audio is not None and len(dash.dolby.audio) > 0:
            source_pool.extend(dash.dolby.audio)
        if dash.flac is not None and dash.flac.audio is not None:
            source_pool.append(dash.flac.audio)
        if dash.audio is not None:
            source_pool.extend(dash.audio)
        return source_pool
