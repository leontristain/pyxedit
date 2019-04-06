# pyxedit

**Note: This library is current in progress and not yet released**

Python API for xedit-lib

## To Run Tests:

1. install Skyrim LE with all DLCs (yes, has to be classic; this is kind of nice
    if you play SSE since you can have a pristine test environment without
    impacting your actual modded game)
2. copy the test esps from the XEditLib folder to your Skyrim Data directory
3. for the time being, copy the `Skyrim.Hardcoded.dat` file from the XEditLib
    folder to the root of your python installation (possibly something like
    `%localappdata%/Programs/Python/Python37`). This is an unfortunate hack,
    which should no longer be needed once Mator updates xedit-lib to xedit 4.0,
    and I update this library to match.
4. with everything in `requirements.txt` installed, run `pytest -v test` from
    root of the code base

Note that running tests will sometimes modify files in your `%localappdata`'s
Skyrim folder. Any modifications, however, will be made within a context manager
that backs up the original file, so it should be quite safe from python's scope;
however, since DLLs can sometimes cause python itself to crash, there is still a
risk, so beware.
