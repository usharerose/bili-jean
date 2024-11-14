"""
Unit test for UGCComponent
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.constants import StreamingCategory
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

        expected_length = 0
        if not DATA_VIEW['data']['is_season_display']:
            expected_length += len(DATA_VIEW['data']['pages'])
        else:
            for section in DATA_VIEW['data']['ugc_season']['sections']:
                for episode in section['episodes']:
                    expected_length += len(episode['pages'])
        self.assertEqual(len(actual_pages), expected_length)

        sample_actual_page, *_ = actual_pages
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.UGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 239927346)
        self.assertEqual(sample_actual_page.page_title, '呼兰：社保')
        self.assertEqual(sample_actual_page.page_duration, 177)
        self.assertEqual(sample_actual_page.view_aid, 842089940)
        self.assertEqual(sample_actual_page.view_bvid, 'BV1X54y1C74U')
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertEqual(sample_actual_page.view_title, '【脱口秀大会】呼兰：社保维系了我的脱口秀梦想...')
        self.assertEqual(sample_actual_page.view_desc, '-')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i0.hdslb.com/bfs/archive/637b892a9d16daf7220071e4a2090533e3782922.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1599717911)
        self.assertEqual(sample_actual_page.view_duration, 177)
        self.assertEqual(sample_actual_page.view_owner_id, 158647239)
        self.assertEqual(sample_actual_page.view_owner_name, '呼兰hooligan')
        self.assertEqual(
            sample_actual_page.view_owner_avatar_url,
            'http://i2.hdslb.com/bfs/face/7bcb54931eb26e29cd75bc8059dd74647fcfe2c3.jpg'
        )
        self.assertIsNone(sample_actual_page.coll_id)
        self.assertIsNone(sample_actual_page.coll_title)
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertIsNone(sample_actual_page.coll_owner_id)
        self.assertIsNone(sample_actual_page.coll_owner_name)
        self.assertIsNone(sample_actual_page.coll_owner_avatar_url)
        self.assertIsNone(sample_actual_page.coll_sect_id)
        self.assertIsNone(sample_actual_page.coll_sect_title)
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_season(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_pages = UGCComponent.get_views(bvid='BV1tN4y1F79k')

        expected_length = 0
        if not DATA_VIEW_WITH_SEASON['data']['is_season_display']:
            expected_length += len(DATA_VIEW_WITH_SEASON['data']['pages'])
        else:
            for section in DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections']:
                for episode in section['episodes']:
                    expected_length += len(episode['pages'])
        self.assertEqual(len(actual_pages), expected_length)

        sample_actual_page, *_ = actual_pages
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.UGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 808240617)
        self.assertEqual(sample_actual_page.page_title, '《黑神话：悟空》6分钟实机剧情片段')
        self.assertEqual(sample_actual_page.page_duration, 381)
        self.assertEqual(sample_actual_page.view_aid, 899743670)
        self.assertEqual(sample_actual_page.view_bvid, 'BV1tN4y1F79k')
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertEqual(sample_actual_page.view_title, '《黑神话：悟空》6分钟实机剧情片段')
        self.assertEqual(
            sample_actual_page.view_desc,
            '有人不入爱河，有人深陷欲网。'
            '\\n有人阴阳两隔，有人各天一方。'
            '\\n最渴望取的，未必是真经，或许是真情。'
             '\\n有道是——\\n易求无价宝，难得有心郎。'
             '\\n\\n由游戏科学开发的西游题材单机·动作·角色扮演游戏《黑神话：悟空》今日正式公布了一段新的6分钟实机剧情片段，'
             '所有出场角色均为首次亮相。'
             '\\n\\n更多信息可关注我们的微博@黑神话之悟空 或前往官网\\u003e\\u003eheishenhua.com'
        )
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i0.hdslb.com/bfs/archive/5484d44e54cc934fd066ccc2f313752fa8fcb77b.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1660960800)
        self.assertEqual(sample_actual_page.view_duration, 381)
        self.assertEqual(sample_actual_page.view_owner_id, 642389251)
        self.assertEqual(sample_actual_page.view_owner_name, '黑神话悟空')
        self.assertEqual(
            sample_actual_page.view_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/5fdac7d9820175f5f0ae1b6c33968bb8f64cc82c.jpg'
        )
        self.assertEqual(sample_actual_page.coll_id, 650336)
        self.assertEqual(sample_actual_page.coll_title, '《黑神话：悟空》6分钟实机剧情片段')
        self.assertEqual(
            sample_actual_page.coll_desc,
            '有人不入爱河，有人深陷欲网。\\n有人阴阳两隔，有人各天一方。\\n最渴望取的，未必是真经，或许是真情。'
            '\\n有道是——\\n易求无价宝，难得有心郎。\\n\\n由游戏科学开发的西游题材单机·动作·角色扮演游戏《黑神话：悟空》'
            '今日正式公布了一段新的6分钟实机剧情片段，所有出场角色均为首次亮相。'
            '\\n\\nP1：正片\\nP2：插曲纯享版\\n\\n视频插曲及伴奏已同步上传网易云音乐，QQ音乐。搜索“黑神话”或“戒网”即可收听。'
            '\\n\\n更多信息可关注我们的微博@黑神话之悟空 或前往官网\\u003e\\u003eheishenhua.com'
        )
        self.assertEqual(
            sample_actual_page.coll_cover_url,
            'https://archive.biliimg.com/bfs/archive/5484d44e54cc934fd066ccc2f313752fa8fcb77b.jpg'
        )
        self.assertEqual(sample_actual_page.coll_owner_id, 642389251)
        self.assertIsNone(sample_actual_page.coll_owner_name)
        self.assertIsNone(sample_actual_page.coll_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, 752877)
        self.assertEqual(sample_actual_page.coll_sect_title, '正片')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_relevant_views_in_season(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
        )
        actual_pages = UGCComponent.get_views(bvid='BV1tN4y1F79k')

        expected_length = 0
        if not DATA_VIEW_WITH_SEASON['data']['is_season_display']:
            expected_length += len(DATA_VIEW_WITH_SEASON['data']['pages'])
        else:
            for section in DATA_VIEW_WITH_SEASON['data']['ugc_season']['sections']:
                for episode in section['episodes']:
                    expected_length += len(episode['pages'])
        self.assertEqual(len(actual_pages), expected_length)

        *_, sample_actual_page = actual_pages
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.UGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 808242611)
        self.assertEqual(sample_actual_page.page_title, '戒网（《黑神话：悟空》游戏插曲）')
        self.assertEqual(sample_actual_page.page_duration, 330)
        self.assertEqual(sample_actual_page.view_aid, 557178878)
        self.assertEqual(sample_actual_page.view_bvid, 'BV1Ye4y1f7kA')
        self.assertIsNone(sample_actual_page.view_ep_id)
        self.assertIsNone(sample_actual_page.view_season_id)
        self.assertEqual(sample_actual_page.view_title, '戒网（《黑神话：悟空》游戏插曲）')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i2.hdslb.com/bfs/archive/7c28fc8c48fdd8c339fb6f0091c8b6ddba65bcf7.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1660960800)
        self.assertEqual(sample_actual_page.view_duration, 330)
        self.assertIsNone(sample_actual_page.view_owner_id)
        self.assertIsNone(sample_actual_page.view_owner_name)
        self.assertIsNone(sample_actual_page.view_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_id, 650336)
        self.assertEqual(sample_actual_page.coll_title, '《黑神话：悟空》6分钟实机剧情片段')
        self.assertEqual(
            sample_actual_page.coll_desc,
            '有人不入爱河，有人深陷欲网。\\n有人阴阳两隔，有人各天一方。\\n最渴望取的，未必是真经，或许是真情。'
            '\\n有道是——\\n易求无价宝，难得有心郎。\\n\\n由游戏科学开发的西游题材单机·动作·角色扮演游戏《黑神话：悟空》'
            '今日正式公布了一段新的6分钟实机剧情片段，所有出场角色均为首次亮相。'
            '\\n\\nP1：正片\\nP2：插曲纯享版\\n\\n视频插曲及伴奏已同步上传网易云音乐，QQ音乐。搜索“黑神话”或“戒网”即可收听。'
            '\\n\\n更多信息可关注我们的微博@黑神话之悟空 或前往官网\\u003e\\u003eheishenhua.com'
        )
        self.assertEqual(
            sample_actual_page.coll_cover_url,
            'https://archive.biliimg.com/bfs/archive/5484d44e54cc934fd066ccc2f313752fa8fcb77b.jpg'
        )
        self.assertEqual(sample_actual_page.coll_owner_id, 642389251)
        self.assertIsNone(sample_actual_page.coll_owner_name)
        self.assertIsNone(sample_actual_page.coll_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, 752877)
        self.assertEqual(sample_actual_page.coll_sect_title, '正片')
        self.assertFalse(sample_actual_page.is_selected_page)

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
