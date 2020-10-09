class Polymer:
    """Class for representing a sequence with its alphabet.


    **Parameters**

    **sequence**
    > `Sequence` class instance.

    **alphabet**
    > `Alphabet` class instance.
    """

    def __init__(self, sequence, alphabet):
        self.sequence = sequence
        self.alphabet = alphabet
        self.segments = self.get_segments()

    def get_segments(self):
        """Create a list of `Segment` instances from the sequence attribute."""
        separator = self.sequence.separators["segment"]
        segment_strings = self.sequence.sequence.split(separator)

        choice_separator = self.sequence.separators["choice"]
        segments = [Segment(string, choice_separator) for string in segment_strings]

        return segments


class Alphabet:
    """The Alphabet class describes the relations between the letters.


    **Parameters**

    **letters**
    > The `set` of letters (symbols) used for the sequence.

    **Complements**
    > The `dict` of complement relations. Format: `{"A": ["T"], "T": ["A", "6"]...`.

    **Relations**
    > Not implemented yet. Non-complement relations between letters.
    """

    def __init__(
        self,
        letters={"A", "T", "C", "G", "4", "5", "6"},
        complements={
            "A": ["T"],
            "T": ["A", "6"],
            "C": ["G"],
            "G": ["C", "4", "5"],
            "4": ["G"],
            "5": ["G"],
            "6": ["T"],
        },
        relations=None,
    ):
        if any([len(letter) > 1 for letter in letters]):
            raise ValueError("Multicharacter letters are not implemented yet.")
        self.letters = letters
        self.complements = complements
        self.relations = relations


class Sequence:
    """The Sequence class stores the sequence (string).


    **Parameters**

    **sequence**
    > The sequence string (`str`).

    **separators**
    > The separator characters in a `dict`. Format:
    `{"segment": "|", "choice": ",", "letter": ".", "del": "-"}`. Letter separators are
    not implemented yet.
    """

    def __init__(
        self,
        sequence="",
        separators={"segment": "|", "choice": ",", "letter": ".", "del": "-"},
    ):
        self.sequence = sequence
        self.separators = separators


class Segment:
    """Segments store the possible subsequences (choices) for a given region.


    **Parameters**

    **string**
    > The subsequence (`str`).

    **choice_separator**
    > Character marking the boundaries of subsequence alternatives (`str`)."""

    def __init__(self, string, choice_separator=","):
        self.choices = string.split(choice_separator)
        if not all([len(choice) == len(self.choices[0]) for choice in self.choices]):
            raise ValueError("Choices of a segment must be the same length.")
