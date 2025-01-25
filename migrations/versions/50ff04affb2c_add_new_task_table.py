"""Add new task table

Revision ID: 50ff04affb2c
Revises: 
Create Date: 2025-01-20 12:41:32.596578

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "50ff04affb2c"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
               CREATE TABLE Task (
                    id SERIAL PRIMARY KEY,
                    repo_url varchar(255),
                    pr_number int,
                    auth_token varchar(255),
                    status varchar(30),
                    created_at TIMESTAMPTZ DEFAULT NOW(),
                    results JSONB NOT NULL DEFAULT '{}'::jsonb
                );
    """
    )


def downgrade() -> None:
    pass
