from sqlalchemy import insert, select, delete

from src.database import engine
from src.exceptions.exc import NoResultFound
from src.repositories.base import BaseRepository
from src.models.rooms import RoomsOrm
from src.schemas.rooms import Room


class RoomsRepository(BaseRepository):
    model = RoomsOrm
    schema = Room

    # async def get_all(self, hotel_id):
    #     query = select(self.model).filter_by(hotel_id=hotel_id)
    #     print(query.compile(engine, compile_kwargs={"literal_binds": True}))
    #     result = await self.session.execute(query)
    #
    #     return [self.schema.model_validate(model, from_attributes=True) for model in result.scalars().all()]

    async def delete(self, **filter_by):
        try:
            await self.get_one_or_none(**filter_by)
        except NoResultFound:
            raise
        delete_data_stmt = delete(self.model).filter_by(**filter_by)
        print(delete_data_stmt.compile(engine, compile_kwargs={"literal_binds": True}))
        await self.session.execute(delete_data_stmt)
