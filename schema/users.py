from typing import List, Union

from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    email: str
    password: str
    full_name: str = None ## Optional field for user's full name
    is_active: bool = True
    is_superuser: bool = False
    is_admin: bool = False

#response model
class UserSchema(UserBase):
    id: int
    full_name: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True


