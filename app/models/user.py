from datetime import datetime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from .base import Base
from .mixins.int_id_pk import IntIdPkMixin


class User(IntIdPkMixin, Base):
    username: Mapped[str] = mapped_column(unique=True)
    foo: Mapped[int]
    bar: Mapped[int]
    last_name: Mapped[str]
    first_name: Mapped[str]
    salary: Mapped[int]
    job_title: Mapped[str]
    hire_date: Mapped[datetime]
