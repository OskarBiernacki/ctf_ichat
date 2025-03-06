from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

app = Flask('ichat_ctf')
app.config['SECRET_KEY'] = 'random_secret_key_2929271738391'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SESSION_COOKIE_HTTPONLY'] = False 

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from ichat import routes