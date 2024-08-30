"""empty message

Revision ID: e5e0c74a0ee4
Revises: 4d9d0ad605ec
Create Date: 2024-08-29 13:29:56.345441

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e5e0c74a0ee4"
down_revision: Union[str, None] = "4d9d0ad605ec"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "parcels", "cost_delivery", existing_type=sa.NUMERIC(), nullable=True
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "parcels", "cost_delivery", existing_type=sa.NUMERIC(), nullable=False
    )
    # ### end Alembic commands ###
