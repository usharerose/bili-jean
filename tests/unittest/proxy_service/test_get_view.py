"""
Unit test for get_view of ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/view_BV1X54y1C74U.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/view_notexistbvid.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/view_BV1tN4y1F79k.json', 'r') as fp:
    DATA_VIEW_WITH_SEASON = json.load(fp)


class ProxyServiceGetViewTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_dm = ProxyService.get_view(bvid='BV1X54y1C74U')
        self.assertEqual(actual_dm.code, DATA_VIEW['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW['message'])
        self.assertEqual(actual_dm.ttl, DATA_VIEW['ttl'])
        self.assertIsNotNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_not_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_dm = ProxyService.get_view(bvid='notexistbvid')
        self.assertEqual(actual_dm.code, DATA_VIEW_NOT_EXIST['code'])
        self.assertEqual(actual_dm.message, DATA_VIEW_NOT_EXIST['message'])
        self.assertEqual(actual_dm.ttl, DATA_VIEW_NOT_EXIST['ttl'])
        self.assertIsNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_data = ProxyService.get_view(bvid='BV1X54y1C74U').data
        expected_data = DATA_VIEW['data']

        self.assertEqual(actual_data.aid, expected_data['aid'])
        self.assertEqual(actual_data.bvid, expected_data['bvid'])
        self.assertEqual(actual_data.cid, expected_data['cid'])
        self.assertEqual(actual_data.ctime, expected_data['ctime'])
        self.assertEqual(actual_data.desc, expected_data['desc'])
        self.assertEqual(actual_data.duration, expected_data['duration'])
        self.assertEqual(actual_data.pic, expected_data['pic'])
        self.assertEqual(actual_data.pubdate, expected_data['pubdate'])
        self.assertEqual(actual_data.title, expected_data['title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_without_season(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_data = ProxyService.get_view(bvid='BV1X54y1C74U').data

        self.assertFalse(actual_data.is_season_display)
        self.assertIsNone(actual_data.ugc_season)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_owner(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_owner = ProxyService.get_view(bvid='BV1X54y1C74U').data.owner
        expected_owner = DATA_VIEW['data']['owner']

        self.assertEqual(actual_owner.face, expected_owner['face'])
        self.assertEqual(actual_owner.mid, expected_owner['mid'])
        self.assertEqual(actual_owner.name, expected_owner['name'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_pages(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_pages = ProxyService.get_view(bvid='BV1X54y1C74U').data.pages
        self.assertIsInstance(actual_pages, list)
        self.assertEqual(len(actual_pages), len(DATA_VIEW['data']['pages']))
        sample_actual_page, *_ = actual_pages
        sample_expected_page, *_ = DATA_VIEW['data']['pages']

        self.assertEqual(sample_actual_page.cid, sample_expected_page['cid'])
        self.assertEqual(sample_actual_page.duration, sample_expected_page['duration'])
        self.assertEqual(sample_actual_page.page, sample_expected_page['page'])
        self.assertEqual(sample_actual_page.part, sample_expected_page['part'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_with_ugc_season(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_data = ProxyService.get_view(bvid='BV1tN4y1F79k').data

        self.assertTrue(actual_data.is_season_display)
        self.assertIsNotNone(actual_data.ugc_season)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_ugc_season_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_data = ProxyService.get_view(bvid='BV1tN4y1F79k').data.ugc_season
        expected_data = DATA_VIEW_WITH_SEASON['data']['ugc_season']

        self.assertEqual(actual_data.cover, expected_data['cover'])
        self.assertEqual(actual_data.ep_count, expected_data['ep_count'])
        self.assertEqual(actual_data.id_field, expected_data['id'])
        self.assertEqual(actual_data.intro, expected_data['intro'])
        self.assertEqual(actual_data.mid, expected_data['mid'])
        self.assertEqual(actual_data.title, expected_data['title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_section_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_sections = ProxyService.get_view(bvid='BV1tN4y1F79k').data.ugc_season.sections
        self.assertIsInstance(actual_sections, list)
        self.assertEqual(
            len(actual_sections),
            len(DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'])
        )
        sample_actual_section, *_ = actual_sections
        sample_expected_section, *_ = DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections']

        self.assertEqual(sample_actual_section.id_field, sample_expected_section['id'])
        self.assertEqual(sample_actual_section.season_id, sample_expected_section['season_id'])
        self.assertEqual(sample_actual_section.title, sample_expected_section['title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_episode_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_episodes = ProxyService.get_view(
            bvid='BV1tN4y1F79k'
        ).data.ugc_season.sections[0].episodes
        self.assertIsInstance(actual_episodes, list)
        self.assertEqual(
            len(actual_episodes),
            len(DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'][0]['episodes'])
        )
        sample_actual_episode, *_ = actual_episodes
        sample_expected_episode, *_ = DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'][0]['episodes']

        self.assertEqual(sample_actual_episode.aid, sample_expected_episode['aid'])
        self.assertEqual(sample_actual_episode.bvid, sample_expected_episode['bvid'])
        self.assertEqual(sample_actual_episode.cid, sample_expected_episode['cid'])
        self.assertEqual(sample_actual_episode.id_field, sample_expected_episode['id'])
        self.assertEqual(sample_actual_episode.season_id, sample_expected_episode['season_id'])
        self.assertEqual(sample_actual_episode.section_id, sample_expected_episode['section_id'])
        self.assertEqual(sample_actual_episode.title, sample_expected_episode['title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_episode_arc(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_arc = ProxyService.get_view(
            bvid='BV1tN4y1F79k'
        ).data.ugc_season.sections[0].episodes[0].arc
        expected_arc = DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'][0]['episodes'][0]['arc']

        self.assertEqual(actual_arc.aid, expected_arc['aid'])
        self.assertEqual(actual_arc.ctime, expected_arc['ctime'])
        self.assertEqual(actual_arc.desc, expected_arc['desc'])
        self.assertEqual(actual_arc.duration, expected_arc['duration'])
        self.assertEqual(actual_arc.pic, expected_arc['pic'])
        self.assertEqual(actual_arc.pubdate, expected_arc['pubdate'])
        self.assertEqual(actual_arc.title, expected_arc['title'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_episode_page(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_page = ProxyService.get_view(
            bvid='BV1tN4y1F79k'
        ).data.ugc_season.sections[0].episodes[0].page
        expected_page = DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'][0]['episodes'][0]['page']

        self.assertEqual(actual_page.cid, expected_page['cid'])
        self.assertEqual(actual_page.duration, expected_page['duration'])
        self.assertEqual(actual_page.page, expected_page['page'])
        self.assertEqual(actual_page.part, expected_page['part'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_episode_pages(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_pages = ProxyService.get_view(
            bvid='BV1tN4y1F79k'
        ).data.ugc_season.sections[0].episodes[0].pages
        self.assertIsInstance(actual_pages, list)
        self.assertEqual(
            len(actual_pages),
            len(DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'][0]['episodes'][0]['pages'])
        )
        sample_actual_page, *_ = actual_pages
        sample_expected_page, *_ = (
            DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections'][0]['episodes'][0]['pages']
        )

        self.assertEqual(sample_actual_page.cid, sample_expected_page['cid'])
        self.assertEqual(sample_actual_page.duration, sample_expected_page['duration'])
        self.assertEqual(sample_actual_page.page, sample_expected_page['page'])
        self.assertEqual(sample_actual_page.part, sample_expected_page['part'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_with_connection_error(self, mocked_request):
        mocked_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /x/web-interface/view?bvid=BV1X54y1C74U'
        )
        with self.assertRaises(ConnectionError):
            ProxyService.get_view(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_with_timeout_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            ProxyService.get_view(bvid='BV1X54y1C74U')

    def test_view_without_params(self):
        with self.assertRaises(ValueError):
            ProxyService.get_view()

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_view_by_aid(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        target_aid = DATA_VIEW['data']['aid']
        actual_data = ProxyService.get_view(aid=target_aid).data

        self.assertEqual(actual_data.aid, target_aid)
