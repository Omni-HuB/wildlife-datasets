import os
import urllib.request
from tqdm import tqdm
import shutil
from contextlib import contextmanager

class ProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)

def download_url(url, output_path='.'):
    with ProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)

def extract_archive(archive, extract_path='.', delete=False):
    shutil.unpack_archive(archive, extract_path)
    if delete:
        os.remove(archive)


@contextmanager
def data_directory(dir):
    '''
    Changes context such that data directory is used as current work directory.
    Data directory is created if it does not exist.
    '''
    current_dir = os.getcwd()
    if not os.path.exists(dir):
        os.makedirs(dir)
    os.chdir(dir)
    try:
        yield
    finally:
        os.chdir(current_dir)


def print_start1(root):
    print('DATASET %s: DOWNLOADING STARTED.' % os.path.split(root)[1])

def print_start2(root):
    print('DATASET %s: EXTRACTING STARTED.' % os.path.split(root)[1])

def print_finish(root):
    print('DATASET %s: FINISHED. If mass downloading, you can remove it from the list.' % os.path.split(root)[1])
    print('')

def kaggle_download(command):
    # TODO: add a check that kaggle is installed
    # TODO: add kaggle as package requirements
    os.system(f"kaggle {command}")