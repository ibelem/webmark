"""empty message

Revision ID: e00a306ca006
Revises: f44759dd72c3
Create Date: 2018-03-30 08:58:15.203287

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e00a306ca006'
down_revision = 'f44759dd72c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('webmark', sa.Column('comments_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('webmark', 'comments_count')
    # ### end Alembic commands ###
