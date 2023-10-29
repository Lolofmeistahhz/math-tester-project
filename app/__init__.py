from flask_sqlalchemy import SQLAlchemy
from flask import Flask

app = Flask(__name__)

app.config.from_object('config')

db: SQLAlchemy = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
app.config["SQLALCHEMY_POOL_RECYCLE"] = -1
db.init_app(app)
with app.app_context():
    db.create_all()


from app import routes