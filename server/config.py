from flask import Flask
from flask_sqlalchemy import SQLAchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.secret_key = "secret_squirrel_key"

app.config["AQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.json.compact = False

db = SQLAchemy()

bcrypt = Bcrypt(app)

migrate = Migrate(app, db)

api = Api(app)