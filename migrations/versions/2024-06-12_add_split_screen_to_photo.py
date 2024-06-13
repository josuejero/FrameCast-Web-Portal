from alembic import op
import sqlalchemy as sa

revision = 'add_split_screen_to_photo'
down_revision = 'c7e6147d997f'

def upgrade():
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.add_column(sa.Column('split_screen_x', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('split_screen_y', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('split_screen_width', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('split_screen_height', sa.Integer(), nullable=True))

def downgrade():
    with op.batch_alter_table('photo', schema=None) as batch_op:
        batch_op.drop_column('split_screen_x')
        batch_op.drop_column('split_screen_y')
        batch_op.drop_column('split_screen_width')
        batch_op.drop_column('split_screen_height')
