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
    position = db.Column(db.String(50))  # e.g., Point Guard

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

# Coach
class Coach(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(50), default="Head Coach")  # Head Coach, Assistant Coach
    sport = db.Column(db.String(50))

    # Relationship with Team
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team', backref='coaches')

# Tournament
class Tournament(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100))
    date = db.Column(db.Date)

    # Relationship with Teams (Many-to-Many)
    teams = db.relationship('Team', secondary='tournament_team', backref='tournaments')

# Team
class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100))

# Many-to-Many Table (Teams & Tournaments)
tournament_team = db.Table(
    'tournament_team',
    db.Column('team_id', db.Integer, db.ForeignKey('team.id'), primary_key=True),
    db.Column('tournament_id', db.Integer, db.ForeignKey('tournament.id'), primary_key=True)
)





