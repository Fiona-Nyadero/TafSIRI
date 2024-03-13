"""users table

Revision ID: ff0463639d6e
Revises: 0172f33d554e
Create Date: 2024-03-13 13:19:51.191942

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ff0463639d6e'
down_revision = '0172f33d554e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('_alembic_tmp_user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('_alembic_tmp_user',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('Username', sa.VARCHAR(length=64), nullable=False),
    sa.Column('Email', sa.VARCHAR(length=120), nullable=False),
    sa.Column('Password_hash', sa.VARCHAR(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
