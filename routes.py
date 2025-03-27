from flask import redirect, render_template, request, url_for
from app import app  # Import the app object from app.py
from models import Athlete
from database_setup import db


# Route for the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/athletes')
def manage_athletes():
    return render_template('athletes/manage_athletes.html')


@app.route('/coaches')
def manage_coaches():
    return render_template('coaches/manage_coaches.html')


@app.route('/teams')
def manage_teams():
    return render_template('teams/manage_teams.html')



@app.route('/tournaments')
def manage_tournaments():
    return render_template('tournaments/manage_tournaments.html')


