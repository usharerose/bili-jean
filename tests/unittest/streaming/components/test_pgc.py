"""
Unit test for PGCComponent
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.streaming.components.pgc import PGCComponent
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
        expected_result = DATA_VIEW['result']
        sample_expected_episode, *_ = DATA_VIEW['result']['episodes']

        self.assertEqual(sample_actual_page.index, 1)
        self.assertEqual(sample_actual_page.cid, sample_expected_episode['cid'])
        self.assertEqual(sample_actual_page.title, sample_expected_episode['title'])
        self.assertEqual(sample_actual_page.duration, sample_expected_episode['duration'] // 1000)
        self.assertEqual(sample_actual_page.view_aid, sample_expected_episode['aid'])
        self.assertEqual(sample_actual_page.view_bvid, sample_expected_episode['bvid'])
        self.assertEqual(sample_actual_page.view_ep_id, sample_expected_episode['ep_id'])
        self.assertEqual(sample_actual_page.view_season_id, expected_result['season_id'])
        self.assertEqual(sample_actual_page.view_title, sample_expected_episode['long_title'])
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(sample_actual_page.view_cover_url, sample_expected_episode['cover'])
        self.assertEqual(sample_actual_page.view_pub_time, sample_expected_episode['pub_time'])
        self.assertEqual(sample_actual_page.view_duration, sample_expected_episode['duration'] // 1000)
        self.assertIsNone(sample_actual_page.view_owner_id)
        self.assertIsNone(sample_actual_page.view_owner_name)
        self.assertIsNone(sample_actual_page.view_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_szn_id, expected_result['series']['series_id'])
        self.assertEqual(sample_actual_page.coll_szn_title, expected_result['series']['series_title'])
        self.assertIsNone(sample_actual_page.coll_szn_desc)
        self.assertIsNone(sample_actual_page.coll_szn_cover_url)
        self.assertIsNone(sample_actual_page.coll_szn_owner_id)
        self.assertIsNone(sample_actual_page.coll_szn_owner_name)
        self.assertIsNone(sample_actual_page.coll_szn_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, expected_result['season_id'])
        self.assertEqual(sample_actual_page.coll_sect_title, expected_result['season_title'])
        self.assertEqual(sample_actual_page.coll_ep_id, sample_expected_episode['ep_id'])
        self.assertEqual(sample_actual_page.coll_ep_title, sample_expected_episode['title'])
        self.assertIsNone(sample_actual_page.coll_ep_desc)
        self.assertEqual(sample_actual_page.coll_ep_cover_url, sample_expected_episode['cover'])
        self.assertEqual(sample_actual_page.coll_ep_pub_time, sample_expected_episode['pub_time'])
        self.assertEqual(sample_actual_page.coll_ep_duration, sample_expected_episode['duration'] // 1000)
        self.assertTrue(sample_actual_page.is_relevant_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_up_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_UP_INFO).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(season_id=12548)
        sample_actual_page, *_ = actual_pages
        expected_result = DATA_VIEW_WITH_UP_INFO['result']

        self.assertEqual(sample_actual_page.view_owner_id, expected_result['up_info']['mid'])
        self.assertEqual(sample_actual_page.view_owner_name, expected_result['up_info']['uname'])
        self.assertEqual(sample_actual_page.view_owner_avatar_url, expected_result['up_info']['avatar'])
        self.assertEqual(sample_actual_page.coll_szn_owner_id, expected_result['up_info']['mid'])
        self.assertEqual(sample_actual_page.coll_szn_owner_name, expected_result['up_info']['uname'])
        self.assertEqual(sample_actual_page.coll_szn_owner_avatar_url, expected_result['up_info']['avatar'])

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
        There could be links of UGC resources as PGC's sidelights
        """
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_SECTION_WITH_UGC_EPISODE).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=249469)

        *_, sample_actual_page = actual_pages

        *_, sample_expected_section = DATA_VIEW_SECTION_WITH_UGC_EPISODE['result']['section']
        *_, sample_expected_episode = sample_expected_section['episodes']

        self.assertEqual(sample_actual_page.index, 1)
        self.assertIsNone(sample_actual_page.cid)
        self.assertEqual(sample_actual_page.title, sample_expected_episode['title'])
        self.assertIsNone(sample_actual_page.duration)
        self.assertEqual(sample_actual_page.view_aid, sample_expected_episode['aid'])
        self.assertIsNone(sample_actual_page.view_bvid)
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertEqual(sample_actual_page.view_title, '')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(sample_actual_page.view_cover_url, sample_expected_episode['cover'])
        self.assertIsNone(sample_actual_page.view_pub_time)
        self.assertIsNone(sample_actual_page.view_duration)
        self.assertIsNone(sample_actual_page.view_owner_id)
        self.assertIsNone(sample_actual_page.view_owner_name)
        self.assertIsNone(sample_actual_page.view_owner_avatar_url)
        self.assertIsNone(sample_actual_page.coll_szn_id)
        self.assertIsNone(sample_actual_page.coll_szn_title)
        self.assertIsNone(sample_actual_page.coll_szn_desc)
        self.assertIsNone(sample_actual_page.coll_szn_cover_url)
        self.assertIsNone(sample_actual_page.coll_szn_owner_id)
        self.assertIsNone(sample_actual_page.coll_szn_owner_name)
        self.assertIsNone(sample_actual_page.coll_szn_owner_avatar_url)
        self.assertIsNone(sample_actual_page.coll_sect_id)
        self.assertIsNone(sample_actual_page.coll_sect_title)
        self.assertIsNone(sample_actual_page.coll_ep_id)
        self.assertIsNone(sample_actual_page.coll_ep_title)
        self.assertIsNone(sample_actual_page.coll_ep_desc)
        self.assertIsNone(sample_actual_page.coll_ep_cover_url)
        self.assertIsNone(sample_actual_page.coll_ep_pub_time)
        self.assertIsNone(sample_actual_page.coll_ep_duration)
        self.assertFalse(sample_actual_page.is_relevant_page)

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
