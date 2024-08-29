from sqlalchemy import select
from core.db_helper import db_helper
from models.parcels import ParcelType


async def insert_initial_data():
    async with db_helper.session_factory() as session:
        parcel_types = ["одежда", "электроника", "разное"]
        query = select(ParcelType)
        result = await session.scalars(query)
        if not result.all():
            for pt in parcel_types:
                session.add(ParcelType(name=pt))
            await session.commit()
