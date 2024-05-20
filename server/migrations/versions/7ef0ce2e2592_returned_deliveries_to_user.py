"""Returned deliveries to user

Revision ID: 7ef0ce2e2592
Revises: 18a4fb017bad
Create Date: 2024-05-17 13:05:10.047709

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7ef0ce2e2592'
down_revision = '18a4fb017bad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('delivery_id', sa.Integer(), nullable=True))
        batch_op.alter_column('buyer_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.create_foreign_key(batch_op.f('fk_order_delivery_id_user'), 'user', ['delivery_id'], ['id'])
        batch_op.drop_column('delivery_person')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('order', schema=None) as batch_op:
        batch_op.add_column(sa.Column('delivery_person', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_order_delivery_id_user'), type_='foreignkey')
        batch_op.alter_column('buyer_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.drop_column('delivery_id')

    # ### end Alembic commands ###
