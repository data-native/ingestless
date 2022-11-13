import pytest

from pathlib import Path
from utils import io as ioutils

class TestIOUtils:

    def test_ensure_path(self):
        testpath_str = '/test/tmp/dir/subfolder/test.csv'
        testpath_path = Path('/test/tmp/dir/subfolder/test.csv')
        return_path = ioutils.ensure_path(testpath_str)
        return_path = ioutils.ensure_path(testpath_path)
        assert isinstance(return_path, Path)