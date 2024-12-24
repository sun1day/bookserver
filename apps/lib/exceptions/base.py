"""
@project: bookserver
@Name: base.py
@Auth: Rrsgdl
@Date: 2024/12/24-17:46
"""


class ServiceBaseException(Exception):
    code = 5000
    msg = "Server Error"

    def __init__(self, code=None, msg=None):
        if code:
            self.code = code
        if msg:
            self.msg = msg
        super().__init__(self.code, self.msg)

    def __repr__(self):
        return f"<{type(self).__name__}: {self.code}: {self.msg}>"
