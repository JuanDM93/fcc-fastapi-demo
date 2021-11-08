"""create posts table

Revision ID: 2baa6aed2473
Revises:
Create Date: 2021-11-08 17:54:10.721972

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2baa6aed2473'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer, primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.Text, nullable=False),
        sa.Column('published', sa.Boolean, nullable=False,
                  server_default=sa.true()),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                  nullable=False, server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('posts')
