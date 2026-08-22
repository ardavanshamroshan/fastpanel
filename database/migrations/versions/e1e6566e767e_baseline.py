"""baseline

Revision ID: e1e6566e767e
Revises: c114bb2f54b7
Create Date: 2026-08-12 11:39:55.237388

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e1e6566e767e'
down_revision: Union[str, Sequence[str], None] = 'c114bb2f54b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
