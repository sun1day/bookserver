"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:44
"""
from fastapi import APIRouter

book_router = APIRouter(prefix='/book')


@book_router.get('/books')
def books(page_no: int, page_size: int):
    return {}
