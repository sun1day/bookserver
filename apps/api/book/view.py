"""
@project: bookserver
@Name: view.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:44
"""
import os
import uuid
from pathlib import Path

import aiofiles
from fastapi import APIRouter, UploadFile, Depends, Query

from apps.db_models.book import Books, UserRelateBooks
from apps.dependencies import get_settings, CurrentUserDep, SessionDep, login_required
from apps.lib.response import SuccessResponse
from apps.utils.util import sha256_hash

book_router = APIRouter(prefix='/book', dependencies=[Depends(login_required)])


@book_router.get('/books')
def books(
        current_user: CurrentUserDep,
        session: SessionDep,
        page_no: int = Query(default=1, ge=1),
        page_size: int = Query(default=10, ge=1, le=100)
):
    """获取自己的书籍"""
    query = session.query(UserRelateBooks) \
        .filter(UserRelateBooks.user_id == current_user.id) \
        .order_by(UserRelateBooks.id.desc())

    count = query.count()
    items = []
    if count:
        items = query.offset((page_no - 1) * page_size).limit(page_size).all()

    return SuccessResponse(data={'total': count, 'items': items})


@book_router.post('/books')
async def books(
        current_user: CurrentUserDep,
        book_file: UploadFile,
        session: SessionDep,
        settings=Depends(get_settings)
):
    """上传书籍"""
    tmp_name = uuid.uuid4()
    file = Path(f'{settings.FilePath}{os.path.sep}{tmp_name}')
    async with aiofiles.open(file, mode='wb') as f:
        while content := await book_file.read(1024 * 5):
            await f.write(content)

        # 指针指向文件头
        await f.seek(0)
        hash_value = b''
        while content := await f.read(1024 * 5):
            hash_value = sha256_hash(hash_value + content)

        hash_value = hash_value.decode()
        book = session.query(Books).filter_by(hash_value=hash_value).one_or_none()
        if not book:
            book = Books()
            book.hash_value = hash_value
            session.add(book)
            session.flush(book)
            user_rela_book = UserRelateBooks()
            user_rela_book.book_id = book.id
            user_rela_book.book_name = book_file.filename
            user_rela_book.user_id = current_user.id
            session.add(user_rela_book)
            session.commit()
            file.rename(hash_value)
        else:
            file.unlink(missing_ok=True)

    return SuccessResponse()
