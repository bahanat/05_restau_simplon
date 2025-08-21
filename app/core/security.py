from passlib.context import CryptContext

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(pwd: str) -> str:
    """
    Hash un mot de passe en utilisant l’algorithme défini dans `contexte_mdp`.

    Args:
        mdp (str): Le mot de passe en clair à hasher.

    Returns:
        str: Le mot de passe hashé sous forme de chaîne de caractères.
    """
    return str(password_context.hash(pwd))


def password_checking(pwd: str, hashed_pwd: str) -> bool:
    """
    Vérifie si un mot de passe correspond à un hash stocké.

    Args:
        mdp (str): Le mot de passe en clair saisi par l’utilisateur.
        mdp_hash (str): Le hash du mot de passe stocké en base.

    Returns:
        bool: True si le mot de passe correspond au hash, False sinon.
    """
    return bool(password_context.verify(pwd, hashed_pwd))
