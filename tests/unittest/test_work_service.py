"""
Unit test for VideoService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.work_service import WorkService
from tests.utils import get_mocked_response


with open('tests/data/video_info_BV1X54y1C74U.json', 'r') as fp:
    DATA = json.load(fp)
with open('tests/data/video_info_BV1tN4y1F79k.json', 'r') as fp:
    DATA_WITH_SEASON = json.load(fp)


class VideoServiceTestCase(TestCase):

    def setUp(self):
        self.sample_url = 'https://www.bilibili.com/video/BV1X54y1C74U'

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )

        work_pages = WorkService.get_work_meta(self.sample_url)
        self.assertEqual(len(work_pages), 1)

        dm, *_ = work_pages
        expected_sample_page, *_ = DATA['data']['pages']

        self.assertEqual(dm.work_url, self.sample_url)
        self.assertEqual(dm.work_title, DATA['data']['title'])
        self.assertEqual(dm.work_description, DATA['data']['desc'])
        self.assertEqual(dm.work_cover_url, DATA['data']['pic'])
        self.assertEqual(dm.work_owner_id, DATA['data']['owner']['mid'])
        self.assertEqual(dm.work_owner_name, DATA['data']['owner']['name'])
        self.assertEqual(dm.work_owner_avatar_url, DATA['data']['owner']['face'])

        self.assertIsNone(dm.section_id)
        self.assertIsNone(dm.section_name)
        self.assertIsNone(dm.episode_id)
        self.assertIsNone(dm.episode_name)

        self.assertIsNone(dm.season_id)
        self.assertIsNone(dm.season_name)
        self.assertIsNone(dm.season_cover_url)
        self.assertIsNone(dm.season_owner_id)
        self.assertIsNone(dm.season_owner_name)
        self.assertIsNone(dm.season_owner_avatar_url)

        self.assertEqual(dm.aid, DATA['data']['aid'])
        self.assertEqual(dm.bvid, DATA['data']['bvid'])
        self.assertEqual(dm.cid, expected_sample_page['cid'])
        self.assertEqual(dm.page_url, self.sample_url + '?p=1')
        self.assertEqual(dm.page_title, expected_sample_page['part'])
        self.assertEqual(dm.duration, expected_sample_page['duration'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta_with_connection_error(self, mock_request):
        mock_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /x/web-interface/view?bvid=BV1X54y1C74U'
        )

        with self.assertRaises(ConnectionError):
            WorkService.get_work_meta(self.sample_url)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta_with_timeout_error(self, mock_request):
        mock_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )

        with self.assertRaises(Timeout):
            WorkService.get_work_meta(self.sample_url)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta_by_aid(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )
        sample_url_with_aid = 'https://www.bilibili.com/video/av842089940'

        work_pages = WorkService.get_work_meta(self.sample_url)
        self.assertEqual(len(work_pages), 1)

        dm, *_ = work_pages
        self.assertEqual(dm.work_url, self.sample_url)

    def test_get_video_meta_with_invaild_url(self):
        sample_url_with_invalid_namespace = 'https://www.bilibili.com/video/X54y1C74U'
        with self.assertRaises(ValueError):
            WorkService.get_work_meta(sample_url_with_invalid_namespace)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta_with_unavailable_source(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps({
                'code': -404,
                'message': '啥都木有',
                'ttl': 1
            }).encode('utf-8')
        )
        sample_url_with_unavailable_id = 'https://www.bilibili.com/video/BV1z5tWefExf'

        dm = WorkService.get_work_meta(sample_url_with_unavailable_id)
        self.assertIsNone(dm)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta_with_returning_season_but_not_return(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_WITH_SEASON).encode('utf-8')
        )
        sample_url = 'https://www.bilibili.com/video/BV1tN4y1F79k'

        work_pages = WorkService.get_work_meta(sample_url)
        self.assertEqual(len(work_pages), 1)

        dm, *_ = work_pages
        expected_sample_page, *_ = DATA_WITH_SEASON['data']['pages']

        self.assertEqual(dm.work_url, sample_url)
        self.assertEqual(dm.work_title, DATA_WITH_SEASON['data']['title'])
        self.assertEqual(dm.work_description, DATA_WITH_SEASON['data']['desc'])
        self.assertEqual(dm.work_cover_url, DATA_WITH_SEASON['data']['pic'])
        self.assertEqual(dm.work_owner_id, DATA_WITH_SEASON['data']['owner']['mid'])
        self.assertEqual(dm.work_owner_name, DATA_WITH_SEASON['data']['owner']['name'])
        self.assertEqual(dm.work_owner_avatar_url, DATA_WITH_SEASON['data']['owner']['face'])

        expected_sample_section, *_ = DATA_WITH_SEASON['data']['ugc_season']['sections']
        self.assertEqual(dm.section_id, expected_sample_section['id'])
        self.assertEqual(dm.section_name, expected_sample_section['title'])
        expected_sample_episode, *_ = expected_sample_section['episodes']
        self.assertEqual(dm.episode_id, expected_sample_episode['id'])
        self.assertEqual(dm.episode_name, expected_sample_episode['title'])

        self.assertEqual(dm.season_id, DATA_WITH_SEASON['data']['ugc_season']['id'])
        self.assertEqual(dm.season_name, DATA_WITH_SEASON['data']['ugc_season']['title'])
        self.assertEqual(dm.season_cover_url, DATA_WITH_SEASON['data']['ugc_season']['cover'])
        self.assertEqual(dm.season_owner_id, DATA_WITH_SEASON['data']['ugc_season']['mid'])
        self.assertIsNone(dm.season_owner_name)
        self.assertIsNone(dm.season_owner_avatar_url)

        self.assertEqual(dm.aid, DATA_WITH_SEASON['data']['aid'])
        self.assertEqual(dm.bvid, DATA_WITH_SEASON['data']['bvid'])
        self.assertEqual(dm.cid, expected_sample_page['cid'])
        self.assertEqual(dm.page_url, sample_url + '?p=1')
        self.assertEqual(dm.page_title, expected_sample_page['part'])
        self.assertEqual(dm.duration, expected_sample_page['duration'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_meta_with_returning_season(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_WITH_SEASON).encode('utf-8')
        )
        sample_url = 'https://www.bilibili.com/video/BV1tN4y1F79k'

        work_pages = WorkService.get_work_meta(sample_url, return_season=True)
        self.assertEqual(len(work_pages), 2)

        dm, *_ = work_pages
        expected_sample_section, *_ = DATA_WITH_SEASON['data']['ugc_season']['sections']
        expected_sample_episode, *_ = expected_sample_section['episodes']
        expected_sample_page, *_ = expected_sample_episode['pages']

        self.assertEqual(dm.work_url, sample_url)
        self.assertIsNone(dm.work_title)
        self.assertIsNone(dm.work_description)
        self.assertIsNone(dm.work_owner_id)
        self.assertIsNone(dm.work_owner_name)
        self.assertIsNone(dm.work_owner_avatar_url)

        expected_sample_section, *_ = DATA_WITH_SEASON['data']['ugc_season']['sections']
        self.assertEqual(dm.section_id, expected_sample_section['id'])
        self.assertEqual(dm.section_name, expected_sample_section['title'])
        expected_sample_episode, *_ = expected_sample_section['episodes']
        self.assertEqual(dm.episode_id, expected_sample_episode['id'])
        self.assertEqual(dm.episode_name, expected_sample_episode['title'])

        self.assertEqual(dm.season_id, DATA_WITH_SEASON['data']['ugc_season']['id'])
        self.assertEqual(dm.season_name, DATA_WITH_SEASON['data']['ugc_season']['title'])
        self.assertEqual(dm.season_cover_url, DATA_WITH_SEASON['data']['ugc_season']['cover'])
        self.assertEqual(dm.season_owner_id, DATA_WITH_SEASON['data']['ugc_season']['mid'])
        self.assertIsNone(dm.season_owner_name)
        self.assertIsNone(dm.season_owner_avatar_url)

        self.assertEqual(dm.aid, DATA_WITH_SEASON['data']['aid'])
        self.assertEqual(dm.bvid, DATA_WITH_SEASON['data']['bvid'])
        self.assertEqual(dm.cid, expected_sample_page['cid'])
        self.assertEqual(dm.page_url, sample_url + '?p=1')
        self.assertEqual(dm.page_title, expected_sample_page['part'])
        self.assertEqual(dm.duration, expected_sample_page['duration'])
