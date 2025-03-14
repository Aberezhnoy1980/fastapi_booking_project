"""add unique attr to email column

Revision ID: b670c6e5503d
Revises: e5a9c2598b9b
Create Date: 2025-03-12 09:02:26.858440

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "b670c6e5503d"
down_revision: Union[str, None] = "e5a9c2598b9b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint(None, "users", type_="unique")
