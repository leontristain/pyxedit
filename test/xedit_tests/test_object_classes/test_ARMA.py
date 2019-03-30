import pytest

from xedit import XEditError

from .. fixtures import xedit, assert_no_opened_handles_after  # NOQA: pytest


class TestARMA:
    @assert_no_opened_handles_after
    def test_bodt(self, xedit):
        arma = xedit['Skyrim.esm\\ARMA\\NakedFeet']

        # signature attribute should work
        assert arma.bodt

        # aliases should work
        assert arma.body_template_12byte

        # cannot set this since it is a non-value element
        with pytest.raises(XEditError):
            arma.bodt = 3

        # this element cannot be deleted since it is a required field
        with pytest.raises(XEditError):
            arma.bodt = None

    @assert_no_opened_handles_after
    def test_bod2(self, xedit):
        pytest.skip('Not sure I understand this field')

    @assert_no_opened_handles_after
    def test_rnam(self, xedit):
        arma = xedit['Skyrim.esm\\ARMA\\NakedFeet']

        # signature attribute should work
        assert arma.rnam

        # aliases should work
        assert arma.race

        # should be able to set this to other races and back
        race_before = arma.race
        assert race_before.name == 'Default Race'

        race_after = xedit['Skyrim.esm\\RACE\\CowRace']
        arma.race = race_after
        assert arma.race.name == 'HighlandCow'

        arma.race = race_before
        assert arma.race.name == 'Default Race'

        # should not be able to delete it since it is a required field
        with pytest.raises(XEditError):
            arma.race = None

    @assert_no_opened_handles_after
    def test_dnam(self, xedit):
        arma = xedit['Skyrim.esm\\ARMA\\NakedFeet']

        # signature attribute should work
        assert arma.dnam

        # aliases should work
        assert arma.data

        # cannot set this since it is a non-value element
        with pytest.raises(XEditError):
            arma.dnam = 3

        # this element cannot be deleted since it is a required field
        with pytest.raises(XEditError):
            arma.dnam = None

    @pytest.mark.parametrize(
        'n,nifpath',
        [(2, 'DLC01\\Clothes\\Vampire\\VampireRobes_1.nif'),
         (3, 'DLC01\\Clothes\\Vampire\\VampireRobesF_1.nif'),
         (4, 'DLC01\\Clothes\\Vampire\\1stPersonVampireRobes_1.nif'),
         (5, 'DLC01\\Clothes\\Vampire\\1stPersonVampireRobesF_1.nif')])
    @assert_no_opened_handles_after
    def test_mod(self, xedit, n, nifpath):
        sig = f'mod{n}'
        alias = {'mod2': 'male_model',
                 'mod3': 'male_firstperson_model',
                 'mod4': 'female_model',
                 'mod5': 'female_firstperson_model'}[sig]

        arma = xedit['Dawnguard.esm\\ARMA\\DLC1VampireRobesAA']

        # signature attribute should work
        assert getattr(arma, sig)

        # aliases should work
        assert getattr(arma, alias)

        # should be able to futher access the model path
        assert getattr(arma, sig).model_filename == nifpath

        # this particular one doesn't have alternate textures
        assert getattr(arma, sig).alternate_textures is None

        # the nif path element should be editable
        getattr(arma, sig).model_filename = 'Some\\Other\\Path.nif'
        assert getattr(arma, sig).model_filename == 'Some\\Other\\Path.nif'
        getattr(arma, sig).model_filename = nifpath
        assert getattr(arma, sig).model_filename == nifpath

        # the nif path element should not be deletable since it is required
        with pytest.raises(XEditError):
            getattr(arma, sig).model_filename = None

        # but we are free to set it to empty
        getattr(arma, sig).model_filename = ''
        assert getattr(arma, sig).model_filename == ''
        getattr(arma, sig).model_filename = nifpath
        assert getattr(arma, sig).model_filename == nifpath

        # cannot set the field itself since it is a non-value element
        with pytest.raises(XEditError):
            setattr(arma, sig, 3)

        # we should be able to delete the field itself
        setattr(arma, sig, None)
        assert getattr(arma, sig) is None

        # we should be able to add it back
        arma.add(sig.upper())
        getattr(arma, sig).model_filename = nifpath
        assert getattr(arma, sig).model_filename == nifpath

    @pytest.mark.parametrize('n,texture_name',
                             [(0, 'SkinBodyMale_1'),
                              (1, 'SkinBodyFemale_1'),
                              (2, 'SkinMaleHumanBody'),
                              (3, 'SkinFemaleHumanBody')])
    @assert_no_opened_handles_after
    def test_nam(self, xedit, n, texture_name):
        sig = f'nam{n}'
        alias = {'nam0': 'base_male_texture',
                 'nam1': 'base_female_texture',
                 'nam2': 'base_male_firstperson_texture',
                 'nam3': 'base_female_firstperson_texture'}[sig]

        # ensure there's an empty foo.esp
        foo = xedit.get_or_add('foo.esp')
        foo.nuke()

        # copy onto esp the NakedTorso from Skyrim.esm
        arma = xedit['Skyrim.esm\\ARMA\\NakedTorso']
        foo_arma = arma.copy_into(foo)
        assert foo_arma

        # nam[n] field should be gettable
        texture = getattr(foo_arma, sig)
        assert texture.name == texture_name

        # alias should work
        assert getattr(foo_arma, alias).name == texture_name

        # nam[n] field should be settable to something else
        skin_mouth = xedit['Skyrim.esm\\Texture Set\\SkinMouth']
        assert skin_mouth
        setattr(foo_arma, sig, skin_mouth)
        assert getattr(foo_arma, sig).name == 'SkinMouth'
        setattr(foo_arma, sig, texture)

        # nam[n] field should be deletable
        assert getattr(foo_arma, sig).name == texture_name
        setattr(foo_arma, sig, None)
        assert getattr(foo_arma, sig) is None
        setattr(foo_arma, sig, texture)
        assert getattr(foo_arma, sig).name == texture_name

    @assert_no_opened_handles_after
    def test_modl(self, xedit):
        # ensure there's an empty foo.esp
        foo = xedit.get_or_add('foo.esp')
        foo.nuke()

        # copy onto esp the NakedTorso from Skyrim.esm
        arma = xedit['Skyrim.esm\\ARMA\\NakedTorso']
        foo_arma = arma.copy_into(foo)
        assert foo_arma

        # modl should be gettable, and it should be an array of size 10
        modl = foo_arma.modl
        assert modl
        assert len(modl) == 10

        # should also be able to access this via alias
        aliased_modl = foo_arma.additional_races
        assert len(aliased_modl) == 10
        assert modl == aliased_modl

        # check expected initial data
        assert set(race.long_name.split()[0] for race in modl) == set(
            ['BretonRace', 'BretonRaceVampire', 'ImperialRace',
                'ImperialRaceVampire', 'NordRace', 'NordRaceVampire',
                'OrcRace', 'OrcRaceVampire', 'RedguardRace',
                'RedguardRaceVampire'])

        # add a race, should work
        wolf_race = xedit['Skyrim.esm\\RACE\\WolfRace']
        assert wolf_race

        modl.add(wolf_race)
        assert len(modl) == 11
        assert set(race.long_name.split()[0] for race in modl) == set(
            ['BretonRace', 'BretonRaceVampire', 'ImperialRace',
                'ImperialRaceVampire', 'NordRace', 'NordRaceVampire',
                'OrcRace', 'OrcRaceVampire', 'RedguardRace',
                'RedguardRaceVampire', 'WolfRace'])

        # should be able to find the added race
        assert wolf_race in modl
        assert modl[modl.index(wolf_race)] == wolf_race

        # should be able to remove all races
        races = [race for race in modl]
        for race in races:
            modl.remove(race)
        assert len(modl) == 0

        # should be able to add them back
        for race in races:
            if not race.long_name.startswith('WolfRace'):
                modl.add(race)
        assert len(modl) == 10
        assert set(race.long_name.split()[0] for race in modl) == set(
            ['BretonRace', 'BretonRaceVampire', 'ImperialRace',
                'ImperialRaceVampire', 'NordRace', 'NordRaceVampire',
                'OrcRace', 'OrcRaceVampire', 'RedguardRace',
                'RedguardRaceVampire'])

    @assert_no_opened_handles_after
    def test_sndd(self, xedit):
        # ensure there's an empty foo.esp
        foo = xedit.get_or_add('foo.esp')
        foo.nuke()

        # copy onto esp the IronBootsAA from Skyrim.esm
        arma = xedit['Skyrim.esm\\ARMA\\IronBootsAA']
        foo_arma = arma.copy_into(foo)
        assert foo_arma

        # sndd should be gettable
        sndd = foo_arma.sndd
        assert sndd.long_name.startswith('FSTArmorHeavyFootstepSet')

        # alias should work
        aliased_sndd = foo_arma.footstep_sound
        assert aliased_sndd == sndd

        # should be able to set it to something else
        light_steps = xedit['Skyrim.esm\\FSTS\\FSTArmorLightFootstepSet']
        assert light_steps

        foo_arma.sndd = light_steps
        assert foo_arma.sndd == light_steps

        # should be able to erase it
        foo_arma.sndd = None
        assert foo_arma.sndd is None

        # should be able to set it back
        foo_arma.sndd = sndd
        assert foo_arma.sndd.long_name.startswith('FSTArmorHeavyFootstepSet')

    @assert_no_opened_handles_after
    def test_onam(self, xedit):
        pytest.skip("can't seem to find a proper example")

    @assert_no_opened_handles_after
    def test_models(self, xedit):
        # should be able to get all model paths
        assert len(list(xedit['Skyrim.esm\\ARMA\\NakedTorso'].models)) == 4

        # should be able to get less than 4 models when some of them are
        # not set
        assert len(list(xedit['Skyrim.esm\\ARMA\\IronGlovesAA'].models)) == 2

    @assert_no_opened_handles_after
    def test_textures(self, xedit):
        # should be able to get all textures
        assert len(list(xedit['Skyrim.esm\\ARMA\\NakedTorso'].textures)) == 4

        # should be able to get less than 4 textures
        assert len(list(xedit['Skyrim.esm\\ARMA\\NakedHands'].textures)) == 3

    @assert_no_opened_handles_after
    def test_file_paths(self, xedit):
        # should be able to get all model paths
        assert set(xedit['Skyrim.esm\\ARMA\\NakedTorso'].file_paths) == set(
            ['Actors\\Character\\Character Assets\\MaleBody_1.NIF',
                'Actors\\Character\\Character Assets\\FemaleBody_1.nif',
                'Actors\\Character\\Character Assets\\1stPersonMaleBody_1.NIF',
                'Actors\\Character\\Character Assets\\1stPersonFemaleBody_1.nif'])

        # should be able to get less than 4 paths when not everything is set
        assert set(xedit['Skyrim.esm\\ARMA\\IronGlovesAA'].file_paths) == set(
            ['Armor\\Iron\\Male\\Gauntlets_1.nif',
                'Armor\\Iron\\F\\Gauntlets_1.nif'])
