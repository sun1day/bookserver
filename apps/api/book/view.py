"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:44
"""
from fastapi import APIRouter, UploadFile, Request
import aiofiles

book_router = APIRouter(prefix='/book')


@book_router.get('/books')
def books(page_no: int, page_size: int):
    return {}


@book_router.post('/books')
async def books(request: Request, book: UploadFile):
    name = book.filename
    print(f'D:\\project\\bookserver\\books\\{name}')
    async with aiofiles.open(f'D:\\project\\bookserver\\books\\{name}', mode='wb') as f:
        while content := await book.read(size=1024 * 10):  # 每次读取 1KB
            await f.write(content)
    return 'OK'
