"""
Unit test for UserService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.user_service import UserService
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/my_info/my_info_1532165.json', 'r') as fp:
    DATA_MY_INFO = json.load(fp)
with open('tests/mock_data/proxy/my_info/my_info_not_login.json', 'r') as fp:
    DATA_MY_INFO_NOT_LOGIN = json.load(fp)


class UserServiceTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_validate(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_MY_INFO).encode('utf-8')
        )
        result = UserService.validate(
            sess_data='mock-sess-data'
        )
        self.assertTrue(result)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_validate_invalid_sess_data(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_MY_INFO_NOT_LOGIN).encode('utf-8')
        )
        result = UserService.validate()
        self.assertFalse(result)
