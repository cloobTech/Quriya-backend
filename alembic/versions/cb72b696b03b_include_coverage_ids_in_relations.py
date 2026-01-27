"""include coverage ids in relations

Revision ID: 4d67eeaff53c
Revises: 
Create Date: 2026-01-13 20:19:41.551528

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text


# revision identifiers, used by Alembic.
revision = '4d67eeaff53c'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade schema."""
    conn = op.get_bind()
    
    # Check if columns already exist before adding them
    
    # Check for state_coverage_id in project_lga_coverage
    try:
        conn.execute(text("SELECT state_coverage_id FROM project_lga_coverage LIMIT 1"))
        print("Column state_coverage_id already exists in project_lga_coverage")
    except:
        # Column doesn't exist, add it
        with op.batch_alter_table('project_lga_coverage') as batch_op:
            batch_op.add_column(sa.Column('state_coverage_id', sa.String(length=60), nullable=True))
    
    # Check for lga_coverage_id in project_ward_coverage
    try:
        conn.execute(text("SELECT lga_coverage_id FROM project_ward_coverage LIMIT 1"))
        print("Column lga_coverage_id already exists in project_ward_coverage")
    except:
        with op.batch_alter_table('project_ward_coverage') as batch_op:
            batch_op.add_column(sa.Column('lga_coverage_id', sa.String(length=60), nullable=True))
    
    # Check for ward_coverage_id in project_pu_coverage
    try:
        conn.execute(text("SELECT ward_coverage_id FROM project_pu_coverage LIMIT 1"))
        print("Column ward_coverage_id already exists in project_pu_coverage")
    except:
        with op.batch_alter_table('project_pu_coverage') as batch_op:
            batch_op.add_column(sa.Column('ward_coverage_id', sa.String(length=60), nullable=True))
    
    # Try to drop the old table if it exists
    try:
        op.drop_table('member_ward_coverage')
    except:
        print("Table member_ward_coverage doesn't exist or can't be dropped")
    
    # Try to remove old column from project_members
    try:
        with op.batch_alter_table('project_members') as batch_op:
            batch_op.drop_column('ward_coverage_id')
    except:
        print("Column ward_coverage_id doesn't exist in project_members or can't be dropped")


def downgrade() -> None:
    """Downgrade schema."""
    # Recreate old table
    op.create_table(
        'member_ward_coverage',
        sa.Column('member_id', sa.String(length=60), nullable=False),
        sa.Column('ward_coverage_id', sa.String(length=60), nullable=True),
        sa.Column('id', sa.String(length=60), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['member_id'], ['project_members.id']),
        sa.ForeignKeyConstraint(['ward_coverage_id'], ['project_ward_coverage.id']),
        sa.PrimaryKeyConstraint('member_id', 'id'),
        sa.UniqueConstraint('member_id', 'ward_coverage_id')
    )
    
    # Remove new columns if they exist
    try:
        with op.batch_alter_table('project_pu_coverage') as batch_op:
            batch_op.drop_column('ward_coverage_id')
    except:
        print("Column ward_coverage_id doesn't exist in project_pu_coverage")
    
    try:
        with op.batch_alter_table('project_ward_coverage') as batch_op:
            batch_op.drop_column('lga_coverage_id')
    except:
        print("Column lga_coverage_id doesn't exist in project_ward_coverage")
    
    try:
        with op.batch_alter_table('project_lga_coverage') as batch_op:
            batch_op.drop_column('state_coverage_id')
    except:
        print("Column state_coverage_id doesn't exist in project_lga_coverage")
    
    # Add back old column
    try:
        with op.batch_alter_table('project_members') as batch_op:
            batch_op.add_column(sa.Column('ward_coverage_id', sa.String(length=60), nullable=True))
    except:
        print("Could not add ward_coverage_id to project_members")