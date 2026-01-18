#!/usr/bin/env python3
"""SCBE-AETHERMOORE Authorization Demo

Demonstrates the complete flow of creating and verifying
quantum-resistant authorization tokens using the Spiralverse system.
"""

import sys
sys.path.insert(0, '..')

from src.spiralverse_integration import SpiralverseSystem, ConsensusValidator
from src.scbe_engine import SCBEEngine
from src.aethermoore_geometry import HyperbolicSpace
from src.lws_core import LWSEngine


def demo_basic_auth():
    """Basic authorization token creation and verification."""
    print('=' * 60)
    print('SPIRALVERSE-AETHERMOORE Authorization Demo')
    print('=' * 60)
    
    # Initialize the system
    master_key = b'demo-master-key-spiralverse-2024'
    system = SpiralverseSystem(master_key)
    
    print(f'\nSystem Version: {system.VERSION}')
    print(f'Protocol: {system.PROTOCOL_ID}')
    
    # Create an authorization token
    print('\n--- Creating Authorization Token ---')
    payload = {
        'user_id': 'user123',
        'action': 'access',
        'resource': 'quantum-vault',
        'permissions': ['read', 'write'],
        'timestamp': '2024-01-15T10:30:00Z'
    }
    
    token = system.create_authorization(
        subject='demo-user@spiralverse.io',
        payload=payload,
        passphrase='sacred-quantum-demo'
    )
    
    print(f'Token ID: {token.token_id}')
    print(f'Subject: {token.subject}')
    print(f'Timestamp: {token.timestamp}')
    print(f'Geometric Signature: {token.geometric_signature.hex()[:32]}...')
    print(f'Semantic Binding: {token.semantic_binding.hex()}')
    
    # Verify the token
    print('\n--- Verifying Authorization Token ---')
    is_valid, decrypted = system.verify_authorization(token, 'sacred-quantum-demo')
    
    if is_valid:
        print('Verification: SUCCESS')
        print(f'Decrypted Payload: {decrypted}')
    else:
        print('Verification: FAILED')
    
    # Test with wrong passphrase
    print('\n--- Testing Wrong Passphrase ---')
    is_valid, _ = system.verify_authorization(token, 'wrong-passphrase')
    print(f'Verification with wrong passphrase: {"FAILED" if not is_valid else "UNEXPECTED SUCCESS"}')
    
    # Export and import token
    print('\n--- Token Export/Import ---')
    exported = system.export_token(token)
    print(f'Exported token length: {len(exported)} characters')
    
    imported = system.import_token(exported)
    print(f'Import successful: {imported.token_id == token.token_id}')
    
    return token


def demo_consensus_validation(token):
    """Demonstrate consensus validation."""
    print('\n--- Consensus Validation ---')
    
    master_key = b'demo-master-key-spiralverse-2024'
    system = SpiralverseSystem(master_key)
    validator = ConsensusValidator(system, threshold=7)
    
    is_valid = validator.validate_trajectory(token)
    print(f'Trajectory validation: {"PASSED" if is_valid else "FAILED"}')


def demo_components():
    """Demonstrate individual components."""
    print('\n--- Individual Components Demo ---')
    
    # SCBE Engine
    print('\nSCBE Engine:')
    engine = SCBEEngine()
    key = engine.derive_key(b'test-password')
    print(f'  Key derivation: {key.hex()[:32]}...')
    
    message = b'Hello, Quantum World!'
    encrypted = engine.encrypt(message, key)
    decrypted = engine.decrypt(encrypted, key)
    print(f'  Encryption/Decryption: {decrypted == message}')
    
    # Hyperbolic Space
    print('\nHyperbolic Space:')
    space = HyperbolicSpace(key)
    point = space.encode_point(b'test-data')
    print(f'  Encoded point: r={point.radius:.4f}')
    
    trajectory = space.traverse_layers(point)
    print(f'  Trajectory length: {len(trajectory)} layers')
    
    # LWS Engine
    print('\nLWS Engine:')
    lws = LWSEngine()
    gematria = lws.compute_gematria('AetherMoore')
    print(f'  Gematria("AetherMoore"): {gematria}')
    
    sacred = lws.sacred_hash('quantum-sacred')
    print(f'  Sacred hash: {sacred.hex()[:32]}...')


if __name__ == '__main__':
    token = demo_basic_auth()
    demo_consensus_validation(token)
    demo_components()
    print('\n' + '=' * 60)
    print('Demo completed successfully!')
    print('=' * 60)
