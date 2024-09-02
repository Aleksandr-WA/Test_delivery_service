import uuid
from decimal import Decimal
from tkinter.constants import ROUND
from typing import Sequence

from fastapi import Request, Response
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models.parcels import Parcel, Session, ParcelType
from schemas.parcels import ParcelCreate
from utils.get_dollar_rate import get_dollar_rate


async def create_parcel(
    session: AsyncSession,
    parcel_create: ParcelCreate,
    session_id: int,
) -> Parcel:
    parcel = Parcel(
        **parcel_create.model_dump(),
        session_id=session_id,
    )
    session.add(parcel)
    await session.commit()
    return parcel


async def check_session_expiry(
    request: Request,
    response: Response,
    session: AsyncSession,
) -> int:
    session_object = await get_session_id(
        session=session,
        request=request,
    )

    if session_object:
        return session_object

    session_id = str(uuid.uuid4())
    response.set_cookie(key="session_id", value=session_id)
    stmt = Session(name=session_id)
    session.add(stmt)
    await session.commit()
    return stmt.id


async def get_session_id(
    session: AsyncSession,
    request: Request,
) -> int:
    session_id = request.cookies.get("session_id")
    query = select(Session).filter(Session.name == session_id)
    result = await session.execute(query)
    session_object = result.scalars().first()
    return session_object.id if session_object else None


async def get_all_parcel_types(
    session: AsyncSession,
) -> Sequence[ParcelType]:
    query = select(ParcelType).order_by(ParcelType.id)
    result = await session.execute(query)
    return result.scalars().all()


async def get_all_parcel_list(
    session: AsyncSession,
    request: Request,
    skip: int,
    limit: int,
    type_id: int | None,
    cost_delivery: bool | None,
) -> Sequence[Parcel]:
    session_id = await get_session_id(
        session=session,
        request=request,
    )

    query = (
        select(Parcel)
        .options(joinedload(Parcel.type))
        .filter(
            Parcel.session_id == session_id,
            Parcel.type_id == type_id if type_id else True,
            Parcel.cost_delivery.isnot(None) if cost_delivery else True,
        )
        .offset(skip)
        .limit(limit)
    )

    result = await session.execute(query)
    parcels_list = result.scalars().all()
    return parcels_list


async def get_parcel_by_id(
    session: AsyncSession,
    parcel_id: int,
    request: Request,
) -> Sequence[Parcel] | None:
    session_id = await get_session_id(
        session=session,
        request=request,
    )
    query = select(Parcel).filter(
        Parcel.id == parcel_id, Parcel.session_id == session_id
    )
    result = await session.execute(query)
    parcels_list_id = result.scalars().all()
    return parcels_list_id


async def calculate_cost_delivery(
    session: AsyncSession,
    parcel: Parcel,
):
    dollars_rate = await get_dollar_rate()

    cost_delivery = round(
        (
            (Decimal("0.5") * parcel.weight + parcel.cost_content * Decimal("0.01"))
            * dollars_rate
        ),
        2,
    )

    stmt = (
        update(Parcel)
        .filter(Parcel.id == parcel.id)
        .values(cost_delivery=cost_delivery)
    )
    await session.execute(stmt)
    await session.commit()
