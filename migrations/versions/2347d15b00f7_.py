"""empty message

Revision ID: 2347d15b00f7
Revises: 25d802a5f282
Create Date: 2018-03-26 12:27:57.764227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2347d15b00f7'
down_revision = '25d802a5f282'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('webmarkproposal', sa.Column('name', sa.String(length=128), nullable=True))
    op.create_index(op.f('ix_webmarkproposal_name'), 'webmarkproposal', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_webmarkproposal_name'), table_name='webmarkproposal')
    op.drop_column('webmarkproposal', 'name')
    # ### end Alembic commands ###
