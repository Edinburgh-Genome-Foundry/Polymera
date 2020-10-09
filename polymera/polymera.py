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

    def get_choice_complement(self, seq):
        """Return the complement of a sequence string (choice).


        **Parameters**

        **seq**
        > String to complement (`str`).
        """
        # The complements of a letter are always a list and the first one is used:
        complement = "".join([self.alphabet.complements[letter][0] for letter in seq])

        return complement

    def get_segment_complement(self, segment):
        """Return the complement of a Segment.

        **Parameters**

        **segment**
        > `Segment` to complement.
        """

        complement_choices = []
        for choice in segment.choices:
            complement_choice = self.get_choice_complement(choice)
            complement_choices.append(complement_choice)

        complement_segment = Segment(complement_choices)

        return complement_segment


class Alphabet:
    """The Alphabet class describes the relations between the letters.


    **Parameters**

    **letters**
    > The `set` of letters (symbols) used for the sequence.

    **complements**
    > The `dict` of complement relations. Format: `{"A": ["T"], "T": ["A", "6"]...`.

    **relations**
    > Not implemented yet. Non-complement relations between letters.
    """

    def __init__(
        self, letters={}, complements={}, relations=None,
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

        self.segments = self.get_segments()

    def create_choices_from_string(self, string):
        choices = string.split(self.separators["choice"])
        if not all([len(choice) == len(choices[0]) for choice in choices]):
            raise ValueError("Choices of a segment must be the same length.")
        return choices

    def get_segments(self):
        """Create a list of `Segment` instances from the sequence attribute."""
        separator = self.separators["segment"]
        segment_strings = self.sequence.split(separator)

        segments = [
            Segment(self.create_choices_from_string(string))
            for string in segment_strings
        ]

        return segments


class Segment:
    """Segments store the possible subsequences (choices) for a given region.


    **Parameters**

    **choices**
    > The `list` of segment choice `str`s.
    """

    def __init__(self, choices):
        self.choices = choices
