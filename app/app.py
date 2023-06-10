# app/app.py

# Main entry point of the Flask application
# This file contains the code to create and run the Flask app
# Modify or add routes, middleware, and other necessary setup code here


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
