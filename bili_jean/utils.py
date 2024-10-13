"""
Common utilities
"""
import re


BVID_LENGTH = 9
MAX_AID = 1 << 51
VIDEO_URL_BV_PATTERN = re.compile(fr'/video/(BV1[a-zA-Z0-9]{{{BVID_LENGTH}}})/?')
VIDEO_URL_AV_PATTERN = re.compile(r'/video/av(\d+)/?')


def parse_aid(url: str) -> int:
    """
    parse AV ID from URL namespace
    """
    search_result = VIDEO_URL_AV_PATTERN.search(url)
    if search_result is None:
        raise ValueError('Given URL doesn\'t contains AV ID namespace')

    aid = 0
    aid_string = search_result.group(1)
    for item in aid_string:
        val = int(item)
        if aid > (MAX_AID - val) // 10:
            raise ValueError('Given AV ID exceeds the limit')
        aid = aid * 10 + val
    return aid


def parse_bvid(url: str) -> str:
    """
    parse BV ID from URL namespace
    """
    search_result = VIDEO_URL_BV_PATTERN.search(url)
    if search_result is None:
        raise ValueError('Given URL doesn\'t contains valid BV ID')
    return search_result.group(1)
