import math
import random


class WrongLetterError(ValueError):
    pass


class DuplicateChoiceError(ValueError):
    pass


class Polymer:
    """Class for representing a sequence with its alphabet.


    **Parameters**

    **sequence**
    > `Sequence` class instance.

    **alphabet**
    > `Alphabet` class instance.
    """

    def __init__(self, sequence, alphabet):
        letters_only = set(sequence.to_string()) - set(sequence.separators.values())
        wrong_letters = letters_only - alphabet.letters
        if wrong_letters != set():
            raise WrongLetterError(
                "These letters are not in the alphabet: %s" % wrong_letters
            )

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

    def get_exact_seq(self, randomize=False):
        """Get an exact sequence and combine the segments.


        **Parameters**

        **random**
        > Choice selection (`bool`). If `True`, use a random choice for each segment,
        if `False`, use the first choice for each segment.
        """
        seq = Sequence()
        string = ""
        if randomize:
            for segment in self.segments:
                choice = random.choice(segment.choices)
                string += choice
        else:
            for segment in self.segments:
                string += segment.choices[0]
        seq.add_sequence_from_string(string)
        return seq


class Segment:
    """Segments store the possible subsequences (choices) for a given region.


    **Parameters**

    **choices**
    > The `list` of segment choice `str`s.
    """

    def __init__(self, choices):
        self.choices = choices
        if len(set(choices)) != len(choices):
            raise DuplicateChoiceError("Choices of a segment must be unique.")


class UnequalLengthError(ValueError):
    pass


def hamming(seq1, seq2, comparison="options"):
    """Calculate Hamming distance between two sequences.


    **Parameters**

    **seq1, seq2**
    > Sequences to compare (`Sequence`).

    **comparison**
    > Interpretation of ambiguity (`str`): `"options"` (default) or `"uncertainty"`.
    """
    if seq1.get_length() != seq2.get_length():
        raise UnequalLengthError("The two sequences must be the same length!")

    if comparison == "options":
        distance = hamming_options(seq1, seq2)
    elif comparison == "uncertainty":
        distance = hamming_uncertainty(seq1, seq2)
    else:
        raise ValueError("Parameter comparison must be 'options' or 'uncertainty'!")

    return distance


def break_segment(segment):
    """Return a list of n 1-length Segments from a Segment of length n."""
    new_segments = []
    for i in range(0, len(segment.choices[0])):
        new_choices = []
        for choice in segment.choices:
            new_choices += choice[i]
            new_choices = list(set(new_choices))  # remove duplicate letters
        new_segment = Segment(choices=new_choices)
        new_segments += [new_segment]

    return new_segments


def convert_to_nosegment(seq):
    """Convert Sequence segments to length 1 segments."""
    new_segments = []
    for segment in seq.segments:
        new_subsegments = break_segment(segment)
        new_segments += new_subsegments

    sequence = Sequence(segments=new_segments)
    return sequence


def hamming_options(seq1, seq2):
    """Calculate Hamming distance between two sequences.

    Interpret ambiguity as options.
    """

    sequence1 = convert_to_nosegment(seq1)
    sequence2 = convert_to_nosegment(seq2)

    distance = 0
    for i, segment1 in enumerate(sequence1.segments):
        segment2 = sequence2.segments[i]
        if set(segment1.choices) & set(segment2.choices) == set():
            distance += 1

    return distance


def hamming_uncertainty(seq1, seq2):
    """Calculate Hamming distance between two sequences.

    Interpret ambiguity as uncertainty.
    """
    sequence1 = convert_to_nosegment(seq1)
    sequence2 = convert_to_nosegment(seq2)

    distance = 0
    for i, segment1 in enumerate(sequence1.segments):
        choice_chance_sum = 0
        segment2 = sequence2.segments[i]

        for choice in segment1.choices:  # single characters as sequences were converted

            if choice in set(segment2.choices):
                choice_chance = 1 / len(segment2.choices)
                choice_chance_sum += choice_chance

        chance = choice_chance_sum / len(segment1.choices)
        pos_distance = 1 - chance
        distance += pos_distance

    return distance
