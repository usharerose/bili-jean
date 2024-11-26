"""
Service component for download remote resource to local
"""
import copy
from http import HTTPStatus
from pathlib import Path
from typing import Optional

from .constants import HEADERS
from .proxy_service import ProxyService


class DownloadError(Exception):

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class PageDownloadService:

    def __init__(self, url: str, file: str):
        self._url = url
        self._path = Path(file)
        if self._path.is_dir():
            raise ValueError('The value of \'file\' should be a file path')
        self._tmp_ext_suffix = '.part'
        self._tmp_path = Path(''.join([str(self._path), self._tmp_ext_suffix]))
        self._remote_file_size: Optional[int] = None

    @property
    def remote_file_size(self) -> int:
        if self._remote_file_size is None:
            response = ProxyService.head(url=self._url)
            if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                raise DownloadError(
                    f'Error {response.status_code} when get content length: '
                    f"{response.content.decode('utf-8')}"
                )
            self._remote_file_size = int(response.headers.get('Content-Length', 0))
        return self._remote_file_size

    def download(self) -> None:
        """
        1. create directory if not exists
        2. compared local temporary file's size with remote one,
           and continue to download the rest of it
        3. change temporary file to normal
        """
        self._path.parent.mkdir(parents=True, exist_ok=True)

        file_size = 0
        if self._tmp_path.exists():
            file_size = self._tmp_path.stat().st_size

        if file_size < self.remote_file_size:
            headers = copy.deepcopy(HEADERS)
            headers.update({"Range": f"bytes={file_size}-"})

            response = ProxyService.get(url=self._url, headers=headers, stream=True)
            if response.status_code not in (HTTPStatus.OK, HTTPStatus.PARTIAL_CONTENT):
                raise DownloadError(
                    f"Error {response.status_code} when download resource: "
                    f"{response.content.decode('utf-8')}"
                )
            with open(str(self._tmp_path.resolve()), 'ab') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

        self._tmp_path.rename(self._path)
