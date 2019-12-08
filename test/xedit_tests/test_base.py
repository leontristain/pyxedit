import pytest

from pyxedit import XelibError, XEditError

from . fixtures import xedit, assert_no_opened_handles_after  # NOQA: pytest


class TestXEditBase:
    @assert_no_opened_handles_after
    def test_basic_attributes(self, xedit):
        # enums on the xelib class should have been forwarded
        assert xedit.ElementTypes
        assert xedit.DefTypes
        assert xedit.SmashTypes
        assert xedit.ValueTypes
        assert xedit.GameModes

        # should have a handle attribute
        assert hasattr(xedit, 'handle')

        # should have an attribute to access the xelib low-level API
        assert xedit.xelib

    @assert_no_opened_handles_after
    def test_indexing(self, xedit):
        # try a combination of indexing patterns, they should all work
        assert xedit['Dawnguard.esm']
        assert xedit['Dawnguard.esm']['Head Part']
        head_part = xedit['Dawnguard.esm\\Head Part']
        assert head_part['MaleEyesSnowElf']
        assert head_part['MaleEyesSnowElf']['Parts\\[0]']

        # try a nonexistent path, it should not work
        with pytest.raises(XelibError):
            assert head_part['NonexistentPath']

    @assert_no_opened_handles_after
    def test_get(self, xedit):
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

    @assert_no_opened_handles_after
    def test_equality(self, xedit):
        # obj1 == obj2 should be determined via xelib's equality abilities
        obj1 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
        obj2 = xedit['Dawnguard.esm']['Head Part\\MaleEyesSnowElf']
        assert obj1.handle != obj2.handle
        assert obj1 == obj2

    @assert_no_opened_handles_after
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
            obj3 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
            obj4 = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf']
            assert obj3.handle == 1
            assert obj4.handle == 2

    @assert_no_opened_handles_after
    def test_promote(self, xedit):
        with xedit.manage_handles():
            # start a handle management scope and grab some handles; the handles
            # should be active within the scope, but not once out of the scope
            with xedit.manage_handles():
                obj1 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
                obj2 = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf']
                assert obj1.signature
                assert obj2.signature

            with pytest.raises(XEditError):
                obj1.signature
            with pytest.raises(XEditError):
                obj2.signature

            # however, we should be able to promote the objects to the parent
            # scope and have them remain usable in the parent scope
            with xedit.manage_handles():
                obj3 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
                obj4 = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf']
                assert obj3.signature
                assert obj4.signature

                obj3.promote()
                obj4.promote()

            assert obj3.signature
            assert obj4.signature

        # promotion should only be effective for one scope
        with pytest.raises(XEditError):
            obj1.signature
        with pytest.raises(XEditError):
            obj2.signature

    @assert_no_opened_handles_after
    def test_type_fields(self, xedit):
        # sanity check all four type fields, when inapplicable they should
        # return None
        dawnguard = xedit['Dawnguard.esm']
        assert dawnguard.element_type == xedit.ElementTypes.File
        assert dawnguard.def_type is None
        assert dawnguard.value_type is None
        assert dawnguard.smash_type is None

        pnam = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf\\PNAM']
        assert pnam.element_type == xedit.ElementTypes.SubRecord
        assert pnam.def_type == xedit.DefTypes.Integer
        assert pnam.value_type == xedit.ValueTypes.Enum
        assert pnam.smash_type == xedit.SmashTypes.Integer

    @assert_no_opened_handles_after
    def test_add_delete(self, xedit):
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
        tx03 = tx.add('TX03')
        assert tx03
        tx03.delete()
        assert not tx.get('TX03')

    @assert_no_opened_handles_after
    def test_names_paths_signatures(self, xedit):
        dawnguard = xedit['Dawnguard.esm']
        assert dawnguard.name == 'Dawnguard.esm'
        assert dawnguard.long_name == '[02] Dawnguard.esm'
        assert dawnguard.display_name == '[02] Dawnguard.esm'
        assert dawnguard.path == 'Dawnguard.esm'
        assert dawnguard.long_path == 'Dawnguard.esm'
        assert dawnguard.local_path == 'Dawnguard.esm'
        assert dawnguard.signature == ''
        assert dawnguard.signature_name == ''

        armo = xedit['Dawnguard.esm\\ARMO']
        assert armo.name == 'Armor'
        assert armo.long_name == 'GRUP Top "ARMO"'
        assert armo.display_name == 'GRUP Top "ARMO"'
        assert armo.path == 'Dawnguard.esm\\ARMO'
        assert armo.long_path == 'Dawnguard.esm\\ARMO'
        assert armo.local_path == 'Dawnguard.esm\\ARMO'
        assert armo.signature == 'ARMO'
        assert armo.signature_name == 'Armor'

        pnam = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf\\PNAM']
        assert pnam.name == 'PNAM - Type'
        assert pnam.long_name == 'PNAM - Type'
        assert pnam.display_name == 'PNAM - Type'
        assert pnam.path == 'Dawnguard.esm\\02003786\\PNAM - Type'
        assert pnam.long_path == 'Dawnguard.esm\\HDPT\\02003786\\PNAM - Type'
        assert pnam.local_path == 'PNAM - Type'
        assert pnam.signature == 'PNAM'
        assert pnam.signature_name == ''

        tx = xedit['Dawnguard.esm\\Texture Set\\EyesSnowElf\\Textures (RGB/A)']
        assert tx.name == 'Textures (RGB/A)'
        assert tx.long_name == 'Textures (RGB/A)'
        assert tx.display_name == 'Textures (RGB/A)'
        assert tx.path == 'Dawnguard.esm\\02003787\\Textures (RGB/A)'
        assert tx.long_path == 'Dawnguard.esm\\TXST\\02003787\\Textures (RGB/A)'
        assert tx.local_path == 'Textures (RGB/A)'
        assert tx.signature == 'TX00'
        assert tx.signature_name == ''

    @assert_no_opened_handles_after
    def test_objectify(self, xedit):
        assert xedit.__class__.__name__ == 'XEdit'

        dawnguard = xedit['Dawnguard.esm']
        assert dawnguard.__class__.__name__ == 'XEditPlugin'

        armo = xedit['Dawnguard.esm\\ARMO']
        assert armo.__class__.__name__ == 'XEditArmor'

        txst = xedit['Dawnguard.esm\\Texture Set\\EyesSnowElf']
        assert txst.__class__.__name__ == 'XEditTextureSet'

        parts = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf\\Parts']
        assert parts.__class__.__name__ == 'XEditArray'
