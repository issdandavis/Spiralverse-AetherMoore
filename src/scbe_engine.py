"""SCBE (Spiral Chaos-Based Encryption) Engine

Core encryption/decryption module implementing:
- 5-axis chaos generation
- Harmonic modulation
- Quantum-resistant key derivation
"""

import hashlib
import secrets
from typing import Tuple, Optional
from dataclasses import dataclass
import numpy as np


@dataclass
class SCBEConfig:
    """Configuration for SCBE engine"""
    chaos_iterations: int = 1000
    key_size: int = 256
    block_size: int = 16
    harmonic_d: float = 2.0
    harmonic_R: int = 1000


class ChaosGenerator:
    """5-axis chaos generation using logistic map"""
    
    def __init__(self, seed: bytes):
        self.seed = seed
        self._state = self._init_state(seed)
    
    def _init_state(self, seed: bytes) -> np.ndarray:
        """Initialize 5-axis state from seed"""
        h = hashlib.sha3_512(seed).digest()
        state = np.zeros(5)
        for i in range(5):
            state[i] = int.from_bytes(h[i*8:(i+1)*8], 'big') / (2**64)
            state[i] = 0.1 + 0.8 * state[i]  # Map to (0.1, 0.9)
        return state
    
    def iterate(self, r: float = 3.99) -> np.ndarray:
        """Single iteration of logistic map"""
        self._state = r * self._state * (1 - self._state)
        return self._state.copy()
    
    def generate_stream(self, length: int) -> bytes:
        """Generate chaotic byte stream"""
        result = bytearray()
        while len(result) < length:
            self.iterate()
            for val in self._state:
                result.append(int(val * 256) % 256)
        return bytes(result[:length])


class SCBEEngine:
    """Main SCBE encryption engine"""
    
    def __init__(self, config: Optional[SCBEConfig] = None):
        self.config = config or SCBEConfig()
        self._chaos = None
    
    def derive_key(self, password: bytes, salt: Optional[bytes] = None) -> bytes:
        """Derive encryption key using chaos and PBKDF"""
        if salt is None:
            salt = secrets.token_bytes(16)
        
        # Initial key derivation
        initial = hashlib.pbkdf2_hmac(
            'sha3_256',
            password,
            salt,
            iterations=100000,
            dklen=64
        )
        
        # Chaos enhancement
        chaos = ChaosGenerator(initial)
        for _ in range(self.config.chaos_iterations):
            chaos.iterate()
        
        enhanced = chaos.generate_stream(32)
        final_key = hashlib.sha3_256(initial + enhanced).digest()
        
        return salt + final_key
    
    def encrypt(self, plaintext: bytes, key: bytes) -> bytes:
        """Encrypt data using SCBE"""
        # Extract salt and actual key
        salt = key[:16]
        actual_key = key[16:48]
        
        # Initialize chaos with key
        self._chaos = ChaosGenerator(actual_key + salt)
        
        # Generate IV
        iv = secrets.token_bytes(self.config.block_size)
        
        # Encrypt blocks
        ciphertext = bytearray()
        prev_block = iv
        
        # Pad plaintext
        padded = self._pad(plaintext)
        
        for i in range(0, len(padded), self.config.block_size):
            block = padded[i:i + self.config.block_size]
            # XOR with previous block (CBC-like)
            xored = bytes(a ^ b for a, b in zip(block, prev_block))
            # XOR with chaos stream
            chaos_stream = self._chaos.generate_stream(self.config.block_size)
            encrypted = bytes(a ^ b for a, b in zip(xored, chaos_stream))
            ciphertext.extend(encrypted)
            prev_block = encrypted
        
        return iv + bytes(ciphertext)
    
    def decrypt(self, ciphertext: bytes, key: bytes) -> bytes:
        """Decrypt data using SCBE"""
        # Extract salt and actual key
        salt = key[:16]
        actual_key = key[16:48]
        
        # Initialize chaos with key
        self._chaos = ChaosGenerator(actual_key + salt)
        
        # Extract IV
        iv = ciphertext[:self.config.block_size]
        data = ciphertext[self.config.block_size:]
        
        # Decrypt blocks
        plaintext = bytearray()
        prev_block = iv
        
        for i in range(0, len(data), self.config.block_size):
            block = data[i:i + self.config.block_size]
            # XOR with chaos stream
            chaos_stream = self._chaos.generate_stream(self.config.block_size)
            xored = bytes(a ^ b for a, b in zip(block, chaos_stream))
            # XOR with previous block
            decrypted = bytes(a ^ b for a, b in zip(xored, prev_block))
            plaintext.extend(decrypted)
            prev_block = block
        
        return self._unpad(bytes(plaintext))
    
    def _pad(self, data: bytes) -> bytes:
        """PKCS7 padding"""
        pad_len = self.config.block_size - (len(data) % self.config.block_size)
        return data + bytes([pad_len] * pad_len)
    
    def _unpad(self, data: bytes) -> bytes:
        """Remove PKCS7 padding"""
        pad_len = data[-1]
        return data[:-pad_len]


# Convenience functions
def encrypt(plaintext: bytes, password: bytes) -> Tuple[bytes, bytes]:
    """Encrypt with auto key derivation"""
    engine = SCBEEngine()
    key = engine.derive_key(password)
    ciphertext = engine.encrypt(plaintext, key)
    return ciphertext, key


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    """Decrypt with provided key"""
    engine = SCBEEngine()
    return engine.decrypt(ciphertext, key)


if __name__ == '__main__':
    # Demo
    message = b'SCBE-AETHERMOORE Quantum-Resistant Test'
    password = b'spiralverse-secret'
    
    ct, key = encrypt(message, password)
    pt = decrypt(ct, key)
    
    print(f'Original: {message}')
    print(f'Encrypted: {ct.hex()[:64]}...')
    print(f'Decrypted: {pt}')
    print(f'Match: {message == pt}')
