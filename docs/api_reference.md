# API Reference

## SpiralverseSystem

Main entry point for the Spiralverse-AetherMoore system.

### Constructor

```python
SpiralverseSystem(master_key: bytes)
```

**Parameters:**
- `master_key`: Primary key for system initialization (32+ bytes recommended)

### Methods

#### create_authorization

```python
def create_authorization(
    subject: str,
    payload: Dict[str, Any],
    passphrase: str
) -> AuthorizationToken
```

Creates a quantum-resistant authorization token.

**Parameters:**
- `subject`: Token subject identifier
- `payload`: Data to encrypt in token
- `passphrase`: User passphrase for semantic binding

**Returns:** `AuthorizationToken` object

#### verify_authorization

```python
def verify_authorization(
    token: AuthorizationToken,
    passphrase: str
) -> Tuple[bool, Optional[Dict[str, Any]]]
```

**Returns:** Tuple of (is_valid, decrypted_payload)

---

## SCBEEngine

Core encryption engine.

### Methods

#### encrypt

```python
def encrypt(plaintext: bytes, key: bytes) -> bytes
```

#### decrypt

```python
def decrypt(ciphertext: bytes, key: bytes) -> bytes
```

#### derive_key

```python
def derive_key(password: bytes, salt: bytes = None) -> bytes
```

---

## HyperbolicSpace

13-layer hyperbolic security space.

### Constructor

```python
HyperbolicSpace(master_key: bytes)
```

### Methods

#### encode_point

```python
def encode_point(data: bytes) -> HyperbolicPoint
```

#### traverse_layers

```python
def traverse_layers(point: HyperbolicPoint) -> List[HyperbolicPoint]
```

#### compute_security_hash

```python
def compute_security_hash(data: bytes) -> bytes
```

---

## LWSEngine

Langues Weighting System engine.

### Methods

#### compute_gematria

```python
def compute_gematria(text: str) -> int
```

#### tokenize

```python
def tokenize(text: str) -> List[LWSToken]
```

#### sacred_hash

```python
def sacred_hash(text: str) -> bytes
```
