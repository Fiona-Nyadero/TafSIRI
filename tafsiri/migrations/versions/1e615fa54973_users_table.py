"""users table

Revision ID: 1e615fa54973
Revises: 
Create Date: 2024-03-13 11:39:50.828039

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1e615fa54973'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('Username', sa.String(length=64), nullable=False),
    sa.Column('Email', sa.String(length=120), nullable=False),
    sa.Column('Password_hash', sa.String(length=256), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_Email'), ['Email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_Username'), ['Username'], unique=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_Username'))
        batch_op.drop_index(batch_op.f('ix_user_Email'))

    op.drop_table('user')
    # ### end Alembic commands ###