from app.core.security import hash_mdp, verification_mdp


def test_hash_and_verify_password_ok():
    password = "passwordok123456"
    hashed = hash_mdp(password)
    assert hashed != password
    assert verification_mdp(password, hashed) is True


def test_verify_password_fail():
    password = "passwordok123456"
    other = "password-not-ok"
    hashed = hash_mdp(password)
    assert verification_mdp(other, hashed) is False
