import os
# from datetime import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask.ext.moment import Moment

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# Configure database
app.config['SECRET_KEY'] = '\xb8m\xa0X\x7fRJ\xdd]\xcb\x13\x8be\xad0\xb4@\xca\xdd|\xe7\xc3\x02\xda'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'thermos.db')
app.config['DEBUG'] = True
db = SQLAlchemy(app)

# Configure authentication
login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.init_app(app)

# for displaying timestamps
moment = Moment(app)

import models
import views