"""Added Location column

Revision ID: 90af2eb7e8b1
Revises: 1542f2246366
Create Date: 2024-05-09 16:09:49.453195

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '90af2eb7e8b1'
down_revision = '1542f2246366'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('location', sa.String(length=250), nullable=True))
        batch_op.alter_column('_password_hash',
               existing_type=sa.VARCHAR(length=100),
               type_=sa.String(length=255),
               existing_nullable=False)

def downgrade():
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('_password_hash',
               existing_type=sa.String(length=255),
               type_=sa.VARCHAR(length=100),
               existing_nullable=False)
        batch_op.drop_column('location')
