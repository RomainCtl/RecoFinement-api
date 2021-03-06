"""Add content type to recommended tables

Revision ID: 6ea6ab643ed1
Revises: aafc7a8cca46
Create Date: 2021-01-24 20:35:29.392369

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6ea6ab643ed1'
down_revision = 'aafc7a8cca46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('recommended_content', sa.Column('content_type', sa.Enum('APPLICATION', 'BOOK', 'GAME', 'MOVIE', 'SERIE', 'TRACK', name='contenttype'), nullable=True))
    op.add_column('recommended_content_for_group', sa.Column('content_type', sa.Enum('APPLICATION', 'BOOK', 'GAME', 'MOVIE', 'SERIE', 'TRACK', name='contenttype'), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('recommended_content_for_group', 'content_type')
    op.drop_column('recommended_content', 'content_type')
    # ### end Alembic commands ###
