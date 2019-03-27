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
                obj1 = xedit.get('Dawnguard.esm\\Head Part\\MaleEyesSnowElf')
                obj2 = xedit['Dawnguard.esm\\Head Part\\MaleEyesSnowElf']
                assert obj1.signature
                assert obj2.signature

                obj1.promote()
                obj2.promote()

            assert obj1.signature
            assert obj2.signature

        # promotion should only be effective for one scope
        with pytest.raises(XEditError):
            obj1.signature
        with pytest.raises(XEditError):
            obj2.signature

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
            assert parts.__class__.__name__ == 'XEditArray'


class TestXEditArray:
    def test___len__(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to determine length using the len() builtin
            assert len(a1) == 3
            assert len(a2) == 3

    def test___getitem__(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to get array item objects directly via indexing
            # (struct arrays)
            assert a1[0]['NAM0'].xelib_run('get_value') == 'Race Morph'
            assert a1[1]['NAM0'].xelib_run('get_value') == 'Tri'
            assert a1[2]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert a1[-1]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert a1[-2]['NAM0'].xelib_run('get_value') == 'Tri'
            assert a1[-3]['NAM0'].xelib_run('get_value') == 'Race Morph'

            # out of range indexes should error (struct arrays)
            with pytest.raises(IndexError):
                a1[3]
            with pytest.raises(IndexError):
                a1[-4]

            # should be able to get referenced objects of array items via
            # indexing (reference arrays)
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Deathhound'
            assert a2[2].display_name == 'Dog'
            assert a2[-1].display_name == 'Dog'
            assert a2[-2].display_name == 'Deathhound'
            assert a2[-3].display_name == 'Wolf'

            # out of range indexes should error (reference arrays)
            with pytest.raises(IndexError):
                a1[3]
            with pytest.raises(IndexError):
                a1[-4]

    def test___iter__(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to iterate over array to get array item objects
            # (struct arrays)
            for i, item in enumerate(a1):
                type_str = item['NAM0'].xelib_run('get_value')
                expected = ['Race Morph', 'Tri', 'Chargen Morph'][i]
                assert type_str == expected

            # should be able to iterate over array to get referenced objects
            # of array items
            # (reference arrays)
            for i, item in enumerate(a2):
                assert item.display_name == ['Wolf', 'Deathhound', 'Dog'][i]

    def test_membership(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to check whether an iteration-produced,
            # indexing-produced, or find_item_with-produced item exists in the
            # array via the `in` operator (struct arrays)
            for item in a1:
                assert item in a1
            assert a1[0] in a1
            assert a1[1] in a1
            assert a1[2] in a1
            item = a1.find_item_with('Tri', subpath='NAM0')
            assert item in a1

            # should be able to check whether an iteration-produced or
            # indexing-produced item exists in the array via the `in` operator
            # (reference arrays)
            for item in a2:
                assert item in a2
            assert a2[0] in a2
            assert a2[1] in a2
            assert a2[2] in a2

            # find_item_with should be producing an array item object even for
            # simple value array items, but its `.value` can be used for the
            # membership test via the `in` operator
            item = a2.find_item_with(a2[0])
            assert item.value in a2

    def test_index(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to check the index of a iteration-produced,
            # indexing-produced, or find_item_with-produced item using the
            # `.index` method
            for i, item in enumerate(a1):
                assert a1.index(item) == i
            assert a1.index(a1[0]) == 0
            assert a1.index(a1[1]) == 1
            assert a1.index(a1[2]) == 2
            item = a1.find_item_with('Tri', subpath='NAM0')
            assert a1.index(item) == 1

            # should be able to check the index of an iteration-produced or
            # indexing-produced item using the `.index` method
            for i, item in enumerate(a2):
                assert a2.index(item) == i
            assert a2.index(a2[0]) == 0
            assert a2.index(a2[1]) == 1
            assert a2.index(a2[2]) == 2

            # find_item_with should be producing an array item object even for
            # simple value array items, but its `.value` can be given to the
            # `.index` method to get its index
            item = a2.find_item_with(a2[1])
            assert a2.index(item.value) == 1

    def test_add_remove(self, xedit):
        with xedit.manage_handles():
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']
            assert len(a2) == 3
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Deathhound'
            assert a2[2].display_name == 'Dog'

            # should be able to add a reference target into a reference array
            # with the `.add` method
            # (NOTE: this is a sorted array so we should not worry that the new
            #        reference was not added at the end)
            fox_race = xedit['Skyrim.esm\\RACE\\FoxRace']
            assert fox_race.signature == 'RACE'
            assert fox_race.display_name == 'Fox'

            a2.add(fox_race)
            assert len(a2) == 4
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Fox'
            assert a2[2].display_name == 'Deathhound'
            assert a2[3].display_name == 'Dog'

            # should be able to remove a reference target from a reference array
            # with the `.remove` method
            a2.remove(fox_race)
            assert len(a2) == 3
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Deathhound'
            assert a2[2].display_name == 'Dog'

    def test_objects(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to iterate over the .objects attribute to get
            # array item objects (struct arrays)
            for i, item in enumerate(a1.objects):
                type_str = item['NAM0'].xelib_run('get_value')
                expected = ['Race Morph', 'Tri', 'Chargen Morph'][i]
                assert type_str == expected

            # should be able to iterate over the .objects attribute to get
            # array item objects (reference arrays)
            for i, item in enumerate(a2.objects):
                assert item.value.display_name == ['Wolf',
                                                   'Deathhound',
                                                   'Dog'][i]

    def test_get_object_at_index(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to get array item objects directly via the
            # `get_object_at_index` method (struct arrays)
            for i, index in enumerate([0, 1, 2, -1, -2, -3]):
                assert (a1.get_object_at_index(index)['NAM0']
                          .xelib_run('get_value') == ['Race Morph',
                                                      'Tri',
                                                      'Chargen Morph',
                                                      'Chargen Morph',
                                                      'Tri',
                                                      'Race Morph'][i])

            # out of range indexes should error (struct arrays)
            with pytest.raises(IndexError):
                a1.get_object_at_index(3)
            with pytest.raises(IndexError):
                a1.get_object_at_index(-4)

            # should be able to get array item objects directly via the
            # `get_object_at_index` method (reference arrays)
            for i, index in enumerate([0, 1, 2, -1, -2, -3]):
                assert (a2.get_object_at_index(index)
                          .value
                          .display_name == ['Wolf', 'Deathhound', 'Dog',
                                            'Dog', 'Deathhound', 'Wolf'][i])

            # out of range indexes should error (reference arrays)
            with pytest.raises(IndexError):
                a2.get_object_at_index(3)
            with pytest.raises(IndexError):
                a2.get_object_at_index(-4)

    def test_has_item_with(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to check whether an item exists via information
            # about its content (struct arrays)
            assert a1.has_item_with('Tri', subpath='NAM0')
            assert not a1.has_item_with('Nope', subpath='NopeNope')

            # should be able to check whether an item exists via information
            # about its content, where objects can be given as value to
            # auto-resolve its reference to use as value
            wolf_race = a2[0]
            assert wolf_race.signature == 'RACE'
            assert wolf_race.display_name == 'Wolf'
            assert a2.has_item_with(wolf_race)

            fox_race = xedit['Skyrim.esm\\RACE\\FoxRace']
            assert fox_race.signature == 'RACE'
            assert fox_race.display_name == 'Fox'
            assert not a2.has_item_with(fox_race)

    def test_find_item_with(self, xedit):
        with xedit.manage_handles():
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

            # should be able to retrieve an object via information about its
            # content
            assert a1.find_item_with('Nope', subpath='NopeNope') is None
            assert a1.find_item_with('Tri', subpath='NAM0')

            # should be able to retrieve an object via information about its
            # content, where objects can be given as value to auto-convert to
            # auto-resolve its reference to use as value
            wolf_race = a2[0]
            assert wolf_race.signature == 'RACE'
            assert wolf_race.display_name == 'Wolf'
            found = a2.find_item_with(wolf_race)
            assert found.value == wolf_race

            fox_race = xedit['Skyrim.esm\\RACE\\FoxRace']
            assert fox_race.signature == 'RACE'
            assert fox_race.display_name == 'Fox'
            assert not a2.find_item_with(fox_race)

    def test_add_move_remove_item_with(self, xedit):
        with xedit.manage_handles():
            # check initial state of struct array
            a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
            assert a1[0]['NAM0'].xelib_run('get_value') == 'Race Morph'
            assert a1[0]['NAM1'].value != 'Foo\\Bar.tri'
            assert a1[1]['NAM0'].xelib_run('get_value') == 'Tri'
            assert a1[1]['NAM1'].value != 'Foo\\Bar.tri'
            assert a1[2]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert a1[2]['NAM1'].value != 'Foo\\Bar.tri'

            # should be able to add an item to the array
            item = a1.add_item_with('Foo\\Bar.tri', subpath='NAM1')
            print(item.long_path)
            assert item['NAM1'].value == 'Foo\\Bar.tri'
            assert len(a1) == 4
            assert a1.index(item) == 3

            # should be able to move the item
            assert a1[-1]['NAM1'].value == 'Foo\\Bar.tri'
            a1.move_item(a1[-1], 0)
            assert a1[-1]['NAM1'].value != 'Foo\\Bar.tri'
            assert a1[0]['NAM1'].value == 'Foo\\Bar.tri'

            # should be able to remove the item; the array should be back to
            # the way it used to be
            assert len(a1) == 4
            a1.remove_item_with('Foo\\Bar.tri', subpath='NAM1')
            assert len(a1) == 3
            assert a1[0]['NAM0'].xelib_run('get_value') == 'Race Morph'
            assert a1[0]['NAM1'].value != 'Foo\\Bar.tri'
            assert a1[1]['NAM0'].xelib_run('get_value') == 'Tri'
            assert a1[1]['NAM1'].value != 'Foo\\Bar.tri'
            assert a1[2]['NAM0'].xelib_run('get_value') == 'Chargen Morph'
            assert a1[2]['NAM1'].value != 'Foo\\Bar.tri'

            # check initial state of reference array
            a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']
            assert len(a2) == 3
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Deathhound'
            assert a2[2].display_name == 'Dog'

            # should be able to provide an object to auto-resolve its reference
            # as value to add to the array
            # (NOTE: this is a sorted array so we should not worry that the new
            #        reference was not added at the end)
            fox_race = xedit['Skyrim.esm\\RACE\\FoxRace']
            assert fox_race.signature == 'RACE'
            assert fox_race.display_name == 'Fox'

            a2.add_item_with(fox_race)
            assert len(a2) == 4
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Fox'
            assert a2[2].display_name == 'Deathhound'
            assert a2[3].display_name == 'Dog'

            # should be able to provide an object to auto-resolve its reference
            # as value to remove from the array
            a2.remove_item_with(fox_race)
            assert len(a2) == 3
            assert a2[0].display_name == 'Wolf'
            assert a2[1].display_name == 'Deathhound'
            assert a2[2].display_name == 'Dog'
