from fastapi import Request
from src.constants import LOGIN_EMAIL_REQ, LOGIN_PASS_REQ, MINIMUM_PASS_LENGTH

class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: list = []
        self.username: str = None
        self.password: str = None

    async def load_data(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")

    async def is_valid(self):
        if not self.username or not (self.username.__contains__("@")):
            self.errors.append(LOGIN_EMAIL_REQ)
        if not self.password or not len(self.password) >= MINIMUM_PASS_LENGTH:
            self.errors.append(LOGIN_PASS_REQ)
        if not self.errors:
            return True
        return False