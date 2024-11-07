"""
Unit test for get_pugv_view of ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/pugv_view/pugv_view_ss6838.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ss2.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ep482484.json', 'r') as fp:
    DATA_VIEW_WITH_EPISODE_ID = json.load(fp)


class ProxyServiceGetPUGVViewTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_dm = ProxyService.get_pugv_view(season_id=6838)
        self.assertEqual(actual_dm.code, DATA_VIEW['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNotNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_not_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_dm = ProxyService.get_pugv_view(season_id=2)
        self.assertEqual(actual_dm.code, DATA_VIEW_NOT_EXIST['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW_NOT_EXIST['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_view_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_data = ProxyService.get_pugv_view(season_id=6838).data
        expected_data = DATA_VIEW['data']

        self.assertEqual(actual_data.cover, expected_data['cover'])
        self.assertEqual(actual_data.season_id, expected_data['season_id'])
        self.assertEqual(actual_data.subtitle, expected_data['subtitle'])
        self.assertEqual(actual_data.title, expected_data['title'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_view_brief(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_brief = ProxyService.get_pugv_view(season_id=6838).data.brief
        expected_brief = DATA_VIEW['data']['brief']

        self.assertEqual(actual_brief.content, expected_brief['content'])
        self.assertEqual(actual_brief.title, expected_brief['title'])
        self.assertEqual(actual_brief.type_field, expected_brief['type'])

        sample_actual_img, *_ = actual_brief.img
        sample_expected_img, *_ = expected_brief['img']

        self.assertEqual(sample_actual_img.aspect_ratio, sample_expected_img['aspect_ratio'])
        self.assertEqual(sample_actual_img.url, sample_expected_img['url'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_view_episodes(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_episodes = ProxyService.get_pugv_view(season_id=6838).data.episodes
        self.assertIsInstance(actual_episodes, list)
        self.assertEqual(len(actual_episodes), len(DATA_VIEW['data']['episodes']))
        sample_actual_episode, *_ = actual_episodes
        sample_expected_episode, *_ = DATA_VIEW['data']['episodes']

        self.assertEqual(sample_actual_episode.aid, sample_expected_episode['aid'])
        self.assertEqual(sample_actual_episode.cid, sample_expected_episode['cid'])
        self.assertEqual(sample_actual_episode.cover, sample_expected_episode['cover'])
        self.assertEqual(sample_actual_episode.duration, sample_expected_episode['duration'])
        self.assertEqual(sample_actual_episode.ep_status, sample_expected_episode['ep_status'])
        self.assertEqual(sample_actual_episode.episode_can_view, sample_expected_episode['episode_can_view'])
        self.assertEqual(sample_actual_episode.from_field, sample_expected_episode['from'])
        self.assertEqual(sample_actual_episode.id_field, sample_expected_episode['id'])
        self.assertEqual(sample_actual_episode.index, sample_expected_episode['index'])
        self.assertEqual(sample_actual_episode.label, sample_expected_episode['label'])
        self.assertEqual(sample_actual_episode.page, sample_expected_episode['page'])
        self.assertEqual(sample_actual_episode.release_date, sample_expected_episode['release_date'])
        self.assertEqual(sample_actual_episode.status, sample_expected_episode['status'])
        self.assertEqual(sample_actual_episode.subtitle, sample_expected_episode['subtitle'])
        self.assertEqual(sample_actual_episode.title, sample_expected_episode['title'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_view_up_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_up_info = ProxyService.get_pugv_view(season_id=6838).data.up_info
        expected_up_info = DATA_VIEW['data']['up_info']

        self.assertEqual(actual_up_info.avatar, expected_up_info['avatar'])
        self.assertEqual(actual_up_info.mid, expected_up_info['mid'])
        self.assertEqual(actual_up_info.uname, expected_up_info['uname'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_view_by_ep_id(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_EPISODE_ID).encode('utf-8')
        )
        actual_dm = ProxyService.get_pugv_view(ep_id=482484)

        self.assertEqual(actual_dm.code, DATA_VIEW_WITH_EPISODE_ID['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW_WITH_EPISODE_ID['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNotNone(actual_dm.data)

    def test_pugv_view_without_params(self):
        with self.assertRaises(ValueError):
            ProxyService.get_pugv_view()
