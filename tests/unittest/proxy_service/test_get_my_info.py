"""
Unit test for get_my_info of ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/my_info/my_info_1532165.json', 'r') as fp:
    DATA_MY_INFO = json.load(fp)
with open('tests/mock_data/proxy/my_info/my_info_not_login.json', 'r') as fp:
    DATA_MY_INFO_NOT_LOGIN = json.load(fp)


class ProxyServiceGetMyInfoTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_my_info_basic(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_MY_INFO).encode('utf-8')
        )
        actual_dm = ProxyService.get_my_info(
            sess_data='mock-sess-data'
        )
        self.assertEqual(actual_dm.code, DATA_MY_INFO['code'])
        self.assertEqual(actual_dm.message, DATA_MY_INFO['message'])
        self.assertEqual(actual_dm.ttl, DATA_MY_INFO['ttl'])
        self.assertIsNotNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_my_info_data(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_MY_INFO).encode('utf-8')
        )
        actual_data = ProxyService.get_my_info(
            sess_data='mock-sess-data'
        ).data
        expected_data = DATA_MY_INFO['data']

        self.assertEqual(actual_data.mid, expected_data['mid'])
        self.assertEqual(actual_data.name, expected_data['name'])
        self.assertEqual(actual_data.face, expected_data['face'])
        self.assertEqual(actual_data.sign, expected_data['sign'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_my_info_not_login(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_MY_INFO_NOT_LOGIN).encode('utf-8')
        )
        actual_dm = ProxyService.get_my_info(
            sess_data='expired-sess-data'
        )

        self.assertEqual(actual_dm.code, DATA_MY_INFO_NOT_LOGIN['code'])
        self.assertEqual(actual_dm.ttl, DATA_MY_INFO_NOT_LOGIN['ttl'])
        self.assertEqual(actual_dm.message, DATA_MY_INFO_NOT_LOGIN['message'])
        self.assertIsNone(actual_dm.data)
