"""
Configuration Loader Module
Loads and validates the .ai-review.yaml configuration file
"""
import os
import yaml
from typing import Dict, Any, List
from pathlib import Path


class ConfigLoader:
    """Handles loading and validation of review configuration"""
    
    DEFAULT_CONFIG = {
        'ignore_patterns': [
            '*.md', '*.txt', '*.json', '*.yaml', '*.yml',
            'node_modules/**', 'venv/**', 'dist/**', 'build/**',
            '__pycache__/**', '.git/**'
        ],
        'focus_areas': {
            'code_quality': True,
            'security': True,
            'performance': True,
            'best_practices': True,
            'documentation': True
        },
        'block_pr_on': 'critical',
        'max_comments': 50,
        'llm': {
            'provider': 'openai',
            'model': 'gpt-4',
            'temperature': 0.3,
            'max_tokens': 2000
        },
        'checks': {
            'sql_injection': True,
            'xss_vulnerabilities': True,
            'hardcoded_secrets': True,
            'insecure_dependencies': True,
            'code_smells': True,
            'anti_patterns': True,
            'memory_leaks': True,
            'n_plus_one_queries': True,
            'missing_error_handling': True,
            'unused_imports': True
        },
        'custom_guidelines': ''
    }
    
    def __init__(self, repo_path: str = '.'):
        """Initialize config loader with repository path"""
        self.repo_path = Path(repo_path)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from .ai-review.yaml or use defaults"""
        config_file = self.repo_path / '.ai-review.yaml'
        
        if config_file.exists():
            try:
                with open(config_file, 'r') as f:
                    user_config = yaml.safe_load(f) or {}
                # Merge with defaults
                config = self._merge_configs(self.DEFAULT_CONFIG.copy(), user_config)
                print(f"✅ Loaded configuration from {config_file}")
                return config
            except Exception as e:
                print(f"⚠️ Error loading config file: {e}. Using defaults.")
                return self.DEFAULT_CONFIG.copy()
        else:
            print("ℹ️ No .ai-review.yaml found. Using default configuration.")
            return self.DEFAULT_CONFIG.copy()
    
    def _merge_configs(self, default: Dict, user: Dict) -> Dict:
        """Deep merge user config with default config"""
        for key, value in user.items():
            if key in default and isinstance(default[key], dict) and isinstance(value, dict):
                default[key] = self._merge_configs(default[key], value)
            else:
                default[key] = value
        return default
    
    def should_ignore_file(self, file_path: str) -> bool:
        """Check if file should be ignored based on patterns"""
        from fnmatch import fnmatch
        for pattern in self.config['ignore_patterns']:
            if fnmatch(file_path, pattern) or fnmatch(file_path, f"**/{pattern}"):
                return True
        return False
    
    def get_focus_areas(self) -> List[str]:
        """Get enabled focus areas"""
        return [area for area, enabled in self.config['focus_areas'].items() if enabled]
    
    def get_enabled_checks(self) -> List[str]:
        """Get enabled security and quality checks"""
        return [check for check, enabled in self.config['checks'].items() if enabled]
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration"""
        return self.config['llm']
    
    def get_max_comments(self) -> int:
        """Get maximum number of comments allowed"""
        return self.config.get('max_comments', 50)
    
    def get_block_threshold(self) -> str:
        """Get PR blocking threshold"""
        return self.config.get('block_pr_on', 'critical')
    
    def get_custom_guidelines(self) -> str:
        """Get custom guidelines if specified"""
        return self.config.get('custom_guidelines', '')
