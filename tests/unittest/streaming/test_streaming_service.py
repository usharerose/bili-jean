"""
Unit test for StreamingService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from requests.exceptions import InvalidSchema, MissingSchema, ReadTimeout
from requests.structures import CaseInsensitiveDict

from bili_jean.constants import (
    AudioBitRateID,
    QualityNumber,
    StreamingCategory,
    VideoCodecID
)
from bili_jean.schemes import Page
from bili_jean.streaming.streaming_service import StreamingService
from tests.utils import get_mocked_response


DATA_HTML = '<!DOCTYPE html><html lang="zh-Hans"></html>'


with open('tests/mock_data/proxy/pgc_play/pgc_play_ep199612.json', 'r') as fp:
    DATA_PGC_PLAY = json.load(fp)
with open('tests/mock_data/proxy/pugv_play/pugv_play_ep482484.json', 'r') as fp:
    DATA_PUGV_PLAY = json.load(fp)
with open('tests/mock_data/proxy/pugv_play/pugv_play_ep482535_unpurchased.json', 'r') as fp:
    DATA_PUGV_PLAY_UNPURCHASED = json.load(fp)
with open('tests/mock_data/proxy/ugc_play/ugc_play_BV1X54y1C74U.json', 'r') as fp:
    DATA_UGC_PLAY = json.load(fp)
with open('tests/mock_data/proxy/pgc_view/pgc_view_ss12548.json', 'r') as fp:
    DATA_PGC_VIEW = json.load(fp)
with open('tests/mock_data/proxy/pugv_view/pugv_view_ep482484.json', 'r') as fp:
    DATA_PUGV_VIEW = json.load(fp)
with open('tests/mock_data/proxy/ugc_view/ugc_view_BV1X54y1C74U.json', 'r') as fp:
    DATA_UGC_VIEW = json.load(fp)


class StreamingServiceParseWebViewURLTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_ugc_url_with_bvid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV1tN4y1F79k?'
            'vd_source=eab9f46166d54e0b07ace25e908097ae&'
            'spm_id_from=333.788.videopod.sections'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict({
                'Location': (
                    '/video/BV1tN4y1F79k?'
                    'vd_source=eab9f46166d54e0b07ace25e908097ae&'
                    'spm_id_from=333.788.videopod.sections'
                )
            })
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.UGC)
        self.assertIsNone(actual_dm.aid)
        self.assertEqual(actual_dm.bvid, 'BV1tN4y1F79k')
        self.assertIsNone(actual_dm.ep_id)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_ugc_url_with_aid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/av2271112/?'
            'vd_source=eab9f46166d54e0b07ace25e908097ae'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.UGC)
        self.assertEqual(actual_dm.aid, 2271112)
        self.assertIsNone(actual_dm.bvid)
        self.assertIsNone(actual_dm.ep_id)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_season_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/bangumi/play/ss357?'
            'from_spmid=666.25.series.0'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertIsNone(actual_dm.ep_id)
        self.assertEqual(actual_dm.season_id, 357)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_ep_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/bangumi/play/ep249470?'
            'from_spmid=666.25.episode.0'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 249470)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_bvid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV1tL4y1i7UZ/'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict({
                'Location': 'https://www.bilibili.com/bangumi/play/ep249470'
            })
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 249470)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pgc_url_with_aid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/av31703892/'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict({
                'Location': 'https://www.bilibili.com/bangumi/play/ep249469'
            })
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PGC)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 249469)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_url_with_season_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/cheese/play/ss13194'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PUGV)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertIsNone(actual_dm.ep_id)
        self.assertEqual(actual_dm.season_id, 13194)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_pugv_url_with_ep_id(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/cheese/play/ep482484'
        )
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            DATA_HTML.encode('utf-8'),
            CaseInsensitiveDict()
        )

        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.PUGV)
        self.assertIsNone(actual_dm.aid)
        self.assertIsNone(actual_dm.bvid)
        self.assertEqual(actual_dm.ep_id, 482484)
        self.assertIsNone(actual_dm.season_id)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_non_url_input(self, mocked_request):
        mocked_request.side_effect = MissingSchema(
            'Invalid URL \'something\': No scheme supplied. Perhaps you meant https://mock_string?'
        )

        sample_url = 'mock_string'
        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertIsNone(actual_dm)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_invalid_url(self, mocked_request):
        mocked_request.side_effect = InvalidSchema(
            'No connection adapters were found for \'ftp://mock_string\''
        )

        sample_url = 'ftp://mock_string'
        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertIsNone(actual_dm)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_invalid_url_but_contains_path(self, mocked_request):
        mocked_request.side_effect = MissingSchema(
            'Invalid URL \'/video/BV1tN4y1F79k\': '
            'No scheme supplied. Perhaps you meant https:///video/BV1tN4y1F79k?'
        )

        sample_url = '/video/BV1tN4y1F79k'
        actual_dm = StreamingService.parse_web_view_url(sample_url)
        self.assertEqual(actual_dm.streaming_category, StreamingCategory.UGC)
        self.assertIsNone(actual_dm.aid)
        self.assertEqual(actual_dm.bvid, 'BV1tN4y1F79k')
        self.assertIsNone(actual_dm.ep_id)
        self.assertIsNone(actual_dm.season_id)


class StreamingServiceGetViewsTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_ugc_views(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV1X54y1C74U'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict({
                    'Location': (
                        '/video/BV1X54y1C74U/'
                    )
                })
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_UGC_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.UGC.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pgc_views(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/bangumi/play/ss12548'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict()
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_PGC_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pgc_views_by_url_with_bvid(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/video/BV14W411g72d/'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict({
                    'Location': 'https://www.bilibili.com/bangumi/play/ep199612'
                })
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_PGC_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PGC.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pugv_views(self, mocked_request):
        sample_url = (
            'https://www.bilibili.com/cheese/play/ep482484'
        )
        mocked_request.side_effect = [
            get_mocked_response(
                HTTPStatus.OK.value,
                DATA_HTML.encode('utf-8'),
                CaseInsensitiveDict()
            ),
            get_mocked_response(
                HTTPStatus.OK.value,
                json.dumps(DATA_PUGV_VIEW).encode('utf-8')
            )
        ]

        sample_actual_page, *_ = StreamingService.get_views(sample_url)
        self.assertIsInstance(sample_actual_page, Page)
        self.assertEqual(sample_actual_page.page_category, StreamingCategory.PUGV.value)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_invalid_url(self, mocked_request):
        sample_url = 'ftp://mock_string'
        mocked_request.side_effect = InvalidSchema(
            'No connection adapters were found for \'ftp://mock_string\''
        )

        with self.assertRaises(ValueError):
            StreamingService.get_views(sample_url)


class StreamingServiceGetPageStreamingSrcTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_ugc_page_streaming_src(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_UGC_PLAY).encode('utf-8')
        )
        video_src, audio_src = StreamingService.get_page_streaming_src(
            category='ugc',
            cid=239927346,
            bvid='BV1X54y1C74U',
            video_qn=QualityNumber.P480.value,
            video_codec_number=VideoCodecID.HEVC.value,
            audio_qn=AudioBitRateID.BPS_132K.value.bit_rate_id
        )

        self.assertEqual(
            video_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/46/73/239927346/239927346_x2-1-30033.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M='
            '\\u0026uipk=5\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=cosbv'
            '\\u0026oi=1929021803\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0\\u0026platform=pc'
            '\\u0026og=cos\\u0026upsig=9db3cff93d80797550f851d7ae044318'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod\\u0026nettype=0'
            '\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0\\u0026agrr=0'
            '\\u0026bw=39113\\u0026logo=80000000'
        )
        self.assertEqual(video_src.qn, QualityNumber.P480.value)
        self.assertEqual(video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(video_src.mime_type, 'video/mp4')
        self.assertEqual(
            audio_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-30232.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=\\u0026uipk=5'
            '\\u0026nbs=1\\u0026deadline=1728826357\\u0026gen=playurlv2\\u0026os=upos\\u0026oi=1929021803'
            '\\u0026trid=4cc3bb76000944a8b32cd0333abcfad8u\\u0026mid=0\\u0026platform=pc\\u0026og=hw'
            '\\u0026upsig=f9d4e954eca822bda3deeb6d55e03264'
            '\\u0026uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og\\u0026bvc=vod\\u0026nettype=0'
            '\\u0026orderid=0,3\\u0026buvid=\\u0026build=0\\u0026f=u_0_0\\u0026agrr=0'
            '\\u0026bw=16667\\u0026logo=80000000'
        )
        self.assertEqual(audio_src.qn, AudioBitRateID.BPS_132K.value.bit_rate_id)
        self.assertEqual(audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_ugc_page_streaming_src_with_http_error(self, mocked_request):
        mocked_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(ReadTimeout):
            StreamingService.get_page_streaming_src(
                category='ugc',
                cid=239927346,
                bvid='BV1X54y1C74U',
                video_qn=QualityNumber.P480.value,
                video_codec_number=VideoCodecID.HEVC.value,
                audio_qn=AudioBitRateID.BPS_132K.value.bit_rate_id
            )

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pgc_page_streaming_src(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PGC_PLAY).encode('utf-8')
        )
        video_src, audio_src = StreamingService.get_page_streaming_src(
            category='pgc',
            cid=34568185,
            bvid='BV14W411g72e',
            video_qn=QualityNumber.PPLUS_1080.value,
            video_codec_number=VideoCodecID.AVC.value,
            audio_qn=AudioBitRateID.BPS_192K.value.bit_rate_id
        )

        self.assertEqual(
            video_src.url,
            'https://upos-sz-estgoss.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30112.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730801113&gen=playurlv2&os=upos&oi=2071715721&trid=37a603d7d7b849f9b79c977eed3fd45dp'
            '&mid=12363921&platform=pc&og=08&upsig=0a284a9dde2d91619c3d873a60d5f86b'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=p_0_0&agrr=1&bw=477918&logo=80000000'
        )
        self.assertEqual(video_src.qn, QualityNumber.PPLUS_1080.value)
        self.assertEqual(video_src.codec_id, VideoCodecID.AVC.value)
        self.assertEqual(video_src.mime_type, 'video/mp4')
        self.assertEqual(
            audio_src.url,
            'https://upos-sz-mirrorbd.bilivideo.com/upgcxcode/85/81/34568185/34568185_p1-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730801113&gen=playurlv2&os=bdbv&oi=2071715721&trid=37a603d7d7b849f9b79c977eed3fd45dp'
            '&mid=12363921&platform=pc&og=08&upsig=e09589c2efdc79bc7d8af0c81c6bcee0'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=p_0_0&agrr=1&bw=39881&logo=80000000'
        )
        self.assertEqual(audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pugv_page_streaming_src(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PUGV_PLAY).encode('utf-8')
        )
        video_src, audio_src = StreamingService.get_page_streaming_src(
            category='pugv',
            ep_id=482484,
            video_qn=QualityNumber.P1080.value,
            video_codec_number=VideoCodecID.HEVC.value,
            audio_qn=AudioBitRateID.BPS_192K.value.bit_rate_id
        )

        self.assertEqual(
            video_src.url,
            'https://upos-sz-estghw.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-100113.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=upos&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=08&upsig=84dafcc06ce9f3b12d76e8d0d6633d33'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=85423&logo=80000000'
        )
        self.assertEqual(video_src.qn, QualityNumber.P1080.value)
        self.assertEqual(video_src.codec_id, VideoCodecID.HEVC.value)
        self.assertEqual(video_src.mime_type, 'video/mp4')
        self.assertEqual(
            audio_src.url,
            'https://upos-sz-mirrorcos.bilivideo.com/upgcxcode/25/99/1444089925/1444089925-1-30280.m4s?'
            'e=ig8euxZM2rNcNbdlhoNvNC8BqJIzNbfqXBvEqxTEto8BTrNvN0GvT90W5JZMkX_'
            'YN0MvXg8gNEV4NC8xNEV4N03eN0B5tZlqNxTEto8BTrNvNeZVuJ10Kj_'
            'g2UB02J0mN0B5tZlqNCNEto8BTrNvNC7MTX502C8f2jmMQJ6mqF2fka1mqx6gqj0eN0B599M=&uipk=5&nbs=1'
            '&deadline=1730824061&gen=playurlv2&os=cosbv&oi=2071715721&trid=84ab82a4174540899e7f9fae8bb349dcu'
            '&mid=0&platform=pc&og=cos&upsig=dd554ca81997015e71ab3db1f6779711'
            '&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform,og&bvc=vod&nettype=0&orderid=0,3'
            '&buvid=&build=0&f=u_0_0&agrr=0&bw=21748&logo=80000000'
        )
        self.assertEqual(audio_src.qn, AudioBitRateID.BPS_192K.value.bit_rate_id)
        self.assertEqual(audio_src.mime_type, 'audio/mp4')

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_pugv_page_streaming_src_unpurchased(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PUGV_PLAY_UNPURCHASED).encode('utf-8')
        )
        with self.assertRaises(ValueError) as context:
            StreamingService.get_page_streaming_src(
                category='pugv',
                ep_id=482535,
                video_qn=QualityNumber.P1080.value,
                video_codec_number=VideoCodecID.HEVC.value,
                audio_qn=AudioBitRateID.BPS_192K.value.bit_rate_id
            )
        self.assertEqual(
            str(context.exception),
            'request play data error: 访问权限不足'
        )
