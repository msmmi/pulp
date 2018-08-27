import datetime

from app import db

# A visual schema lives at https://www.dbdesigner.net/designer/schema/188128


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


class Wager(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    short_description = db.Column(db.String(120))
    long_description = db.Column(db.VARCHAR, nullable=False)

    # 'group' determines if the wager is eligible for the Group Strategy if true and Head to Head if false.
    group = db.Column(db.Boolean, default=False, nullable=False)
    # An activated wager is one that has action on both sides. For instance, when you propose a wager and take one side,
    # it is not activated until someone else takes the other side.
    activated = db.Column(db.Boolean, default=False, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    deactivated_at = db.Column(db.DateTime)

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="user_wagers")


class TakenWager(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    # wager_true declares if the user thinks the wager will turn out to be true.
    # For example, on an over/under bet of Julio Jones getting 300 yards, the wager_true would be true.
    # For Dolphins vs Patriots, Dolphins -5, wager_true would be true if the user thinks the Dolphins will win by more
    # than 5.
    wager_true = db.Column(db.Boolean, nullable=False)
    bet_amount = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    user_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    user = db.relationship("User", backref="user_taken_wagers")

    wager_id = db.Column(db.BigInteger, db.ForeignKey('wager.id'))
    wager = db.relationship("Wager", backref="taken_wagers")


class Result(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)

    wager_result = db.Column(db.SmallInteger, nullable=False)
    evidence = db.Column(db.VARCHAR)

    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)

    created_by_id = db.Column(db.BigInteger, db.ForeignKey('user.id'))
    created_by = db.relationship("User")

    wager_id = db.Column(db.BigInteger, db.ForeignKey('wager.id'))
    wager = db.relationship("Wager", backref="wager_results")
