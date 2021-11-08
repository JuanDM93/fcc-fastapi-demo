"""create users table

Revision ID: bce514e0541f
Revises: 2baa6aed2473
Create Date: 2021-11-08 18:04:32.414327

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bce514e0541f'
down_revision = '2baa6aed2473'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )


def downgrade():
    op.drop_table('users')
