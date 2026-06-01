"""add user address column

Revision ID: a1b2c3d4e5f6
Revises: 6f224a588011
Create Date: 2026-05-31 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a1b2c3d4e5f6'
down_revision = '6f224a588011'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('address', sa.String(length=100), nullable=True))


def downgrade():
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.drop_column('address')
