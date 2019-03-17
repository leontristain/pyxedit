import pytest

from xelib import XelibError, XEditError

from . fixtures import xedit  # NOQA: for pytest


class TestXEditBase:
    def test_basic_attributes(self, xedit):
        # enums on the xelib class should have been forwarded
        assert xedit.Games
        assert xedit.ElementTypes
        assert xedit.DefTypes
        assert xedit.SmashTypes
        assert xedit.ValueTypes

        # should have a handle attribute
        assert hasattr(xedit, 'handle')

        # should have an attribute to access the xelib low-level API
        assert xedit.xelib

    def test_indexing(self, xedit):
        with xedit.manage_handles():
            # try a combination of indexing patterns, they should all work
            assert xedit['Dawnguard.esm']
            assert xedit['Dawnguard.esm']['Head Part']
            head_part = xedit['Dawnguard.esm\\Head Part']
            assert head_part['MaleEyesSnowElf']
            assert head_part['MaleEyesSnowElf']['Parts\\[0]']

            # try a nonexistent path, it should not work
            with pytest.raises(XelibError):
                assert head_part['NonexistentPath']

    def test_get(self, xedit):
        with xedit.manage_handles():
            # try the same indexing patterns but with .get(), should all work
            assert xedit.get('Dawnguard.esm')
            assert xedit.get('Dawnguard.esm').get('Head Part')
            head_part = xedit.get('Dawnguard.esm\\Head Part')
            assert head_part.get('MaleEyesSnowElf')
            assert head_part.get('MaleEyesSnowElf').get('Parts\\[0]')

            # try a nonexistent path, it should just return a None by default
            assert head_part.get('NonexistentPath') is None

            # and if you give it a default it'll return that default
            assert head_part.get('NonexistentPath', 3) == 3

    def test_equality(self, xedit):
        with xedit.manage_handles():
            # obj1 == obj2 should be determined via xelib's equality abilities
            obj1 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
            obj2 = xedit['Dawnguard.esm']['Head Part\\MaleEyesSnowElf']
            assert obj1.handle != obj2.handle
            assert obj1 == obj2

    def test_manage_handles(self, xedit):
        with xedit.manage_handles():
            # we just started, so obj1 and obj2 should get handles 1 and 2
            obj1 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
            obj2 = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf']
            assert obj1.handle == 1
            assert obj2.handle == 2

            # and they should be usable
            assert obj1.signature == 'HDPT'
            assert obj2.signature == 'HDPT'

        # they are now out of scope and no longer usable
        with pytest.raises(XEditError):
            obj1.signature
        with pytest.raises(XEditError):
            obj2.signature

        # we can check whether 1 and 2 were freed up by checking whether
        # they get recycled when we create new handles
        with xedit.manage_handles():
            obj1 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
            obj2 = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf']
            assert obj1.handle == 1
            assert obj2.handle == 2

    def test_type_fields(self, xedit):
        with xedit.manage_handles():
            # sanity check all four type fields, when inapplicable they should
            # return None
            dawnguard = xedit['Dawnguard.esm']
            assert dawnguard.element_type == xedit.ElementTypes.etFile
            assert dawnguard.def_type is None
            assert dawnguard.value_type is None
            assert dawnguard.smash_type is None

            pnam = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf\\PNAM']
            assert pnam.element_type == xedit.ElementTypes.etSubRecord
            assert pnam.def_type == xedit.DefTypes.dtInteger
            assert pnam.value_type == xedit.ValueTypes.vtEnum
            assert pnam.smash_type == xedit.SmashTypes.stInteger

    def test_add_delete(self, xedit):
        with xedit.manage_handles():
            tx = xedit['Dawnguard.esm\\Texture Set\\EyesSnowElf\\'
                       'Textures (RGB/A)']

            # there should be a TX00 here, but no TX03
            assert tx.get('TX00')
            assert not tx.get('TX03')

            # we should be able to add a TX03
            tx.add('TX03')
            assert tx.get('TX03')

            # we should be able to delete the TX03
            tx.delete('TX03')
            assert not tx.get('TX03')

            # add it back; we should be able to delete it via its own object
            tx.add('TX03')
            tx03 = tx.get('TX03')
            assert tx03
            tx03.delete()
            assert not tx.get('TX03')
