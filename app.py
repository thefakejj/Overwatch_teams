from os import getenv
from flask import Flask

ow_app = Flask(__name__)
ow_app.secret_key = getenv("SECRET_KEY")

import routes