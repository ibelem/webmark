"""empty message

Revision ID: 843c25c9d8cb
Revises: 7b6575f2bec2
Create Date: 2018-03-27 14:43:57.281447

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '843c25c9d8cb'
down_revision = '7b6575f2bec2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('comments_ibfk_2', 'comments', type_='foreignkey')
    op.drop_column('comments', 'post_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('post_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_foreign_key('comments_ibfk_2', 'comments', 'posts', ['post_id'], ['id'])
    # ### end Alembic commands ###
