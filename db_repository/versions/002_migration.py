from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
event = Table('event', post_meta,
    Column('id', BigInteger, primary_key=True, nullable=False),
    Column('name', String(length=120), nullable=False),
    Column('start_datetime', DateTime),
    Column('event_over', Boolean, nullable=False, default=ColumnDefault(False)),
    Column('short_description', String(length=120)),
    Column('long_description', VARCHAR),
    Column('event_image', VARCHAR),
    Column('line', Float, default=ColumnDefault(0)),
    Column('created_at', DateTime, nullable=False),
    Column('deactivated_at', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].columns['event_image'].create()
    post_meta.tables['event'].columns['long_description'].create()
    post_meta.tables['event'].columns['short_description'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['event'].columns['event_image'].drop()
    post_meta.tables['event'].columns['long_description'].drop()
    post_meta.tables['event'].columns['short_description'].drop()
