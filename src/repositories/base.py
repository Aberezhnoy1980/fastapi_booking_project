from sqlalchemy import select, insert, delete, update
from pydantic import BaseModel

from src.database import engine


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)

        return result.scalars().one_or_one()

    async def add(self, data: BaseModel):
        add_data_stmt = (
            insert(self.model)
            .values(**data.model_dump())
            .returning(self.model)
        )
        print(add_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_data_stmt)
        return result.scalars().one()

    async def edit(
            self, data: BaseModel,
            exclude_unset: bool = False,
            **filter_by
    ):
        update_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(**data.model_dump(exclude_unset=exclude_unset))
        )
        print(update_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(update_data_stmt)

    async def delete(self, **filter_by):
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        print(delete_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_data_stmt)
