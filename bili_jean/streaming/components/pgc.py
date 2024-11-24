"""
Manipulate PGC resources
"""
from typing import Any, List, Optional, Tuple, Union

from ...constants import FormatNumberValue, StreamingCategory
from ...proxy_service import ProxyService
from ...schemes import (
    AudioStreamingSourceMeta,
    GetPGCPlayResponse,
    GetPGCViewResponse,
    Page,
    VideoStreamingSourceMeta
)
from ...schemes.proxy.pgc_play import GetPGCPlayResultDashMediaItem
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

    @classmethod
    def get_page_streaming_src(
        cls,
        *args: Any,
        **kwargs: Any
    ) -> Tuple[VideoStreamingSourceMeta, AudioStreamingSourceMeta]:
        """
        :key cid: cid of a PGC resource, type is int, optional
        :key ep_id: ep_id of a PGC resource, type is int, optional
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
        ep_id = kwargs.get('ep_id')
        if all([id_val is None for id_val in (cid, ep_id)]):
            raise ValueError("At least one of cid and ep_id is necessary")

        params = {}
        if cid is not None:
            params.update({'cid': cid})
        else:
            params.update({'ep_id': ep_id})
        params.update({
            'fnval': FormatNumberValue.full_format(),
            'fourk': 1,
            'sess_data': kwargs.get('sess_data')
        })

        pgc_play = ProxyService.get_pgc_play(**params)

        if pgc_play.code != 0:
            raise

        is_video_hq_preferred = kwargs.get('is_video_hq_preferred')
        if is_video_hq_preferred is None:
            is_video_hq_preferred = True
        is_video_codec_eff_preferred = kwargs.get('is_video_codec_eff_preferred')
        if is_video_codec_eff_preferred is None:
            is_video_codec_eff_preferred = True
        video_src = cls._parse_page_play_video_src(
            pgc_play=pgc_play,
            is_hq_preferred=is_video_hq_preferred,
            qn=kwargs.get('video_qn'),
            is_codec_eff_preferred=is_video_codec_eff_preferred,
            codec_number=kwargs.get('video_codec_number')
        )

        is_audio_hq_preferred = kwargs.get('is_audio_hq_preferred')
        if is_audio_hq_preferred is None:
            is_audio_hq_preferred = True
        audio_src = cls._parse_page_play_audio_src(
            pgc_play=pgc_play,
            is_hq_preferred=is_audio_hq_preferred,
            qn=kwargs.get('audio_qn')
        )
        return video_src, audio_src

    @classmethod
    def _parse_page_play_video_src(
        cls,
        pgc_play: GetPGCPlayResponse,
        is_hq_preferred: bool = True,
        qn: Optional[int] = None,
        is_codec_eff_preferred: bool = True,
        codec_number: Optional[int] = None
    ) -> VideoStreamingSourceMeta:
        source_pool: List[GetPGCPlayResultDashMediaItem] = pgc_play.result.dash.video

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
        pgc_play: GetPGCPlayResponse,
        is_hq_preferred: bool = True,
        qn: Optional[int] = None
    ) -> AudioStreamingSourceMeta:
        dash = pgc_play.result.dash
        source_pool: List[GetPGCPlayResultDashMediaItem] = []
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
