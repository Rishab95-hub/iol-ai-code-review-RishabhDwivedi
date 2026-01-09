"""
Sample API Handler with Security and Performance Issues
For demonstration purposes only - DO NOT USE IN PRODUCTION
"""
import json
import requests
import pickle
import os


class APIHandler:
    """API request handler with intentional vulnerabilities"""
    
    def __init__(self):
        # ISSUE: Sensitive data in code
        self.secret_key = "my-super-secret-key-12345"
        self.aws_access_key = "AKIAIOSFODNN7EXAMPLE"
        self.aws_secret = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    
    def make_api_call(self, url, user_input):
        # ISSUE: Command injection vulnerability
        os.system(f"curl {url}")
        
        # ISSUE: Insecure SSL verification disabled
        response = requests.get(url, verify=False)
        return response.text
    
    def deserialize_data(self, data):
        # ISSUE: Insecure deserialization using pickle
        return pickle.loads(data)
    
    def execute_user_command(self, command):
        # ISSUE: Code injection via eval
        result = eval(command)
        return result
    
    def load_config(self, config_path):
        # ISSUE: Path traversal vulnerability
        with open(config_path, 'r') as f:
            return json.load(f)
    
    def generate_token(self, user_id):
        # ISSUE: Weak random number generation
        import random
        token = str(random.randint(1000, 9999))
        return token
    
    def process_file_upload(self, filename, content):
        # ISSUE: No file type validation
        # ISSUE: No size limits
        with open(f"/uploads/{filename}", 'wb') as f:
            f.write(content)
    
    def render_template(self, template, user_data):
        # ISSUE: Template injection vulnerability
        return template.format(**user_data)
    
    # ISSUE: Missing type hints
    def calculate_total(self, items):
        total = 0
        # ISSUE: Inefficient loop
        for i in range(len(items)):
            total += items[i]['price'] * items[i]['quantity']
        return total
    
    def get_user_info(self, user_id):
        # ISSUE: No rate limiting
        # ISSUE: No authentication check
        response = requests.get(f"https://api.example.com/users/{user_id}")
        return response.json()
    
    # ISSUE: Missing docstring and error handling
    def process_payment(self, card_number, amount):
        print(f"Processing payment: {card_number} for ${amount}")
        # ISSUE: Logging sensitive data
        return True
    
    def cleanup_old_files(self, directory):
        # ISSUE: Potential for arbitrary file deletion
        import shutil
        shutil.rmtree(directory)


# ISSUE: Debug mode enabled in production
DEBUG = True

# ISSUE: Global exception handler that swallows errors
def safe_execute(func, *args):
    try:
        return func(*args)
    except:
        # ISSUE: Bare except clause
        # ISSUE: Silent failure
        pass
    return None
