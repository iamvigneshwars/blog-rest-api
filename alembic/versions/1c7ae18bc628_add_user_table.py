"""add user table

Revision ID: 1c7ae18bc628
Revises: 7c32bb67d1bd
Create Date: 2022-07-22 20:57:06.288298

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1c7ae18bc628'
down_revision = '7c32bb67d1bd'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable = False),
        sa.PrimaryKeyConstraint('id'), 
        sa.UniqueConstraint('email')
    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
