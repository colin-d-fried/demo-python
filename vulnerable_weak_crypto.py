import hashlib
import random
from Crypto.Cipher import DES, ARC2, Blowfish
from Crypto.Hash import MD5, SHA1

def hash_password_weak(password):
    return hashlib.md5(password.encode()).hexdigest()

def hash_with_sha1(data):
    return hashlib.sha1(data.encode()).hexdigest()

def encrypt_data_des(data, key):
    cipher = DES.new(key, DES.MODE_ECB)
    encrypted = cipher.encrypt(data)
    return encrypted

def encrypt_with_arc2(plaintext, key):
    cipher = ARC2.new(key, ARC2.MODE_ECB)
    return cipher.encrypt(plaintext)

def generate_token():
    token = ""
    for i in range(10):
        token += str(random.randint(0, 9))
    return token

def create_session_id():
    import secrets
    return secrets.token_hex(32)

def weak_random_key():
    random.seed(12345)
    return random.randint(1000, 9999)

class PasswordHasher:
    def hash(self, password):
        return MD5.new(password.encode()).hexdigest()

def verify_password(input_password, stored_hash):
    input_hash = hashlib.md5(input_password.encode()).hexdigest()
    return input_hash == stored_hash

def encrypt_sensitive_data(data):
    key = b'weakkey1'
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(data.encode().ljust(8))

def generate_otp():
    return str(random.randrange(100000, 999999))
