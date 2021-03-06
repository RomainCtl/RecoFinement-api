"""add lock for preferences defined or not

Revision ID: 8e860798bd13
Revises: f41b7813727e
Create Date: 2020-11-06 09:48:32.755927

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8e860798bd13'
down_revision = 'f41b7813727e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('preferences_defined',
                                    sa.Boolean(), nullable=True, server_default='false'))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'preferences_defined')
    # ### end Alembic commands ###
