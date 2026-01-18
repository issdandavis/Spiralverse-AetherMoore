"""Spiralverse-AetherMoore Source Package

Quantum-Resistant Cryptographic Framework with:
- Harmonic Scaling Law H(d,R)
- Six Sacred Tongues encoding
- 13-layer security stack
- SCBE (Spiral Chaos-Based Encryption) Engine
"""

__version__ = "0.1.0"
__author__ = "Isaac Davis"
__email__ = "issdandavis@github.com"

from src.scbe_engine import SCBEEngine, encrypt, decrypt
from src.harmonic_crypto import HarmonicScaling, compute_hdr
from src.aethermoore import AetherMooreProtocol

__all__ = [
    "__version__",
    "__author__",
    "SCBEEngine",
    "encrypt",
    "decrypt",
    "HarmonicScaling",
    "compute_hdr",
    "AetherMooreProtocol",
]
