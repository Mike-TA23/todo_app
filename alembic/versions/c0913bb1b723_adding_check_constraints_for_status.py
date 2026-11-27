"""adding check constraints for status

Revision ID: c0913bb1b723
Revises: 2c7c2fd5aac8
Create Date: 2026-11-27 16:16:45.671323

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c0913bb1b723'
down_revision: Union[str, Sequence[str], None] = '2c7c2fd5aac8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_check_constraint(
        "ck_tasks_status",
        "tasks",
        "status IN ('pending', 'in_progress', 'completed')",
    )


def downgrade():
    op.drop_constraint(
        "ck_tasks_status",
        "tasks",
        type_="check",
    )