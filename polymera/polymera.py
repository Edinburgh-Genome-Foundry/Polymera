import math


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

    def get_information_content(self, method):
        """Get information content of the polymer sequence in bits.

        An ambiguous position can mean one of two things in a sequence:
        1. Options: all letters noted in the position are suitable.
        2. Uncertainty: it's not exactly known what letter occupies the position.


        **Parameters**

        **method**
        > Interpretation of ambiguity (`str`): `option` or `uncertainty`.
        """
        if method == "option":
            return self.get_option_information_content()
        elif method == "uncertainty":
            return self.get_uncertainty_information_content()
        else:
            raise ValueError("`method` must be one of `option` or `uncertainty`")

    def get_option_information_content(self):
        """Get information content of the polymer sequence.

        Ambiguity is interpreted as options.
        """
        total_length = self.sequence.get_length()
        number_of_letters = len(self.alphabet.letters)
        p = 1 / number_of_letters  # probability
        # Shannon information per letter: -log_2 p
        log2_p = math.log(p, 2)
        information = -log2_p * total_length

        return information

    def get_uncertainty_information_content(self):
        """Get information content of the polymer sequence.

        Ambiguity is interpreted as uncertainty: the information content equals to the
        negative base 2 logarithm of the probability of the sequence. The probability
        equals to the number of sequences represented, divided by the number of possible
        sequences with the same length: -log2(represented / possible).
        """
        total_possible = len(self.alphabet.letters) ** self.sequence.get_length()
        p = self.sequence.calculate_number_of_combinations() / total_possible

        log2_p = math.log(p, 2)
        information = -log2_p

        return information


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

    def get_length(self):
        """Return the length of the sequence."""
        total_length = 0
        for segment in self.segments:
            # All choices of a segment have the same length, so the first is used:
            total_length += len(segment.choices[0])

        return total_length


class Segment:
    """Segments store the possible subsequences (choices) for a given region.


    **Parameters**

    **choices**
    > The `list` of segment choice `str`s.
    """

    def __init__(self, choices):
        self.choices = choices
