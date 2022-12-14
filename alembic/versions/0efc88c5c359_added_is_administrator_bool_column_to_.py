"""Added is_administrator -> bool column to the users model

Revision ID: 0efc88c5c359
Revises: cd3e357cc46c
Create Date: 2022-09-29 18:51:26.117530

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0efc88c5c359'
down_revision = 'cd3e357cc46c'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('is_administrator', sa.Boolean(), server_default='False', nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'is_administrator')
    # ### end Alembic commands ###
