

from pydantic import BaseModel
from typing import Optional


class UserCreate(BaseModel):
    username: str
    password: str
    role: str = "user"
    email: str  # now required


class LoginSchema(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str





# -------------------- CREATE --------------------
class StudentCreate(BaseModel):
    name: str
    email: str
    age: Optional[int] = None
    grade: Optional[str] = None

# -------------------- OUTPUT --------------------
class StudentOut(BaseModel):
    id: int
    name: str
    email: str
    age: Optional[int] = None
    grade: Optional[str] = None

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }

# -------------------- UPDATE --------------------
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    grade: Optional[str] = None




class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None  # Optional, if you store user role in the token