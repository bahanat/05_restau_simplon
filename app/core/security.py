from passlib.context import CryptContext

# creation contexte - hashage avec bcrypt

mdp_contexte = CryptContext(schemes=["bcrypt"], deprecated="auto")

# fonction hashing


def hash_mot_de_passe(mot_de_passe: str) -> str:
    return mdp_contexte.hash(mot_de_passe)


def verification_mot_de_passe(mot_de_passe_donne: str, mot_de_passe_hash: str) -> bool:
    return mdp_contexte.verify(mot_de_passe_donne, mot_de_passe_hash)
