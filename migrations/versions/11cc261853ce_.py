"""empty message

Revision ID: 11cc261853ce
Revises: 
Create Date: 2023-02-03 20:25:47.379240

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '11cc261853ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=120), nullable=False),
    sa.Column('email', sa.String(length=120), nullable=False),
    sa.Column('password', sa.String(length=80), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('apellido', sa.String(length=80), nullable=False),
    sa.Column('contacto', sa.String(length=80), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('mascotas',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('genero', sa.String(length=120), nullable=False),
    sa.Column('tamaño', sa.String(length=120), nullable=False),
    sa.Column('color', sa.String(length=80), nullable=False),
    sa.Column('nombre', sa.String(length=80), nullable=False),
    sa.Column('edad', sa.String(length=80), nullable=False),
    sa.Column('raza', sa.String(length=80), nullable=False),
    sa.Column('estado', sa.String(length=80), nullable=False),
    sa.Column('especie', sa.String(length=80), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('genero'),
    sa.UniqueConstraint('tamaño')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('mascotas')
    op.drop_table('usuario')
    # ### end Alembic commands ###
