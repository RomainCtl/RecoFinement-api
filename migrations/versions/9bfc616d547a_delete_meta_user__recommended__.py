"""delete meta_user_ recommended_ recommended__for_group similars_ _genres

Revision ID: 9bfc616d547a
Revises: fd137681f251
Create Date: 2020-12-21 18:19:57.905897

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '9bfc616d547a'
down_revision = 'fd137681f251'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('similars_application')
    op.drop_table('bad_recommendation_application')
    op.drop_table('meta_user_game')
    op.drop_table('bad_recommendation_serie')
    op.drop_table('recommended_track_for_group')
    op.drop_table('bad_recommendation_book')
    op.drop_table('recommended_movie_for_group')
    op.drop_table('recommended_application')
    op.drop_table('meta_user_application')
    op.drop_table('recommended_serie')
    op.drop_table('movie_genres')
    op.drop_table('bad_recommendation_game')
    op.drop_table('recommended_game_for_group')
    op.drop_table('similars_game')
    op.drop_table('recommended_book')
    op.drop_table('meta_user_book')
    op.drop_table('recommended_serie_for_group')
    op.drop_table('recommended_book_for_group')
    op.drop_table('similars_serie')
    op.drop_table('recommended_track')
    op.drop_table('similars_movie')
    op.drop_table('track_genres')
    op.drop_table('bad_recommendation_movie')
    op.drop_table('recommended_game')
    op.drop_table('recommended_movie')
    op.drop_table('similars_track')
    op.drop_table('recommended_application_for_group')
    op.drop_table('meta_user_serie')
    op.drop_table('meta_user_track')
    op.drop_table('serie_genres')
    op.drop_table('bad_recommendation_track')
    op.drop_table('similars_book')
    op.drop_table('meta_user_movie')
    op.drop_table('game_genres')
    op.drop_constraint('application_genre_id_fkey', 'application', type_='foreignkey')
    op.drop_column('application', 'genre_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('application', sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.create_foreign_key('application_genre_id_fkey', 'application', 'genre', ['genre_id'], ['genre_id'])
    op.create_table('game_genres',
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], name='game_genres_game_id_fkey'),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.genre_id'], name='game_genres_genre_id_fkey'),
    sa.PrimaryKeyConstraint('game_id', 'genre_id', name='game_genres_pkey')
    )
    op.create_table('meta_user_movie',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('review_see_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('watch_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.CheckConstraint('(rating <= 5) AND (rating >= 0)', name='meta_user_movie_rating_check'),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.movie_id'], name='meta_user_movie_movie_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='meta_user_movie_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'movie_id', name='meta_user_movie_pkey')
    )
    op.create_table('similars_book',
    sa.Column('isbn0', sa.VARCHAR(length=13), autoincrement=False, nullable=False),
    sa.Column('isbn1', sa.VARCHAR(length=13), autoincrement=False, nullable=False),
    sa.Column('similarity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['isbn0'], ['book.isbn'], name='similars_book_isbn0_fkey'),
    sa.ForeignKeyConstraint(['isbn1'], ['book.isbn'], name='similars_book_isbn1_fkey'),
    sa.PrimaryKeyConstraint('isbn0', 'isbn1', name='similars_book_pkey')
    )
    op.create_table('bad_recommendation_track',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('track_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reason_categorie', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], name='bad_recommendation_track_track_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='bad_recommendation_track_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'track_id', 'reason_categorie', name='bad_recommendation_track_pkey')
    )
    op.create_table('serie_genres',
    sa.Column('serie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.genre_id'], name='serie_genres_genre_id_fkey'),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.serie_id'], name='serie_genres_serie_id_fkey'),
    sa.PrimaryKeyConstraint('serie_id', 'genre_id', name='serie_genres_pkey')
    )
    op.create_table('meta_user_track',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('track_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('play_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('review_see_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('last_played_date', postgresql.TIMESTAMP(), autoincrement=False, nullable=True),
    sa.CheckConstraint('(rating <= 5) AND (rating >= 0)', name='meta_user_track_rating_check'),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], name='meta_user_track_track_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='meta_user_track_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'track_id', name='meta_user_track_pkey')
    )
    op.create_table('meta_user_serie',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('serie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('num_watched_episodes', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.Column('review_see_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.serie_id'], name='meta_user_serie_serie_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='meta_user_serie_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'serie_id', name='meta_user_serie_pkey')
    )
    op.create_table('recommended_application_for_group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('app_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], name='recommended_application_for_group_app_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], name='recommended_application_for_group_group_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'app_id', name='recommended_application_for_group_pkey')
    )
    op.create_table('similars_track',
    sa.Column('track_id0', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('track_id1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('similarity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['track_id0'], ['track.track_id'], name='similars_track_track_id0_fkey'),
    sa.ForeignKeyConstraint(['track_id1'], ['track.track_id'], name='similars_track_track_id1_fkey'),
    sa.PrimaryKeyConstraint('track_id0', 'track_id1', name='similars_track_pkey')
    )
    op.create_table('recommended_movie',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.movie_id'], name='recommended_movie_movie_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='recommended_movie_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'movie_id', name='recommended_movie_pkey')
    )
    op.create_table('recommended_game',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], name='recommended_game_game_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='recommended_game_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'game_id', name='recommended_game_pkey')
    )
    op.create_table('bad_recommendation_movie',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reason_categorie', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.movie_id'], name='bad_recommendation_movie_movie_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='bad_recommendation_movie_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'movie_id', 'reason_categorie', name='bad_recommendation_movie_pkey')
    )
    op.create_table('track_genres',
    sa.Column('track_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.genre_id'], name='track_genres_genre_id_fkey'),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], name='track_genres_track_id_fkey')
    )
    op.create_table('similars_movie',
    sa.Column('movie_id0', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('movie_id1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('similarity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['movie_id0'], ['movie.movie_id'], name='similars_movie_movie_id0_fkey'),
    sa.ForeignKeyConstraint(['movie_id1'], ['movie.movie_id'], name='similars_movie_movie_id1_fkey'),
    sa.PrimaryKeyConstraint('movie_id0', 'movie_id1', name='similars_movie_pkey')
    )
    op.create_table('recommended_track',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('track_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], name='recommended_track_track_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='recommended_track_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'track_id', name='recommended_track_pkey')
    )
    op.create_table('similars_serie',
    sa.Column('serie_id0', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('serie_id1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('similarity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['serie_id0'], ['serie.serie_id'], name='similars_serie_serie_id0_fkey'),
    sa.ForeignKeyConstraint(['serie_id1'], ['serie.serie_id'], name='similars_serie_serie_id1_fkey'),
    sa.PrimaryKeyConstraint('serie_id0', 'serie_id1', name='similars_serie_pkey')
    )
    op.create_table('recommended_book_for_group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('isbn', sa.VARCHAR(length=13), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], name='recommended_book_for_group_group_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['isbn'], ['book.isbn'], name='recommended_book_for_group_isbn_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'isbn', name='recommended_book_for_group_pkey')
    )
    op.create_table('recommended_serie_for_group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('serie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], name='recommended_serie_for_group_group_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.serie_id'], name='recommended_serie_for_group_serie_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'serie_id', name='recommended_serie_for_group_pkey')
    )
    op.create_table('meta_user_book',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('isbn', sa.VARCHAR(length=13), autoincrement=False, nullable=False),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('purchase', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('review_see_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.CheckConstraint('(rating <= 5) AND (rating >= 0)', name='meta_user_book_rating_check'),
    sa.ForeignKeyConstraint(['isbn'], ['book.isbn'], name='meta_user_book_isbn_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='meta_user_book_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'isbn', name='meta_user_book_pkey')
    )
    op.create_table('recommended_book',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('isbn', sa.VARCHAR(length=13), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['isbn'], ['book.isbn'], name='recommended_book_isbn_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='recommended_book_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'isbn', name='recommended_book_pkey')
    )
    op.create_table('similars_game',
    sa.Column('game_id0', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('similarity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['game_id0'], ['game.game_id'], name='similars_game_game_id0_fkey'),
    sa.ForeignKeyConstraint(['game_id1'], ['game.game_id'], name='similars_game_game_id1_fkey'),
    sa.PrimaryKeyConstraint('game_id0', 'game_id1', name='similars_game_pkey')
    )
    op.create_table('recommended_game_for_group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], name='recommended_game_for_group_game_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], name='recommended_game_for_group_group_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'game_id', name='recommended_game_for_group_pkey')
    )
    op.create_table('bad_recommendation_game',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reason_categorie', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], name='bad_recommendation_game_game_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='bad_recommendation_game_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'game_id', 'reason_categorie', name='bad_recommendation_game_pkey')
    )
    op.create_table('movie_genres',
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('genre_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.genre_id'], name='movie_genres_genre_id_fkey'),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.movie_id'], name='movie_genres_movie_id_fkey'),
    sa.PrimaryKeyConstraint('movie_id', 'genre_id', name='movie_genres_pkey')
    )
    op.create_table('recommended_serie',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('serie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.serie_id'], name='recommended_serie_serie_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='recommended_serie_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'serie_id', name='recommended_serie_pkey')
    )
    op.create_table('meta_user_application',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('app_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('review', sa.TEXT(), autoincrement=False, nullable=True),
    sa.Column('popularity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('subjectivity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('downloaded', sa.BOOLEAN(), server_default=sa.text('false'), autoincrement=False, nullable=True),
    sa.Column('review_see_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.CheckConstraint('(rating <= 5) AND (rating >= 0)', name='meta_user_application_rating_check'),
    sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], name='meta_user_application_app_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='meta_user_application_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'app_id', name='meta_user_application_pkey')
    )
    op.create_table('recommended_application',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('app_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], name='recommended_application_app_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='recommended_application_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'app_id', name='recommended_application_pkey')
    )
    op.create_table('recommended_movie_for_group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('movie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], name='recommended_movie_for_group_group_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['movie_id'], ['movie.movie_id'], name='recommended_movie_for_group_movie_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'movie_id', name='recommended_movie_for_group_pkey')
    )
    op.create_table('bad_recommendation_book',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('isbn', sa.VARCHAR(length=13), autoincrement=False, nullable=False),
    sa.Column('reason_categorie', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['isbn'], ['book.isbn'], name='bad_recommendation_book_isbn_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='bad_recommendation_book_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'isbn', 'reason_categorie', name='bad_recommendation_book_pkey')
    )
    op.create_table('recommended_track_for_group',
    sa.Column('group_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('track_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('score', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('engine', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('engine_priority', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['group_id'], ['group.group_id'], name='recommended_track_for_group_group_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], name='recommended_track_for_group_track_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('group_id', 'track_id', name='recommended_track_for_group_pkey')
    )
    op.create_table('bad_recommendation_serie',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('serie_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reason_categorie', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['serie_id'], ['serie.serie_id'], name='bad_recommendation_serie_serie_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='bad_recommendation_serie_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'serie_id', 'reason_categorie', name='bad_recommendation_serie_pkey')
    )
    op.create_table('meta_user_game',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('game_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('purchase', sa.BOOLEAN(), autoincrement=False, nullable=True),
    sa.Column('hours', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.Column('rating', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('review_see_count', sa.INTEGER(), server_default=sa.text('0'), autoincrement=False, nullable=True),
    sa.CheckConstraint('(rating <= 5) AND (rating >= 0)', name='meta_user_game_rating_check'),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], name='meta_user_game_game_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='meta_user_game_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'game_id', name='meta_user_game_pkey')
    )
    op.create_table('bad_recommendation_application',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('app_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('reason_categorie', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('reason', sa.TEXT(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], name='bad_recommendation_application_app_id_fkey', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], name='bad_recommendation_application_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'app_id', 'reason_categorie', name='bad_recommendation_application_pkey')
    )
    op.create_table('similars_application',
    sa.Column('app_id0', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('app_id1', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('similarity', postgresql.DOUBLE_PRECISION(precision=53), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['app_id0'], ['application.app_id'], name='similars_application_app_id0_fkey'),
    sa.ForeignKeyConstraint(['app_id1'], ['application.app_id'], name='similars_application_app_id1_fkey'),
    sa.PrimaryKeyConstraint('app_id0', 'app_id1', name='similars_application_pkey')
    )
    # ### end Alembic commands ###
