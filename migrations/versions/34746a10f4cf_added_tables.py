"""Added tables

Revision ID: 34746a10f4cf
Revises:
Create Date: 2023-05-18 18:23:31.254134

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '34746a10f4cf'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question', sa.String(), nullable=True),
        sa.Column('answer', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(), nullable=True),
        sa.Column('local_created_at', sa.TIMESTAMP(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_questions_id'), 'questions', ['id'], unique=False)
    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('access_token', sa.UUID(), nullable=True),
        sa.Column('username', sa.String(length=128), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('access_token'),
        sa.UniqueConstraint('username')
    )
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('records',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('data', postgresql.BYTEA(), nullable=True),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('access_token', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['access_token'], ['users.access_token'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_records_id'), 'records', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_records_id'), table_name='records')
    op.drop_table('records')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_questions_id'), table_name='questions')
    op.drop_table('questions')
    # ### end Alembic commands ###
