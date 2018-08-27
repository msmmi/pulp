import flask
from flask_jwt import jwt_required, current_identity

from app import app
from app.views.handlers.auth_handler import get_google_authorization_url


@app.route('/')
@app.route('/index')
def index():
    return flask.render_template('index.html',
                                 title='Home',
                                 auth_url=get_google_authorization_url())


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity