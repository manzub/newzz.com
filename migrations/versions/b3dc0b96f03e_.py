"""empty message

Revision ID: b3dc0b96f03e
Revises: c4bbd7bfaa18
Create Date: 2020-10-06 10:51:01.571307

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3dc0b96f03e'
down_revision = 'c4bbd7bfaa18'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'users', ['email'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    # ### end Alembic commands ###
