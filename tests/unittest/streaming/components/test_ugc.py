"""
Unit test for UGCComponent
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import ReadTimeout, Timeout

from bili_jean.constants import (
    AudioBitRateID,
    QualityNumber,
    StreamingCategory,
    VideoCodecID
)
from bili_jean.streaming.components import UGCComponent
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/ugc_play/ugc_play_BV1X54y1C74U.json', 'r') as fp:
    DATA_PLAY = json.load(fp)
with open('tests/mock_data/proxy/ugc_play/ugc_play_BV13L4y1K7th.json', 'r') as fp:
    DATA_PLAY_WITH_DOLBY_AUDIO = json.load(fp)
with open('tests/mock_data/proxy/ugc_play/ugc_play_BV13ht2ejE1S.json', 'r') as fp:
    DATA_PLAY_WITH_HIRES = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_BV1X54y1C74U.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_notexistbvid.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_BV1tN4y1F79k.json', 'r') as fp:
    DATA_VIEW_WITH_SEASON = json.load(fp)
with open('tests/mock_data/proxy/card/card_642389251.json', 'r') as fp:
    DATA_CARD = json.load(fp)


class UGCComponentGetViewsTestCase(TestCase):

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
    def test_get_views_with_season(self, mocked_get_request):
        mocked_get_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_CARD).encode('utf-8')
            )
        ]
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
        self.assertEqual(sample_actual_page.coll_owner_name, '黑神话悟空')
        self.assertEqual(
            sample_actual_page.coll_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/5fdac7d9820175f5f0ae1b6c33968bb8f64cc82c.jpg'
        )
        self.assertEqual(sample_actual_page.coll_sect_id, 752877)
        self.assertEqual(sample_actual_page.coll_sect_title, '正片')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_relevant_views_in_season(self, mocked_get_request):
        mocked_get_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_VIEW_WITH_SEASON).encode('utf-8')
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_CARD).encode('utf-8')
            )
        ]
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
        self.assertEqual(sample_actual_page.coll_owner_name, '黑神话悟空')
        self.assertEqual(
            sample_actual_page.coll_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/5fdac7d9820175f5f0ae1b6c33968bb8f64cc82c.jpg'
        )
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


class UGCComponentGetPageStreamingSrcTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            bvid='BV1X54y1C74U'
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30033.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=cosbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=cos\\u0026upsig=9db3cff93d80797550f851d7ae044318'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=39113\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_prefer_lower_quality_video(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            aid=842089940,
            is_video_hq_preferred=False
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30011.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2'
            '\\u0026os=upos\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u'
            '\\u0026mid=0\\u0026platform=pc\\u0026og=hw\\u0026upsig=69d43e6480992dd7dcab4508889ebee7'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=27086\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P360.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_video_qn(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            bvid='BV1X54y1C74U',
            is_video_hq_preferred=False,
            video_qn=QualityNumber.P480.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30033.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=cosbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=cos\\u0026upsig=9db3cff93d80797550f851d7ae044318'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=39113\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_but_not_support_video_qn(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            bvid='BV1X54y1C74U',
            is_video_hq_preferred=False,
            video_qn=QualityNumber.PPLUS_1080.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30033.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=cosbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=cos\\u0026upsig=9db3cff93d80797550f851d7ae044318'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=39113\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_prefer_not_eff_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            bvid='BV1X54y1C74U',
            is_video_codec_eff_preferred=False
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30032.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2'
            '\\u0026os=cosbv\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u'
            '\\u0026mid=0\\u0026platform=pc\\u0026og=cos\\u0026upsig=96dc6e84ad53264c50f6708a22d1d94a'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=99068\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            bvid='BV1X54y1C74U',
            video_codec_number=VideoCodecID.HEVC.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30033.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=cosbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=cos\\u0026upsig=9db3cff93d80797550f851d7ae044318'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=39113\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_but_not_support_video_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=239927346,
            bvid='BV1X54y1C74U',
            video_codec_number=VideoCodecID.AV1.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30033.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2'
            '\\u0026os=cosbv\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u'
            '\\u0026mid=0\\u0026platform=pc\\u0026og=cos\\u0026upsig=9db3cff93d80797550f851d7ae044318'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=39113\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirror08c.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=08cbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=835ba0f13f48abfc872d9de945262dda'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=0\\u0026bw=40047\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_dolby_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY_WITH_DOLBY_AUDIO).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=733892245,
            bvid='BV13L4y1K7th',
            audio_qn=AudioBitRateID.BPS_DOLBY.value.bit_rate_id
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/45/22/733892245/733892245_dv1-1-30126.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1730535097\\u0026gen=playurlv2\\u0026os=upos'
            '\\u0026oi=2071715721\\u0026trid=ab20f77bb9f847d58fff2dea9800d12bu\\u0026mid=12363921'
            '\\u0026platform=pc\\u0026og=hw\\u0026upsig=22218ec69fa88323e6e6b72be9b16ec1'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=1\\u0026bw=742986\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.DOLBY.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-estghw.bilivideo.com/upgcxcode/45/22/733892245/733892245-1-30250.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1730535097\\u0026gen=playurlv2\\u0026os=upos'
            '\\u0026oi=2071715721\\u0026trid=ab20f77bb9f847d58fff2dea9800d12bu\\u0026mid=12363921'
            '\\u0026platform=pc\\u0026og=08\\u0026upsig=4b2dd0e3a7041c78cc03ba302b43dc45'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=1\\u0026bw=56526\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_DOLBY.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_hires_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY_WITH_HIRES).encode('utf-8')
        )
        actual_video_src, actual_audio_src = UGCComponent.get_page_streaming_src(
            cid=25954616353,
            bvid='BV13ht2ejE1S',
            audio_qn=AudioBitRateID.BPS_HIRES.value.bit_rate_id
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcoso1.bilivideo.com/upgcxcode/53/63/25954616353/25954616353-1-100029.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1730536104\\u0026gen=playurlv2\\u0026os=coso1bv'
            '\\u0026oi=2071715721\\u0026trid=da6e6cd6e86d470abbbc7b10b5ea3ca1u\\u0026mid=12363921'
            '\\u0026platform=pc\\u0026og=cos\\u0026upsig=09a7e0216520343e01c284572d2f2133'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod'
            '\\u0026nettype=0\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0'
            '\\u0026agrr=1\\u0026bw=319519\\u0026logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AV1.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/53/63/25954616353/25954616353-1-30251.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1730536104\\u0026gen=playurlv2'
            '\\u0026os=upos\\u0026oi=2071715721\\u0026trid=da6e6cd6e86d470abbbc7b10b5ea3ca1u'
            '\\u0026mid=12363921\\u0026platform=pc\\u0026og=cos\\u0026upsig=98907c8e4db21350c532aa2c0ff9a061'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod\\u0026nettype=0'
            '\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0\\u0026agrr=1'
            '\\u0026bw=199130\\u0026logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_HIRES.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_without_cid(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        with self.assertRaises(ValueError):
            UGCComponent.get_page_streaming_src(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_without_bvid_or_aid(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        with self.assertRaises(ValueError):
            UGCComponent.get_page_streaming_src(cid=239927346)
