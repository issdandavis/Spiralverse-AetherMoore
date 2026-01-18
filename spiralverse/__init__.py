"""Spiralverse-AetherMoore: Quantum-Resistant Cryptographic Framework

A next-generation cryptographic system combining:
- Post-Quantum Cryptography (Kyber/Dilithium)
- Harmonic Scaling Law H(d,R)
- Six Sacred Tongues encoding
- 13-layer security stack
- Langues Weighting System (LWS)
"""

__version__ = '0.1.0'
__author__ = 'Isaac Davis'
__email__ = 'issdandavis@github.com'

# Core imports
from spiralverse.core.sacred_tongues import (
    SacredTongue,
    SixTonguesLayer,
    LanguesWeight,
    TongueWeight,
    SacredTongueEncoder,
)

from spiralverse.crypto.pqc_module import (
    PQCModule,
    KyberKEM,
    DilithiumSign,
    HarmonicScaling,
    SecurityLevel,
    KyberPublicKey,
    KyberPrivateKey,
    DilithiumPublicKey,
    DilithiumPrivateKey,
)

# Convenience class combining all features
class AetherMooreCipher:
    """Main cipher class combining PQC and Sacred Tongues"""
    
    def __init__(self, security_level: SecurityLevel = SecurityLevel.LEVEL_5):
        self.pqc = PQCModule(security_level)
        self.tongues = SixTonguesLayer()
        self.security_level = security_level
    
    def generate_keypair(self):
        """Generate Kyber keypair"""
        return self.pqc.generate_kem_keypair()
    
    def encrypt(self, plaintext: bytes, public_key: KyberPublicKey) -> bytes:
        """Encrypt with PQC + Sacred Tongues"""
        # Apply Sacred Tongues encoding
        encoded = self.tongues.full_encode(plaintext)
        # Encapsulate with Kyber
        ct, ss = self.pqc.encapsulate(public_key)
        # XOR with shared secret for symmetric encryption
        encrypted = bytes(e ^ s for e, s in zip(encoded, (ss * (len(encoded) // 32 + 1))[:len(encoded)]))
        return ct + encrypted
    
    def decrypt(self, ciphertext: bytes, private_key: KyberPrivateKey) -> bytes:
        """Decrypt with PQC + Sacred Tongues"""
        # Split ciphertext
        ct = ciphertext[:self.pqc.kem.CT_SIZE]
        encrypted = ciphertext[self.pqc.kem.CT_SIZE:]
        # Decapsulate to get shared secret
        ss = self.pqc.decapsulate(private_key, ct)
        # XOR to decrypt
        decoded = bytes(e ^ s for e, s in zip(encrypted, (ss * (len(encrypted) // 32 + 1))[:len(encrypted)]))
        # Reverse Sacred Tongues encoding
        return self.tongues.full_decode(decoded)


__all__ = [
    # Version info
    '__version__',
    '__author__',
    
    # Main cipher
    'AetherMooreCipher',
    
    # Sacred Tongues
    'SacredTongue',
    'SixTonguesLayer',
    'LanguesWeight',
    'TongueWeight',
    'SacredTongueEncoder',
    
    # PQC
    'PQCModule',
    'KyberKEM',
    'DilithiumSign',
    'HarmonicScaling',
    'SecurityLevel',
    'KyberPublicKey',
    'KyberPrivateKey',
    'DilithiumPublicKey',
    'DilithiumPrivateKey',
]
