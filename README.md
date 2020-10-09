<p align="center">
<img alt="Polymera logo" title="Polymera" src="https://raw.githubusercontent.com/Edinburgh-Genome-Foundry/Polymera/main/images/Polymera.png" width="140">
</p>


# Polymera

[![Build Status](https://travis-ci.org/Edinburgh-Genome-Foundry/Polymera.svg?branch=main)](https://travis-ci.org/Edinburgh-Genome-Foundry/Polymera)
[![Coverage Status](https://coveralls.io/repos/github/Edinburgh-Genome-Foundry/Polymera/badge.svg?branch=main)](https://coveralls.io/github/Edinburgh-Genome-Foundry/Polymera?branch=main)

**Work in progress!**

Polymera is a Python package for representing *ambiguous sequences.* An ambiguous sequence has a number of possible letters (symbols, elements) at each position. Additionally, Polymera can model sequences written with *complement alphabets.* Each letter of a complement alphabet can form a pair with specific letters, their *complements.*

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

The choices can span multiple positions with multiletter choices (`GCG|ATC,AGA|TC,GT|AGCA`) and can contain deletions (indels), marked with `-`: `GTAGTG|AT,-T|TAA`. Note that `|AATCCGTCAA|` does not equal to `|AA|TCCGTC|AA|` because the segment boundaries specify the full subsequence that *has* to exist together in the sequence.

Finally, the letters can be written with multiple characters, using a separator character between the letters (`.`):
`A,6mA|T.G.C.T|5mC,C|G.C.5mC`.
This is useful if we want to represent similarities between some letters in a readable way. In the example above, `A` = adenine, `6mA` = N6-methyladenine, `5mC` = C5-methylcytosine. Another example is writing diphthongs, for example `ae`.

### Information content

Note that in a sequence, an ambiguous position can mean one of two things:

1. Options: all letters noted in the position are suitable.
2. Uncertainty: it's not exactly known what letter occupies the position.

This has implications for the information content of the sequence.


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
```
Returns `2`.

Instantiate polymer:

```python
polymer = polymera.Polymer(sequence, alphabet=polymera.bio.DNAAlphabet)
polymer.get_sequence_reverse_complement().to_string()
```
Returns `TTTTTTCTAATATA|GGCAT,TTCAT`.


## Versioning

Polymera uses the [semantic versioning](https://semver.org) scheme.


## License = MIT

Polymera is [free software](https://www.gnu.org/philosophy/free-sw.en.html), which means the users have the freedom to run, copy, distribute, study, change and improve the software.

Polymera was written at the [Edinburgh Genome Foundry](https://edinburgh-genome-foundry.github.io/) by [Peter Vegh](https://github.com/veghp) and is released under the MIT license.
