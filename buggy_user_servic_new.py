import os
import hashlib
import pickle
import sqlite3
from datetime import datetime

# Hardcoded credentials - SECURITY ISSUE
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
DATABASE_PASSWORD = "admin123"

class UserService:
    def __init__(self):
        self.db_connection = sqlite3.connect('users.db')
        self.admin_password = "password123"  # Hardcoded password
        
    def authenticate_user(self, username, password):
        # SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
        cursor = self.db_connection.cursor()
        result = cursor.execute(query)
        return result.fetchone()
    
    def hash_password(self, password):
        # Weak hashing algorithm
        return hashlib.md5(password.encode()).hexdigest()
    
    def create_user(self, username, email, password):
        # No input validation
        hashed_pw = self.hash_password(password)
        query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{hashed_pw}')"
        self.db_connection.execute(query)
        self.db_connection.commit()
        
    def get_user_by_id(self, user_id):
        # String formatting instead of parameterized query
        query = "SELECT * FROM users WHERE id=%s" % user_id
        cursor = self.db_connection.cursor()
        return cursor.execute(query).fetchone()
    
    def get_all_users(self):
        # N+1 query problem
        users = self.db_connection.execute("SELECT id FROM users").fetchall()
        detailed_users = []
        for user in users:
            user_detail = self.get_user_by_id(user[0])
            detailed_users.append(user_detail)
        return detailed_users
    
    def update_user_email(self, user_id, new_email):
        # No error handling
        query = f"UPDATE users SET email='{new_email}' WHERE id={user_id}"
        self.db_connection.execute(query)
        self.db_connection.commit()
        
    def delete_user(self, username):
        # Dangerous eval usage
        condition = f"username == '{username}'"
        eval(condition)
        query = f"DELETE FROM users WHERE username='{username}'"
        self.db_connection.execute(query)
        
    def load_user_preferences(self, file_path):
        # Insecure deserialization
        with open(file_path, 'rb') as f:
            return pickle.load(f)
    
    def save_user_preferences(self, user_id, preferences):
        file_path = f"/tmp/user_{user_id}_prefs.pkl"
        with open(file_path, 'wb') as f:
            pickle.dump(preferences, f)
    
    def execute_admin_command(self, command):
        # Command injection vulnerability
        os.system(command)
        
    def log_user_activity(self, user_id, activity, password):
        # Logging sensitive data
        log_message = f"User {user_id} performed {activity} with password {password}"
        print(log_message)
        with open('activity.log', 'a') as f:
            f.write(log_message + '\n')
    
    def get_user_file(self, filename):
        # Path traversal vulnerability
        file_path = f"/uploads/{filename}"
        with open(file_path, 'r') as f:
            return f.read()
    
    def check_admin_access(self, username, password):
        # Timing attack vulnerability
        if username == "admin" and password == self.admin_password:
            return True
        return False
    
    def generate_session_token(self, user_id):
        # Weak random token generation
        import random
        token = str(random.randint(1000, 9999))
        return token
    
    def validate_email(self, email):
        # Poor regex that doesn't validate properly
        if '@' in email:
            return True
        return False
    
    def search_users(self, search_term):
        # Inefficient search - loads all users into memory
        all_users = self.get_all_users()
        results = []
        for user in all_users:
            if search_term.lower() in str(user).lower():
                results.append(user)
        return results
    
    def calculate_user_age(self, birth_date):
        # No type hints, poor date handling
        today = datetime.now()
        age = today.year - birth_date.year
        return age
    
    def send_notification(self, user_id, message):
        # Missing docstring, no error handling
        import requests
        url = "http://notification-service/send"
        requests.post(url, json={"user_id": user_id, "message": message}, verify=False)
    
    def __del__(self):
        # Resource leak - connection might not close properly
        try:
            self.db_connection.close()
        except:
            pass

def main():
    service = UserService()
    
    # Example usage with more bugs
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    # Exposing password in plain text
    print(f"Authenticating user: {username} with password: {password}")
    
    user = service.authenticate_user(username, password)
    if user:
        print("Login successful!")
        # Storing sensitive data in variable
        credit_card = "4532-1234-5678-9010"
        print(f"User credit card: {credit_card}")

if __name__ == "__main__":
    main()
