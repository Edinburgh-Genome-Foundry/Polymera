"""Protein."""

from ..polymera import Alphabet

ProteinAlphabet = Alphabet(
    letters={
        "*",  # STOP
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "K",
        "L",
        "M",
        "N",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    },
    complements={},
    relations=None,
)
