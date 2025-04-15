from flask import jsonify, request
from app import app, bcrypt, jwt
from extensions import db
from models import User, Habit, HabitCompletion
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import datetime
from sqlalchemy import func

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"msg": "Missing required fields"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"msg": "Email already exists"}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    # Ensure you are using the correct column name from your User model
    new_user = User(username=username, email=email, password=password_hash)
    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 201

@app.route('/login', methods=['POST'])
def login():
    """Logs in a user and returns a JWT token."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify({'access_token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

@app.route('/habits', methods=['POST'])
@jwt_required()
def create_habit():
    """Creates a new habit."""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    frequency = data.get('frequency')
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()

    if not name or not frequency:
        return jsonify({'message': 'Name and frequency are required'}), 400

    new_habit = Habit(name=name, description=description, frequency=frequency, user_id=user.id)
    db.session.add(new_habit)
    db.session.commit()

    return jsonify({'message': 'Habit created successfully', 'id': new_habit.id}), 201

@app.route('/habits', methods=['GET'])
@jwt_required()
def get_habits():
    """Displays all habits."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habits = Habit.query.filter_by(user_id=user.id).all()
    habit_list = []
    for habit in habits:
        habit_list.append({
            'id': habit.id,
            'name': habit.name,
            'description': habit.description,
            'frequency': habit.frequency,
            'creation_date': habit.creation_date.isoformat()
        })
    return jsonify(habit_list), 200

@app.route('/habits/<int:habit_id>', methods=['PUT'])
@jwt_required()
def update_habit(habit_id):
    """Displays habit by the ID"""
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    frequency = data.get('frequency')
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habit = Habit.query.filter_by(id=habit_id, user_id=user.id).first()

    if not habit:
        return jsonify({'message': 'Habit not found'}), 404

    if name:
        habit.name = name
    if description:
        habit.description = description
    if frequency:
        habit.frequency = frequency

    db.session.commit()
    return jsonify({'message': 'Habit updated successfully'}), 200

@app.route('/habits/<int:habit_id>', methods=['DELETE'])
@jwt_required()
def delete_habit(habit_id):
    """Deletes habit"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habit = Habit.query.filter_by(id=habit_id, user_id=user.id).first()

    if not habit:
        return jsonify({'message': 'Habit not found'}), 404

    db.session.delete(habit)
    db.session.commit()
    return jsonify({'message': 'Habit deleted successfully'}), 200

@app.route('/habits/<int:habit_id>/completions', methods=['POST'])
@jwt_required()
def record_completion(habit_id):
    """Marks habit as completed"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habit = Habit.query.filter_by(id=habit_id, user_id=user.id).first()

    if not habit:
        return jsonify({'message': 'Habit not found'}), 404

    data = request.get_json()
    completed_on = data.get('completed_on')
    completed = data.get('completed')

    if not completed_on or completed is None:
        return jsonify({'message': 'Completed date and status are required'}), 400

    try:
        completed_on_date = datetime.datetime.strptime(completed_on, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'message': 'Invalid date format. Use YYYY-MM-DD'}), 400

    new_completion = HabitCompletion(habit_id=habit_id, completed_on=completed_on_date, completed=completed)
    db.session.add(new_completion)
    db.session.commit()

    return jsonify({'message': 'Completion recorded successfully'}), 201

@app.route('/habits/completions', methods=['GET'])
@jwt_required()
def get_completions():
    """Shows the completed habits"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habits = Habit.query.filter_by(user_id=user.id).all()
    completions_list = []
    for habit in habits:
        completions = HabitCompletion.query.filter_by(habit_id=habit.id).all()
        for completion in completions:
            completions_list.append({
                'habit_id': habit.id,
                'completed_on': completion.completed_on.isoformat(),
                'completed': completion.completed
            })
    return jsonify(completions_list), 200

@app.route('/habits/analytics/all', methods=['GET'])
@jwt_required()
def get_all_habits():
    """Shows all habits"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habits = Habit.query.filter_by(user_id=user.id).all()
    habits_list = [{'id': habit.id, 'name': habit.name, 'description': habit.description, 'frequency': habit.frequency} for habit in habits]
    return jsonify(habits_list), 200

