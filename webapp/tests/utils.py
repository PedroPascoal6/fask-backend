import os

from flask_testing import TestCase

from webapp.factory import create_app, db
from webapp.models import generate_data


class MyTest(TestCase):
    SQLALCHEMY_DATABASE_URI = "sqlite:///../politiciansBD.db"
    TESTING = True

    def create_app(self):
        # pass in test configuration
        os.environ['APP_SETTINGS_FILE'] = 'settings/local.py'
        return create_app()

    def setUp(self):
        generate_data(40)
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
