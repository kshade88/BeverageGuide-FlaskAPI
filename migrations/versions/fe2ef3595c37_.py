"""empty message

Revision ID: fe2ef3595c37
Revises: 
Create Date: 2022-01-18 21:21:10.981940

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe2ef3595c37'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'bev_tags', ['name'])
    op.alter_column('cocktails', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'cocktails', ['name'])
    op.alter_column('ingredients', 'name',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.create_unique_constraint(None, 'ingredients', ['name'])
    op.drop_column('ingredients', 'type')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('ingredients', sa.Column('type', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'ingredients', type_='unique')
    op.alter_column('ingredients', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'cocktails', type_='unique')
    op.alter_column('cocktails', 'name',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_constraint(None, 'bev_tags', type_='unique')
    # ### end Alembic commands ###
