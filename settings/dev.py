"""
@project: bookserver
@Name: dev.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:57
"""


class Settings:
    FilePath = 'D:\\project\\bookserver\\books\\'
    OpenDocsUrl = '/open/docs'
    OpenApiUrl = '/open/openapi.json'


def get_settings():
    return Settings