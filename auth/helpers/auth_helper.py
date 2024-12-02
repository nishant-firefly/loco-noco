# Utility functions for Auth Module
import hashlib
import jwt

class AuthHelper:
    SECRET_KEY = "your_secret_key"

    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode()).hexdigest()

    @staticmethod
    def generate_token(data):
        return jwt.encode(data, AuthHelper.SECRET_KEY, algorithm="HS256")
