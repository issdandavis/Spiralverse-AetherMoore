"""Test suite for SCBE Engine."""

import pytest
import sys
sys.path.insert(0, '..')

from src.scbe_engine import SCBEEngine


class TestSCBEEngine:
    """Tests for SCBEEngine class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.engine = SCBEEngine()
    
    def test_key_derivation(self):
        """Test key derivation produces consistent keys."""
        password = b'test-password-123'
        key1 = self.engine.derive_key(password)
        key2 = self.engine.derive_key(password)
        
        # Same password with same salt should produce same key
        assert len(key1) == 32
        assert key1 == key2
    
    def test_key_derivation_different_passwords(self):
        """Test different passwords produce different keys."""
        key1 = self.engine.derive_key(b'password1')
        key2 = self.engine.derive_key(b'password2')
        
        assert key1 != key2
    
    def test_encrypt_decrypt_roundtrip(self):
        """Test encryption and decryption roundtrip."""
        key = self.engine.derive_key(b'roundtrip-test')
        plaintext = b'Hello, Quantum World!'
        
        ciphertext = self.engine.encrypt(plaintext, key)
        decrypted = self.engine.decrypt(ciphertext, key)
        
        assert decrypted == plaintext
    
    def test_ciphertext_is_different(self):
        """Test that ciphertext differs from plaintext."""
        key = self.engine.derive_key(b'diff-test')
        plaintext = b'Secret message'
        
        ciphertext = self.engine.encrypt(plaintext, key)
        
        assert ciphertext != plaintext
        assert len(ciphertext) > len(plaintext)
    
    def test_wrong_key_fails(self):
        """Test decryption with wrong key fails."""
        key1 = self.engine.derive_key(b'correct-key')
        key2 = self.engine.derive_key(b'wrong-key')
        plaintext = b'Sensitive data'
        
        ciphertext = self.engine.encrypt(plaintext, key1)
        
        with pytest.raises(Exception):
            self.engine.decrypt(ciphertext, key2)
    
    def test_empty_message(self):
        """Test encryption of empty message."""
        key = self.engine.derive_key(b'empty-test')
        plaintext = b''
        
        ciphertext = self.engine.encrypt(plaintext, key)
        decrypted = self.engine.decrypt(ciphertext, key)
        
        assert decrypted == plaintext
    
    def test_large_message(self):
        """Test encryption of large message."""
        key = self.engine.derive_key(b'large-test')
        plaintext = b'A' * 10000
        
        ciphertext = self.engine.encrypt(plaintext, key)
        decrypted = self.engine.decrypt(ciphertext, key)
        
        assert decrypted == plaintext


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
