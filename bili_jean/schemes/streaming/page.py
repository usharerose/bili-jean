"""
Scheme definition of normalized page
"""
from typing import Optional

from pydantic import BaseModel


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
    index: int
    cid: int
    title: str
    duration: int

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

    coll_szn_id: Optional[int] = None
    coll_szn_title: Optional[str] = None
    coll_szn_desc: Optional[str] = None
    coll_szn_cover_url: Optional[str] = None
    coll_szn_owner_id: Optional[int] = None
    coll_szn_owner_name: Optional[str] = None
    coll_szn_owner_avatar_url: Optional[str] = None

    coll_sect_id: Optional[int] = None
    coll_sect_title: Optional[str] = None

    coll_ep_id: Optional[int] = None
    coll_ep_title: Optional[str] = None
    coll_ep_desc: Optional[str] = None
    coll_ep_cover_url: Optional[str] = None
    coll_ep_pub_time: Optional[int] = None
    coll_ep_duration: Optional[int] = None

    is_relevant_page: bool = False                   # the page is requested one or relevant one
