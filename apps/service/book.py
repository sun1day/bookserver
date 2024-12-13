"""
@project: bookserver
@Name: book.py
@Auth: Rrsgdl
@Date: 2024/12/13-13:31
"""
import pathlib


class BookService:

    @classmethod
    def file_is_existed(cls, file_path: str) -> bool:
        return pathlib.Path(file_path).exists()
