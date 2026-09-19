import hashlib
from logging import exception
import secrets
import base64
import hmac 

# Function to generate a password hash using PBKDF2 with SHA-256
 
    #now create function to verify password

def generate_password_hash(user_password: str, iterations: int = 200_000) -> str:
    try:
        salt = secrets.token_bytes(16)
        password_bytes = user_password.encode('utf-8')
        key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=32)
        salt_b64 = base64.urlsafe_b64encode(salt).decode('utf-8')
        key_b64 = base64.urlsafe_b64encode(key).decode('utf-8')
        return f"{iterations}${salt_b64}${key_b64}"
    except:
        print("An error occurred while generating the password hash.")
def verify_password_hash(stored_hash: str, user_password: str) -> bool:
    try:
        iterations_str, salt_b64, expected_key_b64 = stored_hash.split('$')
        iterations = int(iterations_str)
        salt = base64.urlsafe_b64decode(salt_b64.encode('utf-8'))
        expected_key = base64.urlsafe_b64decode(expected_key_b64.encode('utf-8'))
        password_bytes = user_password.encode('utf-8')
        key = hashlib.pbkdf2_hmac('sha256', password_bytes, salt, iterations, dklen=32)
        return hmac.compare_digest(key, expected_key)
    except exception as e:
        print("An error occurred while defining the functions.")
        return False
# simple example
user_password = "my_secure_password"
stored = generate_password_hash(user_password)
print(f"Stored password hash: {stored}")
is_valid = verify_password_hash(stored, user_password)
print(f"Password verification result: {is_valid}")
# THANKS :p
