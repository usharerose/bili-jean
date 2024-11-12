"""
Service component to process Bilibili streaming resource
"""
from enum import Enum
import logging
from typing import Optional
import re
from urllib.parse import urlparse

from pydantic import BaseModel

from ..proxy_service import ProxyService


logger = logging.getLogger(__name__)


BVID_LENGTH = 9
WEB_VIEW_URL_UGC_BVID_PATTERN = re.compile(fr'/video/(BV1[a-zA-Z0-9]{{{BVID_LENGTH}}})')
WEB_VIEW_URL_UGC_AVID_PATTERN = re.compile(r'/video/av(\d+)')
WEB_VIEW_URL_EPID_PATTERN_STRING = r'/play/ep(\d+)'
WEB_VIEW_URL_EPID_PATTERN = re.compile(WEB_VIEW_URL_EPID_PATTERN_STRING)
WEB_VIEW_URL_SSID_PATTERN_STRING = r'/play/ss(\d+)'
WEB_VIEW_URL_SSID_PATTERN = re.compile(WEB_VIEW_URL_SSID_PATTERN_STRING)
WEB_VIEW_URL_PGC_NAMESPACE_STRING = '/bangumi'
WEB_VIEW_URL_PGC_EPID_PATTERN = re.compile(
    WEB_VIEW_URL_PGC_NAMESPACE_STRING + WEB_VIEW_URL_EPID_PATTERN_STRING
)
WEB_VIEW_URL_PGC_SSID_PATTERN = re.compile(
    WEB_VIEW_URL_PGC_NAMESPACE_STRING + WEB_VIEW_URL_SSID_PATTERN_STRING
)
WEB_VIEW_URL_PUGV_NAMESPACE_STRING = '/cheese'
WEB_VIEW_URL_PUGV_EPID_PATTERN = re.compile(
    WEB_VIEW_URL_PUGV_NAMESPACE_STRING + WEB_VIEW_URL_EPID_PATTERN_STRING
)
WEB_VIEW_URL_PUGV_SSID_PATTERN = re.compile(
    WEB_VIEW_URL_PUGV_NAMESPACE_STRING + WEB_VIEW_URL_SSID_PATTERN_STRING
)


class StreamingCategory(Enum):
    """
    Categories of streaming source

    UGC is commonly with '/video' in web URL,
    PGC is with '/bangumi/play',
    and PUGV is with '/cheese/play'
    """
    UGC = 'ugc'
    PGC = 'pgc'
    PUGV = 'pugv'


class StreamingIDType(Enum):
    """
    the value of each enum is,
    * keyword name
    * data-type-converted function
    """
    AID = ('aid', int)
    BVID = ('bvid', str)
    EP_ID = ('ep_id', int)
    SEASON_ID = ('season_id', int)


WEB_VIEW_URL_CATEGORY_MAPPING = {
    WEB_VIEW_URL_UGC_BVID_PATTERN: StreamingCategory.UGC,
    WEB_VIEW_URL_UGC_AVID_PATTERN: StreamingCategory.UGC,
    WEB_VIEW_URL_PGC_EPID_PATTERN: StreamingCategory.PGC,
    WEB_VIEW_URL_PGC_SSID_PATTERN: StreamingCategory.PGC,
    WEB_VIEW_URL_PUGV_EPID_PATTERN: StreamingCategory.PUGV,
    WEB_VIEW_URL_PUGV_SSID_PATTERN: StreamingCategory.PUGV
}
WEB_VIEW_URL_ID_TYPE_MAPPING = {
    WEB_VIEW_URL_UGC_BVID_PATTERN: StreamingIDType.BVID,
    WEB_VIEW_URL_UGC_AVID_PATTERN: StreamingIDType.AID,
    WEB_VIEW_URL_PGC_EPID_PATTERN: StreamingIDType.EP_ID,
    WEB_VIEW_URL_PGC_SSID_PATTERN: StreamingIDType.SEASON_ID,
    WEB_VIEW_URL_PUGV_EPID_PATTERN: StreamingIDType.EP_ID,
    WEB_VIEW_URL_PUGV_SSID_PATTERN: StreamingIDType.SEASON_ID
}


class StreamingWebViewMeta(BaseModel):
    """
    necessary resource ID for UGC, PGC and PUGV
    parsed from web view URL
    """
    streaming_category: StreamingCategory
    aid: Optional[int] = None
    bvid: Optional[str] = None
    ep_id: Optional[int] = None
    season_id: Optional[int] = None


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
