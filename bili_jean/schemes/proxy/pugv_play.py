"""
Scheme definition of the response from https://api.bilibili.com/pugv/player/web/playurl
"""
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .base import BaseResponseModel, DashMediaItem


class GetPUGVPlayDataDashFlac(BaseModel):
    """
    Hi-Res audio data
    """
    audio: Optional[DashMediaItem] = None
    display: bool                          # illustrate Hi-Res or not


class GetPUGVPlayDataDashDolby(BaseModel):
    """
    Dolby audio data
    """
    audio: List[DashMediaItem] = []
    # 1 is normal, 2 is panoramic
    # for cheese, could be 'NONE'
    type_field: Union[int, str] = Field(..., alias='type')


class GetPUGVPlayDataDash(BaseModel):
    """
    PUGV stream play's DASH
    """
    audio: Optional[List[DashMediaItem]] = None     # null when resource has no audio
    dolby: GetPUGVPlayDataDashDolby                 # Dolby audio
    duration: int                                   # resource duration which unit is second
    flac: Optional[GetPUGVPlayDataDashFlac] = None  # High quality audio
    video: List[DashMediaItem]                      # video


class GetPUGVPlayDataDUrlItem(BaseModel):
    """
    Common UGC play resource data
    """
    backup_url: List[str]  # URLs of backup resources
    length: int            # duration of resource which unit is millisecond
    order: int             # order number of resource
    size: int              # size of resource, unit is byte
    url: str               # URL of resource


class GetPUGVPlayDataSupportFormatsItem(BaseModel):
    """
    supported UGC play's qualities
    """
    codecs: Optional[List[str]]                     # list of supported codec
    display_desc: str                               # display description
    format_field: str = Field(..., alias='format')  # file format extension
    new_description: str                            # complete description
    quality: int                                    # quality number


class GetPUGVPlayData(BaseModel):
    """
    'data' field, only defines part of necessary fields
    """
    dash: Optional[GetPUGVPlayDataDash] = None                # raw resources
    durl: Optional[List[GetPUGVPlayDataDUrlItem]] = None      # video-audio combined resources
    quality: int
    support_formats: List[GetPUGVPlayDataSupportFormatsItem]  # visible supported formats


class GetPUGVPlayResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -400：request error
    -404：video unavailable
    """
    data: Optional[GetPUGVPlayData] = None
