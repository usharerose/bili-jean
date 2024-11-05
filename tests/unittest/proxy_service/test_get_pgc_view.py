"""
Unit test for get_pgc_view of ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.proxy_service import ProxyService
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


class ProxyServiceGetPGCViewTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_dm = ProxyService.get_pgc_view(ep_id=232465)
        self.assertEqual(actual_dm.code, DATA_VIEW['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNotNone(actual_dm.result)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_not_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_dm = ProxyService.get_pgc_view(ep_id=1)
        self.assertEqual(actual_dm.code, DATA_VIEW_NOT_EXIST['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW_NOT_EXIST['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNone(actual_dm.result)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_result = ProxyService.get_pgc_view(ep_id=232465).result
        expected_result = DATA_VIEW['result']

        self.assertEqual(actual_result.cover, expected_result['cover'])
        self.assertEqual(actual_result.evaluate, expected_result['evaluate'])
        self.assertEqual(actual_result.link, expected_result['link'])
        self.assertEqual(actual_result.media_id, expected_result['media_id'])
        self.assertEqual(actual_result.season_id, expected_result['season_id'])
        self.assertEqual(actual_result.season_title, expected_result['season_title'])
        self.assertEqual(actual_result.title, expected_result['title'])
        self.assertEqual(actual_result.type_field, expected_result['type'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_episodes(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_episodes = ProxyService.get_pgc_view(ep_id=232465).result.episodes
        self.assertIsInstance(actual_episodes, list)
        self.assertEqual(len(actual_episodes), len(DATA_VIEW['result']['episodes']))
        sample_actual_episode, *_ = actual_episodes
        sample_expected_episode, *_ = DATA_VIEW['result']['episodes']

        self.assertEqual(sample_actual_episode.aid, sample_expected_episode['aid'])
        self.assertEqual(sample_actual_episode.bvid, sample_expected_episode['bvid'])
        self.assertEqual(sample_actual_episode.cid, sample_expected_episode['cid'])
        self.assertEqual(sample_actual_episode.cover, sample_expected_episode['cover'])
        self.assertEqual(sample_actual_episode.duration, sample_expected_episode['duration'])
        self.assertEqual(sample_actual_episode.ep_id, sample_expected_episode['ep_id'])
        self.assertEqual(sample_actual_episode.id_field, sample_expected_episode['id'])
        self.assertEqual(sample_actual_episode.link, sample_expected_episode['link'])
        self.assertEqual(sample_actual_episode.long_title, sample_expected_episode['long_title'])
        self.assertEqual(sample_actual_episode.pub_time, sample_expected_episode['pub_time'])
        self.assertEqual(sample_actual_episode.title, sample_expected_episode['title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_episode_badge_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_episodes = ProxyService.get_pgc_view(ep_id=232465).result.episodes
        sample_actual_episode, *_ = actual_episodes
        sample_expected_episode, *_ = DATA_VIEW['result']['episodes']
        actual_badge_info = sample_actual_episode.badge_info
        expected_badge_info = sample_expected_episode['badge_info']

        self.assertEqual(actual_badge_info.bg_color, expected_badge_info['bg_color'])
        self.assertEqual(actual_badge_info.bg_color_night, expected_badge_info['bg_color_night'])
        self.assertEqual(actual_badge_info.text, expected_badge_info['text'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_seasons(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_seasons = ProxyService.get_pgc_view(ep_id=232465).result.seasons
        self.assertIsInstance(actual_seasons, list)
        self.assertEqual(len(actual_seasons), len(DATA_VIEW['result']['seasons']))
        sample_actual_season, *_ = actual_seasons
        sample_expected_season, *_ = DATA_VIEW['result']['seasons']

        self.assertEqual(sample_actual_season.cover, sample_expected_season['cover'])
        self.assertEqual(sample_actual_season.media_id, sample_expected_season['media_id'])
        self.assertEqual(sample_actual_season.season_id, sample_expected_season['season_id'])
        self.assertEqual(sample_actual_season.season_title, sample_expected_season['season_title'])

        actual_badge_info = sample_actual_season.badge_info
        expected_badge_info = sample_expected_season['badge_info']

        self.assertEqual(actual_badge_info.bg_color, expected_badge_info['bg_color'])
        self.assertEqual(actual_badge_info.bg_color_night, expected_badge_info['bg_color_night'])
        self.assertEqual(actual_badge_info.text, expected_badge_info['text'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_without_seasons(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITHOUT_SEASONS).encode('utf-8')
        )
        actual_seasons = ProxyService.get_pgc_view(ep_id=284310).result.seasons
        self.assertIsInstance(actual_seasons, list)
        self.assertEqual(len(actual_seasons), 0)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_section(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_section = ProxyService.get_pgc_view(ep_id=232465).result.section
        self.assertIsInstance(actual_section, list)
        self.assertEqual(len(actual_section), len(DATA_VIEW['result']['section']))
        sample_actual_section, *_ = actual_section
        sample_expected_section, *_ = DATA_VIEW['result']['section']

        self.assertEqual(sample_actual_section.id_field, sample_expected_section['id'])
        self.assertEqual(sample_actual_section.title, sample_expected_section['title'])

        sample_actual_episode, *_ = sample_actual_section.episodes
        sample_expected_episode, *_ = sample_expected_section['episodes']
        actual_badge_info = sample_actual_episode.badge_info
        expected_badge_info = sample_expected_episode['badge_info']

        self.assertEqual(sample_actual_episode.aid, sample_expected_episode['aid'])
        self.assertEqual(sample_actual_episode.bvid, sample_expected_episode['bvid'])
        self.assertEqual(sample_actual_episode.cid, sample_expected_episode['cid'])
        self.assertEqual(sample_actual_episode.cover, sample_expected_episode['cover'])
        self.assertEqual(sample_actual_episode.duration, sample_expected_episode['duration'])
        self.assertEqual(sample_actual_episode.ep_id, sample_expected_episode['ep_id'])
        self.assertEqual(sample_actual_episode.id_field, sample_expected_episode['id'])
        self.assertEqual(sample_actual_episode.link, sample_expected_episode['link'])
        self.assertEqual(sample_actual_episode.long_title, sample_expected_episode['long_title'])
        self.assertEqual(sample_actual_episode.pub_time, sample_expected_episode['pub_time'])
        self.assertEqual(sample_actual_episode.title, sample_expected_episode['title'])

        self.assertEqual(actual_badge_info.bg_color, expected_badge_info['bg_color'])
        self.assertEqual(actual_badge_info.bg_color_night, expected_badge_info['bg_color_night'])
        self.assertEqual(actual_badge_info.text, expected_badge_info['text'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_without_section(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITHOUT_SECTION).encode('utf-8')
        )
        actual_section = ProxyService.get_pgc_view(ep_id=815604).result.section
        self.assertIsNone(actual_section)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_series(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_series = ProxyService.get_pgc_view(ep_id=232465).result.series
        expected_series = DATA_VIEW['result']['series']

        self.assertEqual(actual_series.series_id, expected_series['series_id'])
        self.assertEqual(actual_series.series_title, expected_series['series_title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_without_up_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_result = ProxyService.get_pgc_view(ep_id=232465).result

        self.assertIsNone(actual_result.up_info)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pgc_view_with_up_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_UP_INFO).encode('utf-8')
        )
        actual_up_info = ProxyService.get_pgc_view(season_id=12548).result.up_info
        expected_up_info = DATA_VIEW_WITH_UP_INFO['result']['up_info']

        self.assertEqual(actual_up_info.avatar, expected_up_info['avatar'])
        self.assertEqual(actual_up_info.mid, expected_up_info['mid'])
        self.assertEqual(actual_up_info.uname, expected_up_info['uname'])

    def test_pgc_view_without_params(self):
        with self.assertRaises(ValueError):
            ProxyService.get_pgc_view()
