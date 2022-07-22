"""auto gen

Revision ID: f51833172c9b
Revises: 1c33bb500c10
Create Date: 2022-07-22 21:23:42.979726

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f51833172c9b'
down_revision = '1c33bb500c10'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default='TRUE', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'published')
    # ### end Alembic commands ###