"""
Manipulate UGC resources
"""
from collections import OrderedDict
from typing import Any, List, Optional

from ...constants import FormatNumberValue, StreamingCategory
from ...proxy_service import ProxyService
from ...schemes import GetUGCViewResponse, Page
from .base import AbstractStreamingComponent
from .wrapper import register_component


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
                        coll_owner_name=None,
                        coll_owner_avatar_url=None,
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
    def get_page_streaming_src(cls, *args: Any, **kwargs: Any):
        """
        :key cid: cid of a UGC resource, type is int
        :key bvid: BV ID of a UGC resource, type is str, optional
        :key aid: AV ID of a UGC resource, type is int, optional
        :key qn: quality number, optional,
                 choose the highest one from available resources if undeclared
        :key aqn: audio quality number, optional,
                  choose the highest one from available resources if undeclared
        :key sess_data: cookie of Bilibili user which key is SESSDATA, type is str
        """
        params = {}

        bvid = kwargs.get('bvid')
        if kwargs.get('bvid') is not None:
            params.update({'bvid': bvid})
        else:
            params.update({'aid': kwargs.get('aid')})
        params.update({
            'cid': kwargs['cid'],
            'fnval': FormatNumberValue.full_format(),
            'fourk': 1,
            'sess_data': kwargs.get('sess_data')
        })

        ugc_play = ProxyService.get_ugc_play(**params)

        if ugc_play.code != 0:
            raise
        data = ugc_play.data
        highest_qn = data.quality
        qn = kwargs.get('qn')
        if qn is not None:
            highest_qn = qn if highest_qn >= qn else highest_qn
        video_src, *_ = filter(lambda video: video.id_field == highest_qn, data.dash.video)

        audios = []
        if data.dash.dolby.audio is not None and len(data.dash.dolby.audio) > 0:
            audios.extend(data.dash.dolby.audio)
        if data.dash.flac is not None and data.dash.flac.audio is not None:
            audios.append(data.dash.flac.audio)
        if data.dash.audio is not None:
            audios.extend(data.dash.audio)
        highest_audio, *_ = audios
        highest_aqn = highest_audio.id_field
        aqn = kwargs.get('aqn')
        if aqn is not None:
            highest_aqn = aqn if highest_aqn >= aqn else highest_aqn
        audio_src, *_ = filter(lambda audio: audio.id_field == highest_aqn, audios)
        return {
            'video': {
                'url': video_src.base_url,
                'codecs': video_src.codecs,
                'mime_type': video_src.mime_type
            },
            'audio': {
                'url': audio_src.base_url,
                'codecs': audio_src.codecs,
                'mime_type': audio_src.mime_type
            }
        }
