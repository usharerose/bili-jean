"""
Unit test for ProxyService
"""
from http import HTTPStatus
import json
from unittest import TestCase
from unittest.mock import patch

from bili_jean.proxy_service import ProxyService
from tests.utils import get_mocked_response


with open('tests/data/video_info_BV1X54y1C74U.json', 'r') as fp:
    DATA = json.load(fp)


class ProxyServiceTestCase(TestCase):

    @patch('bili_jean.proxy_service.requests.get')
    def test_request(self, mock_request):
        mock_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            json.dumps(DATA).encode('utf-8')
        )

        response = ProxyService.get_video_info(bvid='BV1X54y1C74U')

        actual_data = json.loads(response.content.decode('utf-8'))
        self.assertDictEqual(actual_data, DATA)
