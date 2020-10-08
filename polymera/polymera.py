class Polymera:
    def __init__(self, sequence, alphabet):
        self.sequence = sequence
        self.alphabet = alphabet
        self.segments = self.get_segments()

    def get_segments(self):
        separator = self.sequence.separators["segment"]
        segment_strings = self.sequence.sequence.split(separator)

        choice_separator = self.sequence.separators["choice"]
        segments = [Segment(string, choice_separator) for string in segment_strings]

        return segments


class Alphabet:
    """The Alphabet class describes the relations between the letters."""

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
    """The Sequence stores the sequence (string).


    **Parameters**

    **sequence**
    > The sequence string (`str`).

    **separators**
    > The separator characters in a `dict`. Example:
    `{"segment": "|", "choice": ",", "letter": ".", "del": "-"}`.
    """

    def __init__(
        self,
        sequence="",
        separators={"segment": "|", "choice": ",", "letter": ".", "del": "-"},
    ):
        self.sequence = sequence
        self.separators = separators


class Segment:
    def __init__(self, string, choice_separator=","):
        self.choices = string.split(choice_separator)
        if not all([len(choice) == len(self.choices[0]) for choice in self.choices]):
            raise ValueError("Choices of a segment must be the same length.")
