"""add event sourcing tables

Revision ID: 6a68be6b9e1c
Revises: 6ea6ab643ed1
Create Date: 2021-01-28 16:43:30.173991

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '6a68be6b9e1c'
down_revision = '6ea6ab643ed1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('application_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('size', sa.String(length=255), nullable=True),
                    sa.Column('installs', sa.String(
                        length=255), nullable=True),
                    sa.Column('type', sa.String(length=45), nullable=True),
                    sa.Column('price', sa.String(length=45), nullable=True),
                    sa.Column('content_rating', sa.String(
                        length=255), nullable=True),
                    sa.Column('last_updated', sa.String(
                        length=255), nullable=True),
                    sa.Column('current_version', sa.String(
                        length=255), nullable=True),
                    sa.Column('android_version', sa.String(
                        length=255), nullable=True),
                    sa.Column('cover', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('book_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('isbn', sa.String(length=13), nullable=True),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('author', sa.String(length=255), nullable=True),
                    sa.Column('year_of_publication',
                              sa.Integer(), nullable=True),
                    sa.Column('publisher', sa.String(
                        length=255), nullable=True),
                    sa.Column('image_url_s', sa.Text(), nullable=True),
                    sa.Column('image_url_m', sa.Text(), nullable=True),
                    sa.Column('image_url_l', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('changed_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('model_name', sa.String(), nullable=False),
                    sa.Column('attribute_name', sa.String(), nullable=False),
                    sa.Column('new_value', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('deletion_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('model_name', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('episode_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('imdbid', sa.String(length=255), nullable=True),
                    sa.Column('title', sa.String(length=512), nullable=True),
                    sa.Column('year', sa.Integer(), nullable=True),
                    sa.Column('season_number', sa.Integer(), nullable=True),
                    sa.Column('episode_number', sa.Integer(), nullable=True),
                    sa.Column('serie_id', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('game_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('steamid', sa.Integer(), nullable=True),
                    sa.Column('name', sa.String(length=255), nullable=True),
                    sa.Column('short_description', sa.Text(), nullable=True),
                    sa.Column('header_image', sa.String(
                        length=255), nullable=True),
                    sa.Column('website', sa.String(length=255), nullable=True),
                    sa.Column('developers', sa.String(
                        length=255), nullable=True),
                    sa.Column('publishers', sa.String(
                        length=255), nullable=True),
                    sa.Column('price', sa.String(length=255), nullable=True),
                    sa.Column('recommendations', sa.Integer(), nullable=True),
                    sa.Column('release_date', sa.String(
                        length=255), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('meta_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('rating', sa.Integer(), nullable=True),
                    sa.Column('review_see_count', sa.Integer(), nullable=True),
                    sa.Column('count', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('movie_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('language', sa.String(
                        length=255), nullable=True),
                    sa.Column('actors', sa.Text(), nullable=True),
                    sa.Column('year', sa.String(length=255), nullable=True),
                    sa.Column('producers', sa.Text(), nullable=True),
                    sa.Column('director', sa.Text(), nullable=True),
                    sa.Column('writer', sa.Text(), nullable=True),
                    sa.Column('imdbid', sa.String(length=255), nullable=True),
                    sa.Column('tmdbid', sa.String(length=255), nullable=True),
                    sa.Column('cover', sa.Text(), nullable=True),
                    sa.Column('plot_outline', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('serie_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('imdbid', sa.String(length=255), nullable=True),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('start_year', sa.Integer(), nullable=True),
                    sa.Column('end_year', sa.Integer(), nullable=True),
                    sa.Column('writers', sa.Text(), nullable=True),
                    sa.Column('directors', sa.Text(), nullable=True),
                    sa.Column('actors', sa.Text(), nullable=True),
                    sa.Column('cover', sa.Text(), nullable=True),
                    sa.Column('plot_outline', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('track_added_event',
                    sa.Column('id', sa.Integer(),
                              autoincrement=True, nullable=False),
                    sa.Column('occured_at', sa.DateTime(), nullable=False),
                    sa.Column('occured_by', sa.Integer(), nullable=False),
                    sa.Column('object_id', sa.Integer(), nullable=False),
                    sa.Column('title', sa.String(length=255), nullable=True),
                    sa.Column('year', sa.SmallInteger(), nullable=True),
                    sa.Column('artist_name', sa.String(
                        length=255), nullable=True),
                    sa.Column('release', sa.String(length=255), nullable=True),
                    sa.Column('track_mmid', sa.String(
                        length=45), nullable=True),
                    sa.Column('recording_mbid', postgresql.UUID(
                        as_uuid=True), nullable=True),
                    sa.Column('spotify_id', sa.String(
                        length=45), nullable=True),
                    sa.Column('covert_art_url', sa.Text(), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('track_added_event')
    op.drop_table('serie_added_event')
    op.drop_table('movie_added_event')
    op.drop_table('meta_added_event')
    op.drop_table('game_added_event')
    op.drop_table('episode_added_event')
    op.drop_table('deletion_event')
    op.drop_table('changed_event')
    op.drop_table('book_added_event')
    op.drop_table('application_added_event')
    # ### end Alembic commands ###
