"""
Unit test for PageDownloadService
"""
import copy
from http import HTTPStatus
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch, MagicMock

from requests.structures import CaseInsensitiveDict

from bili_jean.constants import HEADERS
from bili_jean.page_download_service import DownloadError, PageDownloadService
from tests.utils import get_mocked_response


class PageDownloadServiceTestCase(TestCase):

    @patch('bili_jean.proxy_service.ProxyService.head')
    def test_remote_file_size(self, mocked_request):
        mocked_request.return_value = get_mocked_response(
            HTTPStatus.OK.value,
            ''.encode('utf-8'),
            CaseInsensitiveDict({
                'Date': 'Tue, 26 Nov 2024 13:17:22 GMT',
                'Content-Type': 'application/octet-stream',
                'Content-Length': '41231718',
                'Connection': 'keep-alive',
                'X-Upsig-Version': '20231123',
                'Access-Control-Allow-Origin': 'https://www.bilibili.com',
                'Access-Control-Max-Age': '0',
                'Accept-Ranges': 'bytes',
                'ETag': '"DA04738AEA59B29C92547378E6ED54CF"',
                'Last-Modified': 'Sat, 26 Oct 2024 11:34:43 GMT',
                'Content-MD5': '2gRziupZspySVHN45u1Uzw==',
                'X-Request-ID': '6745CA62471A7C313517E622',
                'Access-Control-Expose-Headers': 'Content-Length, Content-Range'
            })
        )
        mock_source_url = 'https://upos-sz-estgoss.bilivideo.com/upgcxcode/46/73/239927346/239927346-1-100027.m4s'

        download_service = PageDownloadService(
            url=mock_source_url,
            file='/Users/usharerose/Movies/bilibili/ugc/239927346/sample.mp4'
        )
        actual_remote_file_size = download_service.remote_file_size
        self.assertEqual(actual_remote_file_size, 41231718)

    @patch('builtins.open', new_callable=MagicMock)
    @patch('bili_jean.proxy_service.ProxyService.get')
    @patch('bili_jean.proxy_service.ProxyService.head')
    def test_download(self, mocked_head_request, mocked_get_request, mocked_open):
        mocked_head_request.return_value = MagicMock()
        mocked_head_request.return_value.status_code = HTTPStatus.OK.value
        mocked_head_request.return_value.headers = CaseInsensitiveDict({
            'Content-Length': '1024'
        })

        mocked_get_request.return_value = MagicMock()
        mocked_get_request.return_value.status_code = HTTPStatus.PARTIAL_CONTENT.value
        mocked_get_request.return_value.iter_content = MagicMock(return_value=[b'chunk_0', b'chunk_1'])

        mocked_source_url = 'https://example.com/file.m4s'
        mocked_file_path = '/tmp/test_file.mp4'
        download_service = PageDownloadService(
            url=mocked_source_url,
            file=mocked_file_path
        )

        mocked_path = MagicMock(spec=Path)
        mocked_path.parent.mkdir.return_value = None
        mocked_tmp_path = MagicMock(spec=Path)
        mocked_tmp_path.exists.return_value = False  # simulate no temp file exists
        mocked_tmp_path.rename.return_value = None

        download_service._path = mocked_path  # Override with mock
        download_service._tmp_path = mocked_tmp_path

        mock_local_file = MagicMock()  # Simulate the file object returned by open
        mocked_open.return_value.__enter__.return_value = mock_local_file

        # Start downloading
        download_service.download()

        # Verify that the file's parent directory is created
        mocked_path.parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)

        headers = copy.deepcopy(HEADERS)
        headers.update({'Range': 'bytes=0-'})
        # Verify that get was called with the correct Range header
        mocked_get_request.assert_called_once_with(
            url=mocked_source_url,
            headers=headers,
            stream=True
        )

        # Verify that the temporary file is renamed to the final file
        mocked_tmp_path.rename.assert_called_once_with(mocked_path)

    @patch('bili_jean.proxy_service.ProxyService.get')
    @patch('bili_jean.proxy_service.ProxyService.head')
    def test_download_with_source_403(self, mocked_head_request, mocked_get_request):
        mocked_head_request.return_value = MagicMock()
        mocked_head_request.return_value.status_code = HTTPStatus.OK.value
        mocked_head_request.return_value.headers = CaseInsensitiveDict({
            'Content-Length': '1024'
        })

        mocked_get_request.return_value = MagicMock()
        mocked_get_request.return_value.status_code = HTTPStatus.FORBIDDEN.value

        mocked_source_url = 'https://example.com/file.m4s'
        mocked_file_path = '/tmp/test_file.mp4'
        download_service = PageDownloadService(
            url=mocked_source_url,
            file=mocked_file_path
        )

        mocked_path = MagicMock(spec=Path)
        mocked_path.parent.mkdir.return_value = None
        mocked_tmp_path = MagicMock(spec=Path)
        mocked_tmp_path.exists.return_value = False  # simulate no temp file exists
        mocked_tmp_path.rename.return_value = None

        download_service._path = mocked_path  # Override with mock
        download_service._tmp_path = mocked_tmp_path

        with self.assertRaises(DownloadError):
            download_service.download()

    @patch('bili_jean.proxy_service.ProxyService.head')
    def test_download_with_remote_file_size_403(self, mocked_head_request):
        mocked_head_request.return_value = MagicMock()
        mocked_head_request.return_value.status_code = HTTPStatus.FORBIDDEN.value

        mocked_source_url = 'https://example.com/file.m4s'
        mocked_file_path = '/tmp/test_file.mp4'
        download_service = PageDownloadService(
            url=mocked_source_url,
            file=mocked_file_path
        )

        mocked_path = MagicMock(spec=Path)
        mocked_path.parent.mkdir.return_value = None
        mocked_tmp_path = MagicMock(spec=Path)
        mocked_tmp_path.exists.return_value = False

        download_service._path = mocked_path  # Override with mock
        download_service._tmp_path = mocked_tmp_path

        with self.assertRaises(DownloadError):
            download_service.download()

    def test_init_with_directory_path(self):
        mocked_source_url = 'https://example.com/file.m4s'
        mocked_file_path = './'
        with self.assertRaises(ValueError):
            PageDownloadService(
                url=mocked_source_url,
                file=mocked_file_path
            )
