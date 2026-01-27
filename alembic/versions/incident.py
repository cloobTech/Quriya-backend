"""add incident_id to media table

Revision ID: add_incident_id_media
Revises: cb72b696b03b
Create Date: 2026-01-27 12:45:00
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "add_incident_id_media"
down_revision = "4d67eeaff53c"
branch_labels = None
depends_on = None


def upgrade() -> None:
    conn = op.get_bind()

    # Check if column already exists (safe for multiple runs)
    try:
        conn.execute(text("SELECT incident_id FROM media LIMIT 1"))
        print("Column incident_id already exists in media")
    except:
        # Add column as nullable FK
        with op.batch_alter_table("media") as batch_op:
            batch_op.add_column(
                sa.Column(
                    "incident_id",
                    sa.String(length=60),
                    nullable=True,
                )
            )
            # Create foreign key constraint with an explicit name
            batch_op.create_foreign_key(
                "fk_media_incident_id",  # Explicit constraint name
                "incidents",
                ["incident_id"],
                ["id"],
                ondelete="SET NULL"
            )
            # Optional: add an index for faster queries
            batch_op.create_index("ix_media_incident_id", ["incident_id"])


def downgrade() -> None:
    with op.batch_alter_table("media") as batch_op:
        batch_op.drop_index("ix_media_incident_id")
        batch_op.drop_constraint("fk_media_incident_id", type_="foreignkey")
        batch_op.drop_column("incident_id")