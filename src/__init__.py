from flask import Flask
import os

app = Flask(__name__)

DEBUG = True
app.secret_key = "Secret"
app.config['SESSION_TYPE'] = 'filesystem'
WTF_CSRF_ENABLED = True

# This line adds the hasura example routes form the hasura.py file.
# Delete these two lines, and delete the file to remove them from your project
from .hasura import hasura_examples
app.register_blueprint(hasura_examples)

from .views import *
