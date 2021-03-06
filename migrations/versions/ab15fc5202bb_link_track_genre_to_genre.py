"""Link track genre to genre

Revision ID: ab15fc5202bb
Revises: ebfe49179def
Create Date: 2020-10-15 10:57:13.154092

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab15fc5202bb'
down_revision = 'ebfe49179def'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('genre_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'application', 'genre', ['genre_id'], ['genre_id'])
    op.drop_column('application', 'category')
    op.add_column('track_genres', sa.Column('genre_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'track_genres', 'genre', ['genre_id'], ['genre_id'])
    op.drop_column('track_genres', 'frequency')
    op.drop_column('track_genres', 'tag')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('track_genres', sa.Column('tag', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('track_genres', sa.Column('frequency', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'track_genres', type_='foreignkey')
    op.drop_column('track_genres', 'genre_id')
    op.add_column('application', sa.Column('category', sa.VARCHAR(length=255), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'application', type_='foreignkey')
    op.drop_column('application', 'genre_id')
    # ### end Alembic commands ###
