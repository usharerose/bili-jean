"""
Constants components
"""
from enum import Enum, IntEnum
from functools import reduce
import re


class QualityNumber(IntEnum):
    """
    Format quality number of streaming resource, noneffective for DASH format
    | value | description | comment                                          |
    |-------+-------------+--------------------------------------------------|
    | 6     | 240P        | only support MP4                                 |
    | 16    | 360P        |                                                  |
    | 32    | 480P        |                                                  |
    | 64    | 720P        | Web default, login needed                        |
    | 74    | 720P60      | login needed                                     |
    | 80    | 1080P       | login needed                                     |
    | 112   | 1080P+      | VIP needed                                       |
    | 116   | 1080P60     | VIP needed                                       |
    | 120   | 4K          | VIP needed, `fnval&128=128` and `fourk=1`        |
    | 125   | HDR         | VIP needed, only support DASH, `fnval&64=64`     |
    | 126   | Dolby       | VIP needed, only support DASH, `fnval&512=512`   |
    | 127   | 8K          | VIP needed, only support DASH, `fnval&1024=1024` |
    """
    P240 = 6
    P360 = 16
    P480 = 32
    P720 = 64
    P720_60 = 74
    P1080 = 80
    PPLUS_1080 = 112
    P1080_60 = 116
    FOUR_K = 120
    HDR = 125
    DOLBY = 126
    EIGHT_K = 127

    @property
    def is_login_needed(self) -> bool:
        return self >= self.P720

    @property
    def is_vip_needed(self) -> bool:
        return self >= self.PPLUS_1080

    @classmethod
    def from_value(cls, qn: int) -> 'QualityNumber':
        for item in cls:
            if item == qn:
                return item
        raise ValueError(f'Invalid given quality number : {qn}')


class FormatNumberValue(IntEnum):
    """
    integer type value of a binary bitmap standing for multi-attribute combination
    | value | description         | comment                                             |
    |-------+---------------------+-----------------------------------------------------|
    | 0     | FLV                 | exclusive with MP4 and DASH, deprecated             |
    | 1     | MP4                 | exclusive with FLV and DASH                         |
    | 16    | DASH                | exclusive with FLV and MP4                          |
    | 64    | HDR or not          | DASH is necessary, VIP needed, only H.265, `qn=125` |
    | 128   | 4K or not           | VIP needed, `fourk=1` and `qn=120`                  |
    | 256   | Dolby sound or not  | DASH is necessary, VIP needed                       |
    | 512   | Dolby vision or not | DASH is necessary, VIP needed                       |
    | 1024  | 8K or not           | DASH is necessary, VIP needed, `qn=127`             |
    | 2048  | AV1 codec or not    | DASH is necessary                                   |
    support 'or' for combination,
    e.g. DASH format, and HDR, fnval = 16 | 64 = 80
    """
    # FLV = 0             # deprecated
    # MP4 = 1             # not support in this project
    DASH = 16
    HDR = 64
    FOUR_K = 128
    DOLBY_AUDIO = 256
    DOLBY_VISION = 512
    EIGHT_K = 1024
    AV1_ENCODE = 2048

    @classmethod
    def full_format(cls) -> int:
        return reduce(lambda prev, cur: prev | cur, [item.value for item in cls])

    @classmethod
    def get_format_number_value(
        cls,
        qn: int,
        is_dolby_audio: bool = False
    ) -> int:
        """
        get format number value according to Quality Number
        :param qn: format quality number
        :type qn: int
        :param is_dolby_audio: request Dolby Audio or not
        :type is_dolby_audio: bool
        :return: int
        """
        result = cls.DASH.value
        if qn == QualityNumber.HDR:
            result = result | cls.HDR
        if qn >= QualityNumber.FOUR_K:
            result = result | cls.FOUR_K
        if is_dolby_audio:
            result = result | cls.DOLBY_AUDIO
        if qn == QualityNumber.DOLBY:
            result = result | cls.DOLBY_VISION
        if qn == QualityNumber.EIGHT_K:
            result = result | cls.EIGHT_K
        return result


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


class VideoCodecID(IntEnum):
    """
    AVC, which is avc1.64001E, not support 8K
    HEVC, which is hev1.1.6.L120.90
    AV1, which is av01.0.00M.10.0.110.01.01.01.0
    """
    AVC = 7
    HEVC = 12
    AV1 = 13

    @classmethod
    def from_value(cls, codec_id: int) -> 'VideoCodecID':
        for item in cls:
            if item == codec_id:
                return item
        raise ValueError(f'Invalid given video codec ID: {codec_id}')


class AudioBitRateID(IntEnum):
    """
    AVC, which is avc1.64001E, not support 8K
    HEVC, which is hev1.1.6.L120.90
    AV1, which is av01.0.00M.10.0.110.01.01.01.0
    """
    BPS_64K = 30216
    BPS_132K = 30232
    BPS_192K = 30280
    BPS_DOLBY = 30250
    BPS_HIRES = 30251

    @classmethod
    def from_value(cls, bitrate_id: int) -> 'AudioBitRateID':
        for item in cls:
            if item == bitrate_id:
                return item
        raise ValueError(f'Invalid given audio bitrate ID: {bitrate_id}')
