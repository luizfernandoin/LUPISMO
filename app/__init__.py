from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
socketio = SocketIO(app)

app.config.from_object('config')
db = SQLAlchemy(app)

migrate = Migrate(app, db)

from .controllers import default