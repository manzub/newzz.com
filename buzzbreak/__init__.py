from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail

login_manager = LoginManager()
app = Flask(__name__)
app.config.from_object('config.config.DevelopmentConfigs')
db = SQLAlchemy(app)
Migrate(app,db)
mail = Mail(app)
login_manager.init_app(app)
login_manager.login_view = 'login'
