"""DNA.

A  adenine
T  thymine
C  cytosine
G  guanine
4  N4-methylcytosine
5  C5-methylcytosine
6  N6-methyladenine
"""

from ..polymera import Alphabet

DNAAlphabet = Alphabet(
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
)
