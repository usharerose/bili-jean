"""
Base streaming component
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional, Tuple, Union

from ...constants import AudioBitRateID
from ...schemes import (
    AudioStreamingSourceMeta,
    DashMediaItem,
    GetPGCPlayResponse,
    GetPUGVPlayResponse,
    GetUGCPlayResponse,
    Page,
    VideoStreamingSourceMeta
)


class AbstractStreamingComponent(ABC):

    @classmethod
    @abstractmethod
    def get_views(cls, *args: Any, **kwargs: Any) -> Optional[List[Page]]:
        """
        get normalized views info
        """

    @classmethod
    def get_page_streaming_src(
        cls,
        *args: Any,
        **kwargs: Any
    ) -> Tuple[VideoStreamingSourceMeta, AudioStreamingSourceMeta]:
        """
        get source URL of streaming, including both video and audio
        """
        play_dm = cls._get_play(*args, **kwargs)
        if play_dm.code != 0:
            raise

        is_video_hq_preferred = kwargs.get('is_video_hq_preferred')
        if is_video_hq_preferred is None:
            is_video_hq_preferred = True
        is_video_codec_eff_preferred = kwargs.get('is_video_codec_eff_preferred')
        if is_video_codec_eff_preferred is None:
            is_video_codec_eff_preferred = True
        video_src = cls._get_play_video_src(
            media_items=cls._get_play_video_pool(play_dm=play_dm),
            is_hq_preferred=is_video_hq_preferred,
            qn=kwargs.get('video_qn'),
            is_codec_eff_preferred=is_video_codec_eff_preferred,
            codec_id=kwargs.get('video_codec_number')
        )

        is_audio_hq_preferred = kwargs.get('is_audio_hq_preferred')
        if is_audio_hq_preferred is None:
            is_audio_hq_preferred = True
        audio_src = cls._get_play_audio_src(
            media_items=cls._get_play_audio_pool(play_dm=play_dm),
            is_hq_preferred=is_audio_hq_preferred,
            qn=kwargs.get('audio_qn')
        )
        return video_src, audio_src

    @classmethod
    @abstractmethod
    def _get_play(
        cls,
        *args: Any,
        **kwargs: Any
    ) -> Union[GetPGCPlayResponse, GetPUGVPlayResponse, GetUGCPlayResponse]:
        """
        get play response data model
        """

    @classmethod
    def _get_play_video_src(
        cls,
        media_items: List[DashMediaItem],
        is_hq_preferred: bool = True,
        qn: Optional[int] = None,
        is_codec_eff_preferred: bool = True,
        codec_id: Optional[int] = None
    ) -> VideoStreamingSourceMeta:
        avail_hqs: List[int] = list(set([item.id_field for item in media_items]))
        avail_hqs.sort(reverse=is_hq_preferred)
        if qn is not None:
            avail_hqs = [avail_hq for avail_hq in avail_hqs if avail_hq <= qn]
            if avail_hqs:
                avail_hqs.sort(reverse=True)
        qn, *_ = avail_hqs
        media_items = [item for item in media_items if item.id_field == qn]

        avail_codec_ids: List[int] = list(set([item.codecid for item in media_items]))
        avail_codec_ids.sort(reverse=is_codec_eff_preferred)
        if codec_id is not None:
            avail_codec_ids = [avail_codec_id for avail_codec_id in avail_codec_ids if avail_codec_id <= codec_id]
            if avail_codec_ids:
                avail_codec_ids.sort(reverse=True)
        codec_id, *_ = avail_codec_ids
        media, *_ = [item for item in media_items if item.codecid == codec_id]
        return VideoStreamingSourceMeta(
            url=media.base_url,
            codec_id=media.codecid,
            qn=media.id_field,
            mime_type=media.mime_type
        )

    @classmethod
    def _get_play_audio_src(
        cls,
        media_items: List[DashMediaItem],
        is_hq_preferred: bool = True,
        qn: Optional[int] = None
    ) -> AudioStreamingSourceMeta:
        avail_bitrates = list(set([
            AudioBitRateID.from_value(media_item.id_field)
            for media_item in media_items
        ]))
        avail_bitrates.sort(key=lambda item: item.value.quality, reverse=is_hq_preferred)
        if qn is not None:
            avail_bitrates = [
                avail_bitrate for avail_bitrate in avail_bitrates
                if avail_bitrate.value.quality <= AudioBitRateID.from_value(qn).value.quality
            ]
            if avail_bitrates:
                avail_bitrates.sort(key=lambda item: item.value.quality, reverse=True)
        target_bit_rate, *_ = avail_bitrates
        media, *_ = [item for item in media_items if item.id_field == target_bit_rate.value.bit_rate_id]
        return AudioStreamingSourceMeta(
            url=media.base_url,
            qn=media.id_field,
            mime_type=media.mime_type
        )

    @classmethod
    @abstractmethod
    def _get_play_video_pool(cls, *args: Any, **kwargs: Any) -> List[DashMediaItem]:
        """
        get list of media items about video resource
        :key play_dm: data model of the response from Play endpoint
        """

    @classmethod
    @abstractmethod
    def _get_play_audio_pool(cls, *args: Any, **kwargs: Any) -> List[DashMediaItem]:
        """
        get list of media items about audio resource
        :key play_dm: data model of the response from Play endpoint
        """
