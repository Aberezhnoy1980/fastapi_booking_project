from sqlalchemy import select, insert

from src.database import engine


class BaseRepository:
    model = None

    def __init__(self, session):
        self.session = session

    async def get_all(self, *args, **kwargs):
        query = select(self.model)
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(self, **filters):
        query = select(self.model).filter_by(**filters)
        result = await self.session.execute(query)

        return result.scalars().one_or_one()

    async def add(self, data):
        add_hotel_stmt = insert(self.model).values(**data).returning(self.model)
        print(add_hotel_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(add_hotel_stmt)
        inserted_hotel = result.fetchone()[0]
        return inserted_hotel
