"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:33
"""

from fastapi import APIRouter
from fastapi import applications

user_router = APIRouter(prefix='/user')



@user_router.get('/login')
def login(username: str, password: str):
    return {'username': username, 'password': password}
