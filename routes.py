from flask import redirect, render_template, request, url_for
from app import app  # Import the app object from app.py
from models import Athlete, Team
from database_setup import db
from sqlalchemy import text


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


@app.route('/reports')
def reports():
    return render_template('reports.html')



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


@app.route('/add_team', methods = ['GET', 'POST'])
def add_team():
    
    if request.method == 'POST':
        name = request.form['name']
        city = request.form['city']
        wins = request.form['wins']
        losses = request.form['losses']


        # Create new team here
        new_team = Team(
            name=name,
            city=city,
            wins=wins,
            losses=losses
        )

        db.session.add(new_team)
        db.session.commit()

        return render_template(
            'success.html',
            message="Team added successfully!",
            redirect_url = url_for('manage_teams'),
            redirect_text = 'Go back to Manage Teams'
        )
    
    return render_template('teams/add_team.html')



from sqlalchemy import text

@app.route('/reports/athletes', methods=['GET', 'POST'])
def athlete_report():
    # Fetch all teams for the dropdown
    teams_result = db.session.execute(text("SELECT * FROM team"))
    teams = [dict(row._mapping) for row in teams_result]

    # Start raw SQL query with text()
    sql = text("""
        SELECT a.* FROM athlete a
        LEFT JOIN team t ON a.team_id = t.id
        WHERE 1 = 1
    """)
    
    # Start with a string to build upon
    sql_str = sql.text
    params = {}

    # Add filters
    if request.args.get("min_age"):
        sql_str += " AND a.age >= :min_age"
        params["min_age"] = int(request.args["min_age"])
    if request.args.get("max_age"):
        sql_str += " AND a.age <= :max_age"
        params["max_age"] = int(request.args["max_age"])
    if request.args.get("min_ppg"):
        sql_str += " AND a.points_per_game >= :min_ppg"
        params["min_ppg"] = float(request.args["min_ppg"])
    if request.args.get("max_ppg"):
        sql_str += " AND a.points_per_game <= :max_ppg"
        params["max_ppg"] = float(request.args["max_ppg"])
    if request.args.get("min_rpg"):
        sql_str += " AND a.rebounds_per_game >= :min_rpg"
        params["min_rpg"] = float(request.args["min_rpg"])
    if request.args.get("max_rpg"):
        sql_str += " AND a.rebounds_per_game <= :max_rpg"
        params["max_rpg"] = float(request.args["max_rpg"])
    if request.args.get("min_apg"):
        sql_str += " AND a.assists_per_game >= :min_apg"
        params["min_apg"] = float(request.args["min_apg"])
    if request.args.get("max_apg"):
        sql_str += " AND a.assists_per_game <= :max_apg"
        params["max_apg"] = float(request.args["max_apg"])
    if request.args.get("min_spg"):
        sql_str += " AND a.steals_per_game >= :min_spg"
        params["min_spg"] = float(request.args["min_spg"])
    if request.args.get("max_spg"):
        sql_str += " AND a.steals_per_game <= :max_spg"
        params["max_spg"] = float(request.args["max_spg"])
    if request.args.get("min_ftp"):
        sql_str += " AND a.free_throw_percentage >= :min_ftp"
        params["min_ftp"] = float(request.args["min_ftp"])
    if request.args.get("max_ftp"):
        sql_str += " AND a.free_throw_percentage <= :max_ftp"
        params["max_ftp"] = float(request.args["max_ftp"])
    if request.args.get("min_3pt"):
        sql_str += " AND a.three_point_percentage >= :min_3pt"
        params["min_3pt"] = float(request.args["min_3pt"])
    if request.args.get("max_3pt"):
        sql_str += " AND a.three_point_percentage <= :max_3pt"
        params["max_3pt"] = float(request.args["max_3pt"])
    if request.args.get("position"):
        sql_str += " AND LOWER(a.position) = LOWER(:position)"
        params["position"] = request.args["position"]
    if request.args.get("gender"):
        sql_str += " AND a.gender = :gender"
        params["gender"] = request.args["gender"]
    if request.args.get("team"):
        sql_str += " AND t.name = :team_name"
        params["team_name"] = request.args["team"]

    # Wrap final SQL string with text()
    final_sql = text(sql_str)
    result = db.session.execute(final_sql, params)
    athletes = [dict(row._mapping) for row in result]

    return render_template('reports/athlete_report.html', athletes=athletes, teams=teams)





@app.route('/reports/teams', methods=['GET', 'POST'])
def teams_report():


    # Fetch all teams for the dropdown list
    teams = Team.query.all()

    # Base SQL query string
    base_sql = "SELECT * FROM team WHERE 1=1"
    filters = {}
    
    # Dynamically build SQL based on request arguments
    if request.args.get('team_id'):
        base_sql += " AND id = :team_id"
        filters['team_id'] = int(request.args['team_id'])

    if request.args.get('min_wins'):
        base_sql += " AND wins >= :min_wins"
        filters['min_wins'] = int(request.args['min_wins'])

    if request.args.get('max_wins'):
        base_sql += " AND wins <= :max_wins"
        filters['max_wins'] = int(request.args['max_wins'])

    if request.args.get('min_losses'):
        base_sql += " AND losses >= :min_losses"
        filters['min_losses'] = int(request.args['min_losses'])

    if request.args.get('max_losses'):
        base_sql += " AND losses <= :max_losses"
        filters['max_losses'] = int(request.args['max_losses'])


    # Execute raw SQL with bound parameters
    result = db.session.execute(text(base_sql), filters)
    filtered_teams = result.fetchall()

    return render_template('reports/team_reports.html', filtered_teams=filtered_teams, teams=teams)





   









