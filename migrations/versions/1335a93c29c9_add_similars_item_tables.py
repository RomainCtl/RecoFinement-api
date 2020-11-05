"""Add similars_item tables

Revision ID: 1335a93c29c9
Revises: 8af6bbfba52a
Create Date: 2020-11-03 18:05:21.283398

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1335a93c29c9'
down_revision = '8af6bbfba52a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('similars_book',
    sa.Column('isbn0', sa.String(length=13), nullable=False),
    sa.Column('isbn1', sa.String(length=13), nullable=False),
    sa.Column('similarity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['isbn0'], ['book.isbn'], ),
    sa.ForeignKeyConstraint(['isbn1'], ['book.isbn'], ),
    sa.PrimaryKeyConstraint('isbn0', 'isbn1')
    )
    op.create_table('similars_game',
    sa.Column('game_id0', sa.Integer(), nullable=False),
    sa.Column('game_id1', sa.Integer(), nullable=False),
    sa.Column('similarity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['game_id0'], ['game.game_id'], ),
    sa.ForeignKeyConstraint(['game_id1'], ['game.game_id'], ),
    sa.PrimaryKeyConstraint('game_id0', 'game_id1')
    )
    op.create_table('similars_movie',
    sa.Column('movie_id0', sa.Integer(), nullable=False),
    sa.Column('movie_id1', sa.Integer(), nullable=False),
    sa.Column('similarity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id0'], ['movie.movie_id'], ),
    sa.ForeignKeyConstraint(['movie_id1'], ['movie.movie_id'], ),
    sa.PrimaryKeyConstraint('movie_id0', 'movie_id1')
    )
    op.create_table('similars_serie',
    sa.Column('serie_id0', sa.Integer(), nullable=False),
    sa.Column('serie_id1', sa.Integer(), nullable=False),
    sa.Column('similarity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['serie_id0'], ['serie.serie_id'], ),
    sa.ForeignKeyConstraint(['serie_id1'], ['serie.serie_id'], ),
    sa.PrimaryKeyConstraint('serie_id0', 'serie_id1')
    )
    op.create_table('similars_application',
    sa.Column('app_id0', sa.Integer(), nullable=False),
    sa.Column('app_id1', sa.Integer(), nullable=False),
    sa.Column('similarity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['app_id0'], ['application.app_id'], ),
    sa.ForeignKeyConstraint(['app_id1'], ['application.app_id'], ),
    sa.PrimaryKeyConstraint('app_id0', 'app_id1')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('similars_application')
    op.drop_table('similars_serie')
    op.drop_table('similars_movie')
    op.drop_table('similars_game')
    op.drop_table('similars_book')
    # ### end Alembic commands ###
