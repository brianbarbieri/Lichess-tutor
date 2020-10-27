#!/usr/bin/python3

from flask import Flask
from flask_session import Session
from app.config import Config

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    app.config["SECRET_KEY"] = Config.WTF_CSRF_SECRET_KEY
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app) #server side sessions
    
    from app.routes import main

    app.register_blueprint(main)

    return app