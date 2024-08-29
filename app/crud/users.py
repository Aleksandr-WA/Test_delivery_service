from typing import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from models.parcels import Parcel
from schemas.user import UserCreate


async def get_all_users(
    session: AsyncSession,
) -> Sequence[Parcel]:
    stmt = select(Parcel).order_by(Parcel.id)
    result = await session.scalars(stmt)
    return result.all()


async def create_user(
    session: AsyncSession,
    user_create: UserCreate,
) -> Parcel:
    user = Parcel(**user_create.model_dump())
    session.add(user)
    await session.commit()
    # await session.refresh(user)
    return user
