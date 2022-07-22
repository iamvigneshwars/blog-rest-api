"""add content column

Revision ID: 7c32bb67d1bd
Revises: 3c13ced9b818
Create Date: 2022-07-22 20:52:28.445460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7c32bb67d1bd'
down_revision = '3c13ced9b818'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
