"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:44
"""
from fastapi import APIRouter, UploadFile, Request, Depends, Query
from fastapi.responses import ORJSONResponse
import aiofiles
from apps.dependencies import get_settings, CurrentUserDep, SessionDep
import os
from apps.service.book import BookService
from apps.db_models.book import Books, UserRelateBooks
from apps.db_models.user import User
from apps.lib.response import SuccessResponse

book_router = APIRouter(prefix='/book')


@book_router.get('/books')
def books(
        current_user: CurrentUserDep,
        session: SessionDep,
        page_no: int = Query(..., default=1, ge=1),
        page_size: int = Query(..., default=10, ge=1, le=100)
):
    query = session.query(Books).join(UserRelateBooks, Books.id == UserRelateBooks.book_id).filter(
        UserRelateBooks.user_id == current_user.id).order_by(Books.id.desc())

    count = query.count()
    items = []
    if count:
        items = query.offset((page_no - 1) * page_size).limit(page_size).all()

    return SuccessResponse(data={'total': count, 'items': items})


@book_router.post('/books')
async def books(book: UploadFile, settings=Depends(get_settings)) -> ORJSONResponse:
    name = book.filename
    file_path = f'{settings.FilePath}{os.path.sep}{name}'
    if BookService.file_is_existed(file_path):
        return ORJSONResponse(content={'data': {}, 'error_msg': '文件已上传成功', 'code': 1})
    async with aiofiles.open(f'{settings.FilePath}{os.path.sep}{name}', mode='wb') as f:
        while content := await book.read(size=1024 * 10):  # 每次读取 1KB
            await f.write(content)
    return ORJSONResponse(content={'data': {}, 'error_msg': '文件已上传成功', 'code': 1})
