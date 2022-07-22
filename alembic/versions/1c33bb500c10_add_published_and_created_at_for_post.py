"""add published and created at for post

Revision ID: 1c33bb500c10
Revises: 65a258c799cf
Create Date: 2022-07-22 21:11:36.186600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c33bb500c10'
down_revision = '65a258c799cf'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.add_column('posts', sa.Column(
    #     'published', sa.Boolean(), nullable = False, server_default = True),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable = False, server_default = sa.text("NOW()")),)
    pass


def downgrade() -> None:
    # op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
