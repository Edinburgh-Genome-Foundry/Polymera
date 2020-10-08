# Polymera

Polymera is a Python package for representing *ambiguous sequences.* An ambiguous sequence has zero or more letters (symbols, elements) at each position. Additionally, it can model sequences written with *complement alphabets.* Each letter of a complement alphabet can form a pair with a specific letters, their *complements.*, that are specific to the letter.

These sequences can describe linear polymers, for example DNA, that can pair with a complement polymer.


## Details

The Polymer class consists of the Sequence and the Alphabet classes. The relations between the letters are described by the alphabet, and can be complement relations or other type. Polymera has built-in alphabets for nucleic acids (DNA, RNA) and proteins.

---

Representation of these sequences in writing can be in the following way:
`AGXCTGXGTGTA55GTAGT66`
The sequence can contain an arbitrary set of letters. For example, in the case of DNA it can represent xenonucleotides or methylated nucleotides.

Sequence with choice ambiguity:
`GCG|A,G|T,C,G|AGCA` , where a segment separator character `|` (vertical bar) denotes the sections of the sequence, and the choices are separated by another character: `,` (comma). The above can mean one of 6 (=1\*2\*3\*1) strings:
```
GCGATAGCA
   GG
    C
```

The choices can span multiple positions with multiletter choices (`GCG|ATC,AGA|TC,GT|AGCA`) or contain deletions (indels), marked with `-`: `GTAGTG|AT,-T|TAA`.

Finally, the letters can be written with multiple characters, using a separator character between the letters (`.`):
`A,6mA|T.G.C.T|5mC,C|G.C.5mC`.
This is useful if we want to represent similarities between some letters in a readable way. In the example above, `A` = adenine,  `6mA` = N6-methyladenine. Another example is writing diphthongs, for example `ae`.

---

Note that in a sequence, an ambiguous position can mean one of two things:
1. Options: all letters noted in the position are suitable.
2. Uncertainty: it's not exactly known what letter occupies the position.

This has implications for interpreting the information content of the sequence.

---

## Install

```bash
pip install polymera
```

## Usage


## Versioning

Polymera uses the [semantic versioning](https://semver.org) scheme.


## License = MIT

Polymera is [free software](https://www.gnu.org/philosophy/free-sw.en.html), which means the users have the freedom to run, copy, distribute, study, change and improve the software.

Polymera was written at the [Edinburgh Genome Foundry](https://edinburgh-genome-foundry.github.io/) by [Peter Vegh](https://github.com/veghp) and is released under the MIT license.
