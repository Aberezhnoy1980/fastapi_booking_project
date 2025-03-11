from sqlalchemy import select, func, and_

from src.database import engine
from src.repositories.base import BaseRepository
from src.models.hotels import HotelsOrm


class HotelsRepository(BaseRepository):
    model = HotelsOrm

    async def get_all(
            self,
            location,
            title,
            limit,
            offset,
    ):
        query = select(HotelsOrm)
        filters = []
        if location:
            filters.append(HotelsOrm.location.icontains(location.strip().lower()))
        if title:
            filters.append(func.lower(HotelsOrm.title).contains(title.strip().lower()))
        if filters:
            query = query.filter(and_(*filters))
        query = (
            query
            .limit(limit)
            .offset(offset)
        )
        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)

        return result.scalars().all()

    async def get_one_or_none(
            self,
            id: int | None,
            title: str | None = None,
            location: str | None = None,
    ):
        query = select(HotelsOrm)
        filters = []
        if id is not None:
            query = query.filter_by(id=id)
        if location:
            filters.append(HotelsOrm.location.icontains(location.strip().lower()))
        if title:
            filters.append(HotelsOrm.title.icontains(title.strip().lower()))
        if filters:
            query = query.filter(and_(*filters))

        print(query.compile(engine, compile_kwargs={"literal_binds": True}))
        result = await self.session.execute(query)
        return result.scalars().one_or_none()
