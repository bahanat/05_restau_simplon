from passlib.context import CryptContext

# Logique de hashing des mots de passe
contexte_mdp = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_mdp(mdp: str) -> str:
    return str(contexte_mdp.hash(mdp))


def verification_mdp(mdp: str, mdp_hash: str) -> bool:
    return bool(contexte_mdp.verify(mdp, mdp_hash))
