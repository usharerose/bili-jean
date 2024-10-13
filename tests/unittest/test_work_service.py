"""
Unit test for VideoService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.work_service import DEFAULT_STAFF_TITLE, WorkService
from tests.utils import get_mocked_response


with open('tests/data/video_info_BV1X54y1C74U.json', 'r') as fp:
    DATA = json.load(fp)


class VideoServiceTestCase(TestCase):

    def setUp(self):
        self.sample_url = 'https://www.bilibili.com/video/BV1X54y1C74U'

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_meta(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )

        dm = WorkService.get_work_meta(self.sample_url)
        self.assertEqual(dm.url, self.sample_url)
        self.assertEqual(dm.title, DATA['data']['title'])
        self.assertEqual(dm.description, DATA['data']['desc'])
        self.assertEqual(dm.cover_url, DATA['data']['pic'])

        # sample data only has 'owner', no 'staff' field
        self.assertEqual(len(dm.staff), 1)
        actual_sample_staff, *_ = dm.staff
        expected_sample_staff = DATA['data']['owner']
        self.assertEqual(actual_sample_staff.account_id, expected_sample_staff['mid'])
        self.assertEqual(actual_sample_staff.name, expected_sample_staff['name'])
        self.assertEqual(
            actual_sample_staff.title,
            expected_sample_staff.get('title') or DEFAULT_STAFF_TITLE
        )
        self.assertEqual(actual_sample_staff.avatar_url, expected_sample_staff['face'])

        actual_sample_page, *_ = dm.pages
        expected_sample_page, *_ = DATA['data']['pages']
        self.assertEqual(actual_sample_page.url, self.sample_url + '?p=1')
        self.assertEqual(actual_sample_page.aid, DATA['data']['aid'])
        self.assertEqual(actual_sample_page.bvid, DATA['data']['bvid'])
        self.assertEqual(actual_sample_page.cid, expected_sample_page['cid'])
        self.assertEqual(actual_sample_page.title, expected_sample_page['part'])
        self.assertEqual(actual_sample_page.duration, expected_sample_page['duration'])

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_meta_with_connection_error(self, mock_request):
        mock_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /x/web-interface/view?bvid=BV1X54y1C74U'
        )

        with self.assertRaises(ConnectionError):
            WorkService.get_work_meta(self.sample_url)

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_meta_with_timeout_error(self, mock_request):
        mock_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )

        with self.assertRaises(Timeout):
            WorkService.get_work_meta(self.sample_url)

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_meta_by_aid(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )
        sample_url_with_aid = 'https://www.bilibili.com/video/av842089940'

        dm = WorkService.get_work_meta(sample_url_with_aid)
        self.assertEqual(dm.url, self.sample_url)
        self.assertEqual(dm.title, DATA['data']['title'])
        self.assertEqual(dm.description, DATA['data']['desc'])
        self.assertEqual(dm.cover_url, DATA['data']['pic'])

    def test_get_video_meta_with_invaild_url(self):
        sample_url_with_invalid_namespace = 'https://www.bilibili.com/video/X54y1C74U'
        with self.assertRaises(ValueError):
            WorkService.get_work_meta(sample_url_with_invalid_namespace)

    @patch('bili_jean.proxy_service.requests.get')
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
