"""
Scheme definition of the response from https://api.bilibili.com/x/web-interface/card
"""
from typing import Optional

from pydantic import BaseModel

from .base import BaseResponseModel


class GetCardDataCard(BaseModel):

    mid: int   # type is string in source, convert to integer here
    name: str
    face: str
    sign: str


class GetCardData(BaseModel):

    card: GetCardDataCard
    following: bool
    follower: int


class GetCardResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -400：request error
    """
    data: Optional[GetCardData] = None
