"""Corrected rating  column in prodeucts table by removing null constraint. The default value will ensure there is a value

Revision ID: 6588ed0b7e78
Revises: 3ea9fd72bca8
Create Date: 2022-09-28 15:47:11.894963

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6588ed0b7e78'
down_revision = '3ea9fd72bca8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'rating',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('products', 'rating',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
