"""Add track genres

Revision ID: cfe8f681c7b7
Revises: 218fc706a3e9
Create Date: 2020-10-09 22:37:18.306783

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cfe8f681c7b7'
down_revision = '218fc706a3e9'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('track_genres',
                    sa.Column('track_id', sa.Integer(), nullable=False),
                    sa.Column('tag', sa.String(length=255), nullable=False),
                    sa.Column('frequency', sa.Integer(), nullable=True),
                    sa.ForeignKeyConstraint(
                        ['track_id'], ['track.track_id'], ),
                    sa.PrimaryKeyConstraint('track_id', 'tag')
                    )
    op.alter_column('track', 'url',
                    existing_type=sa.TEXT(),
                    type_=sa.String(length=45),
                    new_column_name="spotify_id")
    op.alter_column('episode', 'title',
                    existing_type=sa.VARCHAR(length=255),
                    type_=sa.String(length=512))
    op.add_column('movie', sa.Column('cover', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('movie', 'cover')
    op.alter_column('episode', 'title',
                    existing_type=sa.VARCHAR(length=512),
                    type_=sa.String(length=255))
    op.alter_column('track', 'spotify_id',
                    existing_type=sa.STRING(length=45),
                    type_=sa.TEXT(),
                    new_column_name="url")
    op.drop_table('track_genres')
    # ### end Alembic commands ###