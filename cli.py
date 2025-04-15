import requests
import json

BASE_URL = 'http://127.0.0.1:5000'
TOKEN = None  # Store the token globally

def register():
    """Registers a new user."""
    username = input('Username: ')
    email = input('Email: ')
    password = input('Password: ')
    response = requests.post(f'{BASE_URL}/register', json={'username': username, 'email': email, 'password': password})
    if response.status_code == 201:
        print('Registration successful!')
    else:
        print('Registration failed.')

def login():
    """Logs in a user and stores the JWT token."""
    global TOKEN
    username = input('Username: ')
    password = input('Password: ')
    response = requests.post(f'{BASE_URL}/login', json={'username': username, 'password': password})
    if response.status_code == 200:
        TOKEN = response.json()['access_token']
        print('Login successful!')
    else:
        print('Login failed.')

def create_habit():
    """Creates habit"""
    name = input('Habit name: ')
    description = input('Habit description: ')
    frequency = input('Habit frequency (Daily/Weekly): ')
    response = requests.post(f'{BASE_URL}/habits', headers={'Authorization': f'Bearer {TOKEN}'}, json={'name': name, 'description': description, 'frequency': frequency})
    if response.status_code == 201:
        print('Habit created!')
    else:
        print('Failed to create habit.')

def get_all_habits():
    """Shows all habits"""
    response = requests.get(f'{BASE_URL}/habits/analytics/all', headers={'Authorization': f'Bearer {TOKEN}'})
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print('Failed to get habits.')

def get_habits_by_periodicity():
    """Shows habits by periodicity"""
    periodicity = input('Periodicity (Daily/Weekly): ')
    response = requests.get(f'{BASE_URL}/habits/analytics/periodicity/{periodicity}', headers={'Authorization': f'Bearer {TOKEN}'})
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print('Failed to get habits.')

def get_longest_streak():
    """Displays longest strike"""
    response = requests.get(f'{BASE_URL}/habits/analytics/longest_streak', headers={'Authorization': f'Bearer {TOKEN}'})
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print('Failed to get longest streak.')

def get_longest_streak_by_habit():
    """Displays longest strike by habit"""
    habit_id = input('Habit ID: ')
    response = requests.get(f'{BASE_URL}/habits/analytics/longest_streak/{habit_id}', headers={'Authorization': f'Bearer {TOKEN}'})
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print('Failed to get longest streak.')

def mark_habit_completed():
    """Marks habit as completed"""
    habit_id = input('Habit ID: ')
    completed_on = input('Completed on (YYYY-MM-DD): ')
    completed = input('Completed (True/False): ').lower() == 'true'
    response = requests.post(
        f'{BASE_URL}/habits/{habit_id}/completions',
        headers={'Authorization': f'Bearer {TOKEN}'},
        json={'completed_on': completed_on, 'completed': completed}
    )
    if response.status_code == 201:
        print('Habit completion recorded!')
    else:
        print('Failed to record habit completion.')

def main():
    """Main function for the CLI."""
    while True:
        print('\nOptions:')
        print('1. Register')  # Add this option
        print('2. Login')
        print('3. Create Habit')
        print('4. Get All Habits')
        print('5. Get Habits by Periodicity')
        print('6. Get Longest Streak')
        print('7. Get Longest Streak by Habit')
        print('8. Mark Habit Completed')
        print('9. Exit')

        choice = input('Enter your choice: ')

        if choice == '1': #register
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            create_habit()
        elif choice == '4':
            get_all_habits()
        elif choice == '5':
            get_habits_by_periodicity()
        elif choice == '6':
            get_longest_streak()
        elif choice == '7':
            get_longest_streak_by_habit()
        elif choice == '8':
            mark_habit_completed()
        elif choice == '9':
            break
        else:
            print('Invalid choice.')

if __name__ == '__main__':
    main()