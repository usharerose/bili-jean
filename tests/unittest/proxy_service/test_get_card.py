"""
Unit test for get_card of ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/mock_data/proxy/card/card_1532165.json', 'r') as fp:
    DATA_CARD = json.load(fp)
with open('tests/mock_data/proxy/card/card_10000000000.json', 'r') as fp:
    DATA_CARD_NOT_EXIST = json.load(fp)
with open('tests/mock_data/proxy/card/card_0.json', 'r') as fp:
    DATA_CARD_WITH_EXCEPTION = json.load(fp)


class ProxyServiceGetCardTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_card_basic(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_CARD).encode('utf-8')
        )
        actual_dm = ProxyService.get_card(
            mid=1532165,
            photo=True
        )
        self.assertEqual(actual_dm.code, DATA_CARD['code'])
        self.assertEqual(actual_dm.message, DATA_CARD['message'])
        self.assertEqual(actual_dm.ttl, DATA_CARD['ttl'])
        self.assertIsNotNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_card_data(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_CARD).encode('utf-8')
        )
        actual_data = ProxyService.get_card(
            mid=1532165,
            photo=True
        ).data
        expected_data = DATA_CARD['data']

        self.assertIsNotNone(actual_data.card)
        self.assertEqual(actual_data.following, expected_data['following'])
        self.assertEqual(actual_data.follower, expected_data['follower'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_card_data_card(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_CARD).encode('utf-8')
        )
        actual_card = ProxyService.get_card(
            mid=1532165,
            photo=True
        ).data.card
        expected_card = DATA_CARD['data']['card']

        self.assertEqual(actual_card.mid, int(expected_card['mid']))
        self.assertEqual(actual_card.name, expected_card['name'])
        self.assertEqual(actual_card.face, expected_card['face'])
        self.assertEqual(actual_card.sign, expected_card['sign'])

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_my_info_not_exist(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_CARD_NOT_EXIST).encode('utf-8')
        )
        actual_dm = ProxyService.get_card(
            mid=10000000000,
            photo=True
        )

        self.assertEqual(actual_dm.code, DATA_CARD_NOT_EXIST['code'])
        self.assertEqual(actual_dm.ttl, DATA_CARD_NOT_EXIST['ttl'])
        self.assertEqual(actual_dm.message, DATA_CARD_NOT_EXIST['message'])
        self.assertIsNone(actual_dm.data)

    @patch('bili_jean.proxy_service.ProxyService.get')
    def test_get_card_with_exception(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA_CARD_WITH_EXCEPTION).encode('utf-8')
        )
        actual_dm = ProxyService.get_card(
            mid=10000000000,
            photo=True
        )

        self.assertEqual(actual_dm.code, DATA_CARD_WITH_EXCEPTION['code'])
        self.assertEqual(actual_dm.ttl, DATA_CARD_WITH_EXCEPTION['ttl'])
        self.assertEqual(actual_dm.message, DATA_CARD_WITH_EXCEPTION['message'])
        self.assertIsNone(actual_dm.data)
