"""
Components on streaming resource manipulation
"""
from ...constants import StreamingCategory
from .base import AbstractStreamingComponent
from .pgc import PGCComponent  # NOQA
from .pugv import PUGVComponent  # NOQA
from .ugc import UGCComponent  # NOQA
from .wrapper import COMPONENTS_MAPPING


def get_streaming_component_kls(
    streaming_category: StreamingCategory
) -> AbstractStreamingComponent:
    component_kls = COMPONENTS_MAPPING.get(streaming_category)
    if component_kls is None:
        raise ValueError(
            f'Unregistered component for {streaming_category}'
        )
    return component_kls
