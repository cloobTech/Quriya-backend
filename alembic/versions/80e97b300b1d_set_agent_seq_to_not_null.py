"""set agent_seq to Not Null

Revision ID: 80e97b300b1d
Revises: 727710f71b1d
Create Date: 2026-01-30 00:04:22.835619

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80e97b300b1d'
down_revision: Union[str, Sequence[str], None] = '727710f71b1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    """Set agent_seq default value and make non-nullable"""
    
    # 1. First, handle any existing NULL values
    conn = op.get_bind()
    result = conn.execute(sa.text("SELECT COUNT(*) FROM projects WHERE agent_seq IS NULL"))
    null_count = result.scalar()
    
    if null_count and null_count > 0:
        print(f"Found {null_count} rows with NULL agent_seq, setting to 0")
        op.execute("UPDATE projects SET agent_seq = 0 WHERE agent_seq IS NULL")
    
    # 2. Clean up any leftover temporary tables
    op.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name LIKE '_alembic_tmp_projects'
    """)
    
    # Drop if exists
    op.execute('DROP TABLE IF EXISTS _alembic_tmp_projects')
    
    # 3. Apply schema changes in batch mode
    with op.batch_alter_table('projects') as batch_op:
        # This recreates the table with the new constraints
        batch_op.alter_column(
            'agent_seq',
            existing_type=sa.Integer(),
            nullable=False,
            server_default='0'
        )
    
    # 4. Verify the change
    result = conn.execute(sa.text("""
        SELECT COUNT(*) 
        FROM pragma_table_info('projects') 
        WHERE name='agent_seq' AND "notnull"=1 AND dflt_value='0'
    """))
    
    if result.scalar() == 1:
        print("Successfully updated agent_seq column")
    else:
        print("Warning: agent_seq column may not have been updated correctly")


def downgrade():
    """Revert agent_seq changes"""
    
    # Clean up temporary tables
    op.execute('DROP TABLE IF EXISTS _alembic_tmp_projects')
    
    with op.batch_alter_table('projects') as batch_op:
        batch_op.alter_column(
            'agent_seq',
            existing_type=sa.Integer(),
            nullable=True,
            server_default=None
        )