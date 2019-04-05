from functools import wraps
import hashlib
from pathlib import Path
import pytest
import shutil

from pyxedit import XEdit


@pytest.fixture(scope='class')
def xedit():
    # list of vanilla master plugins
    vanilla_masters = ['Skyrim.esm',
                       'Update.esm',
                       'Dawnguard.esm',
                       'HearthFires.esm',
                       'Dragonborn.esm']

    # construct the XEdit object we will use for running the test
    xedit = XEdit(game_mode=XEdit.Games.SkyrimSE, plugins=vanilla_masters)

    # open a quick non-loading session to retrieve the auto-discovered game path
    with xedit.session(load_plugins=False):
        game_path = xedit.game_path
        assert game_path

    # the game path gives us the Data dir, from which we can construct paths
    # for the vanilla master plugins; these we will need to back up before the
    # test is run, since we may be changing them during the test. The back up
    # file path will be a `{file_name}.pytest.bak` from the game path itself
    data_dir = Path(game_path, 'Data')

    backup_paths = [(Path(data_dir, file_),
                     Path(game_path, f'{file_}.pytest.bak'))
                    for file_ in vanilla_masters]

    # back them up if they're not already backed up; if a file already exists
    # there, we can trust that it's a correct backup file since there is only
    # one valid state for this file, which is the vanilla state, which should
    # never have changed no matter how long ago you've backed it up
    for file_, backup in backup_paths:
        if not backup.is_file():
            shutil.copyfile(file_, backup)

    # with the files sure to have been backed up, we can proceed to open a
    # loading xedit session, and run the test(s)
    with xedit.session():
        yield xedit

    # the test either completed or errored; at this point, we will proceed to
    # restore any file that have changed; this is done by doing md5 comparison
    # between files before determining whether a restore is necessary
    for file_, backup in backup_paths:
        file_md5 = compute_file_md5(file_)
        backup_md5 = compute_file_md5(backup)
        if file_md5 != backup_md5:
            shutil.copyfile(backup, file_)


def assert_no_opened_handles_after(test):
    @wraps(test)
    def wrapped_test(self, xedit, *args, **kwargs):
        # run the test
        returned = test(self, xedit, *args, **kwargs)

        # The test method should now be out of scope, meaning all objects
        # in its scope should have been cleaned up, which in turn means
        # all XEditBase-derived classes should have released all their
        # handles. At this point, there should be no opened handles tracked
        # by xelib. If there is, then something somewhere is failing to
        # release handle during finalization. This could happen if, say,
        # an object has errorneously set auto_release to False.
        assert xedit.xelib.opened_handles == set()

        return returned
    return wrapped_test


def compute_file_md5(file_path):
    '''
    Utility function that computes the md5 checksum of a file at the given
    file path

    @param file_path: path to the file to get md5 checksum for
    @return: the computed md5 hexdigest
    '''
    hash_md5 = hashlib.md5()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
