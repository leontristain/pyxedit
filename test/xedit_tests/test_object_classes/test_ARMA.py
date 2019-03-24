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
