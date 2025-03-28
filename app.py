from flask import Flask
from database_setup import db
from routes import *

# Initialize Flask app
app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recruitment.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the app
db.init_app(app)

# Import all the routes from routes.py
from routes import *

# Import the models after initializing db
from models import Athlete, Tournament, Team, tournament_team


# Create the database tables within an app context
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)


