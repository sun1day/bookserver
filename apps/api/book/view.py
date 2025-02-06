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
from fastapi.responses import FileResponse

from apps.api.book.models import DeleteBookModel
from apps.db_models.book import Books, UserRelateBooks
from apps.dependencies import get_settings, CurrentUserDep, SessionDep, login_required
from apps.lib.response import SuccessResponse, FailResponse
from apps.utils.util import sha256_hash

book_router = APIRouter(prefix='/book', dependencies=[Depends(login_required)])


@book_router.get('/')
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


@book_router.post('/')
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


@book_router.delete("/")
def delete_books(
        current_user: CurrentUserDep,
        delete_book_model: DeleteBookModel,
        session: SessionDep,
):
    """删除书籍"""
    relate = (
        session.query(UserRelateBooks)
        .filter_by(user_id=current_user.id, book_id=delete_book_model.book_id, status=1)
        .one_or_none()
    )
    if not relate:
        return SuccessResponse()

    relate.soft_delete()
    session.commit()
    return SuccessResponse()


"""下载书籍"""


@book_router.get('/download/{book_id}')
def download_books(current_user: CurrentUserDep, session: SessionDep, book_id: int, settings=Depends(get_settings)):
    books = (
        session.query(UserRelateBooks, Books)
        .join(Books, Books.id == UserRelateBooks.book_id)
        .filter(Books.id == book_id)
        .filter(UserRelateBooks.user_id == current_user.id, UserRelateBooks.status == 1)
        .first()
    )
    if not books:
        return FailResponse(error_msg='当前用户没有此书籍!')

    book: Books = books.Books
    relate: UserRelateBooks = books.UserRelateBooks
    file_path = Path(f'{settings.FilePath}{os.path.sep}{book.hash_value}')
    return FileResponse(file_path, filename=relate.book_name)
