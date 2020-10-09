import pytest
import polymera


def test_segment():
    polymera.Segment(["A", "T"])


def test_sequence():
    sequence = polymera.Sequence()  # test without segment
    sequence = polymera.Sequence(segments=[polymera.Segment(["A", "T"])])
    sequence.add_sequence_from_string("ATGAA,ATGCC|TATATTAGAAAAAA")

    assert sequence.calculate_number_of_combinations() == 4


def test_alphabet():
    polymera.Alphabet()
    with pytest.raises(ValueError):
        polymera.Alphabet(letters={"multicharacter_letter"})  # not implemented yet


def test_polymer():
    sequence = polymera.Sequence()
    sequence.add_sequence_from_string("ATGAA,ATGCC|TATATTAGAAAAAA")
    sequence.add_sequence_from_string("ATGAA,ATGCC")

    polymer = polymera.Polymer(sequence, alphabet=polymera.bio.DNAAlphabet)
    assert polymer.get_sequence_complement().segments[0].choices == ["TACTT", "TACGG"]
    assert polymer.get_sequence_reverse().segments[2].choices == ["CCGTA", "AAGTA"]
    assert polymer.get_sequence_reverse_complement().segments[2].choices == [
        "GGCAT",
        "TTCAT",
    ]

    with pytest.raises(ValueError):
        sequence.add_sequence_from_string("ATGAA,ATGC")  # choices must have same length

    assert polymer.sequence.to_string() == "ATGAA,ATGCC|TATATTAGAAAAAA|ATGAA,ATGCC"
