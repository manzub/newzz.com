"""empty message

Revision ID: 37887654fab5
Revises: ad1c0fb4dde3
Create Date: 2020-09-27 07:12:00.240460

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '37887654fab5'
down_revision = 'ad1c0fb4dde3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cashouts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_email', sa.String(), nullable=True),
    sa.Column('amount', sa.String(), nullable=True),
    sa.Column('payout_type', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('cashouts')
    # ### end Alembic commands ###
