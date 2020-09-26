"""initial_version

Revision ID: 10ed0a49659d
Revises: 
Create Date: 2020-09-26 16:56:40.499473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '10ed0a49659d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('app_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('reviews', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=255), nullable=True),
    sa.Column('installs', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('content_rating', sa.String(length=255), nullable=True),
    sa.Column('genres', sa.String(length=255), nullable=True),
    sa.Column('last_updated', sa.String(length=255), nullable=True),
    sa.Column('current_version', sa.String(length=255), nullable=True),
    sa.Column('android_version', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('app_id')
    )
    op.create_index(op.f('ix_application_app_id'), 'application', ['app_id'], unique=False)
    op.create_index(op.f('ix_application_name'), 'application', ['name'], unique=True)
    op.create_table('book',
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.Column('year_of_publication', sa.Integer(), nullable=True),
    sa.Column('publisher', sa.String(length=255), nullable=True),
    sa.Column('image_url_s', sa.String(length=255), nullable=True),
    sa.Column('image_url_m', sa.String(length=255), nullable=True),
    sa.Column('image_url_l', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('isbn')
    )
    op.create_index(op.f('ix_book_author'), 'book', ['author'], unique=False)
    op.create_index(op.f('ix_book_isbn'), 'book', ['isbn'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.create_table('game',
    sa.Column('game_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('steamid', sa.Integer(), nullable=True),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('short_description', sa.Text(), nullable=True),
    sa.Column('header_image', sa.String(length=255), nullable=True),
    sa.Column('website', sa.String(length=255), nullable=True),
    sa.Column('developers', sa.String(length=255), nullable=True),
    sa.Column('publishers', sa.String(length=255), nullable=True),
    sa.Column('price', sa.String(length=255), nullable=True),
    sa.Column('genres', sa.String(length=255), nullable=True),
    sa.Column('recommendations', sa.String(length=255), nullable=True),
    sa.Column('release_date', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('game_id')
    )
    op.create_index(op.f('ix_game_game_id'), 'game', ['game_id'], unique=False)
    op.create_index(op.f('ix_game_name'), 'game', ['name'], unique=False)
    op.create_table('revoked_token',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('jti', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tag',
    sa.Column('tag_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('tag_id')
    )
    op.create_index(op.f('ix_tag_tag_id'), 'tag', ['tag_id'], unique=False)
    op.create_table('track',
    sa.Column('track_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('year', sa.SmallInteger(), nullable=True),
    sa.Column('artist_name', sa.String(length=255), nullable=True),
    sa.Column('release', sa.String(length=255), nullable=True),
    sa.Column('recording_mbid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('language', sa.String(length=45), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('rating_count', sa.Integer(), nullable=True),
    sa.Column('url', sa.String(length=255), nullable=True),
    sa.Column('covert_art_url', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('track_id'),
    sa.UniqueConstraint('recording_mbid')
    )
    op.create_index(op.f('ix_track_artist_name'), 'track', ['artist_name'], unique=False)
    op.create_index(op.f('ix_track_title'), 'track', ['title'], unique=False)
    op.create_index(op.f('ix_track_track_id'), 'track', ['track_id'], unique=False)
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_user_user_id'), 'user', ['user_id'], unique=False)
    op.create_table('meta_user_application',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('app_id', sa.Integer(), nullable=False),
    sa.Column('review', sa.Text(), nullable=True),
    sa.Column('popularity', sa.Float(), nullable=True),
    sa.Column('subjectivity', sa.Float(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.CheckConstraint('rating <= 5 and rating >= 0'),
    sa.ForeignKeyConstraint(['app_id'], ['application.app_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'app_id')
    )
    op.create_table('meta_user_book',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.CheckConstraint('rating <= 5 and rating >= 0'),
    sa.ForeignKeyConstraint(['isbn'], ['book.isbn'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'isbn')
    )
    op.create_table('meta_user_game',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('game_id', sa.Integer(), nullable=False),
    sa.Column('purchase', sa.Boolean(), nullable=True),
    sa.Column('hours', sa.Float(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.CheckConstraint('rating <= 5 and rating >= 0'),
    sa.ForeignKeyConstraint(['game_id'], ['game.game_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'game_id')
    )
    op.create_table('meta_user_track',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('play_count', sa.Integer(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=True),
    sa.CheckConstraint('rating <= 5 and rating >= 0'),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('user_id', 'track_id')
    )
    op.create_table('similars_track',
    sa.Column('track_id0', sa.Integer(), nullable=False),
    sa.Column('track_id1', sa.Integer(), nullable=False),
    sa.Column('similarity', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['track_id0'], ['track.track_id'], ),
    sa.ForeignKeyConstraint(['track_id1'], ['track.track_id'], ),
    sa.PrimaryKeyConstraint('track_id0', 'track_id1')
    )
    op.create_table('track_tags',
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('tag_id', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag_id'], ['tag.tag_id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['track.track_id'], ),
    sa.PrimaryKeyConstraint('track_id', 'tag_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_tags')
    op.drop_table('similars_track')
    op.drop_table('meta_user_track')
    op.drop_table('meta_user_game')
    op.drop_table('meta_user_book')
    op.drop_table('meta_user_application')
    op.drop_index(op.f('ix_user_user_id'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_track_track_id'), table_name='track')
    op.drop_index(op.f('ix_track_title'), table_name='track')
    op.drop_index(op.f('ix_track_artist_name'), table_name='track')
    op.drop_table('track')
    op.drop_index(op.f('ix_tag_tag_id'), table_name='tag')
    op.drop_table('tag')
    op.drop_table('revoked_token')
    op.drop_index(op.f('ix_game_name'), table_name='game')
    op.drop_index(op.f('ix_game_game_id'), table_name='game')
    op.drop_table('game')
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_isbn'), table_name='book')
    op.drop_index(op.f('ix_book_author'), table_name='book')
    op.drop_table('book')
    op.drop_index(op.f('ix_application_name'), table_name='application')
    op.drop_index(op.f('ix_application_app_id'), table_name='application')
    op.drop_table('application')
    # ### end Alembic commands ###
