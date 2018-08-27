import json
from urllib3.exceptions import HTTPError

import flask
from flask import redirect
from flask import request
from flask import session as flask_session
from flask import url_for

from app import app, db
from app.lib.user_lib import create_user
from app.models import User
from app.views.handlers.auth_handler import get_google_auth
from config import Auth


@app.route('/gCallback')
def callback():
    current_user = flask.g.user
    session = db.session

    # Redirect user to home page if already logged in.
    if current_user is not None and current_user.is_authenticated:
        return redirect(url_for('index'))
    if 'error' in request.args:
        if request.args.get('error') == 'access_denied':
            return 'You are denied access.'
        return 'Error encountered.'
    if 'code' not in request.args and 'state' not in request.args:
        return redirect(url_for('login'))
    else:
        # Execution reaches here when user has
        # successfully authenticated our app.
        google = get_google_auth(state=flask_session['oauth_state'])
        try:
            token = google.fetch_token(
                Auth.TOKEN_URI,
                client_secret=Auth.CLIENT_SECRET,
                authorization_response=request.url.replace('http://', 'https://'),
            )
        except HTTPError:
            return 'HTTPError occurred.'
        google = get_google_auth(token=token)
        # todo: cool stuff in here
        resp = google.get(Auth.USER_INFO)
        if resp.status_code == 200:
            user_data = resp.json()
            email = user_data['email']
            user = User.query.filter_by(email=email).first()
            if user is None:
                user = User(
                    name=user_data['name'] or user_data['email'].split('@')[0].capitalize(),
                    email=email,
                    avatar=user_data['picture']
                )
            user.tokens = json.dumps(token)
            session.add(user)
            session.commit()
            return redirect(url_for('index'))
        return 'Could not fetch your information.'


@app.route('/create_user', methods=['POST'])
def create_user_view():
    current_user = flask.g.user
    if current_user.is_authenticated:
        return 'You must not be logged in to create a user', 400

    session = db.session

    data = request.get_json()

    user = create_user(data)

    session.add(user)
    session.commit()

    return 'ok', 200
