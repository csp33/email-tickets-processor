import tempfile
from contextlib import contextmanager
from typing import Generator


class TmpFileManager:
    @contextmanager
    def __call__(self, file_content: bytes) -> Generator[str, None, None]:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
            tmp_file.write(file_content)
            tmp_file.flush()
            yield tmp_file.name
