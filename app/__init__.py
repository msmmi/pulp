from flask import Flask
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy

from app.lib.logging_lib import init_logs, set_rotating_logs

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

jwt = JWTManager(app)

from app import views, models


@jwt.user_claims_loader
def add_claims_to_access_token(email):
    session = db.session
    user = session.query(models.User).filter(models.User.email == email).first()
    if not user:
        app.logger.warn('No user found in add_claims_to_access_token for user email %s', email)
        return {}
    return user.dict


init_logs()
set_rotating_logs(app)
