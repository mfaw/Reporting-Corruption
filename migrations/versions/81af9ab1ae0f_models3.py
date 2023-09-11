"""models3

Revision ID: 81af9ab1ae0f
Revises: 368f55f7301d
Create Date: 2023-09-03 21:03:00.865390

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '81af9ab1ae0f'
down_revision = '368f55f7301d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('report', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
