"""
@project: bookserver
@Name: book.py
@Auth: Rrsgdl
@Date: 2024/12/13-13:31
"""
import os
import pathlib

import aiofiles
from fastapi import UploadFile
import hashlib

from apps.db_models.book import Books
from apps.db_models.user import User


class BookService:

    @classmethod
    def file_is_existed(cls, file_path: str) -> bool:
        return pathlib.Path(file_path).exists()
