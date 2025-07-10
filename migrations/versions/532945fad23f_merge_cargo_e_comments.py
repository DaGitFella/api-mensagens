"""merge cargo e comments

Revision ID: 532945fad23f
Revises: a437a6da2771, f837ea56fb45
Create Date: 2025-07-10 18:14:48.885041

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '532945fad23f'
down_revision: Union[str, None] = ('a437a6da2771', 'f837ea56fb45')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
