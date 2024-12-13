"""
@project: bookserver
@Name: dependencies.py
@Auth: Rrsgdl
@Date: 2024/10/15-14:18
"""

# dependencies
import functools
from settings import settings
from typing import Type


@functools.lru_cache
def get_settings():
    return settings.Settings
