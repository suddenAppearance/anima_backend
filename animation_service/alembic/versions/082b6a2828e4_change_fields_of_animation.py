"""change fields of Animation

Revision ID: 082b6a2828e4
Revises: f5e8656f50e9
Create Date: 2022-12-07 20:49:40.549618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '082b6a2828e4'
down_revision = 'f5e8656f50e9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animation', sa.Column('file_id', postgresql.UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_animation_author_id'), 'animation', ['author_id'], unique=False)
    op.create_index(op.f('ix_animation_file_id'), 'animation', ['file_id'], unique=False)
    op.drop_column('animation', 'minio_file_url')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('animation', sa.Column('minio_file_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_index(op.f('ix_animation_file_id'), table_name='animation')
    op.drop_index(op.f('ix_animation_author_id'), table_name='animation')
    op.drop_column('animation', 'file_id')
    # ### end Alembic commands ###
