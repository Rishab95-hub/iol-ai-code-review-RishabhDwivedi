"""
LLM Client Module
Handles communication with various LLM providers (OpenAI, Anthropic, Azure OpenAI)
"""
import os
from typing import Dict, Any, Optional
import json


class LLMClient:
    """Client for interacting with LLM providers"""
    
    def __init__(self, provider: str = "openai", model: str = "gpt-4", 
                 temperature: float = 0.3, max_tokens: int = 2000):
        """Initialize LLM client with provider and model settings"""
        self.provider = provider.lower()
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = None
        
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize the appropriate LLM client based on provider"""
        try:
            if self.provider == "openai":
                import openai
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    raise ValueError("OPENAI_API_KEY environment variable not set")
                self.client = openai.OpenAI(api_key=api_key)
                print(f"✅ Initialized OpenAI client with model: {self.model}")
                
            elif self.provider == "anthropic":
                import anthropic
                api_key = os.getenv("ANTHROPIC_API_KEY")
                if not api_key:
                    raise ValueError("ANTHROPIC_API_KEY environment variable not set")
                self.client = anthropic.Anthropic(api_key=api_key)
                print(f"✅ Initialized Anthropic client with model: {self.model}")
                
            elif self.provider == "azure_openai":
                import openai
                api_key = os.getenv("AZURE_OPENAI_API_KEY")
                endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
                if not api_key or not endpoint:
                    raise ValueError("AZURE_OPENAI_API_KEY and AZURE_OPENAI_ENDPOINT must be set")
                self.client = openai.AzureOpenAI(
                    api_key=api_key,
                    api_version="2024-02-15-preview",
                    azure_endpoint=endpoint
                )
                print(f"✅ Initialized Azure OpenAI client with model: {self.model}")
            else:
                raise ValueError(f"Unsupported LLM provider: {self.provider}")
                
        except ImportError as e:
            raise ImportError(f"Failed to import {self.provider} library. Install with: pip install {self.provider}")
        except Exception as e:
            raise Exception(f"Failed to initialize LLM client: {str(e)}")
    
    def analyze_code(self, code_diff: str, file_path: str, focus_areas: list, 
                     custom_guidelines: str = "", enabled_checks: list = None) -> Dict[str, Any]:
        """
        Analyze code diff and return structured feedback
        
        Returns:
            Dict with structure:
            {
                'comments': [
                    {
                        'line': int,
                        'severity': 'critical'|'warning'|'suggestion',
                        'category': str,
                        'message': str,
                        'suggestion': str (optional)
                    }
                ],
                'summary': str
            }
        """
        prompt = self._build_analysis_prompt(code_diff, file_path, focus_areas, 
                                             custom_guidelines, enabled_checks)
        
        try:
            response = self._call_llm(prompt)
            return self._parse_response(response)
        except Exception as e:
            print(f"❌ Error during LLM analysis: {str(e)}")
            return {'comments': [], 'summary': f'Analysis failed: {str(e)}'}
    
    def _build_analysis_prompt(self, code_diff: str, file_path: str, focus_areas: list,
                               custom_guidelines: str, enabled_checks: list) -> str:
        """Build the analysis prompt for the LLM"""
        
        focus_areas_str = ", ".join(focus_areas)
        checks_str = ", ".join(enabled_checks) if enabled_checks else "all standard checks"
        
        prompt = f"""You are an expert code reviewer. Analyze the following code diff from file "{file_path}" and provide detailed, actionable feedback.

FOCUS AREAS: {focus_areas_str}
ENABLED CHECKS: {checks_str}

CODE DIFF:
```
{code_diff}
```

{f"CUSTOM GUIDELINES:\n{custom_guidelines}\n" if custom_guidelines else ""}

INSTRUCTIONS:
1. Analyze the code for:
   - Code Quality: code smells, anti-patterns, maintainability issues
   - Security: SQL injection, XSS, hardcoded secrets, insecure dependencies
   - Performance: inefficient algorithms, memory leaks, N+1 queries
   - Best Practices: language/framework conventions
   - Documentation: missing comments, docstrings, or unclear code

2. For each issue found, provide:
   - Specific line number (if identifiable from diff context)
   - Severity: "critical", "warning", or "suggestion"
   - Category: one of [security, performance, code_quality, best_practices, documentation]
   - Clear explanation of the issue
   - Actionable suggestion for fixing it

3. Be specific and avoid obvious comments. Focus on meaningful improvements.

4. Output MUST be valid JSON in this exact format:
{{
  "comments": [
    {{
      "line": <line_number or null>,
      "severity": "critical|warning|suggestion",
      "category": "security|performance|code_quality|best_practices|documentation",
      "message": "Description of the issue",
      "suggestion": "How to fix it (optional)"
    }}
  ],
  "summary": "Overall assessment of the changes"
}}

Provide only the JSON output, no additional text."""
        
        return prompt
    
    def _call_llm(self, prompt: str) -> str:
        """Call the LLM API and return the response"""
        if self.provider == "openai" or self.provider == "azure_openai":
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are an expert code reviewer that provides structured JSON output."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            return response.choices[0].message.content
            
        elif self.provider == "anthropic":
            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            return response.content[0].text
        
        return ""
    
    def _parse_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response into structured format"""
        try:
            # Extract JSON from response (in case there's extra text)
            response = response.strip()
            if response.startswith("```json"):
                response = response[7:]
            if response.startswith("```"):
                response = response[3:]
            if response.endswith("```"):
                response = response[:-3]
            response = response.strip()
            
            # Try to fix truncated JSON by adding closing braces
            if not response.endswith('}'):
                # Count open braces and add missing closing braces
                open_count = response.count('{')
                close_count = response.count('}')
                if open_count > close_count:
                    response += '}' * (open_count - close_count)
            
            result = json.loads(response)
            
            # Validate structure
            if 'comments' not in result:
                result['comments'] = []
            if 'summary' not in result:
                result['summary'] = 'No summary provided'
            
            return result
        except json.JSONDecodeError as e:
            print(f"⚠️ Failed to parse LLM response as JSON: {e}")
            print(f"Response was: {response[:500]}")
            return {
                'comments': [],
                'summary': 'Failed to parse LLM response'
            }
    
    def chunk_large_diff(self, diff: str, max_chars: int = 12000) -> list:
        """Split large diffs into chunks to handle token limits"""
        if len(diff) <= max_chars:
            return [diff]
        
        chunks = []
        lines = diff.split('\n')
        current_chunk = []
        current_size = 0
        
        for line in lines:
            line_size = len(line) + 1  # +1 for newline
            if current_size + line_size > max_chars and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_size = line_size
            else:
                current_chunk.append(line)
                current_size += line_size
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
