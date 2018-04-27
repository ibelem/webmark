"""empty message

Revision ID: 6536d6e30666
Revises: 946e6cc0f4b5
Create Date: 2018-04-02 12:56:15.481183

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6536d6e30666'
down_revision = '946e6cc0f4b5'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('news',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('summary', sa.String(length=256), nullable=True),
    sa.Column('url', sa.String(length=1024), nullable=True),
    sa.Column('source', sa.String(length=128), nullable=True),
    sa.Column('details', sa.Text(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('webmark_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['webmark_id'], ['webmark.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_news_timestamp'), 'news', ['timestamp'], unique=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_news_timestamp'), table_name='news')
    op.drop_table('news')
    # ### end Alembic commands ###
