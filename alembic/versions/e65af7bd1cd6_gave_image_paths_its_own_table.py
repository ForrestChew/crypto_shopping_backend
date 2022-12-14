"""Gave image paths its own table

Revision ID: e65af7bd1cd6
Revises: e9f8e9f2b8aa
Create Date: 2022-10-13 12:50:43.063066

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e65af7bd1cd6'
down_revision = 'e9f8e9f2b8aa'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_image_paths',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('image_path', sa.String(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_column('products', 'image_path')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('products', sa.Column('image_path', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_table('product_image_paths')
    # ### end Alembic commands ###
