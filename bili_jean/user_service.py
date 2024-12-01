"""
Service component on user
"""
import logging
from typing import Optional

from .proxy_service import ProxyService


logger = logging.getLogger(__name__)


class UserService:

    @classmethod
    def validate(cls, sess_data: Optional[str] = None) -> bool:
        """
        check sess_data validity
        :param sess_data: cookie of Bilibili user, SESSDATA
        :type sess_data: str, optional
        :return: bool
        """
        data = ProxyService.get_my_info(sess_data=sess_data)
        if data.code == 0:
            return True
        logger.error(f'User validation failed: {data.message}')
        return False
