import unittest
import json
from app import app, db
from models import User, Habit, HabitCompletion

class HabitTrackerTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test environment."""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use an in-memory database for testing
        self.app = app.test_client()
        db.create_all()

        # Create a user for testing
        user = User(username='testuser', email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        #login and get token for use in other tests.
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'password'})
        self.token = json.loads(response.data)['access_token']

    def tearDown(self):
        """Clean up after each test."""
        db.session.remove()
        db.drop_all()

    def test_register_user(self):
        """Test user registration."""
        response = self.app.post('/register', json={'username': 'newuser', 'email': 'new@example.com', 'password': 'password'})
        self.assertEqual(response.status_code, 201)

    def test_login_user(self):
        """Test user login."""
        response = self.app.post('/login', json={'username': 'testuser', 'password': 'password'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', json.loads(response.data))

    def test_create_habit(self):
        """Test habit creation."""
        response = self.app.post('/habits', headers={'Authorization': f'Bearer {self.token}'}, json={'name': 'Test Habit', 'description': 'Test Description', 'frequency': 'Daily'})
        self.assertEqual(response.status_code, 201)

    def test_record_completion(self):
        """Test recording a habit completion."""
        # Create a habit first
        response = self.app.post('/habits', headers={'Authorization': f'Bearer {self.token}'}, json={'name': 'Test Habit', 'description': 'Test Description', 'frequency': 'Daily'})
        habit_id = json.loads(response.data)['id']

        # Record completion
        response = self.app.post(f'/habits/{habit_id}/completions', headers={'Authorization': f'Bearer {self.token}'}, json={'completed_on': '2024-10-27', 'completed': True})
        self.assertEqual(response.status_code, 201)

    def test_get_completions(self):
        """Test getting all habit completions."""
        # Create a habit first
        response = self.app.post('/habits', headers={'Authorization': f'Bearer {self.token}'}, json={'name': 'Test Habit', 'description': 'Test Description', 'frequency': 'Daily'})
        habit_id = json.loads(response.data)['id']

        # Record completion
        self.app.post(f'/habits/{habit_id}/completions', headers={'Authorization': f'Bearer {self.token}'}, json={'completed_on': '2024-10-27', 'completed': True})
        response = self.app.get('/habits/completions', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_all_habits(self):
        """Test getting all habits."""
        response = self.app.get('/habits/analytics/all', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_habits_by_periodicity(self):
        """Test getting habits by periodicity."""
        response = self.app.get('/habits/analytics/periodicity/Daily', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_longest_streak(self):
        """Test getting the longest streak."""
        response = self.app.get('/habits/analytics/longest_streak', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('longest_streak', json.loads(response.data))

    def test_get_longest_streak_by_habit(self):
        """Test getting the longest streak for a habit."""
        # Create a habit first
        response = self.app.post('/habits', headers={'Authorization': f'Bearer {self.token}'}, json={'name': 'Test Habit', 'description': 'Test Description', 'frequency': 'Daily'})
        habit_id = json.loads(response.data)['id']

        response = self.app.get(f'/habits/analytics/longest_streak/{habit_id}', headers={'Authorization': f'Bearer {self.token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('longest_streak', json.loads(response.data))

if __name__ == '__main__':
    unittest.main()