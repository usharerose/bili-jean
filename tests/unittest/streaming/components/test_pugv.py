"""
Unit test for PUGVComponent
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.streaming.components.pugv import PUGVComponent
from bili_jean.streaming.streaming_service import StreamingCategory
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/pugv_view/pugv_view_ss6838.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ss2.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)


class PUGVComponentTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_by_not_exist_season_id(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_pages = PUGVComponent.get_views(season_id=2)
        self.assertIsNone(actual_pages)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_pages = PUGVComponent.get_views(season_id=6838)

        expected_length = 0
        expected_length += len(DATA_VIEW['data']['episodes'])

        self.assertEqual(len(actual_pages), expected_length)
        sample_actual_page, *_ = actual_pages

        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PUGV.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 1313813259)
        self.assertEqual(sample_actual_page.page_title, '马克思的哲学革命及其当代意义')
        self.assertEqual(sample_actual_page.page_duration, 239)
        self.assertEqual(sample_actual_page.view_aid, 277630557)
        self.assertIsNone(sample_actual_page.view_bvid)
        self.assertEqual(sample_actual_page.view_ep_id, 261830)
        self.assertEqual(sample_actual_page.view_season_id, 6838)
        self.assertEqual(sample_actual_page.view_title, '马克思的哲学革命及其当代意义')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'https://archive.biliimg.com/bfs/archive/caf0edf6f943c1f0d674a7620bb1bdaf8cbda2dd.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1698497411)
        self.assertEqual(sample_actual_page.view_duration, 239)
        self.assertEqual(sample_actual_page.view_owner_id, 514924891)
        self.assertEqual(sample_actual_page.view_owner_name, '王德峰')
        self.assertEqual(
            sample_actual_page.view_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/044a0dfa856d37b23eb87fdc4216745af38358b7.jpg'
        )
        self.assertIsNone(sample_actual_page.coll_id)
        self.assertIsNone(sample_actual_page.coll_title)
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertEqual(sample_actual_page.coll_owner_id, 514924891)
        self.assertEqual(sample_actual_page.coll_owner_name, '王德峰')
        self.assertEqual(
            sample_actual_page.coll_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/044a0dfa856d37b23eb87fdc4216745af38358b7.jpg'
        )
        self.assertEqual(sample_actual_page.coll_sect_id, 6838)
        self.assertEqual(sample_actual_page.coll_sect_title, '王德峰哲学课：马克思的哲学革命及其当代意义')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_connection_error(self, mocked_request):
        mocked_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /pugv/view/web/season?season_id=6838'
        )
        with self.assertRaises(ConnectionError):
            PUGVComponent.get_views(season_id=6838)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_timeout_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            PUGVComponent.get_views(season_id=6838)

    def test_get_views_without_params(self):
        with self.assertRaises(ValueError):
            PUGVComponent.get_views()
