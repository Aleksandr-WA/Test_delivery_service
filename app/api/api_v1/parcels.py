from typing import Annotated, Sequence

from fastapi import (
    APIRouter,
    Depends,
    Request,
    Response,
)
from sqlalchemy.ext.asyncio import AsyncSession

from core.db_helper import db_helper
from crud.parcels import (
    check_session_expiry,
    create_parcel,
    get_all_parcel_types,
    get_all_parcel_list,
    get_parcel_by_id,
)
from models.parcels import Parcel
from schemas.parcels import (
    ParcelCreate,
    ParcelType,
    ParcelReadParcelId,
    ParcelReadSessionId,
)

router = APIRouter()


@router.post("/registration")
async def register_parcel(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    parcel_create: ParcelCreate,
    request: Request,
    response: Response,
) -> int:
    session_id = await check_session_expiry(
        request=request,
        response=response,
        session=session,
    )

    parcel = await create_parcel(
        session=session,
        parcel_create=parcel_create,
        session_id=session_id,
    )

    def calculate_cost_delivery():
        # TODO: calculate cost delivery
        pass

    return parcel.id


@router.get("/parcels_types", response_model=list[ParcelType])
async def get_parcels_type(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
) -> Sequence[ParcelType]:
    parcels_types = await get_all_parcel_types(session=session)
    return parcels_types


# отфильтровать поля как надо
@router.get("/parcels_list", response_model=list[ParcelReadSessionId])
async def get_parcels_by_session_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    request: Request,
    skip: int = 0,
    limit: int = 10,
    type_id: int | None = None,
    cost_delivery: bool | None = None,
) -> Sequence[Parcel] | None:
    parcels_list = await get_all_parcel_list(
        session=session,
        request=request,
        skip=skip,
        limit=limit,
        type_id=type_id,
        cost_delivery=cost_delivery,
    )
    return parcels_list


@router.get("/{parcel_id}", response_model=list[ParcelReadParcelId])
async def get_parcels_by_parcel_id(
    session: Annotated[
        AsyncSession,
        Depends(db_helper.session_getter),
    ],
    parcel_id: int,
    request: Request,
) -> Sequence[Parcel] | None:
    parcels_list_id = await get_parcel_by_id(
        session=session, parcel_id=parcel_id, request=request
    )
    return parcels_list_id
