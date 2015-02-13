"""empty message

Revision ID: 376650d684d7
Revises: 1fa7caa8a01f
Create Date: 2015-01-09 16:27:20.402521

"""

# revision identifiers, used by Alembic.
revision = '376650d684d7'
down_revision = '1fa7caa8a01f'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('relation_job_manager',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('job_id', sa.Integer(), nullable=True),
    sa.Column('manager_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['job.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('relation_job_manager')
    ### end Alembic commands ###
