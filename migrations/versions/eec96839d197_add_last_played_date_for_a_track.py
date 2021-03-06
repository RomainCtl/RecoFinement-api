"""Add last_played_date for a track

Revision ID: eec96839d197
Revises: 7de2196cb792
Create Date: 2020-10-21 19:52:47.089678

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eec96839d197'
down_revision = '7de2196cb792'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('meta_user_track', sa.Column('last_played_date', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('meta_user_track', 'last_played_date')
    # ### end Alembic commands ###
