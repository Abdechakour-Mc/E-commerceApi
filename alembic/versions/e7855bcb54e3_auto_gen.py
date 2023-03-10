"""auto-gen

Revision ID: e7855bcb54e3
Revises: 7f3740a5cbfc
Create Date: 2023-02-08 21:45:17.782684

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7855bcb54e3'
down_revision = '7f3740a5cbfc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
    # ### end Alembic commands ###
