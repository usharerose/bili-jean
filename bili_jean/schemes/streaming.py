"""
Scheme definition of streaming objects
"""
from typing import Optional

from pydantic import BaseModel

from ..constants import StreamingCategory


class Page(BaseModel):
    """
    Normalized page model,
    which is the finest granularity of resource
    * UGC: page of a UGC video
    * PUGC: episode of a bangumi
    * cheese: episode of a cheese

    the page could be the requested one,
    or relevant collections' pages
    """
    page_category: str
    page_index: int = 1
    page_cid: int
    page_title: str                              # Normalized title for display
    page_duration: int                           # Total seconds of the page

    view_aid: Optional[int] = None
    view_bvid: Optional[str] = None
    view_ep_id: Optional[int] = None
    view_season_id: Optional[int] = None

    view_title: Optional[str] = None
    view_desc: Optional[str] = None
    view_cover_url: Optional[str] = None
    view_pub_time: Optional[int] = None
    view_duration: Optional[int] = None
    view_owner_id: Optional[int] = None
    view_owner_name: Optional[str] = None
    view_owner_avatar_url: Optional[str] = None

    coll_id: Optional[int] = None
    coll_title: Optional[str] = None
    coll_desc: Optional[str] = None
    coll_cover_url: Optional[str] = None
    coll_owner_id: Optional[int] = None
    coll_owner_name: Optional[str] = None
    coll_owner_avatar_url: Optional[str] = None

    coll_sect_id: Optional[int] = None
    coll_sect_title: Optional[str] = None

    is_selected_page: bool                       # the page is requested one or relevant one


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
