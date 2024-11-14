"""
Unit test for StreamingService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import InvalidSchema, MissingSchema
from requests.structures import CaseInsensitiveDict

from bili_jean.constants import StreamingCategory
from bili_jean.schemes import Page
from bili_jean.streaming.streaming_service import StreamingService
from tests.utils import get_mocked_response


DATA_HTML = '<!DOCTYPE html><html lang="zh-Hans"></html>'


with open('tests/mock_data/proxy/pgc_view/pgc_view_ss12548.json', 'r') as fp:
    DATA_PGC_VIEW = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ep482484.json', 'r') as fp:
    DATA_PUGV_VIEW = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_BV1X54y1C74U.json', 'r') as fp:
    DATA_UGC_VIEW = json.load(fp)


class StreamingServiceParseWebViewURLTestCase(TestCase):

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


class StreamingServiceGetViewsTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_ugc_views(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV1X54y1C74U'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict({
                    'Location': (
                        '/video/BV1X54y1C74U/'
                    )
                })
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_UGC_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.UGC.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pgc_views(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/bangumi/play/ss12548'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict()
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_PGC_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pgc_views_by_url_with_bvid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV14W411g72d/'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict({
                    'Location': 'https://www.bilibili.com/bangumi/play/ep199612'
                })
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_PGC_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pugv_views(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/cheese/play/ep482484'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict()
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_PUGV_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PUGV.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_invalid_url(self, mocked_request):
        sample_url = 'ftp://mock_string'
        mocked_request.side_effect = InvalidSchema(
            'No connection adapters were found for \'ftp://mock_string\''
        )

        with self.assertRaises(ValueError):
            StreamingService.get_views(sample_url)
