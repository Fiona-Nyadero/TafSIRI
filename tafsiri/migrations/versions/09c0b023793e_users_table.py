"""users table

Revision ID: 09c0b023793e
Revises: ff0463639d6e
Create Date: 2024-03-14 13:28:36.088688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09c0b023793e'
down_revision = 'ff0463639d6e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Phone_number', sa.String(length=20), nullable=True))
        batch_op.add_column(sa.Column('Date_of_birth', sa.Date(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('Date_of_birth')
        batch_op.drop_column('Phone_number')

    # ### end Alembic commands ###
