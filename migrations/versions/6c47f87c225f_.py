"""empty message

Revision ID: 6c47f87c225f
Revises: 
Create Date: 2018-03-26 10:56:59.924869

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6c47f87c225f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('webmarkproposal',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(length=1024), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_webmarkproposal_timestamp'), 'webmarkproposal', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_webmarkproposal_timestamp'), table_name='webmarkproposal')
    op.drop_table('webmarkproposal')
    # ### end Alembic commands ###