@app.route('/habits/analytics/periodicity/<periodicity>', methods=['GET'])
@jwt_required()
def get_habits_by_periodicity(periodicity):
    """Shows habits by periodicity"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habits = Habit.query.filter_by(user_id=user.id, frequency=periodicity).all()
    habits_list = [{'id': habit.id, 'name': habit.name, 'description': habit.description, 'frequency': habit.frequency} for habit in habits]
    return jsonify(habits_list), 200

@app.route('/habits/analytics/longest_streak', methods=['GET'])
@jwt_required()
def get_longest_streak():
    """Calculates the longest streak"""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habits = Habit.query.filter_by(user_id=user.id).all()
    longest_streak = 0
    for habit in habits:
        streak = calculate_streak(habit.id)
        if streak > longest_streak:
            longest_streak = streak
    return jsonify({'longest_streak': longest_streak}), 200

@app.route('/habits/analytics/longest_streak/<int:habit_id>', methods=['GET'])
@jwt_required()
def get_longest_streak_for_given_habit(habit_id):
    """Returns the longest run streak for a given habit."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habit = Habit.query.filter_by(id=habit_id, user_id=user.id).first()

    if not habit:
        return jsonify({'message': 'Habit not found'}), 404

    completions = HabitCompletion.query.filter_by(habit_id=habit_id, completed=True).order_by(HabitCompletion.completed_on).all()

    if not completions:
        return jsonify({'longest_streak': 0}), 200

    longest_streak = 0
    current_streak = 0
    previous_date = None

    for completion in completions:
        if previous_date is None or (completion.completed_on - previous_date).days == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
        previous_date = completion.completed_on

    longest_streak = max(longest_streak, current_streak)  # Check for streak ending on the last completion

    return jsonify({'longest_streak': longest_streak}), 200

def calculate_longest_streak(completions):
    """Helper function to calculate the longest streak from a list of completions."""
    if not completions:
        return 0

    longest_streak = 0
    current_streak = 0
    previous_date = None

    for completion in completions:
        if previous_date is None or (completion.completed_on - previous_date).days == 1:
            current_streak += 1
        else:
            longest_streak = max(longest_streak, current_streak)
            current_streak = 1
        previous_date = completion.completed_on

    longest_streak = max(longest_streak, current_streak)
    return longest_streak

@app.route('/habits/analytics/longest_streak', methods=['GET'])
@jwt_required()
def get_longest_streak_of_all_habits():
    """Returns the longest run streak across all defined habits for the user."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habits = Habit.query.filter_by(user_id=user.id).all()

    overall_longest_streak = 0

    for habit in habits:
        completions = HabitCompletion.query.filter_by(habit_id=habit.id, completed=True).order_by(HabitCompletion.completed_on).all()
        habit_longest_streak = calculate_longest_streak(completions)
        overall_longest_streak = max(overall_longest_streak, habit_longest_streak)

    return jsonify({'longest_streak': overall_longest_streak}), 200

@app.route('/habits/analytics/longest_streak/<int:habit_id>', methods=['GET'])
@jwt_required()
def get_longest_streak_by_habit(habit_id):
    """Calculates the longest streak for a given habit."""
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user).first()
    habit = Habit.query.filter_by(user_id=user.id, id=habit_id).first()
    if not habit:
        return jsonify({'message': 'Habit not found'}), 404
    streak = calculate_streak(habit_id)
    return jsonify({'longest_streak': streak}), 200

def calculate_streak(habit_id):
    completions = HabitCompletion.query.filter_by(habit_id=habit_id, completed=True).order_by(HabitCompletion.completed_on).all()
    if not completions:
        return 0
    streak = 1
    longest_streak = 1
    for i in range(1, len(completions)):
        if (completions[i].completed_on - completions[i - 1].completed_on).days == 1:
            streak += 1
            if streak > longest_streak:
                longest_streak = streak
        else:
            streak = 1
    return longest_streak