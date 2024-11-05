"""
Scheme definition of the response from https://api.bilibili.com/pgc/player/web/playurl
"""
from typing import List, Optional, Union

from pydantic import BaseModel, Field

from .base import BaseResponseModel


class GetPGCPlayResultDashMediaItem(BaseModel):
    """
    PGC digital media data
    """
    backup_url: List[str]                   # URLs of backup resources
    bandwidth: int                          # minimum of network bandwidth that needed
    base_url: str                           # resource URL
    codecid: int
    codecs: str
    height: int                             # 0 for audio
    id_field: int = Field(..., alias='id')
    mime_type: str
    width: int                              # 0 for audio


class GetPGCPlayResultDashDolby(BaseModel):
    """
    Dolby audio data
    """
    audio: List[GetPGCPlayResultDashMediaItem] = []
    # 1 is normal, 2 is panoramic
    # for cheese, could be 'NONE'
    type_field: Union[int, str] = Field(..., alias='type')


class GetPGCPlayResultDashFlac(BaseModel):
    """
    Hi-Res audio data
    """
    audio: Optional[GetPGCPlayResultDashMediaItem] = None
    display: bool                                        # illustrate Hi-Res or not


class GetPGCPlayResultDash(BaseModel):
    """
    PGC stream play's DASH
    """
    audio: Optional[List[GetPGCPlayResultDashMediaItem]] = None  # null when resource has no audio
    dolby: GetPGCPlayResultDashDolby                             # Dolby audio
    duration: int                                                # resource duration which unit is second
    flac: Optional[GetPGCPlayResultDashFlac] = None              # High quality audio
    video: List[GetPGCPlayResultDashMediaItem]                   # video


class GetPGCPlayResultDUrlItem(BaseModel):
    """
    Common UGC play resource data
    """
    backup_url: List[str]  # URLs of backup resources
    length: int            # duration of resource which unit is millisecond
    order: int             # order number of resource
    size: int              # size of resource, unit is byte
    url: str               # URL of resource


class GetPGCPlayResultSupportFormatsItem(BaseModel):
    """
    supported PGC play's qualities
    """
    codecs: Optional[List[str]]                     # list of supported codec
    display_desc: str                               # display description
    format_field: str = Field(..., alias='format')  # file format extension
    new_description: str                            # complete description
    quality: int                                    # quality number


class GetPGCPlayResult(BaseModel):
    """
    'result' field, only defines part of necessary fields
    """
    dash: Optional[GetPGCPlayResultDash] = None                # raw resources
    durl: Optional[List[GetPGCPlayResultDUrlItem]] = None      # video-audio combined resources
    quality: int
    support_formats: List[GetPGCPlayResultSupportFormatsItem]  # visible supported formats


class GetPGCPlayResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -400：request error
    -404：video unavailable
    """
    result: Optional[GetPGCPlayResult] = None
