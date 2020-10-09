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

    def get_sequence_complement(self):
        """Return the complement of the polymer sequence."""
        complement_segments = []
        for segment in self.sequence.segments:
            complement_segment = self.get_segment_complement(segment)

            complement_segments.append(complement_segment)
        return Sequence(complement_segments, self.sequence.separators)

    def get_choice_reverse(self, seq):
        """Get reverse of a sequence string (choice).


        **Parameters**

        **seq**
        > String to reverse (`str`).
        """
        reverse = seq[::-1]

        return reverse

    def get_segment_reverse(self, segment):
        """Return the reverse of a Segment.

        **Parameters**

        **segment**
        > `Segment` to reverse.
        """

        reverse_choices = []
        for choice in reversed(segment.choices):
            reverse_choice = self.get_choice_reverse(choice)
            reverse_choices.append(reverse_choice)

        reverse_segment = Segment(reverse_choices)

        return reverse_segment

    def get_sequence_reverse(self):
        """Return the reverse of the polymer sequence."""
        reverse_segments = []
        for segment in reversed(self.sequence.segments):
            reverse_segment = self.get_segment_reverse(segment)

            reverse_segments.append(reverse_segment)
        return Sequence(reverse_segments, self.sequence.separators)

    def get_sequence_reverse_complement(self):
        """Return the reverse complement of the polymer sequence."""
        reverse = self.get_sequence_reverse()
        reversed_polymer = Polymer(sequence=reverse, alphabet=self.alphabet)
        reverse_complement = reversed_polymer.get_sequence_complement()

        return reverse_complement


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

    **segments**
    > A `list` of `Segment`s.

    **separators**
    > The separator characters in a `dict`. Format:
    `{"segment": "|", "choice": ",", "letter": ".", "del": "-"}`. Letter
    separators are not implemented yet.
    """

    def __init__(
        self,
        segments=None,
        separators={"segment": "|", "choice": ",", "letter": ".", "del": "-"},
    ):
        if segments is None:
            self.segments = []
        else:
            self.segments = segments
        self.separators = separators

    def create_choices_from_string(self, string):
        choices = string.split(self.separators["choice"])
        if not all([len(choice) == len(choices[0]) for choice in choices]):
            raise ValueError("Choices of a segment must have the same length.")
        return choices

    def create_segments_from_string(self, string):
        """Create a list of `Segment` instances from the sequence attribute."""
        separator = self.separators["segment"]
        segment_strings = string.split(separator)

        segments = [
            Segment(self.create_choices_from_string(string))
            for string in segment_strings
        ]

        return segments

    def add_sequence_from_string(self, string):
        """Convert a string into segments and append to the sequence.

        **Parameters**

        **string**
        > `str`.
        """
        if self.segments is []:
            self.segments = self.create_segments_from_string(string)
        else:
            self.segments += self.create_segments_from_string(string)

    def calculate_number_of_combinations(self):
        """Calculate the number of exact sequences represented."""
        multiplier_list = []
        for segment in self.segments:
            multiplier_list.append(len(segment.choices))
        x = 1
        for multiplier in multiplier_list:
            x *= multiplier

        return x

    def to_string(self):
        """Return a string representation of the ambiguous sequence."""
        joined_choices = [
            self.separators["choice"].join(segment.choices) for segment in self.segments
        ]
        string = self.separators["segment"].join(joined_choices)

        return string


class Segment:
    """Segments store the possible subsequences (choices) for a given region.


    **Parameters**

    **choices**
    > The `list` of segment choice `str`s.
    """

    def __init__(self, choices):
        self.choices = choices
