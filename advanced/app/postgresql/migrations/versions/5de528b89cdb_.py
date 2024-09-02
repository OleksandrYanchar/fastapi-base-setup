"""empty message

Revision ID: 5de528b89cdb
Revises: 
Create Date: 2024-09-02 21:46:51.063546

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5de528b89cdb'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'blacklisted_tokens', ['id'])
    op.add_column('users', sa.Column('email', sa.String(length=255), nullable=False))
    op.drop_constraint('users_emalil_key', 'users', type_='unique')
    op.create_unique_constraint(None, 'users', ['email'])
    op.create_unique_constraint(None, 'users', ['id'])
    op.drop_column('users', 'emalil')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('emalil', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'users', type_='unique')
    op.drop_constraint(None, 'users', type_='unique')
    op.create_unique_constraint('users_emalil_key', 'users', ['emalil'])
    op.drop_column('users', 'email')
    op.drop_constraint(None, 'blacklisted_tokens', type_='unique')
    # ### end Alembic commands ###
