"""empty message

Revision ID: c56fe74c489f
Revises: 464d7ba68d4f
Create Date: 2018-04-11 10:41:25.405422

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c56fe74c489f'
down_revision = '464d7ba68d4f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('e_browser', sa.Column('channel', sa.String(length=12), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('e_browser', 'channel')
    # ### end Alembic commands ###
