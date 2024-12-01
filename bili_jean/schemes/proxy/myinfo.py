"""
Scheme definition of the response from https://api.bilibili.com/x/space/myinfo
"""
from typing import Optional

from pydantic import BaseModel

from .base import BaseResponseModel


class GetMyInfoData(BaseModel):

    mid: int
    name: str
    face: str
    sign: str


class GetMyInfoResponse(BaseResponseModel):
    """
    On 'code' field,

    0：success, and has 'data'
    -101：not login
    """
    data: Optional[GetMyInfoData] = None
