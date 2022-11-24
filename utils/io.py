"""
Utils handling IO
"""
from typing import Union
from pathlib import Path

def ensure_path(path: Union[str, Path]) -> Path:
    if isinstance(path, str):
        path =  Path(path)
    return path

