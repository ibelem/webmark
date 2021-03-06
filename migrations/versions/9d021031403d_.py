"""empty message

Revision ID: 9d021031403d
Revises: 28b564c8ffc4
Create Date: 2018-04-04 16:07:25.405047

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9d021031403d'
down_revision = '28b564c8ffc4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('score',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('webmark_id', sa.Integer(), nullable=True),
    sa.Column('score', sa.String(length=64), nullable=True),
    sa.Column('hardware_id', sa.Integer(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['author_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['webmark_id'], ['webmark.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_score_timestamp'), 'score', ['timestamp'], unique=False)
    op.drop_column('webmark', 'score')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('webmark', sa.Column('score', mysql.VARCHAR(collation='utf8_unicode_ci', length=64), nullable=True))
    op.drop_index(op.f('ix_score_timestamp'), table_name='score')
    op.drop_table('score')
    # ### end Alembic commands ###
