"""
Unit test for ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/data/video_info_BV1X54y1C74U.json', 'r') as fp:
    DATA = json.load(fp)


class ProxyServiceTestCase(TestCase):

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_info(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )

        dm = ProxyService.get_video_info(bvid='BV1X54y1C74U')
        self.assertEqual(dm.code, DATA['code'])
        self.assertEqual(dm.message, DATA['message'])
        self.assertEqual(dm.ttl, DATA['ttl'])

        data = dm.data
        self.assertEqual(data.bvid, DATA['data']['bvid'])
        self.assertEqual(data.aid, DATA['data']['aid'])
        self.assertEqual(data.pic, DATA['data']['pic'])
        self.assertEqual(data.title, DATA['data']['title'])
        self.assertEqual(data.desc, DATA['data']['desc'])
        self.assertEqual(data.duration, DATA['data']['duration'])
        self.assertEqual(data.cid, DATA['data']['cid'])

        actual_sample_page, *_ = data.pages
        expected_sample_page, *_ = DATA['data']['pages']
        self.assertEqual(actual_sample_page.cid, expected_sample_page['cid'])
        self.assertEqual(actual_sample_page.page, expected_sample_page['page'])
        self.assertEqual(actual_sample_page.part, expected_sample_page['part'])
        self.assertEqual(actual_sample_page.duration, expected_sample_page['duration'])
        self.assertEqual(actual_sample_page.vid, expected_sample_page['vid'])

        actual_sample_owner = data.owner
        expected_sample_owner = DATA['data']['owner']
        self.assertEqual(actual_sample_owner.mid, expected_sample_owner['mid'])
        self.assertEqual(actual_sample_owner.name, expected_sample_owner['name'])
        self.assertEqual(actual_sample_owner.face, expected_sample_owner['face'])

        self.assertIsNone(data.staff)

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_info_with_connection_error(self, mock_request):
        mock_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /x/web-interface/view?bvid=BV1X54y1C74U'
        )
        with self.assertRaises(ConnectionError):
            ProxyService.get_video_info(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.requests.get')
    def test_get_video_info_with_timeout_error(self, mock_request):
        mock_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            ProxyService.get_video_info(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.requests.get')
    def test__get_video_info_response(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )

        response = ProxyService._get_video_info_response(bvid='BV1X54y1C74U')

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, DATA)

    @patch('bili_jean.proxy_service.requests.get')
    def test__get_video_info_response_by_aid(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )

        response = ProxyService._get_video_info_response(aid=842089940)

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, DATA)

    def test_get_video_info_without_params(self):
        with self.assertRaises(ValueError):
            ProxyService.get_video_info()
