"""
Base streaming component
"""
from abc import ABC, abstractmethod
from typing import Any, List, Optional

from ...schemes import Page


class AbstractStreamingComponent(ABC):

    @classmethod
    @abstractmethod
    def get_views(cls, *args: Any, **kwargs: Any) -> Optional[List[Page]]:
        """
        get normalized views info
        """
