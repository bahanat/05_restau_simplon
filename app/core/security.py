from passlib.context import CryptContext

# creation contexte - hashage avec bcrypt

mdp_contexte = CryptContext(schemes=["bcrypt"], deprecated="auto")

# fonction hashing


def hash_password(password: str) -> str:
    return mdp_contexte.hash(password)


def verification_password(password_given: str, password_hash: str) -> bool:
    return mdp_contexte.verify(password_given, password_hash)
