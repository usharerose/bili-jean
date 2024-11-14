"""
Unit test for PGCComponent
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.streaming.components.pgc import PGCComponent
from bili_jean.streaming.streaming_service import StreamingCategory
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/pgc_view/pgc_view_ep232465.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/pgc_view/pgc_view_ep1.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/pgc_view/pgc_view_ss12548.json', 'r') as fp:
    DATA_VIEW_WITH_UP_INFO = json.load(fp)
with open('tests/mock_data/proxy/pgc_view/pgc_view_ep284310.json', 'r') as fp:
    DATA_VIEW_WITHOUT_SEASONS = json.load(fp)
with open('tests/mock_data/proxy/pgc_view/pgc_view_ep815604.json', 'r') as fp:
    DATA_VIEW_WITHOUT_SECTION = json.load(fp)
with open('tests/mock_data/proxy/pgc_view/pgc_view_ep249469.json', 'r') as fp:
    DATA_VIEW_SECTION_WITH_UGC_EPISODE = json.load(fp)


class PGCComponentTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_by_not_exist_ep_id(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=1)
        self.assertIsNone(actual_pages)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=232465)

        expected_length = 0
        expected_length += len(DATA_VIEW['result']['episodes'])
        for section in DATA_VIEW['result']['section']:
            expected_length += len(section['episodes'])

        self.assertEqual(len(actual_pages), expected_length)
        sample_actual_page, *_ = actual_pages

        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 49053680)
        self.assertEqual(sample_actual_page.page_title, '1 肺炎链球菌')
        self.assertEqual(sample_actual_page.page_duration, 1421)
        self.assertEqual(sample_actual_page.view_aid, 26361000)
        self.assertEqual(sample_actual_page.view_bvid, 'BV1as411p7ae')
        self.assertEqual(sample_actual_page.view_ep_id, 232465)
        self.assertEqual(sample_actual_page.view_season_id, 24588)
        self.assertEqual(sample_actual_page.view_title, '1 肺炎链球菌')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i0.hdslb.com/bfs/archive/18f237427319864f1074b0fb48c31a7b47bafb35.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1530981000)
        self.assertEqual(sample_actual_page.view_duration, 1421)
        self.assertIsNone(sample_actual_page.view_owner_id)
        self.assertIsNone(sample_actual_page.view_owner_name)
        self.assertIsNone(sample_actual_page.view_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_id, 4034)
        self.assertEqual(sample_actual_page.coll_title, '工作细胞')
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertIsNone(sample_actual_page.coll_owner_id)
        self.assertIsNone(sample_actual_page.coll_owner_name)
        self.assertIsNone(sample_actual_page.coll_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, 24588)
        self.assertEqual(sample_actual_page.coll_sect_title, '工作细胞')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_up_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_UP_INFO).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(season_id=12548)
        sample_actual_page, *_ = actual_pages

        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 34568185)
        self.assertEqual(sample_actual_page.page_title, '普通话')
        self.assertEqual(sample_actual_page.page_duration, 7598)
        self.assertEqual(sample_actual_page.view_aid, 21071819)
        self.assertEqual(sample_actual_page.view_bvid, 'BV14W411g72d')
        self.assertEqual(sample_actual_page.view_ep_id, 199612)
        self.assertEqual(sample_actual_page.view_season_id, 12548)
        self.assertEqual(sample_actual_page.view_title, '普通话')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i0.hdslb.com/bfs/archive/96a3cd3740536a5b36635f5e6a423f9f0365e698.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1522398180)
        self.assertEqual(sample_actual_page.view_duration, 7598)
        self.assertEqual(
            sample_actual_page.view_owner_id,
            15773384
        )
        self.assertEqual(
            sample_actual_page.view_owner_name,
            '哔哩哔哩电影'
        )
        self.assertEqual(
            sample_actual_page.view_owner_avatar_url,
            'https://i2.hdslb.com/bfs/face/d21a82eb5738155b2b99b5f6102e054e2e0d0700.jpg'
        )
        self.assertEqual(sample_actual_page.coll_id, 4971)
        self.assertEqual(sample_actual_page.coll_title, '民国三部曲')
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertEqual(
            sample_actual_page.coll_owner_id,
            15773384
        )
        self.assertEqual(
            sample_actual_page.coll_owner_name,
            '哔哩哔哩电影'
        )
        self.assertEqual(
            sample_actual_page.coll_owner_avatar_url,
            'https://i2.hdslb.com/bfs/face/d21a82eb5738155b2b99b5f6102e054e2e0d0700.jpg'
        )
        self.assertEqual(sample_actual_page.coll_sect_id, 12548)
        self.assertEqual(sample_actual_page.coll_sect_title, '让子弹飞')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_without_section(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITHOUT_SECTION).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=815604)

        expected_length = 0
        expected_length += len(DATA_VIEW_WITHOUT_SECTION['result']['episodes'])
        for section in DATA_VIEW_WITHOUT_SECTION['result'].get('section', []):
            expected_length += len(section['episodes'])

        self.assertEqual(len(actual_pages), expected_length)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_ugc_episode_in_section(self, mocked_request):
        """
        There could be links of UGC resources as PGC's sidelights, which would be ignored
        """
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_SECTION_WITH_UGC_EPISODE).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=249469)

        resources_length = 0
        resources_length += len(DATA_VIEW_SECTION_WITH_UGC_EPISODE['result']['episodes'])
        for section in DATA_VIEW_SECTION_WITH_UGC_EPISODE['result']['section']:
            resources_length += len(section['episodes'])
        self.assertTrue(len(actual_pages) < resources_length)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_connection_error(self, mocked_request):
        mocked_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /pgc/view/web/season?ep_id=232465'
        )
        with self.assertRaises(ConnectionError):
            PGCComponent.get_views(ep_id=232465)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_timeout_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            PGCComponent.get_views(ep_id=232465)

    def test_get_views_without_params(self):
        with self.assertRaises(ValueError):
            PGCComponent.get_views()
