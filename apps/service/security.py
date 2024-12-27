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
    def decode(cls, secret: bytes, token: str) -> dict[str, t.Any]:
        try:
            return jwt.decode(token, secret, algorithms=cls.ALGORITHM)['payload']
        except Exception:
            raise InvalidTokenException()


if __name__ == '__main__':
    token1 = """eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwYXlsb2FkIjp7ImlkIjoxLCJhY2NvdW50IjoiXHU2ZDRiXHU4YmQ1XHU4ZDI2XHU1M2Y3IiwidGltZXN0YW1wIjoxNzM1MjkwODczfSwiZXhwIjoxNzM1Mzc3MjczfQ.h4PFP_JeZEhkVzHhrO6vJWPbrag_x800M9YXKsnhH9s"""
    res = Security.decode(b"\xd7\xcd\xb2\xa7\xcb\x85\x8a\xe9/7'B\xe4X\xa2\x02", token1)
    print(res)