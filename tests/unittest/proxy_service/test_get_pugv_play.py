"""
Unit test for get_pgc_play of ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

import pytest

from bili_jean.constants import FormatNumberValue, QualityNumber
from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/pugv_play/pugv_play_ep482484.json', 'r') as fp:
    DATA_PLAY = json.load(fp)
with open('tests/mock_data/proxy/pugv_play/pugv_play_ep1.json', 'r') as fp:
    DATA_PLAY_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/pugv_play/pugv_play_ep482535_unpurchased.json', 'r') as fp:
    DATA_PLAY_UNPURCHASED = json.load(fp)
with open('tests/mock_data/proxy/pugv_play/pugv_play_ep482485_trial.json', 'r') as fp:
    DATA_PLAY_TRIAL = json.load(fp)


class ProxyServiceGetPGCPlayTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_dm = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        )
        self.assertEqual(actual_dm.code, DATA_PLAY['code'])
        self.assertEqual(actual_dm.message, DATA_PLAY['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNotNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_not_effective_request(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY_NOT_EXIST).encode('utf-8')
        )
        actual_dm = ProxyService.get_pugv_play(
            ep_id=1,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        )
        self.assertEqual(actual_dm.code, DATA_PLAY_NOT_EXIST['code'])
        self.assertEqual(actual_dm.message, DATA_PLAY_NOT_EXIST['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_data = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data
        expected_data = DATA_PLAY['data']

        self.assertEqual(actual_data.quality, expected_data['quality'])
        self.assertIsNotNone(actual_data.dash)
        self.assertIsNone(actual_data.durl)
        self.assertIsNotNone(actual_data.support_formats)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_dash_basic_info(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_dash = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.dash
        expected_dash = DATA_PLAY['data']['dash']

        self.assertEqual(actual_dash.duration, expected_dash['duration'])
        self.assertIsNotNone(actual_dash.audio, expected_dash['audio'])
        self.assertIsNotNone(actual_dash.dolby, expected_dash['dolby'])
        self.assertIsNone(actual_dash.flac)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_dash_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_audio = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.dash.audio
        self.assertIsInstance(actual_audio, list)
        self.assertEqual(len(actual_audio), len(DATA_PLAY['data']['dash']['audio']))
        sample_actual_audio, *_ = actual_audio
        sample_expected_audio, *_ = DATA_PLAY['data']['dash']['audio']

        self.assertEqual(sample_actual_audio.backup_url, sample_expected_audio['backup_url'])
        self.assertEqual(sample_actual_audio.bandwidth, sample_expected_audio['bandwidth'])
        self.assertEqual(sample_actual_audio.base_url, sample_expected_audio['base_url'])
        self.assertEqual(sample_actual_audio.codecid, sample_expected_audio['codecid'])
        self.assertEqual(sample_actual_audio.codecs, sample_expected_audio['codecs'])
        self.assertEqual(sample_actual_audio.height, sample_expected_audio['height'])
        self.assertEqual(sample_actual_audio.id_field, sample_expected_audio['id'])
        self.assertEqual(sample_actual_audio.mime_type, sample_expected_audio['mime_type'])
        self.assertEqual(sample_actual_audio.width, sample_expected_audio['width'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_dash_without_dolby_audio(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_dolby = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.dash.dolby
        expected_dolby = DATA_PLAY['data']['dash']['dolby']

        self.assertEqual(actual_dolby.type_field, expected_dolby['type'])
        self.assertIsInstance(actual_dolby.audio, list)
        self.assertEqual(len(actual_dolby.audio), 0)

    @pytest.mark.skip(reason="No sample case data which PUGV has Dolby vision and audio")
    def test_pugv_play_dash_with_dolby_audio(self):
        raise AssertionError

    @pytest.mark.skip(reason="No sample case data which PUGV has Hi-Res audio")
    def test_pugv_play_dash_with_hires(self):
        raise AssertionError

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_dash_video(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_video = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.dash.video
        self.assertIsInstance(actual_video, list)
        self.assertEqual(len(actual_video), len(DATA_PLAY['data']['dash']['video']))
        sample_actual_video, *_ = actual_video
        sample_expected_video, *_ = DATA_PLAY['data']['dash']['video']

        self.assertEqual(sample_actual_video.backup_url, sample_expected_video['backup_url'])
        self.assertEqual(sample_actual_video.bandwidth, sample_expected_video['bandwidth'])
        self.assertEqual(sample_actual_video.base_url, sample_expected_video['base_url'])
        self.assertEqual(sample_actual_video.codecid, sample_expected_video['codecid'])
        self.assertEqual(sample_actual_video.codecs, sample_expected_video['codecs'])
        self.assertEqual(sample_actual_video.height, sample_expected_video['height'])
        self.assertEqual(sample_actual_video.id_field, sample_expected_video['id'])
        self.assertEqual(sample_actual_video.mime_type, sample_expected_video['mime_type'])
        self.assertEqual(sample_actual_video.width, sample_expected_video['width'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_without_privilege(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY_UNPURCHASED).encode('utf-8')
        )
        actual_dm = ProxyService.get_pugv_play(
            ep_id=482535,
            qn=QualityNumber.P1080.value,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        )

        self.assertEqual(actual_dm.code, DATA_PLAY_UNPURCHASED['code'])
        self.assertEqual(actual_dm.message, DATA_PLAY_UNPURCHASED['message'])
        self.assertIsNone(actual_dm.ttl)
        self.assertIsNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_trial_durl(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY_TRIAL).encode('utf-8')
        )
        actual_durl = ProxyService.get_pugv_play(
            ep_id=482485,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.durl
        self.assertIsInstance(actual_durl, list)
        self.assertEqual(len(actual_durl), len(DATA_PLAY_TRIAL['data']['durl']))
        sample_actual_durl, *_ = actual_durl
        sample_expected_durl, *_ = DATA_PLAY_TRIAL['data']['durl']

        self.assertEqual(sample_actual_durl.length, sample_expected_durl['length'])
        self.assertEqual(sample_actual_durl.order, sample_expected_durl['order'])
        self.assertEqual(sample_actual_durl.size, sample_expected_durl['size'])
        self.assertEqual(sample_actual_durl.url, sample_expected_durl['url'])

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_trial_durl_backup_url(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY_TRIAL).encode('utf-8')
        )
        actual_backup_url = ProxyService.get_pugv_play(
            ep_id=482485,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.durl[0].backup_url
        self.assertIsInstance(actual_backup_url, list)
        self.assertEqual(len(actual_backup_url), len(DATA_PLAY_TRIAL['data']['durl'][0]['backup_url']))
        sample_actual_backup_url, *_ = actual_backup_url
        sample_expected_backup_url, *_ = DATA_PLAY_TRIAL['data']['durl'][0]['backup_url']

        self.assertEqual(sample_actual_backup_url, sample_expected_backup_url)

    @patch('bili_jean.proxy_service.ProxyService._get')
    def test_pugv_play_support_formats(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_PLAY).encode('utf-8')
        )
        actual_support_formats = ProxyService.get_pugv_play(
            ep_id=482484,
            qn=None,
            fnval=FormatNumberValue.DASH.value,
            fourk=1,
            sess_data='mock-sess-data'
        ).data.support_formats
        self.assertIsInstance(actual_support_formats, list)
        self.assertEqual(len(actual_support_formats), len(DATA_PLAY['data']['support_formats']))
        sample_actual_support_format, *_ = actual_support_formats
        sample_expected_support_format, *_ = DATA_PLAY['data']['support_formats']

        self.assertEqual(
            sample_actual_support_format.codecs,
            sample_expected_support_format['codecs']
        )
        self.assertEqual(
            sample_actual_support_format.display_desc,
            sample_expected_support_format['display_desc']
        )
        self.assertEqual(
            sample_actual_support_format.format_field,
            sample_expected_support_format['format']
        )
        self.assertEqual(
            sample_actual_support_format.new_description,
            sample_expected_support_format['new_description']
        )
        self.assertEqual(
            sample_actual_support_format.quality,
            sample_expected_support_format['quality']
        )
