from passlib.context import CryptContext


_pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    return _pwd_context.hash(password)


def verify(plaintext: str, hashed_password):
    return _pwd_context.verify(plaintext, hashed_password)
