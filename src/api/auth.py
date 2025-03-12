from fastapi import APIRouter, Body, HTTPException, Response, Request
from sqlalchemy.exc import IntegrityError

from src.database import async_session_maker
from src.repositories.users import UsersRepository
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from templates.openapi_examples import user_examples

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    description="<h2>Добавляет запись в базу данных если пользователь не существует</h2>")
async def register_user(
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)
    async with async_session_maker() as session:
        try:
            await UsersRepository(session).add(new_user_data)
            await session.commit()
        except IntegrityError:
            return {"status": "email already exists"}

    return {"status": "OK"}


@router.post(
    "/login",
    summary="Вход пользователя в систему",
    description="Сверяет переданные пользователем логин и пароль с  базой данных"
)
async def login_user(
        response: Response,
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    async with async_session_maker() as session:
        user = await UsersRepository(session).get_user_with_hashed_password(email=data.email)
        if not user:
            raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
        if not AuthService().verify_password(data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Пароль неверный")
        access_token = AuthService().create_access_token({"user_id": user.id})
        response.set_cookie("access_token", access_token)
        return {"access_token": access_token}


@router.get("/only_auth")
async def only_auth(
        request: Request,
):
    access_token = request.cookies.get("access_token") or None
    return {"access_token": access_token} if access_token else {"status": "user not authorized"}
