from flask import Flask
from config import Config
from database import db
from flask_cors import CORS  # Import CORS here

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)

    from routes import bp
    app.register_blueprint(bp)

    return app
