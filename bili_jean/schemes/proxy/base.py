"""
Scheme definition of the Bilibili API response
"""
from typing import Optional

from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    """
    Base of Bilibili API response
    """
    code: int = 0              # status code
    message: str = '0'         # error message
    ttl: Optional[int] = None
