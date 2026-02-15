from pydantic import BaseModel, EmailStr


class UserSingUp(BaseModel):
    email: EmailStr
    password: str

    first_name: str
    last_name: str
