import os

from pathlib import Path
from dotenv import load_dotenv, find_dotenv
from envparse import env

try:
    load_dotenv(find_dotenv(raise_error_if_not_found=True))
except IOError as e:
    print('No .env file found, using defaults.')

ROOT_DIR = Path().resolve()
FIXTURES_DIR = ROOT_DIR / 'fixtures'

# Where the model server will be listening
TRANSLATE_HOST = os.getenv('HOST', '0.0.0.0')
TRANSLATE_PORT = env.int('PORT', default=5005)

# Database URI
DB_PASSWORD = os.getenv('DATABASE_PASSWORD', 'secret')
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../politiciansBD.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False



TESTING = False

SECRET_KEY = "acnkla9999qeacno5kcbasfrtgtrgtrgdvsdvblrsivbsevisekqwl"
