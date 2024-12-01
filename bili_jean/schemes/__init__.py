"""
Scheme definitions of the cross-project objects
"""
from .proxy.base import DashMediaItem  # NOQA
from .proxy.card import GetCardResponse  # NOQA
from .proxy.myinfo import GetMyInfoResponse  # NOQA
from .proxy.pgc_play import GetPGCPlayResponse  # NOQA
from .proxy.pgc_view import GetPGCViewResponse  # NOQA
from .proxy.pugv_play import GetPUGVPlayResponse  # NOQA
from .proxy.pugv_view import GetPUGVViewResponse  # NOQA
from .proxy.ugc_play import GetUGCPlayResponse  # NOQA
from .proxy.ugc_view import GetUGCViewResponse  # NOQA
from .streaming import (  # NOQA
    AudioStreamingSourceMeta,
    Page,
    StreamingWebViewMeta,
    VideoStreamingSourceMeta
)
