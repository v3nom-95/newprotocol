from auth.security import create_token, decode_token
from datetime import timedelta


def test_token_roundtrip():
    token = create_token("user@qai.local", "user", "access", timedelta(minutes=10))
    payload = decode_token(token)
    assert payload["sub"] == "user@qai.local"
    assert payload["role"] == "user"
    assert payload["type"] == "access"
