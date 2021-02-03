"""add tables for recommended medias

Revision ID: 068b8ca8a66f
Revises: 6f2981ad367c
Create Date: 2020-11-12 18:21:24.450148

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '068b8ca8a66f'
down_revision = '6f2981ad367c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('recommended_book',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('engine', sa.String(), nullable=True),
    sa.Column('engine_priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['isbn'], ['book.isbn'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'isbn')
    )
    op.create_table('recommended_game',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('engine', sa.String(), nullable=True),
    sa.Column('engine_priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'game_id')
    )
    op.create_table('recommended_movie',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('movie_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('engine', sa.String(), nullable=True),
    sa.Column('engine_priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.movie_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'movie_id')
    )
    op.create_table('recommended_serie',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('serie_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('engine', sa.String(), nullable=True),
    sa.Column('engine_priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.serie_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'serie_id')
    )
    op.create_table('recommended_track',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('engine', sa.String(), nullable=True),
    sa.Column('engine_priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'track_id')
    )
    op.create_table('recommended_application',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('app_id', sa.Integer(), nullable=False),
    sa.Column('score', sa.Float(), nullable=True),
    sa.Column('engine', sa.String(), nullable=True),
    sa.Column('engine_priority', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'app_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('recommended_application')
    op.drop_table('recommended_track')
    op.drop_table('recommended_serie')
    op.drop_table('recommended_movie')
    op.drop_table('recommended_game')
    op.drop_table('recommended_book')
    # ### end Alembic commands ###