"""
Unit test for backend application
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.app import app
from tests.utils import get_mocked_response


with open('tests/data/video_info_BV1tN4y1F79k.json', 'r') as fp:
    DATA_WITH_SEASON = json.load(fp)
with open('tests/data/user_card_642389251.json', 'r') as fp:
    USER_CARD_DATA_WO_PHOTO = json.load(fp)


class AppGetVideoInfoTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = app.test_client()
        cls.client.testing = True

    @classmethod
    def tearDownClass(cls):
        pass

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_info(self, mock_request):
        mock_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_WITH_SEASON).encode('utf-8')
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(USER_CARD_DATA_WO_PHOTO).encode('utf-8')
            ),
        ]
        response = self.client.post(
            '/get_video_info',
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'url': 'https://www.bilibili.com/video/BV1tN4y1F79k',
                'return_season': False
            })
        )
        self.assertEqual(response.status_code, 200)
        actual_response = json.loads(response.get_data().decode('utf-8'))
        self.assertIsInstance(actual_response['data'], list)
        self.assertEqual(len(actual_response['data']), 1)
        actual_page, *_ = actual_response['data']

        self.assertEqual(actual_page['work_url'], 'https://www.bilibili.com/video/BV1tN4y1F79k')
        self.assertEqual(actual_page['work_title'], DATA_WITH_SEASON['data']['title'])

        expected_sample_section, *_ = DATA_WITH_SEASON['data']['ugc_season']['sections']
        self.assertEqual(actual_page['section_id'], expected_sample_section['id'])
        self.assertEqual(actual_page['section_name'], expected_sample_section['title'])
        expected_sample_episode, *_ = expected_sample_section['episodes']
        self.assertEqual(actual_page['episode_id'], expected_sample_episode['id'])
        self.assertEqual(actual_page['episode_name'], expected_sample_episode['title'])
