from flask import Flask
from extensions import db
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
import logging
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql://postgres:1234@localhost/habit_tracker')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'didi'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = False

db.init_app(app)
migrate = Migrate(app, db)  # Initialize Migrate AFTER db.init_app(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

logging.basicConfig(level=logging.DEBUG)

def setup_database(app):
    """Sets up the database and populates initial data (assuming migrations are already run)."""
    with app.app_context():
        from models import User, Habit, HabitCompletion

        print("Assuming database migrations are complete.")

        # Create a default user if one doesn't exist
        if not User.query.filter_by(username='default_user').first():
            default_user = User(username='default_user', password=bcrypt.generate_password_hash('password').decode('utf-8'))
            db.session.add(default_user)
            db.session.commit()
            default_user_id = default_user.id
            print(f"Default user created with ID: {default_user_id}")
        else:
            default_user = User.query.filter_by(username='default_user').first()
            default_user_id = default_user.id
            print(f"Default user already exists with ID: {default_user_id}")

        # Create predefined habits associated with the default user
        if not Habit.query.filter_by(name='Read a book', user_id=default_user_id).first():
            new_habit1 = Habit(name='Read a book', description='Read for 30 minutes', frequency='Daily', user_id=default_user_id)
            db.session.add(new_habit1)

        if not Habit.query.filter_by(name='Exercise', user_id=default_user_id).first():
            new_habit2 = Habit(name='Exercise', description='30 minutes of cardio', frequency='Daily', user_id=default_user_id)
            db.session.add(new_habit2)

        if not Habit.query.filter_by(name='Learn a new language', user_id=default_user_id).first():
            new_habit3 = Habit(name='Learn a new language', description='Practice for 1 hour', frequency='Weekly', user_id=default_user_id)
            db.session.add(new_habit3)

        if not Habit.query.filter_by(name='Write in a journal', user_id=default_user_id).first():
            new_habit4 = Habit(name='Write in a journal', description='Write 3 pages', frequency='Daily', user_id=default_user_id)
            db.session.add(new_habit4)

        if not Habit.query.filter_by(name='Clean the house', user_id=default_user_id).first():
            new_habit5 = Habit(name='Clean the house', description='Clean for 2 hours', frequency='Weekly', user_id=default_user_id)
            db.session.add(new_habit5)

        db.session.commit()

        # Create random completion data (associated with the default user's habits)
        import datetime
        habits = Habit.query.filter_by(user_id=default_user_id).all()
        start_date = datetime.date.today() - datetime.timedelta(days=28)
        for habit in habits:
            for i in range(28):
                current_date = start_date + datetime.timedelta(days=i)
                if habit.frequency == 'Daily' or (habit.frequency == 'Weekly' and current_date.weekday() == 0):
                    completion = HabitCompletion(habit_id=habit.id, completed_on=current_date, completed=i % 2 == 0)
                    db.session.add(completion)
        db.session.commit()

if __name__ == '__main__':
    # We will now run migrations using the Flask CLI
    from routes import *
    app.run(debug=True)