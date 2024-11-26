"""
Unit test for PUGVComponent
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
from bili_jean.streaming.components import PUGVComponent
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/pugv_play/pugv_play_ep482484.json', 'r') as fp:
    DATA_PLAY = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ss6838.json', 'r') as fp:
    DATA_VIEW = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ss2.json', 'r') as fp:
    DATA_VIEW_NOT_EXIST = json.load(fp)


class PUGVComponentTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_by_not_exist_season_id(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW_NOT_EXIST).encode('utf-8')
        )
        actual_pages = PUGVComponent.get_views(season_id=2)
        self.assertIsNone(actual_pages)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_VIEW).encode('utf-8')
        )
        actual_pages = PUGVComponent.get_views(season_id=6838)

        expected_length = 0
        expected_length += len(DATA_VIEW['data']['episodes'])

        self.assertEqual(len(actual_pages), expected_length)
        sample_actual_page, *_ = actual_pages

        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PUGV.value)
        self.assertEqual(sample_actual_page.page_index, 1)
        self.assertEqual(sample_actual_page.page_cid, 1313813259)
        self.assertEqual(sample_actual_page.page_title, '马克思的哲学革命及其当代意义')
        self.assertEqual(sample_actual_page.page_duration, 239)
        self.assertEqual(sample_actual_page.view_aid, 277630557)
        self.assertIsNone(sample_actual_page.view_bvid)
        self.assertEqual(sample_actual_page.view_ep_id, 261830)
        self.assertEqual(sample_actual_page.view_season_id, 6838)
        self.assertEqual(sample_actual_page.view_title, '马克思的哲学革命及其当代意义')
        self.assertEqual(sample_actual_page.view_desc, '')
        self.assertEqual(
            sample_actual_page.view_cover_url,
            'https://archive.biliimg.com/bfs/archive/caf0edf6f943c1f0d674a7620bb1bdaf8cbda2dd.jpg'
        )
        self.assertEqual(sample_actual_page.view_pub_time, 1698497411)
        self.assertEqual(sample_actual_page.view_duration, 239)
        self.assertEqual(sample_actual_page.view_owner_id, 514924891)
        self.assertEqual(sample_actual_page.view_owner_name, '王德峰')
        self.assertEqual(
            sample_actual_page.view_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/044a0dfa856d37b23eb87fdc4216745af38358b7.jpg'
        )
        self.assertIsNone(sample_actual_page.coll_id)
        self.assertIsNone(sample_actual_page.coll_title)
        self.assertIsNone(sample_actual_page.coll_desc)
        self.assertIsNone(sample_actual_page.coll_cover_url)
        self.assertEqual(sample_actual_page.coll_owner_id, 514924891)
        self.assertEqual(sample_actual_page.coll_owner_name, '王德峰')
        self.assertEqual(
            sample_actual_page.coll_owner_avatar_url,
            'https://i1.hdslb.com/bfs/face/044a0dfa856d37b23eb87fdc4216745af38358b7.jpg'
        )
        self.assertEqual(sample_actual_page.coll_sect_id, 6838)
        self.assertEqual(sample_actual_page.coll_sect_title, '王德峰哲学课：马克思的哲学革命及其当代意义')
        self.assertTrue(sample_actual_page.is_selected_page)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_connection_error(self, mocked_request):
        mocked_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /pugv/view/web/season?season_id=6838'
        )
        with self.assertRaises(ConnectionError):
            PUGVComponent.get_views(season_id=6838)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_views_with_timeout_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            PUGVComponent.get_views(season_id=6838)

    def test_get_views_without_params(self):
        with self.assertRaises(ValueError):
            PUGVComponent.get_views()


class PUGVComponentGetPageStreamingSrcTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100143.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=6a8bd0937951172427f01b38a41e5e40'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=177712&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_prefer_lower_quality_video(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            is_video_hq_preferred=False
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-estghw.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100109.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=upos&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=08&upsig=54e963f129c2b0c52cab01c76e2a46c0'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21045&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P360.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_video_qn(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            is_video_hq_preferred=False,
            video_qn=QualityNumber.P480.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100110.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=536105a034242d7a22f7edd874925596'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=30246&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.P480.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_but_not_support_video_qn(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            is_video_hq_preferred=False,
            video_qn=QualityNumber.EIGHT_K.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100143.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=6a8bd0937951172427f01b38a41e5e40'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=177712&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_prefer_not_eff_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            is_video_codec_eff_preferred=False
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30112.m4s'
            '?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=bdbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=08&upsig=510f90cdbf378dc7cff2a1f39043048f'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=391935&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            video_codec_number=VideoCodecID.AVC.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30112.m4s'
            '?e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=bdbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=08&upsig=510f90cdbf378dc7cff2a1f39043048f'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=391935&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.AVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_declared_but_not_support_video_codec(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            is_video_codec_eff_preferred=False,
            video_codec_number=VideoCodecID.AV1.value
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100143.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=6a8bd0937951172427f01b38a41e5e40'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=177712&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_64Kbps_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            audio_qn=AudioBitRateID.BPS_64K.value.bit_rate_id
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100143.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=6a8bd0937951172427f01b38a41e5e40'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=177712&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30216.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=fc93b9d7bd8e5b986f7f8ede04f707cd'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=5741&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_64K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_page_streaming_src_with_not_supported_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video_src, actual_audio_src = PUGVComponent.get_page_streaming_src(
            ep_id=482484,
            audio_qn=AudioBitRateID.BPS_DOLBY.value.bit_rate_id
        )
        self.assertEqual(
            actual_video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100143.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=6a8bd0937951172427f01b38a41e5e40'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=177712&logo=80000000'
        )
        self.assertEqual(actual_video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(actual_video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(actual_video_src.mime_type, 'video/mp4')
        self.assertEqual(
            actual_audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5'
            '&nbs=1&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3&buvid='
            '&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(actual_audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(actual_audio_src.mime_type, 'audio/mp4')

    def test_get_page_streaming_src_without_identifier(self):
        with self.assertRaises(ValueError):
            PUGVComponent.get_page_streaming_src()
