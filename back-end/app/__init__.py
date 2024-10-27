from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)  # This will enable CORS for all routes
    # Import and register your routes here
    from .app import scrape_walmart
    app.register_blueprint(scrape_walmart)

    return app
