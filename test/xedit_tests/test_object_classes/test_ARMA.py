import pytest

from xelib import XEditError

from .. fixtures import xedit  # NOQA: for pytest


class TestARMA:
    def test_bodt(self, xedit):
        with xedit.manage_handles():
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

    def test_bod2(self, xedit):
        pytest.skip('Not sure I understand this field')

    def test_rnam(self, xedit):
        with xedit.manage_handles():
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

    def test_dnam(self, xedit):
        with xedit.manage_handles():
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
    def test_mod(self, xedit, n, nifpath):
        sig = f'mod{n}'
        alias = {'mod2': 'male_model',
                 'mod3': 'male_firstperson_model',
                 'mod4': 'female_model',
                 'mod5': 'female_firstperson_model'}[sig]

        with xedit.manage_handles():
            arma = xedit['Dawnguard.esm\\ARMA\\DLC1VampireRobesAA']

            # signature attribute should work
            assert getattr(arma, sig)

            # aliases should work
            assert getattr(arma, alias)

            # should be able to futher access the model path
            assert getattr(arma, sig).model == nifpath

            # this particular one doesn't have alternate textures
            assert getattr(arma, sig).alternate_textures is None

            # the nif path element should be editable
            getattr(arma, sig).model = 'Some\\Other\\Path.nif'
            assert getattr(arma, sig).model == 'Some\\Other\\Path.nif'
            getattr(arma, sig).model = nifpath
            assert getattr(arma, sig).model == nifpath

            # the nif path element should not be deletable since it is required
            with pytest.raises(XEditError):
                getattr(arma, sig).model = None

            # but we are free to set it to empty
            getattr(arma, sig).model = ''
            assert getattr(arma, sig).model == ''
            getattr(arma, sig).model = nifpath
            assert getattr(arma, sig).model == nifpath

            # cannot set the field itself since it is a non-value element
            with pytest.raises(XEditError):
                setattr(arma, sig, 3)

            # we should be able to delete the field itself
            setattr(arma, sig, None)
            assert getattr(arma, sig) is None

            # we should be able to add it back
            arma.add(sig.upper())
            getattr(arma, sig).model = nifpath
            assert getattr(arma, sig).model == nifpath

    @pytest.mark.parametrize('n,texture_name',
                             [(0, 'SkinBodyMale_1'),
                              (1, 'SkinBodyFemale_1'),
                              (2, 'SkinMaleHumanBody'),
                              (3, 'SkinFemaleHumanBody')])
    def test_nam(self, xedit, n, texture_name):
        sig = f'nam{n}'
        alias = {'nam0': 'base_male_texture',
                 'nam1': 'base_female_texture',
                 'nam2': 'base_male_firstperson_texture',
                 'nam3': 'base_female_firstperson_texture'}[sig]
        with xedit.manage_handles():
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
