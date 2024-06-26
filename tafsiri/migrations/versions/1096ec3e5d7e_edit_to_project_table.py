"""Edit to project table

Revision ID: 1096ec3e5d7e
Revises: 5374da42a659
Create Date: 2024-03-21 03:58:47.994114

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1096ec3e5d7e'
down_revision = '5374da42a659'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Cover', sa.String(length=10), nullable=True))
        batch_op.drop_column('Coverphoto')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('project', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Coverphoto', sa.VARCHAR(length=10), nullable=True))
        batch_op.drop_column('Cover')

    # ### end Alembic commands ###
