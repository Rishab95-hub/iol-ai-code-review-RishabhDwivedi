"""
Code Analyzer Module
Orchestrates the code analysis process
"""
from typing import List, Dict, Any
from .llm_client import LLMClient
from .config_loader import ConfigLoader


class CodeAnalyzer:
    """Main code analysis orchestrator"""
    
    def __init__(self, config: ConfigLoader, llm_client: LLMClient):
        """Initialize analyzer with configuration and LLM client"""
        self.config = config
        self.llm_client = llm_client
        self.focus_areas = config.get_focus_areas()
        self.enabled_checks = config.get_enabled_checks()
        self.custom_guidelines = config.get_custom_guidelines()
    
    def analyze_files(self, files: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Analyze multiple files and return aggregated results
        
        Args:
            files: List of file data with filename, patch, etc.
            
        Returns:
            List of analysis results per file
        """
        results = []
        
        for file_data in files:
            filename = file_data['filename']
            
            # Check if file should be ignored
            if self.config.should_ignore_file(filename):
                print(f"⏭️  Skipping {filename} (matches ignore pattern)")
                continue
            
            # Skip files without patches (binary files, etc.)
            if not file_data.get('patch'):
                print(f"⏭️  Skipping {filename} (no patch available)")
                continue
            
            print(f"🔍 Analyzing {filename}...")
            
            analysis = self._analyze_single_file(filename, file_data['patch'])
            
            if analysis['comments']:
                results.append({
                    'filename': filename,
                    'analysis': analysis,
                    'file_data': file_data
                })
                print(f"✅ Found {len(analysis['comments'])} issues in {filename}")
            else:
                print(f"✅ No issues found in {filename}")
        
        return results
    
    def _analyze_single_file(self, filename: str, patch: str) -> Dict[str, Any]:
        """Analyze a single file's diff"""
        
        # Handle large diffs by chunking
        chunks = self.llm_client.chunk_large_diff(patch)
        
        all_comments = []
        summaries = []
        
        for i, chunk in enumerate(chunks):
            if len(chunks) > 1:
                print(f"  Analyzing chunk {i+1}/{len(chunks)}...")
            
            result = self.llm_client.analyze_code(
                code_diff=chunk,
                file_path=filename,
                focus_areas=self.focus_areas,
                custom_guidelines=self.custom_guidelines,
                enabled_checks=self.enabled_checks
            )
            
            all_comments.extend(result.get('comments', []))
            summaries.append(result.get('summary', ''))
        
        # Deduplicate and sort comments
        unique_comments = self._deduplicate_comments(all_comments)
        
        return {
            'comments': unique_comments,
            'summary': ' '.join(summaries)
        }
    
    def _deduplicate_comments(self, comments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicate comments based on line and message similarity"""
        seen = set()
        unique = []
        
        for comment in comments:
            # Create a unique key based on line and first 50 chars of message
            key = (
                comment.get('line', 0),
                comment.get('message', '')[:50]
            )
            
            if key not in seen:
                seen.add(key)
                unique.append(comment)
        
        # Sort by severity (critical first) and then by line number
        severity_order = {'critical': 0, 'warning': 1, 'suggestion': 2}
        unique.sort(key=lambda c: (
            severity_order.get(c.get('severity', 'suggestion'), 3),
            c.get('line', 0) or 0
        ))
        
        return unique
    
    def aggregate_results(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Aggregate analysis results across all files"""
        total_comments = 0
        severity_counts = {'critical': 0, 'warning': 0, 'suggestion': 0}
        all_summaries = []
        
        for result in results:
            comments = result['analysis']['comments']
            total_comments += len(comments)
            
            for comment in comments:
                severity = comment.get('severity', 'suggestion')
                severity_counts[severity] = severity_counts.get(severity, 0) + 1
            
            all_summaries.append(result['analysis']['summary'])
        
        # Create overall summary
        overall_summary = self._create_overall_summary(
            len(results), 
            total_comments, 
            severity_counts
        )
        
        return {
            'total_files': len(results),
            'total_comments': total_comments,
            'severity_counts': severity_counts,
            'summary': overall_summary,
            'file_summaries': all_summaries
        }
    
    def _create_overall_summary(self, num_files: int, num_comments: int, 
                               severity_counts: Dict[str, int]) -> str:
        """Create a human-readable overall summary"""
        if num_comments == 0:
            return f"✨ Analyzed {num_files} file(s). No issues found. Code looks good!"
        
        summary = f"Analyzed {num_files} file(s) and found {num_comments} issue(s). "
        
        critical = severity_counts.get('critical', 0)
        warning = severity_counts.get('warning', 0)
        suggestion = severity_counts.get('suggestion', 0)
        
        if critical > 0:
            summary += f"⚠️ {critical} critical issue(s) require immediate attention. "
        if warning > 0:
            summary += f"{warning} warning(s) should be addressed. "
        if suggestion > 0:
            summary += f"{suggestion} suggestion(s) for improvement."
        
        return summary
