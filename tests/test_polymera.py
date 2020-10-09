import pytest
import polymera


def test_segment():
    with pytest.raises(ValueError):
        polymera.Segment("A,AA")


def test_sequence():
    polymera.Sequence()


def test_alphabet():
    polymera.Alphabet()
    with pytest.raises(ValueError):
        polymera.Alphabet(letters={"multicharacter_letter"})  # not implemented yet


def test_polymer():
    polymera.Polymer(
        polymera.Sequence("ATGAA,ATGCC|TATATTAGAAAAAA"), polymera.Alphabet()
    )
