"""RE

Revision ID: 8fc7faa03ba4
Revises: ddbebe056175
Create Date: 2022-10-14 15:39:50.185372

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fc7faa03ba4'
down_revision = 'ddbebe056175'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_image_paths_product_id_fkey', 'product_image_paths', type_='foreignkey')
    op.drop_column('product_image_paths', 'product_id')
    op.add_column('products', sa.Column('image_path_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'products', 'product_image_paths', ['image_path_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='foreignkey')
    op.drop_column('products', 'image_path_id')
    op.add_column('product_image_paths', sa.Column('product_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.create_foreign_key('product_image_paths_product_id_fkey', 'product_image_paths', 'products', ['product_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###
