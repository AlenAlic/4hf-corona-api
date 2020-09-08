"""add_notes_column

Revision ID: c273e9da4fff
Revises: a3695fe24315
Create Date: 2020-09-08 14:14:58.035943

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c273e9da4fff'
down_revision = 'a3695fe24315'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('dancing_class_person', sa.Column('notes', sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('dancing_class_person', 'notes')
    # ### end Alembic commands ###
