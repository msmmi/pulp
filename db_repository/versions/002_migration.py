from sqlalchemy import *
from migrate import *
import datetime

from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', BigInteger, primary_key=True, nullable=False),
    Column('name', String(length=64), nullable=False),
    Column('email', String(length=120), nullable=False),
    Column('username', String(length=120), nullable=False),
    Column('password', String(length=120)),
    Column('admin', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('avatar', String(length=200)),
    Column('liquid_cash', Integer, nullable=False, default=ColumnDefault(0)),
    Column('cash_in_play', Integer, nullable=False, default=ColumnDefault(0)),
    Column('created_at', DateTime, nullable=False, default=ColumnDefault(datetime.datetime(2018, 8, 27, 3, 50, 36, 720562))),
    Column('deactivated_at', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['password'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].columns['password'].drop()
