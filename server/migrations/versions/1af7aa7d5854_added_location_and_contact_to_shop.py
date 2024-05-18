"""Added location and contact to shop

Revision ID: 1af7aa7d5854
Revises: 9945fac7da57
Create Date: 2024-05-18 16:17:28.765601

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af7aa7d5854'
down_revision = '9945fac7da57'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=250), nullable=True))
        batch_op.add_column(sa.Column('contact', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('shop', schema=None) as batch_op:
        batch_op.drop_column('contact')
        batch_op.drop_column('location')

    # ### end Alembic commands ###
