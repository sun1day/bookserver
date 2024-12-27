"""
@project: bookserver
@Name: util.py
@Auth: Rrsgdl
@Date: 2024/12/20-16:00
"""
import functools
import re
import hashlib


def hump2underline(name):
    """驼峰命名转化为蛇形"""
    # 使用正则表达式将大写字母前加上下划线，并将字母转换为小写
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)  # 小写字母或数字后跟大写字母
    return name.lower()  # 将整个字符串转换为小写


def not_protect(f):
    f._need_login = False
    return f


def sha256_hash(content: str | bytes) -> str:
    if isinstance(content, str):
        content = content.encode()
    return hashlib.sha256(content).hexdigest()


if __name__ == "__main__":
    res = sha256_hash("aaaa")
    print()
