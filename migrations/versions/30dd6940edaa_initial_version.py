"""initial_version

Revision ID: 30dd6940edaa
Revises: 
Create Date: 2020-09-21 20:26:48.354469

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '30dd6940edaa'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('app_name', sa.String(length=255), nullable=True),
    sa.Column('category', sa.String(length=255), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('reviews', sa.Integer(), nullable=True),
    sa.Column('installs', sa.String(length=255), nullable=True),
    sa.Column('size', sa.String(length=255), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('content_rating', sa.String(length=255), nullable=True),
    sa.Column('last_updated', sa.String(length=255), nullable=True),
    sa.Column('minimum_version', sa.String(length=255), nullable=True),
    sa.Column('latest_version', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_index(op.f('ix_application_app_name'), 'application', ['app_name'], unique=True)
    op.create_table('book',
    sa.Column('isbn', sa.String(length=13), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=True),
    sa.Column('author', sa.String(length=255), nullable=True),
    sa.Column('year_of_publication', sa.Integer(), nullable=True),
    sa.Column('publisher', sa.String(length=255), nullable=True),
    sa.Column('image_url_s', sa.String(length=255), nullable=True),
    sa.Column('image_url_m', sa.String(length=255), nullable=True),
    sa.Column('image_url_l', sa.String(length=255), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('rating_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('isbn')
    )
    op.create_index(op.f('ix_book_author'), 'book', ['author'], unique=False)
    op.create_index(op.f('ix_book_isbn'), 'book', ['isbn'], unique=False)
    op.create_index(op.f('ix_book_title'), 'book', ['title'], unique=False)
    op.create_table('game',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('icon_url', sa.String(length=255), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('rating_count', sa.Integer(), nullable=True),
    sa.Column('price', sa.Float(), nullable=True),
    sa.Column('in_app_purchases', sa.Float(), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('developer', sa.String(length=255), nullable=True),
    sa.Column('languages', sa.String(length=255), nullable=True),
    sa.Column('size', sa.Integer(), nullable=True),
    sa.Column('primary_genre', sa.String(length=45), nullable=True),
    sa.Column('genres', sa.String(length=255), nullable=True),
    sa.Column('original_release_date', sa.String(length=45), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('uid')
    )
    op.create_table('genre',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gid')
    )
    op.create_table('tag',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tag_name'), 'tag', ['name'], unique=False)
    op.create_table('track',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('gid', postgresql.UUID(as_uuid=True), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('artist_name', sa.String(length=255), nullable=True),
    sa.Column('album_name', sa.String(length=255), nullable=True),
    sa.Column('language', sa.String(length=2), nullable=True),
    sa.Column('date_year', sa.SmallInteger(), nullable=True),
    sa.Column('date_month', sa.SmallInteger(), nullable=True),
    sa.Column('date_day', sa.SmallInteger(), nullable=True),
    sa.Column('rating', sa.Float(), nullable=True),
    sa.Column('rating_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('gid')
    )
    op.create_index(op.f('ix_track_artist_name'), 'track', ['artist_name'], unique=False)
    op.create_index(op.f('ix_track_name'), 'track', ['name'], unique=False)
    op.create_table('user',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', postgresql.UUID(as_uuid=True), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('username', sa.String(length=45), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('track_tags',
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('tag', sa.Integer(), nullable=False),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tag'], ['tag.id'], ),
    sa.ForeignKeyConstraint(['track_id'], ['track.id'], ),
    sa.PrimaryKeyConstraint('track_id', 'tag')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_tags')
    op.drop_table('user')
    op.drop_index(op.f('ix_track_name'), table_name='track')
    op.drop_index(op.f('ix_track_artist_name'), table_name='track')
    op.drop_table('track')
    op.drop_index(op.f('ix_tag_name'), table_name='tag')
    op.drop_table('tag')
    op.drop_table('genre')
    op.drop_table('game')
    op.drop_index(op.f('ix_book_title'), table_name='book')
    op.drop_index(op.f('ix_book_isbn'), table_name='book')
    op.drop_index(op.f('ix_book_author'), table_name='book')
    op.drop_table('book')
    op.drop_index(op.f('ix_application_app_name'), table_name='application')
    op.drop_table('application')
    # ### end Alembic commands ###
