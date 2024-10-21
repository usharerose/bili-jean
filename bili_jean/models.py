"""
Model of Bilibili data
"""
from typing import List, Optional, Union

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


class GetVideoInfoDataUGCSeasonSectionsItemEpisodesItemARC(BaseModel):
    """
    episode video info
    """
    aid: int       # AV ID of video
    pic: str       # URL of episode cover
    title: str     # Title of episode
    pubdate: int   # Unix timestamp when video published (audited)
    ctime: int     # Unix timestamp when video contributed
    desc: str      # legacy version episode description
    duration: int  # Total seconds of episode


class GetVideoInfoDataUGCSeasonSectionsItemEpisodesItem(BaseModel):
    """
    Video info
    """
    season_id: int                          # season ID
    section_id: int                         # Section ID
    id_field: int = Field(..., alias='id')  # episode ID, which links to a video
    title: str                              # episode title
    aid: int                                # AV ID of video
    bvid: str                               # BV ID of video
    cid: int                                # cid of video's 1P
    arc: GetVideoInfoDataUGCSeasonSectionsItemEpisodesItemARC
    page: GetVideoInfoDataPagesItem
    pages: List[GetVideoInfoDataPagesItem]


class GetVideoInfoDataUGCSeasonSectionsItem(BaseModel):
    """
    Video section
    """
    season_id: int                          # season ID
    id_field: int = Field(..., alias='id')  # section ID
    title: str                              # section title
    episodes: List[GetVideoInfoDataUGCSeasonSectionsItemEpisodesItem]


class GetVideoInfoDataUGCSeason(BaseModel):
    """
    season and episode info
    """
    id_field: int = Field(..., alias='id')  # season ID
    title: str                              # season title
    cover: str                              # URL of season cover
    mid: int                                # Identifier of user
    intro: str                              # Introduction of the season
    ep_count: int                           # Count of episodes
    sections: List[GetVideoInfoDataUGCSeasonSectionsItem]


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
    is_season_display: bool                    # be included in season or not
    ugc_season: Optional[GetVideoInfoDataUGCSeason] = None


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


class WorkOwner(BaseModel):
    """
    metadata of work's owner
    """
    account_id: int  # Identifier of user
    name: str        # Nickname of user
    avatar_url: str  # Profile icon's source URL


class WorkPage(BaseModel):
    """
    normalized Bilibili work page with necessary metadata
    """
    aid: Optional[int] = None
    bvid: Optional[str] = None
    cid: int                                       # cid of this page
    page_url: str
    page_title: str
    duration: Optional[int]                        # unit is second

    season_id: Optional[int] = None
    season_name: Optional[str] = None
    season_cover_url: Optional[str] = None
    season_owner_id: Optional[int] = None
    season_owner_name: Optional[str] = None
    season_owner_avatar_url: Optional[str] = None

    section_id: Optional[int] = None
    section_name: Optional[str] = None
    episode_id: Optional[int] = None
    episode_name: Optional[str] = None

    work_url: Optional[str] = None
    work_title: Optional[str] = None
    work_description: Optional[str] = None
    work_cover_url: str
    work_owner_id: Optional[int] = None
    work_owner_name: Optional[str] = None
    work_owner_avatar_url: Optional[str] = None


class GetVideoStreamDataDashMediaItem(BaseModel):
    """
    media data
    """
    id_field: int = Field(..., alias='id')
    base_url: str
    backup_url: List[str]
    bandwidth: int                          # minimum of network bandwidth that needed
    mime_type: str
    codecid: int
    codecs: str
    width: int                              # 0 for audio
    height: int                             # 0 for audio


class GetVideoStreamDataDashFlac(BaseModel):
    """
    Hi-Res audio data
    """
    display: bool                                            # illustrate Hi-Res or not
    audio: Optional[GetVideoStreamDataDashMediaItem] = None


class GetVideoStreamDataDashDolby(BaseModel):
    """
    Dolby audio data
    """
    # 1 is normal, 2 is panoramic
    # for cheese, could be 'NONE'
    type_field: Union[int, str] = Field(..., alias='type')
    audio: Optional[List[GetVideoStreamDataDashMediaItem]] = None


class GetVideoStreamDataDash(BaseModel):
    """
    DASH data
    """
    audio: Optional[List[GetVideoStreamDataDashMediaItem]] = None  # null when video has no audio
    flac: Optional[GetVideoStreamDataDashFlac] = None
    dolby: GetVideoStreamDataDashDolby
    video: List[GetVideoStreamDataDashMediaItem]
    duration: int                                                  # second


class GetVideoStreamDataDURLItem(BaseModel):
    """
    common video stream data
    """
    order: int
    length: int
    size: int              # size of video, unit is byte
    url: str
    backup_url: List[str]


class GetVideoStreamDataSupportFormatsItem(BaseModel):
    """
    supported video qualities
    """
    quality: int
    new_description: str
    format_field: str = Field(..., alias='format')
    display_desc: str
    codecs: Optional[List[str]]


class GetVideoStreamData(BaseModel):
    """
    only define necessary fields
    """
    dash: Optional[GetVideoStreamDataDash] = None
    durl: Optional[List[GetVideoStreamDataDURLItem]] = None
    quality: int
    support_formats: List[GetVideoStreamDataSupportFormatsItem]


class GetVideoStreamResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -400：request error
    -404：video unavailable
    """
    data: Optional[GetVideoStreamData] = None


class GetUserInfoVIP(BaseModel):
    """
    VIP status of user
    """
    vip_type: int = Field(..., alias='type')  # 0: No VIP; 1：Monthly VIP; 2: Yearly or superior VIP
    status: int                               # 0: No VIP; 1: Has VIP
    theme_type: int


class GetUserInfoData(BaseModel):
    """
    only define necessary fields
    """
    mid: int             # User ID
    name: str            # User name
    face: str            # Profile icon's source URL
    vip: GetUserInfoVIP


class GetUserInfoResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -101：not login
    """
    data: Optional[GetUserInfoData] = None


class GetUserCardDataCard(BaseModel):
    """
    User card with basic user info
    only define necessary fields
    """
    mid: int       # type is string in source, convert to integer here
    name: str
    approve: bool
    sex: str
    rank: str
    face: str


class GetUserCardDataSpace(BaseModel):
    """
    space photo URLs
    """
    s_img: str  # small size image's URL
    l_img: str  # large size image's URL


class GetUserCardData(BaseModel):
    """
    data of user card
    """
    card: GetUserCardDataCard
    space: Optional[GetUserCardDataSpace] = None
    following: bool
    archive_count: int
    article_count: int
    follower: int
    like_num: int


class GetUserCardResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -400：request error
    """
    data: Optional[GetUserCardData] = None
