import hashlib
import secrets
import base64
import hmac

# Function to generate a password hash using PBKDF2 with SHA-256

def generate_password_hash(password: str, iterations: int = 200_000) -> str:
    salt = secrets.token_bytes(16)
    password_bytes = password.encode('utf-8')
    key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=32)
    salt_b64 = base64.urlsafe_b64encode(salt).decode('utf-8')
    key_b64 = base64.urlsafe_b64encode(key).decode('utf-8')
    return f"{iterations}${salt_b64}${key_b64}"

#now create function to verify password hash

def verify_password_hash(stored_hash: str, password: str) -> bool:
    try:
        iterations_str, salt_b64, expected_key_b64 = stored_hash.split('$')
        iterations = int(iterations_str)
        salt = base64.urlsafe_b64decode(salt_b64.encode('utf-8'))
        expected_key = base64.urlsafe_b64decode(expected_key_b64.encode('utf-8'))

# we then compute the hash of the provided password using the same salt and iterations, and compare it to the expected key.

        password_bytes = password.encode('utf-8')
        key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=32)
        return hmac.compare_digest(key, expected_key)
    except Exception as e:
        print(f"Error verifying password hash: {e}")
        return False

# simpl example
password = "my_secure_password"
stored = generate_password_hash(password)
print(f"Stored password hash: {stored}")
is_valid = verify_password_hash(stored, password)
print(f"Password verification result: {is_valid}")
# THANKS :p