"""empty message

Revision ID: 08ee08533b97
Revises: 
Create Date: 2024-09-05 20:48:22.731320

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "08ee08533b97"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "parcel_types",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcel_types")),
        sa.UniqueConstraint("name", name=op.f("uq_parcel_types_name")),
    )
    op.create_table(
        "sessions",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_sessions")),
        sa.UniqueConstraint("name", name=op.f("uq_sessions_name")),
    )
    op.create_table(
        "parcels",
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("weight", sa.Numeric(), nullable=False),
        sa.Column("type_id", sa.Integer(), nullable=False),
        sa.Column("cost_content", sa.Numeric(), nullable=False),
        sa.Column(
            "cost_delivery", sa.Numeric(), server_default="0.0", nullable=True
        ),
        sa.Column("session_id", sa.Integer(), nullable=False),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["session_id"],
            ["sessions.id"],
            name=op.f("fk_parcels_session_id_sessions"),
        ),
        sa.ForeignKeyConstraint(
            ["type_id"],
            ["parcel_types.id"],
            name=op.f("fk_parcels_type_id_parcel_types"),
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_parcels")),
    )
    op.create_index(
        op.f("ix_parcels_session_id"), "parcels", ["session_id"], unique=False
    )
    op.create_index(
        op.f("ix_parcels_type_id"), "parcels", ["type_id"], unique=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_parcels_type_id"), table_name="parcels")
    op.drop_index(op.f("ix_parcels_session_id"), table_name="parcels")
    op.drop_table("parcels")
    op.drop_table("sessions")
    op.drop_table("parcel_types")
    # ### end Alembic commands ###
