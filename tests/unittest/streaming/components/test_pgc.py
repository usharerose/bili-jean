"""
Unit test for PGCComponent
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
from bili_jean.streaming.components import PGCComponent
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/pgc_play/pgc_play_ep199612.json', 'r') as fp:
    DATA_PLAY = json.load(fp)
with open('tests/mock_data/proxy/pgc_play/pgc_play_ep1113563_unpurchased.json', 'r') as fp:
    DATA_PLAY_UNPURCHASED = json.load(fp)
with open('tests/mock_data/proxy/pgc_play/pgc_play_ep199612_trial.json', 'r') as fp:
    DATA_PLAY_TRIAL = json.load(fp)
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
with open('tests/mock_data/proxy/pgc_view/pgc_view_ep249469.json', 'r') as fp:
    DATA_VIEW_SECTION_WITH_UGC_EPISODE = json.load(fp)


class PGCComponentGetViewsTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_by_not_exist_ep_id(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=1)
        self.assertIsNone(actual_pages)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=232465)

        expected_length = 0
        expected_length += len(DATA_VIEW['result']['episodes'])
        for section in DATA_VIEW['result']['section']:
            expected_length += len(section['episodes'])

        self.assertEqual(len(actual_pages), expected_length)
        sample_actual_page, *_ = actual_pages

        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 49053680)
        self.assertEqual(sample_actual_page.page_title, '1 肺炎链球菌')
        self.assertEqual(sample_actual_page.page_duration, 1421)
        self.assertEqual(sample_actual_page.view_aid, 26361000)
        self.assertEqual(sample_actual_page.view_bvid, 'BV1as411p7ae')
        self.assertEqual(sample_actual_page.view_ep_id, 232465)
        self.assertEqual(sample_actual_page.view_season_id, 24588)
        self.assertEqual(sample_actual_page.view_title, '1 肺炎链球菌')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i0.hdslb.com/bfs/archive/18f237427319864f1074b0fb48c31a7b47bafb35.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1530981000)
        self.assertEqual(sample_actual_page.view_duration, 1421)
        self.assertIsNone(sample_actual_page.view_owner_id)
        self.assertIsNone(sample_actual_page.view_owner_name)
        self.assertIsNone(sample_actual_page.view_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_id, 4034)
        self.assertEqual(sample_actual_page.coll_title, '工作细胞')
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertIsNone(sample_actual_page.coll_owner_id)
        self.assertIsNone(sample_actual_page.coll_owner_name)
        self.assertIsNone(sample_actual_page.coll_owner_avatar_url)
        self.assertEqual(sample_actual_page.coll_sect_id, 24588)
        self.assertEqual(sample_actual_page.coll_sect_title, '工作细胞')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_up_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITH_UP_INFO).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(season_id=12548)
        sample_actual_page, *_ = actual_pages

        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 34568185)
        self.assertEqual(sample_actual_page.page_title, '普通话')
        self.assertEqual(sample_actual_page.page_duration, 7598)
        self.assertEqual(sample_actual_page.view_aid, 21071819)
        self.assertEqual(sample_actual_page.view_bvid, 'BV14W411g72d')
        self.assertEqual(sample_actual_page.view_ep_id, 199612)
        self.assertEqual(sample_actual_page.view_season_id, 12548)
        self.assertEqual(sample_actual_page.view_title, '普通话')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'http://i0.hdslb.com/bfs/archive/96a3cd3740536a5b36635f5e6a423f9f0365e698.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1522398180)
        self.assertEqual(sample_actual_page.view_duration, 7598)
        self.assertEqual(
            sample_actual_page.view_owner_id,
            15773384
        )
        self.assertEqual(
            sample_actual_page.view_owner_name,
            '哔哩哔哩电影'
        )
        self.assertEqual(
            sample_actual_page.view_owner_avatar_url,
            'https://i2.hdslb.com/bfs/face/d21a82eb5738155b2b99b5f6102e054e2e0d0700.jpg'
        )
        self.assertEqual(sample_actual_page.coll_id, 4971)
        self.assertEqual(sample_actual_page.coll_title, '民国三部曲')
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertEqual(
            sample_actual_page.coll_owner_id,
            15773384
        )
        self.assertEqual(
            sample_actual_page.coll_owner_name,
            '哔哩哔哩电影'
        )
        self.assertEqual(
            sample_actual_page.coll_owner_avatar_url,
            'https://i2.hdslb.com/bfs/face/d21a82eb5738155b2b99b5f6102e054e2e0d0700.jpg'
        )
        self.assertEqual(sample_actual_page.coll_sect_id, 12548)
        self.assertEqual(sample_actual_page.coll_sect_title, '让子弹飞')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_without_section(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_WITHOUT_SECTION).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=815604)

        expected_length = 0
        expected_length += len(DATA_VIEW_WITHOUT_SECTION['result']['episodes'])
        for section in DATA_VIEW_WITHOUT_SECTION['result'].get('section', []):
            expected_length += len(section['episodes'])

        self.assertEqual(len(actual_pages), expected_length)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_ugc_episode_in_section(self, mocked_request):
        """
        There could be links of UGC resources as PGC's sidelights, which would be ignored
        """
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_SECTION_WITH_UGC_EPISODE).encode('utf-8')
        )
        actual_pages = PGCComponent.get_views(ep_id=249469)

        resources_length = 0
        resources_length += len(DATA_VIEW_SECTION_WITH_UGC_EPISODE['result']['episodes'])
        for section in DATA_VIEW_SECTION_WITH_UGC_EPISODE['result']['section']:
            resources_length += len(section['episodes'])
        self.assertTrue(len(actual_pages) < resources_length)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_connection_error(self, mocked_request):
        mocked_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /pgc/view/web/season?ep_id=232465'
        )
        with self.assertRaises(ConnectionError):
            PGCComponent.get_views(ep_id=232465)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_timeout_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            PGCComponent.get_views(ep_id=232465)

    def test_get_views_without_params(self):
        with self.assertRaises(ValueError):
            PGCComponent.get_views()


class PGCComponentGetPageStreamingSrcTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=34568185
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_sr1-1-100036.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=1a0aead873f447d4cb1f7b253bf6cf4d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=663208&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_prefer_lower_quality_video(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            ep_id=199612,
            is_video_hq_preferred=False
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-100022.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=cosbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=36bbf9a398bbea7be24f18d8a09885a8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=25541&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AV1.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P360.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_video_qn(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=239927346,
            is_video_hq_preferred=False,
            video_qn=QualityNumber.P480.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-100023.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=cosbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=31a82371ce83b835f98fd8091eb8d9a1&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=52833&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AV1.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_but_not_support_video_qn(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=239927346,
            is_video_hq_preferred=False,
            video_qn=QualityNumber.EIGHT_K.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_sr1-1-100036.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=1a0aead873f447d4cb1f7b253bf6cf4d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=663208&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_prefer_not_eff_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=239927346,
            is_video_codec_eff_preferred=False
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_sr1-1-100035.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=89468389f1a2973b67a8ae0d231bd519&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=1201845&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=239927346,
            video_codec_number=VideoCodecID.HEVC.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_sr1-1-100036.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5'
            '&nbs=1&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=1a0aead873f447d4cb1f7b253bf6cf4d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=663208&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_but_not_support_video_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=239927346,
            is_video_codec_eff_preferred=False,
            video_codec_number=VideoCodecID.AV1.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_sr1-1-100036.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=1a0aead873f447d4cb1f7b253bf6cf4d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=663208&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=08'
            '&upsig=e09589c2efdc79bc7d8af0c81c6bcee0&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_64Kbps_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PGCComponent.get_page_streaming_src(
            cid=239927346,
            audio_qn=AudioBitRateID.BPS_64K.value.bit_rate_id
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_sr1-1-100036.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '&uipk=5&nbs=1&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721'
            '&trid=37a603d7d7b849f9b79c977eed3fd45dp&mid=12363921&platform=pc&og=cos'
            '&upsig=1a0aead873f447d4cb1f7b253bf6cf4d&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og'
            '&bvc=vod&nettype=0&orderid=0,3&buvid=&build=0&f=p_0_0&agrr=1&bw=663208&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.FOUR_K.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-estghw.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30216.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721&trid=37a603d7d7b849f9b79c977eed3fd45dp'
            '&mid=12363921&platform=pc&og=08&upsig=0635a254e683e981ad0e88b15f35179b'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=p_0_0&agrr=1&bw=8406&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_64K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    def test_get_page_streaming_src_without_identifier(self):
        with self.assertRaises(ValueError):
            PGCComponent.get_page_streaming_src()
