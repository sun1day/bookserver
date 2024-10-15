"""
@project: bookserver
@Name: router.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:46
"""
from fastapi import FastAPI
from fastapi import APIRouter
from .book.view import book_router
from .user.view import user_router


def create_router():
    api_router = APIRouter(prefix='/api')
    api_router.include_router(book_router)
    api_router.include_router(user_router)
    return api_router
