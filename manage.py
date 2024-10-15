"""
@project: bookserver
@Name: manage.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:42
"""

from apps.app import create_app
from uvicorn import run




app = create_app()

if __name__ == '__main__':
    run('manage:app', reload=True)
