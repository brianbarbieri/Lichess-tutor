#!/usr/bin/python3

from flask import Flask
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = Config.WTF_CSRF_SECRET_KEY

    from app.routes import main

    app.register_blueprint(main)

    return app