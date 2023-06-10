# app/config.py

# Configuration settings for the Flask app
# This file contains classes or variables that define various configuration options for your application
# Modify or add additional configuration settings based on your specific requirements


class Config:
    SECRET_KEY = 'your_secret_key_here'
    SQLALCHEMY_DATABASE_URI = 'your_database_uri_here'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
