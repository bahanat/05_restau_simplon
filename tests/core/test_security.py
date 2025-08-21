from app.core.security import hash_password, password_checking


def test_hash_and_password_checking_ok() -> None:
    """Teste le hashage et la vérification correcte d'un mot de passe.

    - Vérifie que le mot de passe hashé n'est pas identique au mot de passe brut.
    - Vérifie que la fonction password_checking retourne True pour le bon mot de
      passe.
    """
    password = "passwordok123456"
    hashed = hash_password(password)
    assert hashed != password
    assert password_checking(password, hashed) is True


def test_failed_password_checking() -> None:
    """Teste la vérification d'un mot de passe incorrect.

    - Vérifie que password_checking retourne False si le mot de passe fourni est
      incorrect par rapport au hash.
    """
    password = "passwordok123456"
    other = "password-not-ok"
    hashed = hash_password(password)
    assert password_checking(other, hashed) is False
