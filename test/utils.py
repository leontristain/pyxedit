from contextlib import contextmanager
from pathlib import Path
import os
import shutil
import textwrap
import time


@contextmanager
def backed_up(path):
    path = Path(path)
    back_up = path.parent / f'{path.name}.bak'
    try:
        if path.is_file():
            shutil.copyfile(path, back_up)
        elif path.is_dir():
            shutil.copytree(path, back_up)
        elif path.exists():
            raise ValueError(f'backed_up expected file or folder, got '
                             f'something else')
        yield
    finally:
        if back_up.is_file():
            shutil.copyfile(back_up, path)
            os.remove(back_up)
        elif back_up.is_dir():
            if path.exists():
                shutil.rmtree(path)
            shutil.move(back_up, path)


class Timer:
    def __init__(self):
        self._start = None
        self._end = None

    def __enter__(self):
        self._start = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._end = time.time()

    @property
    def start(self):
        if self._start is None:
            raise ValueError('Timer has not started execution')
        return self._start

    @property
    def end(self):
        if self._end is None:
            raise ValueError('Timer has not finished execution')
        return self._end

    @property
    def seconds(self):
        return self.end - self.start


def stripped_block(text):
    return textwrap.dedent(text).strip()
