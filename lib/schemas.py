import enum
from typing import Optional

from pydantic import BaseModel


class ErrorResponseSchema(BaseModel):
    detail: str


class UserLoginSchema(BaseModel):
    email: str
    password: str


class UserRegisterSchema(BaseModel):
    email: str
    password: str


class UserDataUpdateSchema(BaseModel):
    name: Optional[str] = None
    gender: Optional[str] = None
    height: Optional[int] = None
    weight: Optional[int] = None
    password: Optional[str] = None
    age: Optional[int] = None
    desired_weight: Optional[int] = None

    # Throws an error if any extra fields are present
    class Config:
        extra = "forbid"


class UserSchema(BaseModel):
    email: str
    age: int
    name: str
    height: int
    weight: int


class UserLoginResponseSchema(BaseModel):
    email: str
    access_token: str
    name: str


class UserRegisterResponseSchema(BaseModel):
    email: str
    access_token: str
    name: str
    message: str
