"""add foreign key

Revision ID: 11b80498abeb
Revises: bce514e0541f
Create Date: 2021-11-08 18:26:51.860396

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11b80498abeb'
down_revision = 'bce514e0541f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer, nullable=False))
    op.create_foreign_key(
        'post_users_fk',
        'posts', 'users',
        ['owner_id'], ['id'],
        ondelete='CASCADE'
    )


def downgrade():
    op.drop_constraint('post_users_fk', 'posts')
    op.drop_column('posts', 'owner_id')
