"""adding table again

Revision ID: 9036040d046e
Revises: 37b9c401cfa2
Create Date: 2020-03-20 20:02:55.778267

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9036040d046e'
down_revision = '37b9c401cfa2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('playlist',
    sa.Column('playlist_id', sa.Integer(), nullable=False),
    sa.Column('playlist_title', sa.String(length=200), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('created_by', sa.Integer(), nullable=False),
    sa.Column('emotion', sa.String(length=10), nullable=True),
    sa.PrimaryKeyConstraint('playlist_id')
    )
    op.create_table('track',
    sa.Column('track_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('duration', sa.String(length=5), nullable=False),
    sa.Column('file', sa.String(length=1000), nullable=False),
    sa.Column('emotion', sa.String(length=10), nullable=False),
    sa.PrimaryKeyConstraint('track_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=15), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=True),
    sa.Column('password', sa.String(length=80), nullable=True),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.add_column('track_group', sa.Column('playlist_id', sa.Integer(), nullable=False))
    op.add_column('track_group', sa.Column('tg_id', sa.Integer(), nullable=False))
    op.add_column('track_group', sa.Column('track_id', sa.Integer(), nullable=False))
    op.drop_column('track_group', 'id')
    op.drop_column('track_group', 'Playlist_id')
    op.drop_column('track_group', 'Track_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('track_group', sa.Column('Track_id', sa.INTEGER(), nullable=False))
    op.add_column('track_group', sa.Column('Playlist_id', sa.INTEGER(), nullable=False))
    op.add_column('track_group', sa.Column('id', sa.INTEGER(), nullable=False))
    op.drop_column('track_group', 'track_id')
    op.drop_column('track_group', 'tg_id')
    op.drop_column('track_group', 'playlist_id')
    op.drop_table('user')
    op.drop_table('track')
    op.drop_table('playlist')
    # ### end Alembic commands ###
