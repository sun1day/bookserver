"""
@project: bookserver
@Name: add_user.py
@Auth: Rrsgdl
@Date: 2024/12/27-17:06
"""
from apps.db_models.user import User
from apps.dependencies import LocalSession

name = '测试账号'
password = 'test123'


def main():
    user = User()
    user.account = name
    user.password = password
    with LocalSession() as session:
        session.add(user)
        session.commit()


if __name__ == '__main__':
    main()
