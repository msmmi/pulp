import datetime
from enum import Enum

import sqlalchemy

from app import db

# A visual schema lives at https://www.dbdesigner.net/designer/schema/196986


class User(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120))

    admin = db.Column(db.Boolean, default=False, nullable=False)
    avatar = db.Column(db.String(200))

    liquid_cash = db.Column(db.Integer, default=0, nullable=False)
    cash_in_play = db.Column(db.Integer, default=0, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    deactivated_at = db.Column(db.DateTime)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.deactivated_at is not None

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id

    @property
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'username': self.username,
            'admin': self.admin,
            'avatar': self.avatar,
            'active': self.deactivated_at is not None,
            'created_at': str(self.created_at) if self.created_at else None,
            'liquid_cash': self.liquid_cash,
            'cash_in_play': self.cash_in_play,
        }


class Event(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    # if unknown, leave blank. Then when the event starts, to close betting, put start_datetime as now
    start_datetime = db.Column(db.DateTime)
    event_over = db.Column(db.Boolean, nullable=False, default=False)

    short_description = db.Column(db.String(120))
    long_description = db.Column(db.VARCHAR)
    event_image = db.Column(db.VARCHAR)

    line = db.Column(db.Float, default=0)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    deactivated_at = db.Column(db.DateTime)


class Wager(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    short_description = db.Column(db.String(120))
    long_description = db.Column(db.VARCHAR, nullable=False)

    # string description of what side you're betting on (Miami Dolphins)
    side_1_name = db.Column(db.String(120))
    side_2_name = db.Column(db.String(120))

    # the Wager should only get shown when the line on the Wager matches the line on the Event
    line = db.Column(db.Float, default=0)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    deactivated_at = db.Column(db.DateTime)

    created_by_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    created_by = db.relationship("User", backref="user_created_wagers")

    event_id = db.Column(db.BigInteger, db.ForeignKey('event.id'))
    event = db.relationship("Event", backref="event_wagers")


class TakenWager(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    bet_on_side_1 = db.Column(db.Boolean, nullable=False)
    bet_amount = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="user_taken_wagers")

    wager_id = db.Column(db.BigInteger, db.ForeignKey('wager.id'))
    wager = db.relationship("Wager", backref="taken_wagers")


class MatchedWager(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    amount = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    taken_wager_1_id = db.Column(db.BigInteger, db.ForeignKey('taken_wager.id', ondelete="CASCADE"))
    taken_wager_2_id = db.Column(db.BigInteger, db.ForeignKey('taken_wager.id', ondelete="CASCADE"))

    taken_wager_1 = db.relationship(
        "TakenWager",
        foreign_keys=[taken_wager_1_id],
        backref=sqlalchemy.orm.backref('taken_1'))
    taken_wager_2 = db.relationship(
        "TakenWager",
        foreign_keys=[taken_wager_2_id],
        backref=sqlalchemy.orm.backref('taken_2'))


class WagerResult(Enum):
    Undetermined = 0
    Side1Wins = 1
    Side2Wins = 2
    Push = 3
    UnderArbitration = 4


class Result(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    wager_result = db.Column(db.SmallInteger, nullable=False, default=WagerResult.Undetermined)
    evidence = db.Column(db.VARCHAR)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    created_by_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    created_by = db.relationship("User")

    wager_id = db.Column(db.BigInteger, db.ForeignKey('wager.id'))
    wager = db.relationship("Wager", backref="wager_results")
