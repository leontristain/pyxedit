import pytest

from . fixtures import xedit, check_handles_after  # NOQA: for pytest


class TestXEditArray:
    @check_handles_after
    def test___len__(self, xedit):
        a1 = xedit['Dawnguard.esm\\HDPT\\MaleHeadHighElfSnow\\Parts']
        a2 = xedit['Dawnguard.esm\\ARMA\\VampireWolfAA\\MODL']

        # should be able to determine length using the len() builtin
        assert len(a1) == 3
        assert len(a2) == 3

    @check_handles_after
    def test___getitem__(self, xedit):
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

    @check_handles_after
    def test___iter__(self, xedit):
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

    @check_handles_after
    def test_membership(self, xedit):
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

    @check_handles_after
    def test_index(self, xedit):
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

    @check_handles_after
    def test_add_remove(self, xedit):
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

    @check_handles_after
    def test_objects(self, xedit):
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

    @check_handles_after
    def test_get_object_at_index(self, xedit):
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

    @check_handles_after
    def test_has_item_with(self, xedit):
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

    @check_handles_after
    def test_find_item_with(self, xedit):
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

    @check_handles_after
    def test_add_move_remove_item_with(self, xedit):
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
