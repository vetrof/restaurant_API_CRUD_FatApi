"""123

Revision ID: a0b750a55ce9
Revises: 
Create Date: 2024-01-20 16:53:11.355008

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a0b750a55ce9'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_table('submenus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_submenus_id'), 'submenus', ['id'], unique=False)
    op.create_table('dishes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('submenu_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.Column('price', sa.Numeric(precision=10, scale=2), nullable=True),
    sa.ForeignKeyConstraint(['submenu_id'], ['submenus.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_dishes_id'), 'dishes', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_dishes_id'), table_name='dishes')
    op.drop_table('dishes')
    op.drop_index(op.f('ix_submenus_id'), table_name='submenus')
    op.drop_table('submenus')
    op.drop_index(op.f('ix_menus_id'), table_name='menus')
    op.drop_table('menus')
    # ### end Alembic commands ###