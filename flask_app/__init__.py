from flask import Flask 
from flask_bcrypt import Bcrypt

app = Flask(__name__)

BCRYPT = Bcrypt(app)
DATABASE = 'marketing_platform_db'

app.secret_key = 'hushhush'