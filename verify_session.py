import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from otpdoor.config import config
from otpdoor.auth import encrypt_session, decrypt_session
from datetime import datetime, timedelta, timezone

# 1. Test encryption and decryption
now = datetime.now(timezone.utc)
expires_at = now + timedelta(hours=24)
token = encrypt_session(expires_at)
print(f"Token: {token}")

decrypted_expires = decrypt_session(token)
print(f"Decrypted: {decrypted_expires}")
assert decrypted_expires.isoformat() == expires_at.isoformat()
print("Encryption/Decryption test passed!")

# 2. Test expiration check
past = now - timedelta(hours=1)
expired_token = encrypt_session(past)
decrypted_past = decrypt_session(expired_token)
assert decrypted_past < now
print("Expiration logic check (manual) passed!")

# 3. Test invalid secret (simulated by using a new Fernet instance)
from cryptography.fernet import Fernet
another_fernet = Fernet(Fernet.generate_key())
try:
    another_fernet.decrypt(token.encode())
    print("Security failure: another key decrypted the token!")
except Exception:
    print("Security check passed: invalid key cannot decrypt token.")
