"""Converted price from type int to type float in the products model

Revision ID: c2a904a30226
Revises: 0efc88c5c359
Create Date: 2022-09-29 19:32:59.270826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2a904a30226'
down_revision = '0efc88c5c359'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('title', sa.String(), nullable=False))
    op.add_column('products', sa.Column('quantity', sa.Integer(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('products', 'quantity')
    op.drop_column('products', 'title')
    # ### end Alembic commands ###
