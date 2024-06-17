import asyncio
import logging
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException

from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from lib.models import User
from lib.schemas import UserSchema, ErrorResponseSchema, UserRegisterSchema
from lib.database import create_tables, drop_tables, get_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    # asyncio.create_task(drop_tables())
    asyncio.create_task(create_tables())
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get(
    "/users",
    responses={
        200: {"model": list[UserSchema], "description": "The users"},
    },
)
async def get_all_users(db: AsyncSession = Depends(get_db)):
    query = select(User)
    result = await db.execute(query)
    results = result.scalars().all()
    users = []

    for result in results:
        users.append(
            UserSchema(
                email=result.email,
                name=result.name,
                height=result.height,
                weight=result.weight,
                age=result.age,
            )
        )

    return users


@app.get(
    "/users/{user_id}",
    responses={
        200: {"model": UserSchema, "description": "The user"},
        404: {"model": ErrorResponseSchema, "description": "User not found"},
    },
)
async def get_a_user(user_id: int, db: AsyncSession = Depends(get_db)):
    query = select(User).where(User.id == user_id)
    result = await db.execute(query)
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserSchema(
        email=user.email,
        name=user.name,
        height=user.height,
        weight=user.weight,
        age=user.age,
    )


@app.post(
    "/users",
    responses={
        201: {"model": UserSchema, "description": "The user"},
        400: {"model": ErrorResponseSchema, "description": "Invalid request"},
    },
)
async def create_user(user: UserRegisterSchema, db: AsyncSession = Depends(get_db)):
    new_user = User(
        email=user.email,
        name=user.name,
        height=user.height,
        weight=user.weight,
        age=user.age,
        password=user.password,
    )
    db.add(new_user)
    await db.commit()
    return UserSchema(
        email=new_user.email,
        name=new_user.name,
        height=new_user.height,
        weight=new_user.weight,
        age=new_user.age,
    )
