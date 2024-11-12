"""
Unit test for UGCComponent
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.streaming.components import UGCComponent
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/ugc_view/ugc_view_BV1X54y1C74U.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_notexistbvid.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_BV1tN4y1F79k.json', 'r') as fp:
    DATA_VIEW_WITH_SEASON = json.load(fp)


class UGCComponentTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_by_not_exist_bvid(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_pages = UGCComponent.get_views(bvid='notexistbvid')
        self.assertIsNone(actual_pages)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_pages = UGCComponent.get_views(bvid='BV1X54y1C74U')

        self.assertEqual(len(actual_pages), 1)
        sample_actual_page, *_ = actual_pages
        expected_data = DATA_VIEW['data']
        sample_expected_page, *_ = DATA_VIEW['data']['pages']

        self.assertEqual(sample_actual_page.index, sample_expected_page['page'])
        self.assertEqual(sample_actual_page.cid, sample_expected_page['cid'])
        self.assertEqual(sample_actual_page.title, sample_expected_page['part'])
        self.assertEqual(sample_actual_page.duration, sample_expected_page['duration'])
        self.assertEqual(sample_actual_page.view_aid, expected_data['aid'])
        self.assertEqual(sample_actual_page.view_bvid, expected_data['bvid'])
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertEqual(sample_actual_page.view_title, expected_data['title'])
        self.assertEqual(sample_actual_page.view_desc, expected_data['desc'])
        self.assertEqual(sample_actual_page.view_cover_url, expected_data['pic'])
        self.assertEqual(sample_actual_page.view_pub_time, expected_data['pubdate'])
        self.assertEqual(sample_actual_page.view_duration, expected_data['duration'])
        self.assertEqual(sample_actual_page.view_owner_id, expected_data['owner']['mid'])
        self.assertEqual(sample_actual_page.view_owner_name, expected_data['owner']['name'])
        self.assertEqual(sample_actual_page.view_owner_avatar_url, expected_data['owner']['face'])
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
    def test_get_views_with_season(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_pages = UGCComponent.get_views(bvid='BV1tN4y1F79k')

        self.assertEqual(len(actual_pages), 2)
        sample_actual_page, *_ = actual_pages
        expected_data = DATA_VIEW_WITH_SEASON['data']
        sample_expected_page, *_ = DATA_VIEW_WITH_SEASON['data']['pages']
        sample_expected_season = DATA_VIEW_WITH_SEASON['data']['ugc_season']
        sample_expected_section, *_ = sample_expected_season['sections']
        sample_expected_episode, *_ = sample_expected_section['episodes']

        self.assertEqual(sample_actual_page.index, sample_expected_page['page'])
        self.assertEqual(sample_actual_page.cid, sample_expected_page['cid'])
        self.assertEqual(sample_actual_page.title, sample_expected_page['part'])
        self.assertEqual(sample_actual_page.duration, sample_expected_page['duration'])
        self.assertEqual(sample_actual_page.view_aid, expected_data['aid'])
        self.assertEqual(sample_actual_page.view_bvid, expected_data['bvid'])
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertEqual(sample_actual_page.view_title, expected_data['title'])
        self.assertEqual(sample_actual_page.view_desc, expected_data['desc'])
        self.assertEqual(sample_actual_page.view_cover_url, expected_data['pic'])
        self.assertEqual(sample_actual_page.view_pub_time, expected_data['pubdate'])
        self.assertEqual(sample_actual_page.view_duration, expected_data['duration'])
        self.assertEqual(sample_actual_page.view_owner_id, expected_data['owner']['mid'])
        self.assertEqual(sample_actual_page.view_owner_name, expected_data['owner']['name'])
        self.assertEqual(sample_actual_page.view_owner_avatar_url, expected_data['owner']['face'])
        self.assertEqual(sample_actual_page.coll_szn_id, sample_expected_season['id'])
        self.assertEqual(sample_actual_page.coll_szn_title, sample_expected_season['title'])
        self.assertEqual(sample_actual_page.coll_szn_desc, sample_expected_season['intro'])
        self.assertEqual(sample_actual_page.coll_szn_cover_url, sample_expected_season['cover'])
        self.assertEqual(sample_actual_page.coll_szn_owner_id, sample_expected_season['mid'])
        self.assertIsNone(sample_actual_page.coll_szn_owner_name)
        self.assertIsNone(sample_actual_page.coll_szn_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, sample_expected_section['id'])
        self.assertEqual(sample_actual_page.coll_sect_title, sample_expected_section['title'])
        self.assertEqual(sample_actual_page.coll_ep_id, sample_expected_episode['id'])
        self.assertEqual(sample_actual_page.coll_ep_title, sample_expected_episode['title'])
        self.assertEqual(sample_actual_page.coll_ep_desc, sample_expected_episode['arc']['desc'])
        self.assertEqual(sample_actual_page.coll_ep_cover_url, sample_expected_episode['arc']['pic'])
        self.assertEqual(sample_actual_page.coll_ep_pub_time, sample_expected_episode['arc']['pubdate'])
        self.assertEqual(sample_actual_page.coll_ep_duration, sample_expected_episode['arc']['duration'])
        self.assertFalse(sample_actual_page.is_relevant_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_relevant_views_in_season(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_pages = UGCComponent.get_views(bvid='BV1tN4y1F79k')

        self.assertEqual(len(actual_pages), 2)
        *_, sample_actual_page = actual_pages
        sample_expected_season = DATA_VIEW_WITH_SEASON['data']['ugc_season']
        *_, sample_expected_section = sample_expected_season['sections']
        *_, sample_expected_episode = sample_expected_section['episodes']
        *_, sample_expected_page = sample_expected_episode['pages']

        self.assertEqual(sample_actual_page.index, sample_expected_page['page'])
        self.assertEqual(sample_actual_page.cid, sample_expected_page['cid'])
        self.assertEqual(sample_actual_page.title, sample_expected_page['part'])
        self.assertEqual(sample_actual_page.duration, sample_expected_page['duration'])
        self.assertEqual(sample_actual_page.view_aid, sample_expected_episode['aid'])
        self.assertEqual(sample_actual_page.view_bvid, sample_expected_episode['bvid'])
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertIsNone(sample_actual_page.view_title)
        self.assertIsNone(sample_actual_page.view_desc)
        self.assertIsNone(sample_actual_page.view_cover_url)
        self.assertIsNone(sample_actual_page.view_pub_time)
        self.assertIsNone(sample_actual_page.view_duration)
        self.assertIsNone(sample_actual_page.view_owner_id)
        self.assertIsNone(sample_actual_page.view_owner_name)
        self.assertIsNone(sample_actual_page.view_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_szn_id, sample_expected_season['id'])
        self.assertEqual(sample_actual_page.coll_szn_title, sample_expected_season['title'])
        self.assertEqual(sample_actual_page.coll_szn_desc, sample_expected_season['intro'])
        self.assertEqual(sample_actual_page.coll_szn_cover_url, sample_expected_season['cover'])
        self.assertEqual(sample_actual_page.coll_szn_owner_id, sample_expected_season['mid'])
        self.assertIsNone(sample_actual_page.coll_szn_owner_name)
        self.assertIsNone(sample_actual_page.coll_szn_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, sample_expected_section['id'])
        self.assertEqual(sample_actual_page.coll_sect_title, sample_expected_section['title'])
        self.assertEqual(sample_actual_page.coll_ep_id, sample_expected_episode['id'])
        self.assertEqual(sample_actual_page.coll_ep_title, sample_expected_episode['title'])
        self.assertEqual(sample_actual_page.coll_ep_desc, sample_expected_episode['arc']['desc'])
        self.assertEqual(sample_actual_page.coll_ep_cover_url, sample_expected_episode['arc']['pic'])
        self.assertEqual(sample_actual_page.coll_ep_pub_time, sample_expected_episode['arc']['pubdate'])
        self.assertEqual(sample_actual_page.coll_ep_duration, sample_expected_episode['arc']['duration'])
        self.assertTrue(sample_actual_page.is_relevant_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_connection_error(self, mocked_request):
        mocked_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /x/web-interface/view?bvid=BV1X54y1C74U'
        )
        with self.assertRaises(ConnectionError):
            UGCComponent.get_views(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_timeout_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            UGCComponent.get_views(bvid='BV1X54y1C74U')

    def test_get_views_without_params(self):
        with self.assertRaises(ValueError):
            UGCComponent.get_views()
