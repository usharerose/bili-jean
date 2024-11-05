"""
Scheme definition of the response from https://api.bilibili.com/pugv/view/web/season
"""
from typing import List, Optional

from pydantic import BaseModel, Field

from .base import BaseResponseModel


class GetPUGVViewDataBriefImgItem(BaseModel):
    """
    course introduction image
    """
    aspect_ratio: float
    url: str             # URL of poster image


class GetPUGVViewDataBrief(BaseModel):
    """
    course brief introduction posters
    """
    content: str = ''
    img: List[GetPUGVViewDataBriefImgItem]                 # poster images
    title: str                                             # default is '课程概述'
    type_field: int = Field(default=2, alias='type')


class GetPUGVViewDataEpisodesItem(BaseModel):
    """
    course episode
    """
    aid: int                                                    # AV ID of the episode
    cid: int                                                    # cid of episode
    cover: str                                                  # URL of the cover
    duration: int                                               # unit is second
    ep_status: int
    episode_can_view: bool                                      # visibility
    from_field: str = Field(default='pugv', alias='from')
    id_field: int = Field(..., alias='id')                      # ep_id
    index: int                                                  # index of the episode in the series
    label: Optional[str] = None                                 # label of the episode
    page: int
    release_date: int                                           # Unix timestamp when published
    # episode privilege
    # 1: watchable
    # 2: unwatchable
    # 3: part is watchable
    status: int
    subtitle: str
    title: str


class GetPUGVViewDataUPInfo(BaseModel):
    """
    UP metadata
    """
    avatar: str  # Profile icon's source URL
    mid: int     # User ID
    uname: str   # User name


class GetPUGVViewData(BaseModel):
    """
    'data' field, only defines part of necessary fields
    """
    brief: GetPUGVViewDataBrief
    cover: str                                   # URL of cheese cover
    episodes: List[GetPUGVViewDataEpisodesItem]  # Episodes
    season_id: int                               # Identifier of this season
    subtitle: str
    title: str
    up_info: GetPUGVViewDataUPInfo               # UP info if exists


class GetPUGVViewResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -404：video unavailable
    """
    data: Optional[GetPUGVViewData] = None
