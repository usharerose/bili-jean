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
    VIDEO_INFO_DATA = json.load(fp)
with open('tests/data/video_stream_BV1X54y1C74U.json', 'r') as fp:
    VIDEO_STREAM_DATA = json.load(fp)
with open('tests/data/video_stream_BV1Ys421M7YM.json', 'r') as fp:
    PAID_VIDEO_STREAM_DATA = json.load(fp)


class ProxyServiceTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_info(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(VIDEO_INFO_DATA).encode('utf-8')
        )

        dm = ProxyService.get_video_info(bvid='BV1X54y1C74U')
        self.assertEqual(dm.code, VIDEO_INFO_DATA['code'])
        self.assertEqual(dm.message, VIDEO_INFO_DATA['message'])
        self.assertEqual(dm.ttl, VIDEO_INFO_DATA['ttl'])

        data = dm.data
        self.assertEqual(data.bvid, VIDEO_INFO_DATA['data']['bvid'])
        self.assertEqual(data.aid, VIDEO_INFO_DATA['data']['aid'])
        self.assertEqual(data.pic, VIDEO_INFO_DATA['data']['pic'])
        self.assertEqual(data.title, VIDEO_INFO_DATA['data']['title'])
        self.assertEqual(data.desc, VIDEO_INFO_DATA['data']['desc'])
        self.assertEqual(data.duration, VIDEO_INFO_DATA['data']['duration'])
        self.assertEqual(data.cid, VIDEO_INFO_DATA['data']['cid'])

        actual_sample_page, *_ = data.pages
        expected_sample_page, *_ = VIDEO_INFO_DATA['data']['pages']
        self.assertEqual(actual_sample_page.cid, expected_sample_page['cid'])
        self.assertEqual(actual_sample_page.page, expected_sample_page['page'])
        self.assertEqual(actual_sample_page.part, expected_sample_page['part'])
        self.assertEqual(actual_sample_page.duration, expected_sample_page['duration'])
        self.assertEqual(actual_sample_page.vid, expected_sample_page['vid'])

        actual_sample_owner = data.owner
        expected_sample_owner = VIDEO_INFO_DATA['data']['owner']
        self.assertEqual(actual_sample_owner.mid, expected_sample_owner['mid'])
        self.assertEqual(actual_sample_owner.name, expected_sample_owner['name'])
        self.assertEqual(actual_sample_owner.face, expected_sample_owner['face'])

        self.assertIsNone(data.staff)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_info_with_connection_error(self, mock_request):
        mock_request.side_effect = ConnectionError(
            'Max retries exceeded with url: /x/web-interface/view?bvid=BV1X54y1C74U'
        )
        with self.assertRaises(ConnectionError):
            ProxyService.get_video_info(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_info_with_timeout_error(self, mock_request):
        mock_request.side_effect = ReadTimeout(
            'HTTPSConnectionPool(host=\'api.bilibili.com\', port=443): Read timed out. (read timeout=5)'
        )
        with self.assertRaises(Timeout):
            ProxyService.get_video_info(bvid='BV1X54y1C74U')

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test__get_video_info_response(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(VIDEO_INFO_DATA).encode('utf-8')
        )

        response = ProxyService._get_video_info_response(bvid='BV1X54y1C74U')

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, VIDEO_INFO_DATA)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test__get_video_info_response_by_aid(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(VIDEO_INFO_DATA).encode('utf-8')
        )

        response = ProxyService._get_video_info_response(aid=842089940)

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, VIDEO_INFO_DATA)

    def test_get_video_info_without_params(self):
        with self.assertRaises(ValueError):
            ProxyService.get_video_info()

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_stream(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(VIDEO_STREAM_DATA).encode('utf-8')
        )

        dm = ProxyService.get_video_stream(
            cid=239927346,
            bvid='BV1X54y1C74U',
            aid=842089940,
            qn=None,
            fnval=16,
            fourk=1
        )
        self.assertEqual(dm.code, VIDEO_STREAM_DATA['code'])
        self.assertEqual(dm.message, VIDEO_STREAM_DATA['message'])
        self.assertEqual(dm.ttl, VIDEO_STREAM_DATA['ttl'])

        data = dm.data
        self.assertEqual(data.quality, VIDEO_STREAM_DATA['data']['quality'])

        self.assertEqual(
            len(dm.data.support_formats),
            len(VIDEO_STREAM_DATA['data']['support_formats'])
        )
        actual_sample_support_format, *_ = dm.data.support_formats
        expected_sample_support_format, *_ = VIDEO_STREAM_DATA['data']['support_formats']
        self.assertEqual(
            actual_sample_support_format.quality,
            expected_sample_support_format['quality']
        )
        self.assertEqual(
            actual_sample_support_format.new_description,
            expected_sample_support_format['new_description']
        )
        self.assertEqual(
            actual_sample_support_format.format_field,
            expected_sample_support_format['format']
        )
        self.assertEqual(
            actual_sample_support_format.display_desc,
            expected_sample_support_format['display_desc']
        )

        actual_sample_dash = dm.data.dash
        expected_sample_dash = VIDEO_STREAM_DATA['data']['dash']
        self.assertEqual(
            actual_sample_dash.duration,
            expected_sample_dash['duration']
        )

        actual_sample_dash_audio, *_ = actual_sample_dash.audio
        expected_sample_dash_audio, *_ = expected_sample_dash['audio']
        self.assertEqual(
            actual_sample_dash_audio.id_field,
            expected_sample_dash_audio['id']
        )
        self.assertEqual(
            actual_sample_dash_audio.base_url,
            expected_sample_dash_audio['base_url']
        )
        self.assertEqual(
            actual_sample_dash_audio.backup_url,
            expected_sample_dash_audio['backup_url']
        )
        self.assertEqual(
            actual_sample_dash_audio.bandwidth,
            expected_sample_dash_audio['bandwidth']
        )
        self.assertEqual(
            actual_sample_dash_audio.mime_type,
            expected_sample_dash_audio['mime_type']
        )
        self.assertEqual(
            actual_sample_dash_audio.codecid,
            expected_sample_dash_audio['codecid']
        )
        self.assertEqual(
            actual_sample_dash_audio.codecs,
            expected_sample_dash_audio['codecs']
        )
        self.assertEqual(
            actual_sample_dash_audio.width,
            expected_sample_dash_audio['width']
        )
        self.assertEqual(
            actual_sample_dash_audio.height,
            expected_sample_dash_audio['height']
        )

        self.assertIsNone(actual_sample_dash.flac)

        actual_sample_dash_dolby = actual_sample_dash.dolby
        expected_sample_dash_dolby = expected_sample_dash['dolby']
        self.assertEqual(
            actual_sample_dash_dolby.type_field,
            expected_sample_dash_dolby['type']
        )
        self.assertIsNone(actual_sample_dash_dolby.audio)

        actual_sample_dash_video, *_ = actual_sample_dash.video
        expected_sample_dash_video, *_ = expected_sample_dash['video']
        self.assertEqual(
            actual_sample_dash_video.id_field,
            expected_sample_dash_video['id']
        )
        self.assertEqual(
            actual_sample_dash_video.base_url,
            expected_sample_dash_video['base_url']
        )
        self.assertEqual(
            actual_sample_dash_video.backup_url,
            expected_sample_dash_video['backup_url']
        )
        self.assertEqual(
            actual_sample_dash_video.bandwidth,
            expected_sample_dash_video['bandwidth']
        )
        self.assertEqual(
            actual_sample_dash_video.mime_type,
            expected_sample_dash_video['mime_type']
        )
        self.assertEqual(
            actual_sample_dash_video.codecid,
            expected_sample_dash_video['codecid']
        )
        self.assertEqual(
            actual_sample_dash_video.codecs,
            expected_sample_dash_video['codecs']
        )
        self.assertEqual(
            actual_sample_dash_video.width,
            expected_sample_dash_video['width']
        )
        self.assertEqual(
            actual_sample_dash_video.height,
            expected_sample_dash_video['height']
        )

    def test_get_video_stream_without_bv_or_av_id(self):
        with self.assertRaises(ValueError):
            ProxyService.get_video_stream(
                cid=239927346,
                bvid=None,
                aid=None,
                qn=None,
                fnval=16,
                fourk=1
            )

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_video_stream_by_aid(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(VIDEO_STREAM_DATA).encode('utf-8')
        )

        dm = ProxyService.get_video_stream(
            cid=239927346,
            bvid=None,
            aid=842089940,
            qn=None,
            fnval=16,
            fourk=1
        )
        actual_sample_dash_video, *_ = dm.data.dash.video
        expected_sample_dash_video, *_ = VIDEO_STREAM_DATA['data']['dash']['video']
        self.assertEqual(
            actual_sample_dash_video.base_url,
            expected_sample_dash_video['base_url']
        )

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_get_paid_video_stream_without_privilege(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(PAID_VIDEO_STREAM_DATA).encode('utf-8')
        )

        dm = ProxyService.get_video_stream(
            cid=1566548814,
            bvid='BV1Ys421M7YM',
            aid=1855474163,
            qn=None,
            fnval=16,
            fourk=1
        )
        self.assertEqual(dm.code, PAID_VIDEO_STREAM_DATA['code'])
        self.assertEqual(dm.message, PAID_VIDEO_STREAM_DATA['message'])
        self.assertEqual(dm.ttl, PAID_VIDEO_STREAM_DATA['ttl'])

        data = dm.data
        # for paid video which has no privilege,
        # there would be no DASH even though request with `fnval=16`
        self.assertIsNone(data.dash)

        actual_sample_durl, *_ = dm.data.durl
        expected_sample_durl, *_ = PAID_VIDEO_STREAM_DATA['data']['durl']
        self.assertEqual(
            actual_sample_durl.order,
            expected_sample_durl['order']
        )
        self.assertEqual(
            actual_sample_durl.length,
            expected_sample_durl['length']
        )
        self.assertEqual(
            actual_sample_durl.size,
            expected_sample_durl['size']
        )
        self.assertEqual(
            actual_sample_durl.url,
            expected_sample_durl['url']
        )
        self.assertEqual(
            actual_sample_durl.backup_url,
            expected_sample_durl['backup_url']
        )
