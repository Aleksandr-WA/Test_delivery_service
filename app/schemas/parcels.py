from decimal import Decimal
from pydantic import BaseModel, Field


class ParcelType(BaseModel):
    id: int
    name: str = Field(max_length=255)


class ParcelBase(BaseModel):
    name: str = Field(max_length=255)
    weight: Decimal
    cost_content: Decimal


class ParcelCreate(ParcelBase):
    type_id: int = Field(ge=1, le=3)


class ParcelRead(ParcelCreate):
    id: int
    type: ParcelType
    coast_delivery: Decimal | None
