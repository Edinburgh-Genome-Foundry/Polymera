import pytest
import polymera


def test_segment():
    polymera.Segment(["A", "T"])
    with pytest.raises(ValueError):
        polymera.Segment(["A", "A"])  # duplicate choice


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
    sequence.add_sequence_from_string("ATGCX")
    with pytest.raises(ValueError):
        polymera.Polymer(sequence, alphabet=polymera.bio.DNAAlphabet)

    sequence = polymera.Sequence()
    sequence.add_sequence_from_string("A,T|CC")
    exact_seq = sequence.get_exact_seq(randomize=False)
    assert type(exact_seq) == polymera.Sequence
    assert exact_seq.to_string() == "ACC"
    assert sequence.get_exact_seq(randomize=True).to_string() in ["ACC", "TCC"]

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

    sequence = polymera.Sequence()
    sequence.add_sequence_from_string("T,A")
    polymer = polymera.Polymer(
        sequence, alphabet=polymera.Alphabet(letters={"A", "T", "C", "G"})
    )

    with pytest.raises(ValueError):
        polymer.get_information_content(method="wrong parameter")
    assert polymer.get_information_content(method="option") == 2
    assert polymer.get_information_content(method="uncertainty") == 1
