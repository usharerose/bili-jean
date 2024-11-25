"""
Service component to process Bilibili streaming resource
"""
import logging
from typing import List, Optional, Tuple
from urllib.parse import urlparse

from .components import get_streaming_component_kls
from ..constants import (
    StreamingCategory,
    WEB_VIEW_URL_ID_TYPE_MAPPING,
    WEB_VIEW_URL_CATEGORY_MAPPING
)
from ..proxy_service import ProxyService
from ..schemes import (
    AudioStreamingSourceMeta,
    Page,
    StreamingWebViewMeta,
    VideoStreamingSourceMeta
)


logger = logging.getLogger(__name__)


class StreamingService:

    @classmethod
    def parse_web_view_url(cls, url: str) -> Optional[StreamingWebViewMeta]:
        """
        extract metadata from web view URL,
        which would help dispatch to corresponding component
        to request specific resource information

        requesting by the web view URL before parse it,
        is for getting the destination URL redirected from the source

        e.g. PGC which namespace is '/bangumi/play' commonly
             also has BV ID and the web URL like '/video/BV',
             which would be redirected
        """
        target_url = url
        response = None
        try:
            response = ProxyService.get(url, timeout=1, allow_redirects=False)
        except Exception:  # NOQA
            logger.warning(f'Request URL {url} failed when parse it')
            pass
        if response is not None:
            try:
                target_url = response.headers['location']
            except KeyError:
                pass

        url_path = urlparse(target_url).path

        for web_url_pattern, streaming_category in WEB_VIEW_URL_CATEGORY_MAPPING.items():
            search_result = web_url_pattern.search(url_path)
            if search_result:
                metadata = StreamingWebViewMeta(streaming_category=streaming_category)
                id_type = WEB_VIEW_URL_ID_TYPE_MAPPING[web_url_pattern]
                keyword_name, convert_func = id_type.value
                metadata.__setattr__(keyword_name, convert_func(search_result.group(1)))
                return metadata
        return None

    @classmethod
    def get_views(cls, url: str, sess_data: Optional[str] = None) -> Optional[List[Page]]:
        """
        get normalized views pages with primary information
        :param url: Web URL of a Bilibili streaming resource
        :type url: str
        :param sess_data: cookie of Bilibili user, SESSDATA
        :type sess_data: str
        :return: list of normalized pages
        """
        web_view_meta = cls.parse_web_view_url(url)
        if web_view_meta is None:
            raise ValueError(f'URL {url} is invalid')
        component_kls = get_streaming_component_kls(web_view_meta.streaming_category)
        return component_kls.get_views(
            aid=web_view_meta.aid,
            bvid=web_view_meta.bvid,
            season_id=web_view_meta.season_id,
            ep_id=web_view_meta.ep_id,
            sess_data=sess_data
        )

    @classmethod
    def get_page_streaming_src(
        cls,
        category: str,
        cid: Optional[int] = None,
        ep_id: Optional[int] = None,
        bvid: Optional[str] = None,
        aid: Optional[int] = None,
        is_video_hq_preferred: bool = True,
        video_qn: Optional[int] = None,
        is_video_codec_eff_preferred: bool = True,
        video_codec_number: Optional[int] = None,
        is_audio_hq_preferred: bool = True,
        audio_qn: Optional[int] = None,
        sess_data: Optional[str] = None
    ) -> Tuple[VideoStreamingSourceMeta, AudioStreamingSourceMeta]:
        streaming_category = StreamingCategory.from_value(category)
        component_kls = get_streaming_component_kls(streaming_category)
        return component_kls.get_page_streaming_src(
            cid=cid,
            ep_id=ep_id,
            bvid=bvid,
            aid=aid,
            is_video_hq_preferred=is_video_hq_preferred,
            video_qn=video_qn,
            is_video_codec_eff_preferred=is_video_codec_eff_preferred,
            video_codec_number=video_codec_number,
            is_audio_hq_preferred=is_audio_hq_preferred,
            audio_qn=audio_qn,
            sess_data=sess_data
        )
