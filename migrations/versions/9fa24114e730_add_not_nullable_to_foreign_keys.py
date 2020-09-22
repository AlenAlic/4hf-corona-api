"""add_not_nullable_to_foreign_keys

Revision ID: 9fa24114e730
Revises: c74668935352
Create Date: 2020-09-22 10:34:35.805891

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9fa24114e730'
down_revision = 'c74668935352'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dancing_class_couple', 'dancing_class_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('dancing_class_couple', 'partner_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('dancing_class_couple', 'person_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('dancing_class_person', 'dancing_class_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    op.alter_column('dancing_class_person', 'person_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('dancing_class_person', 'person_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('dancing_class_person', 'dancing_class_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('dancing_class_couple', 'person_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('dancing_class_couple', 'partner_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    op.alter_column('dancing_class_couple', 'dancing_class_id',
               existing_type=mysql.INTEGER(display_width=11),
               nullable=True)
    # ### end Alembic commands ###