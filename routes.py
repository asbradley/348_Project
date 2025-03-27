from flask import redirect, render_template, request, url_for
from app import app  # Import the app object from app.py
from models import Athlete, Team
from database_setup import db


# Route for the welcome page
@app.route('/')
def welcome():
    return render_template('welcome.html')


@app.route('/athletes')
def manage_athletes():

    athletes = Athlete.query.all()
    return render_template('athletes/manage_athletes.html', athletes=athletes)


@app.route('/coaches')
def manage_coaches():
    return render_template('coaches/manage_coaches.html')


@app.route('/teams')
def manage_teams():
    
    # Get all teams
    teams = Team.query.all()
    return render_template('teams/manage_teams.html', teams=teams)



@app.route('/tournaments')
def manage_tournaments():
    return render_template('tournaments/manage_tournaments.html')



@app.route('/add_athlete', methods=['GET', 'POST'])
def add_athlete():
    
    if request.method == 'POST':
        
        # Add the new athlete if can be
        name = request.form['name']
        age = request.form['age']
        sport = request.form['sport']
        height = request.form['height']
        weight = request.form['weight']
        gender = request.form['gender']
        position = request.form['position']
        team_id = request.form['team_id']
        points_per_game = request.form['points_per_game']
        rebounds_per_game = request.form['rebounds_per_game']
        assists_per_game = request.form['assists_per_game']
        blocks_per_game = request.form['blocks_per_game']
        steals_per_game = request.form['steals_per_game']
        field_goal_percentage = request.form['field_goal_percentage']
        three_point_percentage = request.form['three_point_percentage']
        free_throw_percentage = request.form['free_throw_percentage']

        # Create a new Athlete object
        new_athlete = Athlete(
            name=name,
            age=age,
            sport=sport,
            height=height,
            weight=weight,
            gender=gender,
            position=position,
            team_id=team_id,
            points_per_game=points_per_game,
            rebounds_per_game=rebounds_per_game,
            assists_per_game=assists_per_game,
            blocks_per_game=blocks_per_game,
            steals_per_game=steals_per_game,
            field_goal_percentage=field_goal_percentage,
            three_point_percentage=three_point_percentage,
            free_throw_percentage=free_throw_percentage
        )

        db.session.add(new_athlete)
        db.session.commit()

        return render_template(
            'success.html',
            message="Athlete added successfully!",
            redirect_url = url_for('manage_athletes'),
            redirect_text = 'Go back to Manage Athletes'
        )

    # Fetch all teams from database

    teams = Team.query.all()

    return render_template('athletes/add_athlete.html', teams=teams)


@app.route('/edit_athlete/<int:athlete_id>', methods=['GET', 'POST'])
def edit_athlete(athlete_id):
    athlete = Athlete.query.get_or_404(athlete_id)


    if request.method == 'POST':
        # Update athlete stats with form data
        athlete.points_per_game = request.form['points_per_game']
        athlete.rebounds_per_game = request.form['rebounds_per_game']
        athlete.assists_per_game = request.form['assists_per_game']
        athlete.blocks_per_game = request.form['blocks_per_game']
        athlete.steals_per_game = request.form['steals_per_game']
        athlete.field_goal_percentage = request.form['field_goal_percentage']
        athlete.three_point_percentage = request.form['three_point_percentage']
        athlete.free_throw_percentage = request.form['free_throw_percentage']
        athlete.team_id = request.form['team_id']

        # Commit changes to the database
        db.session.commit()

        return render_template(
            'success.html',
            message="Athlete Editted successfully!",
            redirect_url = url_for('manage_athletes'),
            redirect_text = 'Go back to Manage Athletes'
        )
    
    teams = Team.query.all()
    return render_template('athletes/edit_athlete.html', athlete=athlete, teams=teams)


@app.route('/delete_athlete/<int:athlete_id>', methods=['POST'])
def delete_athlete(athlete_id):
    athlete = Athlete.query.get_or_404(athlete_id)
    db.session.delete(athlete)
    db.session.commit()

    return render_template(
        'success.html',
        message="Athlete Deleted Successfully!",
        redirect_url = url_for('manage_athletes'),
        redirect_text = "Go back to Manage Athletes"
    )



@app.route('/delete_teams/<int:team_id>', methods=['POST'])
def delete_team(team_id):
    team = Team.query.get_or_404(team_id)
   
    # Set team_id to NULL for all athletese bleonging to the team being deleted
    Athlete.query.filter_by(team_id=team_id).update({'team_id': None})

    # Delete the team
    db.session.delete(team)
    db.session.commit()

    return render_template(
        'success.html',
        message="Team Deleted Successfully!",
        redirect_url = url_for('manage_teams'),
        redirect_text = "Go back to Manage Teams"
    )










