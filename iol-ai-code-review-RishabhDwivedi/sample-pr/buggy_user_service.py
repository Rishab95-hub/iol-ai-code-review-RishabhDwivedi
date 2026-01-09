"""
Sample User Service with Intentional Issues
This file contains various code quality, security, and performance issues
for demonstration purposes.
"""
import sqlite3
import os
import hashlib


class UserService:
    """Handles user operations - CONTAINS INTENTIONAL BUGS FOR DEMO"""
    
    def __init__(self):
        # ISSUE: Hardcoded credentials
        self.db_password = "admin123"
        self.api_key = "sk-1234567890abcdef"
        self.db = None
    
    def connect_db(self, db_name):
        # ISSUE: No error handling
        self.db = sqlite3.connect(db_name)
        return self.db
    
    def authenticate_user(self, username, password):
        # ISSUE: SQL Injection vulnerability
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        cursor = self.db.cursor()
        cursor.execute(query)
        return cursor.fetchone()
    
    def get_user_posts(self, user_id):
        # ISSUE: N+1 query problem
        user_query = f"SELECT * FROM users WHERE id = {user_id}"
        user = self.db.cursor().execute(user_query).fetchone()
        
        posts = []
        post_ids_query = f"SELECT id FROM posts WHERE user_id = {user_id}"
        post_ids = self.db.cursor().execute(post_ids_query).fetchall()
        
        for post_id in post_ids:
            # Making separate query for each post
            post_query = f"SELECT * FROM posts WHERE id = {post_id[0]}"
            post = self.db.cursor().execute(post_query).fetchone()
            posts.append(post)
        
        return posts
    
    def hash_password(self, password):
        # ISSUE: Weak hashing algorithm (MD5)
        return hashlib.md5(password.encode()).hexdigest()
    
    def get_all_users(self):
        # ISSUE: Memory inefficient - loads all users at once
        cursor = self.db.cursor()
        cursor.execute("SELECT * FROM users")
        all_users = cursor.fetchall()
        return all_users
    
    # ISSUE: Missing docstring
    def update_user(self, user_id, data):
        name = data['name']
        email = data['email']
        query = f"UPDATE users SET name='{name}', email='{email}' WHERE id={user_id}"
        self.db.cursor().execute(query)
        self.db.commit()
    
    def search_users(self, search_term):
        # ISSUE: XSS vulnerability - no input sanitization
        return f"<div>Search results for: {search_term}</div>"
    
    def calculate_user_score(self, user_id):
        # ISSUE: Inefficient algorithm - O(n^2)
        scores = []
        for i in range(1000):
            for j in range(1000):
                if i * j == user_id:
                    scores.append(i + j)
        return sum(scores)
    
    # ISSUE: Unused method
    def old_legacy_method(self):
        pass
    
    def process_user_data(self, data):
        # ISSUE: Missing error handling for key access
        user_name = data['name']
        user_age = data['age']
        user_email = data['email']
        
        # ISSUE: No validation
        return {
            'name': user_name,
            'age': user_age,
            'email': user_email
        }
    
    def __del__(self):
        # ISSUE: Resource leak - connection not properly closed
        if self.db:
            self.db = None


# ISSUE: Global mutable state
current_user = None
logged_in_users = []


def login_user(username, password):
    """ISSUE: Uses global state and has no error handling"""
    global current_user
    service = UserService()
    service.connect_db("users.db")
    user = service.authenticate_user(username, password)
    current_user = user
    logged_in_users.append(user)
    return user


# ISSUE: Missing error handling and validation
def register_user(username, password, email):
    service = UserService()
    service.connect_db("users.db")
    hashed_pw = service.hash_password(password)
    
    query = f"INSERT INTO users (username, password, email) VALUES ('{username}', '{hashed_pw}', '{email}')"
    service.db.cursor().execute(query)
    service.db.commit()
