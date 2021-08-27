# -*- coding: utf-8 -*-
#esse aquivo init eh nosso arquivo construtor do nosso app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
#from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user

#para o heroku
import os

app = Flask(__name__)
app = Flask(__name__,template_folder='templates')# embora redudante, especifiquei ao flask a pasta de template por causa do heroku
app.config.from_object('config')
app.config["SECRET_KEY"] = "secret"

db = SQLAlchemy(app)
migrate = Migrate(app,db)
manager = Manager(app)
manager.add_command('db',MigrateCommand)

from app.controllers import default