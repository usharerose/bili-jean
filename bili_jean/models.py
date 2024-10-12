"""
Model of Bilibili data
"""
from typing import List, Optional

from pydantic import BaseModel, Field


class BaseResponseModel(BaseModel):

    code: int = 0
    message: str = '0'
    ttl: Optional[int] = None


class GetVideoInfoDataOwner(BaseModel):
    """
    Bilibili account who participants in the work
    """
    mid: int   # User ID
    name: str  # User name
    face: str  # Profile icon's source URL


class GetVideoInfoDataPagesItem(BaseModel):
    """
    meta info of Bilibili work which is an individual video streaming
    """
    cid: int                                    # cid of this page
    page: int                                   # Serial num of this page
    part: str                                   # Title of this page
    duration: int                               # Total seconds of this page
    vid: str                                    # Identifier of outside site video


class GetVideoInfoDataStaffItemVip(BaseModel):
    """
    Bilibili account's VIP status
    """
    vip_type: int = Field(..., alias='type')  # 0: No VIP; 1：Monthly VIP; 2: Yearly or superior VIP
    status: int                               # 0: No VIP; 1: Has VIP
    theme_type: int


class GetVideoInfoDataStaffItemOfficial(BaseModel):
    """
    Official meta info
    """
    # 0: unverified
    # 1: personal verified, famous UP
    # 2: personal verified, V
    # 3: organization verified, enterprise
    # 4: organization verified, organization
    # 5: organization verified, media
    # 6: organization verified, government
    # 7: personal verified, Live show host
    # 9: personal verified, Social KOL
    role: int
    title: str                                     # Title of role
    official_type: int = Field(..., alias='type')  # -1 as unverified, 0 as verified
    desc: str = ''                                 # Verification description


class GetVideoInfoDataStaffItem(BaseModel):
    """
    Bilibili account who participants in the work
    """
    mid: int                        # Identifier of user
    title: str                      # Name of user
    name: str                       # Nickname of user
    face: str                       # Profile icon's source URL
    vip: GetVideoInfoDataStaffItemVip
    official: GetVideoInfoDataStaffItemOfficial
    follower: int                   # Count of followers


class GetVideoInfoData(BaseModel):
    """
    only define necessary fields
    """
    aid: int                                   # AV ID of video
    bvid: str                                  # BV ID of video
    cid: int                                   # cid of video's 1P
    pic: str                                   # URL of video cover
    title: str                                 # Title of video
    desc: str                                  # legacy version video description
    pubdate: int                               # Unix timestamp when video published (audited)
    ctime: int                                 # Unix timestamp when video contributed
    duration: int                              # Total seconds of video
    staff: Optional[List[GetVideoInfoDataStaffItem]] = None
    owner: GetVideoInfoDataOwner
    pages: List[GetVideoInfoDataPagesItem]


class GetVideoInfoResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -400：request error
    -403：authentication limit
    -404：video unavailable
    62002：video invisible
    62004：video in review
    """
    data: Optional[GetVideoInfoData] = None
