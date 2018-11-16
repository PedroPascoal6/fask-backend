import os
from flask import Flask, render_template

from webapp.models import db


def create_app():
    print('Running with settings from: {}'
          .format(os.environ['APP_SETTINGS_FILE']))

    flask_app = Flask(__name__)
    flask_app.config.from_envvar('APP_SETTINGS_FILE')
    flask_app.secret_key = flask_app.config['SECRET_KEY']

    with flask_app.app_context():
        db.init_app(flask_app)  # Required by Flask-SQLAlchemy
        if not flask_app.config['TESTING']:
            db.create_all()
    return flask_app
