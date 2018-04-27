"""empty message

Revision ID: 051f2c7a2695
Revises: 9d021031403d
Create Date: 2018-04-09 14:40:42.359237

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '051f2c7a2695'
down_revision = '9d021031403d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('webmark', sa.Column('metrics', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('webmark', 'metrics')
    # ### end Alembic commands ###
