"""
@project: bookserver
@Name: security.py
@Auth: Rrsgdl
@Date: 2024/12/24-17:28
"""
import time

import jwt
import typing as t
from apps.lib.exceptions.exception import InvalidTokenException


class Security:
    ALGORITHM = "HS256"

    @classmethod
    def create_token(
            cls, secret: str, payload: dict["str", t.Any], expire=60 * 60 * 24
    ) -> str:
        """创建token"""
        _payload = {"payload": payload, "exp": int(time.time()) + expire}
        return jwt.encode(_payload, secret, algorithm=cls.ALGORITHM)

    @classmethod
    def decode(cls, secret: str, token: str) -> dict[str, t.Any]:
        try:
            return jwt.decode(token, secret)['payload']
        except Exception:
            raise InvalidTokenException()
