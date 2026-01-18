"""Langues Weighting System (LWS) Core Module

Implements the mathematical foundations of the Sacred Tongue linguistic
weighting system for cryptographic semantic binding.

Core Formula: W(x) = sum_{i=1}^{n} alpha_i * phi(x_i) * delta(c_i)

Where:
- alpha_i: Base weight coefficient (Hebrew gematria-derived)
- phi(x_i): Phonetic transformation function
- delta(c_i): Contextual modifier based on position
"""

import math
import hashlib
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from enum import Enum
import struct


class HebrewLetter(Enum):
    """Hebrew letter gematria values."""
    ALEPH = 1
    BET = 2
    GIMEL = 3
    DALET = 4
    HE = 5
    VAV = 6
    ZAYIN = 7
    CHET = 8
    TET = 9
    YOD = 10
    KAF = 20
    LAMED = 30
    MEM = 40
    NUN = 50
    SAMECH = 60
    AYIN = 70
    PE = 80
    TSADE = 90
    QOF = 100
    RESH = 200
    SHIN = 300
    TAV = 400


@dataclass
class PhoneticVector:
    """Phonetic feature representation."""
    voicing: float  # 0 = unvoiced, 1 = voiced
    place: float    # 0-1 normalized articulation place
    manner: float   # 0-1 normalized articulation manner
    nasality: float # 0 = oral, 1 = nasal
    
    def to_array(self) -> List[float]:
        return [self.voicing, self.place, self.manner, self.nasality]
    
    def dot(self, other: 'PhoneticVector') -> float:
        return sum(a * b for a, b in zip(self.to_array(), other.to_array()))


@dataclass
class LWSToken:
    """Weighted linguistic token."""
    symbol: str
    base_weight: float
    phonetic: PhoneticVector
    position: int
    context_modifier: float = 1.0
    
    @property
    def computed_weight(self) -> float:
        phonetic_factor = sum(self.phonetic.to_array()) / 4.0
        return self.base_weight * phonetic_factor * self.context_modifier


class LWSEngine:
    """Langues Weighting System computational engine."""
    
    PHI = (1 + math.sqrt(5)) / 2  # Golden ratio
    SACRED_PRIMES = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
    
    def __init__(self):
        self.gematria_map = self._build_gematria_map()
        self.phonetic_map = self._build_phonetic_map()
    
    def _build_gematria_map(self) -> Dict[str, int]:
        """Build Hebrew-to-Latin phonetic gematria mapping."""
        return {
            'a': HebrewLetter.ALEPH.value,
            'b': HebrewLetter.BET.value,
            'g': HebrewLetter.GIMEL.value,
            'd': HebrewLetter.DALET.value,
            'h': HebrewLetter.HE.value,
            'v': HebrewLetter.VAV.value, 'w': HebrewLetter.VAV.value,
            'z': HebrewLetter.ZAYIN.value,
            'ch': HebrewLetter.CHET.value,
            't': HebrewLetter.TET.value,
            'y': HebrewLetter.YOD.value, 'i': HebrewLetter.YOD.value,
            'k': HebrewLetter.KAF.value, 'c': HebrewLetter.KAF.value,
            'l': HebrewLetter.LAMED.value,
            'm': HebrewLetter.MEM.value,
            'n': HebrewLetter.NUN.value,
            's': HebrewLetter.SAMECH.value,
            'o': HebrewLetter.AYIN.value,
            'p': HebrewLetter.PE.value, 'f': HebrewLetter.PE.value,
            'ts': HebrewLetter.TSADE.value,
            'q': HebrewLetter.QOF.value,
            'r': HebrewLetter.RESH.value,
            'sh': HebrewLetter.SHIN.value,
            'th': HebrewLetter.TAV.value,
            'e': 5, 'u': 6
        }
    
    def _build_phonetic_map(self) -> Dict[str, PhoneticVector]:
        """Build phonetic feature vectors for letters."""
        return {
            'a': PhoneticVector(1.0, 0.5, 0.2, 0.0),
            'b': PhoneticVector(1.0, 0.0, 0.8, 0.0),
            'c': PhoneticVector(0.0, 0.7, 0.8, 0.0),
            'd': PhoneticVector(1.0, 0.3, 0.8, 0.0),
            'e': PhoneticVector(1.0, 0.4, 0.2, 0.0),
            'f': PhoneticVector(0.0, 0.1, 0.4, 0.0),
            'g': PhoneticVector(1.0, 0.7, 0.8, 0.0),
            'h': PhoneticVector(0.0, 1.0, 0.4, 0.0),
            'i': PhoneticVector(1.0, 0.3, 0.2, 0.0),
            'k': PhoneticVector(0.0, 0.7, 0.8, 0.0),
            'l': PhoneticVector(1.0, 0.3, 0.5, 0.0),
            'm': PhoneticVector(1.0, 0.0, 0.8, 1.0),
            'n': PhoneticVector(1.0, 0.3, 0.8, 1.0),
            'o': PhoneticVector(1.0, 0.6, 0.2, 0.0),
            'p': PhoneticVector(0.0, 0.0, 0.8, 0.0),
            'r': PhoneticVector(1.0, 0.4, 0.5, 0.0),
            's': PhoneticVector(0.0, 0.3, 0.4, 0.0),
            't': PhoneticVector(0.0, 0.3, 0.8, 0.0),
            'u': PhoneticVector(1.0, 0.7, 0.2, 0.0),
            'v': PhoneticVector(1.0, 0.1, 0.4, 0.0),
            'w': PhoneticVector(1.0, 0.0, 0.3, 0.0),
            'y': PhoneticVector(1.0, 0.5, 0.3, 0.0),
            'z': PhoneticVector(1.0, 0.3, 0.4, 0.0),
        }
    
    def compute_gematria(self, text: str) -> int:
        """Compute total gematria value of text."""
        text = text.lower()
        total = 0
        i = 0
        while i < len(text):
            if i + 1 < len(text):
                digraph = text[i:i+2]
                if digraph in self.gematria_map:
                    total += self.gematria_map[digraph]
                    i += 2
                    continue
            if text[i] in self.gematria_map:
                total += self.gematria_map[text[i]]
            i += 1
        return total
    
    def tokenize(self, text: str) -> List[LWSToken]:
        """Tokenize text into weighted LWS tokens."""
        text = text.lower()
        tokens = []
        position = 0
        for i, char in enumerate(text):
            if char.isalpha():
                base = self.gematria_map.get(char, 1)
                phonetic = self.phonetic_map.get(char, PhoneticVector(0.5, 0.5, 0.5, 0.0))
                context = 1.0 + 0.1 * math.sin(position * self.PHI)
                tokens.append(LWSToken(symbol=char, base_weight=float(base), phonetic=phonetic, position=position, context_modifier=context))
                position += 1
        return tokens
    
    def sacred_hash(self, text: str) -> bytes:
        """Generate sacred geometry-bound hash."""
        tokens = self.tokenize(text)
        combined = sum(t.computed_weight * self.SACRED_PRIMES[i % len(self.SACRED_PRIMES)] for i, t in enumerate(tokens))
        combined *= (self.compute_gematria(text) / 1000.0 + 1)
        return hashlib.sha256(struct.pack('>d', combined) + text.encode()).digest()


if __name__ == '__main__':
    engine = LWSEngine()
    test_text = 'AetherMoore Quantum Sacred'
    print(f'Gematria: {engine.compute_gematria(test_text)}')
    print(f'Sacred hash: {engine.sacred_hash(test_text).hex()[:32]}...')
