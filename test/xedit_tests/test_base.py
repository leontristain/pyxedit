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
            tx03 = tx.add('TX03')
            assert tx03
            tx03.delete()
            assert not tx.get('TX03')

    def test_names_paths_and_signature(self, xedit):
        with xedit.manage_handles():
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

    def test_objectify(self, xedit):
        with xedit.manage_handles():
            assert xedit.__class__.__name__ == 'XEdit'

            dawnguard = xedit['Dawnguard.esm']
            assert dawnguard.__class__.__name__ == 'XEditPlugin'

            armo = xedit['Dawnguard.esm\\ARMO']
            assert armo.__class__.__name__ == 'XEditGenericObject'

            txst = xedit['Dawnguard.esm\\Texture Set\\EyesSnowElf']
            assert txst.__class__.__name__ == 'XEditTextureSet'

            parts = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf\\Parts']
            assert parts.__class__.__name__ == 'XEditCollection'


class TestXEditCollection:
    def test_basic_functionality(self, xedit):
        with xedit.manage_handles():
            parts = xedit['Dawnguard.esm\\Head Part\\MaleHeadHighElfSnow\\'
                          'Parts']

            # should be able to determine length using the len() builtin
            assert len(parts) == 3

            # should be able to get part objects via indexing
            assert parts[0]['NAM0'].xelib_run('get_value') == 'Race Morph'
            assert parts[1]['NAM0'].xelib_run('get_value') == 'Tri'
            assert parts[2]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert parts[-1]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert parts[-2]['NAM0'].xelib_run('get_value') == 'Tri'
            assert parts[-3]['NAM0'].xelib_run('get_value') == 'Race Morph'
            with pytest.raises(IndexError):
                parts[3]

            # should be able to iterate over parts, resulting in objects
            for i, part in enumerate(parts):
                type_str = part['NAM0'].xelib_run('get_value')
                expected = ['Race Morph', 'Tri', 'Chargen Morph'][i]
                assert type_str == expected

            # should be able to check whether an item exists via information
            # about its content
            assert parts.has_item_with('Tri', subpath='NAM0')
            assert not parts.has_item_with('Nope', subpath='NopeNope')

            # should be able to retrieve an object via information about its
            # content
            assert parts.find_item_with('Nope', subpath='NopeNope') is None
            part = parts.find_item_with('Tri', subpath='NAM0')
            assert part

            # should be able to check whether an object exists in the collection
            # with the `in` operator
            assert part in parts

            # should be able to find the index of a part using the part object
            assert parts.index(part) == 1

            # should be able to add an item to the collection
            item = parts.add_item_with('Foo\\Bar.tri', subpath='NAM1')
            print(item.long_path)
            assert item['NAM1'].value == 'Foo\\Bar.tri'
            assert len(parts) == 4
            assert parts.index(item) == 3

            # should be able to move the item
            assert parts[-1]['NAM1'].value == 'Foo\\Bar.tri'
            parts.move_item(parts[-1], 0)
            assert parts[-1]['NAM1'].value != 'Foo\\Bar.tri'
            assert parts[0]['NAM1'].value == 'Foo\\Bar.tri'

            # should be able to remove the item; the array should be back to
            # the way it used to be
            assert len(parts) == 4
            parts.remove_item_with('Foo\\Bar.tri', subpath='NAM1')
            assert len(parts) == 3
            assert parts[0]['NAM0'].xelib_run('get_value') == 'Race Morph'
            assert parts[0]['NAM1'].value != 'Foo\\Bar.tri'
            assert parts[1]['NAM0'].xelib_run('get_value') == 'Tri'
            assert parts[1]['NAM1'].value != 'Foo\\Bar.tri'
            assert parts[2]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert parts[2]['NAM1'].value != 'Foo\\Bar.tri'
