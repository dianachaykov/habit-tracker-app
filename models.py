from extensions import db
import datetime

class User(db.Model):
    """Represents a user in the application."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    habits = db.relationship('Habit', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Habit(db.Model):
    """Represents a habit tracked by a user."""
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    frequency = db.Column(db.String(20), nullable=False)
    creation_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    completions = db.relationship('HabitCompletion', backref='habit', lazy=True)

    def __repr__(self):
        return f'<Habit {self.name}>'

class HabitCompletion(db.Model):
    """Represents a completion record for a habit."""
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    completed_on = db.Column(db.Date, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<HabitCompletion {self.habit_id} - {self.completed_on}>'