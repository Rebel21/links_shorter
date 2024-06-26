"""initial migration

Revision ID: b218e02c0edd
Revises: 
Create Date: 2024-05-02 23:33:33.298128

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'b218e02c0edd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('url',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('original_url', sa.String(), nullable=False),
                    sa.PrimaryKeyConstraint('id')
                    )
    op.create_table('short_url',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('url_id', sa.Integer(), nullable=False),
                    sa.Column('number_of_transitions', sa.Integer(), nullable=True),
                    sa.Column('short_url', sa.String(), nullable=False),
                    sa.Column('qr_code', sa.String(), nullable=False),
                    sa.Column('is_activ', sa.Boolean(), nullable=False),
                    sa.ForeignKeyConstraint(['url_id'], ['url.id'], ondelete='CASCADE'),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('short_url')
                    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('short_url')
    op.drop_table('url')
    # ### end Alembic commands ###
