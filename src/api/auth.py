from fastapi import APIRouter, Body

from passlib.context import CryptContext

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from templates.openapi_examples import user_examples

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    description="<h2>Добавляет запись в базу данных если пользователь не существует</h2>")
async def register_user(
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    hashed_password = pwd_context.hash(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        await UsersRepository(session).add(new_user_data)
        await session.commit()

    return {"status": "OK"}
