"""
Manipulate UGC resources
"""
from collections import OrderedDict
from typing import Any, List, Optional, Tuple

from ...constants import FormatNumberValue, StreamingCategory
from ...proxy_service import ProxyService
from ...schemes import (
    AudioStreamingSourceMeta,
    GetUGCPlayResponse,
    GetUGCViewResponse,
    Page,
    VideoStreamingSourceMeta
)
from ...schemes.proxy.ugc_play import GetUGCPlayDataDashMediaItem
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

        if ugc_play.code != 0:
            raise

        is_video_hq_preferred = kwargs.get('is_video_hq_preferred')
        if is_video_hq_preferred is None:
            is_video_hq_preferred = True
        is_video_codec_eff_preferred = kwargs.get('is_video_codec_eff_preferred')
        if is_video_codec_eff_preferred is None:
            is_video_codec_eff_preferred = True
        video_src = cls._parse_page_play_video_src(
            ugc_play=ugc_play,
            is_hq_preferred=is_video_hq_preferred,
            qn=kwargs.get('video_qn'),
            is_codec_eff_preferred=is_video_codec_eff_preferred,
            codec_number=kwargs.get('video_codec_number')
        )

        is_audio_hq_preferred = kwargs.get('is_audio_hq_preferred')
        if is_audio_hq_preferred is None:
            is_audio_hq_preferred = True
        audio_src = cls._parse_page_play_audio_src(
            ugc_play=ugc_play,
            is_hq_preferred=is_audio_hq_preferred,
            qn=kwargs.get('audio_qn')
        )
        return video_src, audio_src

    @classmethod
    def _parse_page_play_video_src(
        cls,
        ugc_play: GetUGCPlayResponse,
        is_hq_preferred: bool = True,
        qn: Optional[int] = None,
        is_codec_eff_preferred: bool = True,
        codec_number: Optional[int] = None
    ) -> VideoStreamingSourceMeta:
        source_pool: List[GetUGCPlayDataDashMediaItem] = ugc_play.data.dash.video

        avail_hqs: List[int] = list(set([item.id_field for item in source_pool]))
        avail_hqs.sort(reverse=is_hq_preferred)
        if qn is not None:
            avail_hqs = [avail_hq for avail_hq in avail_hqs if avail_hq <= qn]
            if avail_hqs:
                avail_hqs.sort(reverse=True)
        qn, *_ = avail_hqs
        source_pool = list(filter(lambda item: item.id_field == qn, source_pool))

        avail_codecs: List[int] = list(set([item.codecid for item in source_pool]))
        avail_codecs.sort(reverse=is_codec_eff_preferred)
        if codec_number is not None:
            avail_codecs = [avail_codec for avail_codec in avail_codecs if avail_codec <= codec_number]
            if avail_codecs:
                avail_codecs.sort(reverse=True)
        codec_id, *_ = avail_codecs
        media, *_ = list(filter(lambda item: item.codecid == codec_id, source_pool))
        return VideoStreamingSourceMeta(
            url=media.base_url,
            codec_id=media.codecid,
            qn=media.id_field,
            mime_type=media.mime_type
        )

    @classmethod
    def _parse_page_play_audio_src(
        cls,
        ugc_play: GetUGCPlayResponse,
        is_hq_preferred: bool = True,
        qn: Optional[int] = None
    ) -> AudioStreamingSourceMeta:
        dash = ugc_play.data.dash
        source_pool: List[GetUGCPlayDataDashMediaItem] = []
        if dash.dolby.audio is not None and len(dash.dolby.audio) > 0:
            source_pool.extend(dash.dolby.audio)
        if dash.flac is not None and dash.flac.audio is not None:
            source_pool.append(dash.flac.audio)
        if dash.audio is not None:
            source_pool.extend(dash.audio)

        avail_bitrates = list(set([item.id_field for item in source_pool]))
        avail_bitrates.sort(reverse=is_hq_preferred)
        if qn is not None:
            avail_bitrates = [avail_bitrate for avail_bitrate in avail_bitrates if avail_bitrate <= qn]
            if avail_bitrates:
                avail_bitrates.sort(reverse=True)
        qn, *_ = avail_bitrates
        media, *_ = [item for item in source_pool if item.id_field == qn]
        return AudioStreamingSourceMeta(
            url=media.base_url,
            qn=media.id_field,
            mime_type=media.mime_type
        )
