"""
Components wrapper
"""
from typing import Callable, Dict

from ...constants import StreamingCategory
from .base import AbstractStreamingComponent


COMPONENTS_MAPPING: Dict[StreamingCategory, AbstractStreamingComponent] = {}


def register_component(streaming_category: StreamingCategory) -> Callable:

    def wrapper(klass: AbstractStreamingComponent) -> AbstractStreamingComponent:
        if streaming_category in COMPONENTS_MAPPING:
            raise ValueError(f'Category {streaming_category} has been registered')
        COMPONENTS_MAPPING[streaming_category] = klass
        return klass

    return wrapper
