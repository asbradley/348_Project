from sqlalchemy import CheckConstraint
from database_setup import db

# Athlete
class Athlete(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    sport = db.Column(db.String(50))  # e.g., Basketball
    height = db.Column(db.Float)
    weight = db.Column(db.Float)
    gender = db.Column(db.String(10))
    position = db.Column(db.String(2), CheckConstraint("position IN ('PG', 'SG', 'SF', 'PF', 'C')"), nullable=False)

    # Stats
    points_per_game = db.Column(db.Float, default=0.0)
    rebounds_per_game = db.Column(db.Float, default=0.0)
    assists_per_game = db.Column(db.Float, default=0.0)
    blocks_per_game = db.Column(db.Float, default=0.0)
    steals_per_game = db.Column(db.Float, default=0.0)

    # Shooting Percentages
    field_goal_percentage = db.Column(db.Float, default=0.0)
    three_point_percentage = db.Column(db.Float, default=0.0)
    free_throw_percentage = db.Column(db.Float, default=0.0)

    # Relationships
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', backref='athletes')

    
    
    tournament_stats = db.relationship('TournamentAthleteStats', back_populates='athlete')

   

# Tournament
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    date = db.Column(db.Date)

    # Relationship with Teams (Many-to-Many)
    teams = db.relationship('Team', secondary='tournament_team', backref='tournaments')


    athlete_stats = db.relationship('TournamentAthleteStats', back_populates='tournament')



# Team
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    city = db.Column(db.String(100))

# Many-to-Many Table (Teams & Tournaments)
tournament_team = db.Table(
    'tournament_team',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True)
)


class TournamentAthleteStats(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athlete.id'), nullable=False)
    
    # Stats specific to the tournament
    points_per_game = db.Column(db.Float, default=0.0)
    rebounds_per_game = db.Column(db.Float, default=0.0)
    assists_per_game = db.Column(db.Float, default=0.0)
    blocks_per_game = db.Column(db.Float, default=0.0)
    steals_per_game = db.Column(db.Float, default=0.0)
    
    # Relationships
    tournament = db.relationship('Tournament', back_populates='athlete_stats')
    athlete = db.relationship('Athlete', back_populates='tournament_stats')

