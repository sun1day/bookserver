"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:44
"""
from fastapi import APIRouter, UploadFile, Request, Depends
from fastapi.responses import ORJSONResponse
import aiofiles
from apps.dependencies import get_settings
import os
from apps.service.book import BookService

book_router = APIRouter(prefix='/book')


@book_router.get('/books')
def books(page_no: int, page_size: int):
    return {}


@book_router.post('/books')
async def books(book: UploadFile, settings: Depends(get_settings)) -> ORJSONResponse:
    name = book.filename
    file_path = f'{settings.FilePath}{os.path.sep}{name}'
    if BookService.file_is_existed(file_path):
        return ORJSONResponse(content={'data': {}, 'error_msg': '文件已上传成功', 'code': 1})
    async with aiofiles.open(f'{settings.FilePath}{os.path.sep}{name}', mode='wb') as f:
        while content := await book.read(size=1024 * 10):  # 每次读取 1KB
            await f.write(content)
    return ORJSONResponse(content={'data': {}, 'error_msg': '文件已上传成功', 'code': 1})
