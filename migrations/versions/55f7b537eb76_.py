"""empty message

Revision ID: 55f7b537eb76
Revises: c2597252f5fc
Create Date: 2018-04-25 13:59:15.534513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '55f7b537eb76'
down_revision = 'c2597252f5fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feedback',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=True),
    sa.Column('title', sa.String(length=256), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('reviewed', sa.Boolean(), nullable=True),
    sa.Column('replied', sa.Boolean(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feedback_timestamp'), 'feedback', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_feedback_timestamp'), table_name='feedback')
    op.drop_table('feedback')
    # ### end Alembic commands ###
