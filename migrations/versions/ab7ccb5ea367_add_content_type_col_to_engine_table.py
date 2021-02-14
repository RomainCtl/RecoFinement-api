"""Add content_type col to engine table

Revision ID: ab7ccb5ea367
Revises: eecf1702bc5c
Create Date: 2021-02-14 22:31:15.826517

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = 'ab7ccb5ea367'
down_revision = 'eecf1702bc5c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('engine', sa.Column('content_type', postgresql.ENUM('APPLICATION', 'BOOK', 'GAME',
                                                                      'MOVIE', 'SERIE', 'TRACK', name='contenttype', create_type=False), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('engine', 'content_type')
    # ### end Alembic commands ###
