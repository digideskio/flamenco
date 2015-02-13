"""Add time_cost to Workers

Revision ID: bb419a4193b
Revises: 556e494b5f75
Create Date: 2015-02-10 12:46:42.590041

"""

# revision identifiers, used by Alembic.
revision = 'bb419a4193b'
down_revision = '556e494b5f75'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.add_column(sa.Column('time_cost', sa.Integer(), nullable=True))

    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('worker', schema=None) as batch_op:
        batch_op.drop_column('time_cost')

    ### end Alembic commands ###
