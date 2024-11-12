"""
Unit test for StreamingService
"""
from http import HTTPStatus
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import InvalidSchema, MissingSchema
from requests.structures import CaseInsensitiveDict

from bili_jean.streaming.streaming_service import StreamingCategory, StreamingService
from tests.utils import get_mocked_response


DATA_HTML = '<!DOCTYPE html><html lang="zh-Hans"></html>'


class StreamingServiceTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_ugc_url_with_bvid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV1tN4y1F79k?'
            'vd_source=eab9f46166d54e0b07ace25e908097ae&'
            'spm_id_from=333.788.videopod.sections'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict({
                'Location': (
                    '/video/BV1tN4y1F79k?'
                    'vd_source=eab9f46166d54e0b07ace25e908097ae&'
                    'spm_id_from=333.788.videopod.sections'
                )
            })
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.UGC)
        self.assertIsNone(actual_dm.aid)
        self.assertEqual(actual_dm.bvid, 'BV1tN4y1F79k')
        self.assertIsNone(actual_dm.ep_id)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_ugc_url_with_aid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/av2271112/?'
            'vd_source=eab9f46166d54e0b07ace25e908097ae'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.UGC)
        self.assertEqual(actual_dm.aid, 2271112)
        self.assertIsNone(actual_dm.bvid)
        self.assertIsNone(actual_dm.ep_id)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_season_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/bangumi/play/ss357?'
            'from_spmid=666.25.series.0'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertIsNone(actual_dm.ep_id)
        self.assertEqual(actual_dm.season_id, 357)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_ep_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/bangumi/play/ep249470?'
            'from_spmid=666.25.episode.0'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 249470)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_bvid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV1tL4y1i7UZ/'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict({
                'Location': 'https://www.bilibili.com/bangumi/play/ep249470'
            })
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 249470)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_aid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/av31703892/'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict({
                'Location': 'https://www.bilibili.com/bangumi/play/ep249469'
            })
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 249469)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_url_with_season_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/cheese/play/ss13194'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PUGV)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertIsNone(actual_dm.ep_id)
        self.assertEqual(actual_dm.season_id, 13194)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_url_with_ep_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/cheese/play/ep482484'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PUGV)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 482484)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_non_url_input(self, mocked_request):
        mocked_request.side_effect = MissingSchema(
            'Invalid URL \'something\': No scheme supplied. Perhaps you meant https://mock_string?'
        )

        sample_url = 'mock_string'
        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertIsNone(actual_dm)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_invalid_url(self, mocked_request):
        mocked_request.side_effect = InvalidSchema(
            'No connection adapters were found for \'ftp://mock_string\''
        )

        sample_url = 'ftp://mock_string'
        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertIsNone(actual_dm)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_invalid_url_but_contains_path(self, mocked_request):
        mocked_request.side_effect = MissingSchema(
            'Invalid URL \'/video/BV1tN4y1F79k\': '
            'No scheme supplied. Perhaps you meant https:///video/BV1tN4y1F79k?'
        )

        sample_url = '/video/BV1tN4y1F79k'
        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.UGC)
        self.assertIsNone(actual_dm.aid)
        self.assertEqual(actual_dm.bvid, 'BV1tN4y1F79k')
        self.assertIsNone(actual_dm.ep_id)
        self.assertIsNone(actual_dm.season_id)
