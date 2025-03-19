from fastapi import APIRouter, Body, HTTPException, Response
from sqlalchemy.exc import IntegrityError

from src.api.dependencies import UserIdDep, DBDep
from src.schemas.users import UserRequestAdd, UserAdd
from src.services.auth import AuthService
from templates.openapi_examples import user_examples

router = APIRouter(prefix="/auth", tags=["Авторизация и аутентификация"])


@router.post(
    "/register",
    summary="Регистрация нового пользователя",
    description="<h2>Добавляет запись в базу данных если пользователь не существует</h2>"
)
async def register_user(
        db: DBDep,
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    hashed_password = AuthService().hash_password(data.password)
    new_user_data = UserAdd(email=data.email, hashed_password=hashed_password)

    try:
        await db.users.add(new_user_data)
        await db.commit()
    except IntegrityError:
        return {"status": "email already exists"}

    return {"status": "OK"}


@router.post(
    "/login",
    summary="Вход пользователя в систему",
    description="Сверяет переданные пользователем логин и пароль с  базой данных"
)
async def login_user(
        db: DBDep,
        response: Response,
        data: UserRequestAdd = Body(openapi_examples=user_examples),
):
    user = await db.users.get_user_with_hashed_password(email=data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Пользователь с таким email не зарегистрирован")
    if not AuthService().verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Пароль неверный")
    access_token = AuthService().create_access_token({"user_id": user.id})
    response.set_cookie("access_token", access_token)
    return {"access_token": access_token}


@router.post("/logout")
async def logout(
        response: Response
):
    response.delete_cookie("access_token")
    return {"status": "OK"}


@router.get(
    "/me",
    summary="Получение данных текущего пользователя",
    description="Возвращает данные текущего пользователя")
async def get_me(
        db: DBDep,
        user_id: UserIdDep,
):
    user = await db.users.get_one_or_none(id=user_id)
    return {"user": user}
