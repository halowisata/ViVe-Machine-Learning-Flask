# app.py

from flask import Flask
from config import config

def create_app(env='development'):
    app = Flask(__name__)
    app.config.from_object(config[env])
    
    # Additional app setup and routes...
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
