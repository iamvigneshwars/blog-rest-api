"""add foreign key to post table

Revision ID: 65a258c799cf
Revises: 1c7ae18bc628
Create Date: 2022-07-22 21:06:41.383402

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65a258c799cf'
down_revision = '1c7ae18bc628'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable = False))
    op.create_foreign_key('post_fk', source_table='posts', referent_table='users',
    local_cols=['owner_id'], remote_cols=['id'] , ondelete='CASCADE')
    pass


def downgrade() -> None:
    op.drop_constraint('post_fk', table_name='posts')
    op.drop_constraint('posts', 'owner_id')
    pass
