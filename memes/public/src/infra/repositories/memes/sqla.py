import uuid

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.memes import Meme
from domain.protocols.errors import MemeNotFoundError
from domain.protocols.meme_repository import IMemeRepository
from infra.db.models import MemeORM
from infra.mappers.meme.orm_mapper import MemeORMDomainMapper


class SQLAMemeRepository(IMemeRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def fetch_by_id(self, meme_id: uuid.UUID) -> Meme:
        query = sa.select(MemeORM).where(MemeORM.id == meme_id)
        result = (await self.session.execute(query)).scalar_one_or_none()
        if result is None:
            raise MemeNotFoundError(meme_id=meme_id)
        return MemeORMDomainMapper.from_orm(result)

    async def fetch_list(self, limit: int, offset: int) -> list[Meme]:
        query = sa.select(MemeORM).limit(limit).offset(offset)
        result = (await self.session.execute(query)).scalars().all()
        return [MemeORMDomainMapper.from_orm(res) for res in result]

    async def add(self, meme: Meme) -> uuid.UUID:
        orm = MemeORMDomainMapper.to_orm(meme)
        self.session.add(orm)
        await self.session.flush()
        await self.session.refresh(orm)
        return orm.id

    async def update(self, meme_id: uuid.UUID, image_url: str, text: str) -> Meme:
        query = sa.select(MemeORM).where(MemeORM.id == meme_id)
        found_meme = (await self.session.execute(query)).scalar_one_or_none()
        if not found_meme:
            raise MemeNotFoundError(meme_id=meme_id)
        found_meme.image_url = image_url
        found_meme.text = text
        await self.session.flush()
        await self.session.refresh(found_meme)
        return MemeORMDomainMapper.from_orm(found_meme)

    async def delete(self, meme_id: uuid.UUID) -> None:
        query = sa.select(MemeORM).where(MemeORM.id == meme_id)
        found_meme = (await self.session.execute(query)).scalar_one_or_none()
        if not found_meme or found_meme.deleted:
            raise MemeNotFoundError(meme_id=meme_id)
        found_meme.deleted = True
        await self.session.flush()
        await self.session.refresh(found_meme)
