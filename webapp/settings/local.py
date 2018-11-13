from webapp.settings.base import *  # noqa
from webapp.settings.base import os

UNBABEL_SANDBOX = True

# Should be generate a new one on https://ngrok.com/ to use callback functionality in localhost
# ngrok should redirect to 5005 port
CALLBACK_URL = os.getenv('URL_CALLBACK', '0.0.0.0')
