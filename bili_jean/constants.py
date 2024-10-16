"""
Constants on work's parameters
"""
from enum import IntEnum
from functools import reduce


class VideoWorkQualityNumber(IntEnum):
    """
    Video stream's quality number, noneffective for DASH format

    | 6    | 240P    |                                                  |
    | 16   | 360P    |                                                  |
    | 32   | 480P    |                                                  |
    | 64   | 720P    |                                                  |
    | 74   | 720P60  |                                                  |
    | 80   | 1080P   | login needed                                     |
    | 112  | 1080P+  | VIP needed                                       |
    | 116  | 1080P60 | VIP needed                                       |
    | 120  | 4K      | VIP needed, `fnval&128=128` and `fourk=1`        |
    | 125  | HDR     | VIP needed, only support DASH, `fnval&64=64`     |
    | 126  | Dolby   | VIP needed, only support DASH, `fnval&512=512`   |
    | 127  | 8K      | VIP needed, only support DASH, `fnval&1024=1024` |
    """
    P240 = 6          # Only support MP4
    P360 = 16
    P480 = 32
    P720 = 64         # Web default, from this level, need login, but can fetch from source URL directly
    P720_60 = 74
    P1080 = 80        # from this level, need VIP
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
        return self > self.P1080

    @classmethod
    def from_value(cls, qn: int) -> 'VideoWorkQualityNumber':
        for item in cls:
            if item == qn:
                return item
        raise ValueError(f'Invalid given quality number : {qn}')


class VideoWorkFormatNumberValue(IntEnum):
    """
    integer value of binary bitmap which stands for attributions
    | 1    | MP4                 | exclusive with DASH                                 |
    | 16   | DASH                | exclusive with MP4                                  |
    | 64   | HDR or not          | DASH is necessary, VIP needed, only H.265, `qn=125` |
    | 128  | 4K or not           | VIP needed, `fourk=1` and `qn=120`                  |
    | 256  | Dolby sound or not  | DASH is necessary, VIP needed                       |
    | 512  | Dolby vision or not | DASH is necessary, VIP needed                       |
    | 1024 | 8K or not           | DASH is necessary, VIP needed, `qn=127`             |
    | 2048 | AV1 codec or not    | DASH is necessary                                   |
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
    AV1_ENCODE = 2048     # not supported in this project

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
        :param qn: Video stream's quality number
        :type qn: int
        :param is_dolby_audio: request Dolby Audio or not
        :type is_dolby_audio: bool
        :return: int
        """
        result = cls.DASH.value
        if qn == VideoWorkQualityNumber.HDR:
            result = result | cls.HDR
        if qn >= VideoWorkQualityNumber.FOUR_K:
            result = result | cls.FOUR_K
        if is_dolby_audio:
            result = result | cls.DOLBY_AUDIO
        if qn == VideoWorkQualityNumber.DOLBY:
            result = result | cls.DOLBY_VISION
        if qn == VideoWorkQualityNumber.EIGHT_K:
            result = result | cls.EIGHT_K
        return result
