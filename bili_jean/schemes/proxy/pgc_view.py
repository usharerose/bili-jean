"""
Scheme definition of the response from https://api.bilibili.com/pgc/view/web/season
"""
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponseModel


class GetPGCViewResultEpisodesItemBadgeInfo(BaseModel):

    bg_color: str        # color hex
    bg_color_night: str  # color hex
    text: str = ''       # text of badge, e.g. '会员', '减免'


class GetPGCViewResultEpisodesItem(BaseModel):
    """
    metadata of the episode in current season
    """
    aid: int                                           # AV ID of episode
    badge_info: GetPGCViewResultEpisodesItemBadgeInfo  # badge of episode
    bvid: str                                          # BV ID of episode
    cid: int                                           # cid of episode
    cover: str                                         # URL of episode cover
    duration: int                                      # Total seconds of the episode
    ep_id: int                                         # Identifier of the episode
    id_field: int = Field(..., alias='id')             # ep_id
    link: str                                          # URL of the episode
    long_title: str                                    # supplement of episode title
    pub_time: int                                      # Unix timestamp when the episode published
    title: str                                         # Title of the episode


class GetPGCViewResultSeasonsItem(BaseModel):
    """
    season metadata
    """
    badge_info: GetPGCViewResultEpisodesItemBadgeInfo  # badge of the season
    cover: str                                         # URL of season cover
    media_id: int                                      # Identifier of the season media
    season_id: int                                     # Identifier of this season
    season_title: str                                  # Title of the season


class GetPGCViewResultSectionItem(BaseModel):
    """
    side stories section of the season
    """
    episodes: List[GetPGCViewResultEpisodesItem]             # section episodes
    id_field: int = Field(..., alias='id')                   # Identifier of the section
    title: str                                               # Section title


class GetPGCViewResultUPInfo(BaseModel):
    """
    UP metadata
    """
    avatar: str  # Profile icon's source URL
    mid: int     # User ID
    uname: str   # User name


class GetPGCViewResultSeries(BaseModel):
    """
    series metadata which the season belongs to
    """
    series_id: int     # Identifier of the series, could be 0 if no series
    series_title: str  # Name of the series, could be '' if no series


class GetPGCViewResult(BaseModel):
    """
    'result' field, only defines part of necessary fields
    """
    cover: str                                                   # URL of season (bangumi) cover
    episodes: List[GetPGCViewResultEpisodesItem]                 # Episodes
    evaluate: str                                                # Season evaluate description
    link: str                                                    # Link of season abstract
    media_id: int                                                # Identifier of this season media
    season_id: int                                               # Identifier of this season
    season_title: str                                            # Title of the season
    # All of seasons metadata of one series
    # could be empty if only one season which is the current one
    seasons: List[GetPGCViewResultSeasonsItem]
    section: Optional[List[GetPGCViewResultSectionItem]] = None  # side stories of the season
    series: GetPGCViewResultSeries                               # metadata of the series
    title: str                                                   # title of the season
    # type of the season
    # 1：bangumi
    # 2：movie
    # 3：documentary
    # 4：Chinese bangumi
    # 5：TV play
    # 7：variety
    type_field: int = Field(..., alias='type')
    up_info: Optional[GetPGCViewResultUPInfo] = None             # UP info if exists


class GetPGCViewResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -404：video unavailable
    """
    result: Optional[GetPGCViewResult] = None
