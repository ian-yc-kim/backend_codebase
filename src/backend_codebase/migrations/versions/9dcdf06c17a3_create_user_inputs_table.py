"""Create user_inputs table

Revision ID: 9dcdf06c17a3
Revises: None
Create Date: 2023-10-01 12:00:00.000000
"""

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as psql

# revision identifiers, used by Alembic.
revision = '9dcdf06c17a3'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'user_inputs',
        sa.Column('id', psql.UUID(as_uuid=True), primary_key=True, default=sa.text('uuid_generate_v4()')),
        sa.Column('user_id', psql.UUID(as_uuid=True), nullable=True),
        sa.Column('plot', sa.Text(), nullable=False),
        sa.Column('setting', sa.Text(), nullable=False),
        sa.Column('theme', sa.Text(), nullable=False),
        sa.Column('conflict', sa.Text(), nullable=False),
        sa.Column('additional_preferences', psql.JSONB(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now()),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    )

def downgrade():
    op.drop_table('user_inputs')
