from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from auth.security import decode_token


bearer_scheme = HTTPBearer(auto_error=False)


def get_current_actor(credentials: HTTPAuthorizationCredentials = Security(bearer_scheme)) -> dict:
    if credentials is None or not credentials.credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing bearer token")
    try:
        payload = decode_token(credentials.credentials)
    except Exception as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    return payload


def require_roles(*roles: str):
    def _role_checker(actor: dict = Depends(get_current_actor)) -> dict:
        if actor.get("role") not in roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Insufficient role")
        return actor

    return _role_checker
