<p align="center">
<img alt="Polymera logo" title="Polymera" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Polymera/main/images/Polymera.png" width="140">
</p>


# Polymera

[![Build Status](https://travis-ci.org/Edinburgh-Genome-Foundry/Polymera.svg?branch=main)](https://travis-ci.org/Edinburgh-Genome-Foundry/Polymera)
[![Coverage Status](https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/Polymera/badge.svg?branch=main)](https://coveralls.io/github/Edinburgh-Genome-Foundry/Polymera?branch=main)

**Work in progress!**

Polymera is a Python package for representing *ambiguous sequences.* An ambiguous sequence has a number of possible letters (symbols, elements) at each position. Additionally, Polymera can model sequences written with *complement alphabets.* Each letter of a complement alphabet can form a pair with specific letters, their *complements.* A special type is the *exact sequence,* which has only one letter at each position.

These sequences can describe linear polymers, for example DNA, that can pair with a complement polymer.

*Polymera* is a genus of crane fly.


## Details

The Polymer class consists of the Sequence and the Alphabet classes. The relations between the letters are described by the alphabet, and can be complement relations or other type. Polymera has built-in alphabets for nucleic acids (DNA) and proteins.

### Representation in writing

Representation of these sequences in writing can be in the following way: `AGXCTGXGTGTA55GTAGT66`. The sequence can contain an arbitrary set of letters. For example, in the case of DNA, it can represent xenonucleotides or methylated nucleotides.

Sequence with choice ambiguity: `GCG|A,G|TC,GG`, where a segment separator character, here `|` (vertical bar), denotes the sections of the sequence, and the choices are separated by another character: here we use `,` (comma). The above can mean one of 4 (=1\*2\*2) strings:
```
GCGATC
GCGAGG
GCGGTC
GCGGGG
```

The choices can span multiple positions with multiletter choices (`GCG|ATC,AGA|TC,GT|AGCA`) and can contain deletions (indels), marked with `-` (hyphen): `GTAGTG|AT,-T|TAA`. Note that `|AATCCGTCAA|` does *not* equal to `|AA|TCCGTC|AA|` because the segment boundaries specify the full subsequence that *has* to exist as is, in the sequence.

Finally, the letters can be written with multiple characters, using a separator character between the letters (`.`, period): `A,6mA|T.G.C.T|5mC,C|G.C.5mC`. This is useful if we want to represent similarities between some letters in a readable way. In the example above the multiletters denote methylated variants of the standard letters: `A` = adenine, `6mA` = N6-methyladenine, `C` = cytosine, `5mC` = C5-methylcytosine. Another example is writing diphthongs, for example `ae`.


### Information content

Note that in a sequence, an ambiguous position can mean one of two things:

1. Options: all letters noted in the position are suitable.
2. Uncertainty: it's not exactly known what letter occupies the position.

This has implications for interpreting the Shannon information content of the sequence. For case (1) above (options), the Shannon information of a letter position is -log2(p), where p = 1 / n, with n letters in the alphabet. The information of a 1 letter-long sequence with 2 choices (e.g. `A,T`), from a 4-letter alphabet is 2 bit: -log2(1/4). For calculating information of longer sequences, the information of a position is multiplied by the length of the sequence.

For case (2) (uncertainty), the probability (p) is calculated as the number of sequences represented divided by the number of possible sequences with the same length. Thus the information of `A,T` (which means one of `A` or `T`, but not known which one) is only 1 bit: -log2(2/4).
Consequently, the information of the uncertain letter `A,T,C,G` (representing `A` or `T` or `C` or `G`) is zero, because -log2(4/4) = 0.


## Install

```bash
pip install polymera
```


## Usage

Define a sequence:

```python
sequence = polymera.Sequence()
sequence.add_sequence_from_string("ATGAA,ATGCC|TATATTAGAAAAAA")
sequence.calculate_number_of_combinations()
# 2
```

Instantiate polymer:

```python
polymer = polymera.Polymer(sequence, alphabet=polymera.bio.DNAAlphabet)
polymer.get_sequence_reverse_complement().to_string()
# TTTTTTCTAATATA|GGCAT,TTCAT
```

Get an exact sequence:

```python
exact_seq = sequence.get_exact_seq(randomize=True)
exact_seq.to_string()
# ATGAATATATTAGAAAAAA
```

Polymera can calculate the information of a sequence, in bits:

```python
sequence = polymera.Sequence()
sequence.add_sequence_from_string("T,A")
polymer = polymera.Polymer(
    sequence, alphabet=polymera.Alphabet(letters={"A", "T", "C", "G"})
)
polymer.get_information_content(method="option")
# 2
```

```python
polymer.get_information_content(method="uncertainty")
# 1
```


## Versioning

Polymera uses the [semantic versioning](https://semver.org) scheme.


## License = MIT

Polymera is [free software](https://www.gnu.org/philosophy/free-sw.en.html), which means the users have the freedom to run, copy, distribute, study, change and improve the software.

Polymera was written at the [Edinburgh Genome Foundry](https://edinburgh-genome-foundry.github.io/) by [Peter Vegh](https://github.com/veghp) and is released under the MIT license.
