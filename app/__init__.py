import os
from pathlib import Path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow


BASE_DIR = Path(__file__).parent.parent.resolve()
db = SQLAlchemy()
ma = Marshmallow()


def create_app(config=None):
    # create and configure the app
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{BASE_DIR / "empls.db"}'

    db.init_app(app)
    with app.app_context():
        from app.models import Employee
        db.create_all()
        db.session.commit()

    ma.init_app(app)

    # apply the blueprints to the app
    from . import views
    app.register_blueprint(views.bp)
    return app
