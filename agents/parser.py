#!/usr/bin/env python3
"""
Repository Parser Agent

Parses repository structure, README files, dependencies, and code organization.
Extracts key information needed for documentation generation.
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any


class RepoParser:
    """Agent responsible for parsing repository structure and content."""
    
    def __init__(self):
        self.supported_readme_files = [
            'README.md', 'README.rst', 'README.txt', 'README',
            'readme.md', 'readme.rst', 'readme.txt', 'readme'
        ]
        
        self.dependency_files = {
            'python': ['requirements.txt', 'setup.py', 'pyproject.toml', 'Pipfile', 'environment.yml'],
            'node': ['package.json', 'package-lock.json', 'yarn.lock'],
            'java': ['pom.xml', 'build.gradle', 'build.gradle.kts'],
            'ruby': ['Gemfile', 'Gemfile.lock'],
            'go': ['go.mod', 'go.sum'],
            'rust': ['Cargo.toml', 'Cargo.lock'],
            'php': ['composer.json', 'composer.lock'],
            'dotnet': ['*.csproj', '*.sln', 'packages.config'],
            'docker': ['Dockerfile', 'docker-compose.yml', 'docker-compose.yaml']
        }
        
        self.config_files = [
            '.env', '.env.example', '.env.template',
            'config.json', 'config.yaml', 'config.yml',
            '.gitignore', '.dockerignore',
            'Makefile', 'makefile'
        ]
    
    def parse_repository(self, repo_path: Path) -> Dict[str, Any]:
        """
        Parse the entire repository and extract relevant information.
        
        Args:
            repo_path (Path): Path to the cloned repository
            
        Returns:
            Dict[str, Any]: Parsed repository data
        """
        repo_path = Path(repo_path)
        
        print(f"📁 Parsing repository structure at {repo_path}")
        
        repo_data = {
            'path': str(repo_path),
            'name': repo_path.name,
            'structure': self._analyze_structure(repo_path),
            'readme': self._parse_readme(repo_path),
            'dependencies': self._parse_dependencies(repo_path),
            'languages': self._detect_languages(repo_path),
            'config_files': self._find_config_files(repo_path),
            'entry_points': self._find_entry_points(repo_path),
            'documentation': self._find_documentation(repo_path),
            'tests': self._find_tests(repo_path),
            'ci_cd': self._find_ci_cd(repo_path),
            'license': self._find_license(repo_path),
            'statistics': self._calculate_statistics(repo_path)
        }
        
        print(f"✅ Repository parsing complete")
        return repo_data
    
    def _analyze_structure(self, repo_path: Path) -> Dict[str, Any]:
        """Analyze the directory structure of the repository."""
        structure = {
            'root_files': [],
            'directories': [],
            'total_files': 0,
            'max_depth': 0,
            'tree': self._build_tree(repo_path)
        }
        
        # Get root level files and directories
        for item in repo_path.iterdir():
            if item.name.startswith('.'):
                continue  # Skip hidden files for now
            
            if item.is_file():
                structure['root_files'].append(item.name)
            elif item.is_dir():
                structure['directories'].append(item.name)
        
        # Calculate statistics
        structure['total_files'] = sum(1 for _ in repo_path.rglob('*') if _.is_file())
        structure['max_depth'] = self._calculate_max_depth(repo_path)
        
        return structure
    
    def _build_tree(self, repo_path: Path, max_depth: int = 3) -> Dict[str, Any]:
        """Build a tree representation of the repository structure."""
        def _build_node(path: Path, current_depth: int = 0) -> Dict[str, Any]:
            if current_depth >= max_depth:
                return {'type': 'truncated', 'name': '...'}
            
            node = {
                'name': path.name,
                'type': 'directory' if path.is_dir() else 'file',
                'children': []
            }
            
            if path.is_dir():
                try:
                    children = sorted(path.iterdir(), key=lambda x: (x.is_file(), x.name.lower()))
                    for child in children:
                        if not child.name.startswith('.'):
                            node['children'].append(_build_node(child, current_depth + 1))
                except PermissionError:
                    node['children'] = [{'type': 'error', 'name': 'Permission denied'}]
            
            return node
        
        return _build_node(repo_path)
    
    def _calculate_max_depth(self, repo_path: Path) -> int:
        """Calculate the maximum directory depth."""
        max_depth = 0
        for root, dirs, files in os.walk(repo_path):
            depth = len(Path(root).relative_to(repo_path).parts)
            max_depth = max(max_depth, depth)
        return max_depth
    
    def _parse_readme(self, repo_path: Path) -> Dict[str, Any]:
        """Parse README file content."""
        readme_data = {
            'found': False,
            'filename': None,
            'content': None,
            'sections': [],
            'badges': [],
            'links': []
        }
        
        # Find README file
        for readme_name in self.supported_readme_files:
            readme_path = repo_path / readme_name
            if readme_path.exists():
                readme_data['found'] = True
                readme_data['filename'] = readme_name
                
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    readme_data['content'] = content
                    readme_data['sections'] = self._extract_sections(content)
                    readme_data['badges'] = self._extract_badges(content)
                    readme_data['links'] = self._extract_links(content)
                    
                except Exception as e:
                    print(f"⚠️ Could not read README: {e}")
                    readme_data['error'] = str(e)
                
                break
        
        return readme_data
    
    def _extract_sections(self, content: str) -> List[Dict[str, str]]:
        """Extract sections from markdown content."""
        sections = []
        lines = content.split('\n')
        
        current_section = None
        current_content = []
        
        for line in lines:
            # Check for markdown headers
            if line.startswith('#'):
                # Save previous section
                if current_section:
                    sections.append({
                        'title': current_section,
                        'content': '\n'.join(current_content).strip()
                    })
                
                # Start new section
                current_section = line.lstrip('#').strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Add last section
        if current_section:
            sections.append({
                'title': current_section,
                'content': '\n'.join(current_content).strip()
            })
        
        return sections
    
    def _extract_badges(self, content: str) -> List[str]:
        """Extract badge URLs from markdown content."""
        badge_pattern = r'!\[.*?\]\((https://.*?)\)'
        return re.findall(badge_pattern, content)
    
    def _extract_links(self, content: str) -> List[Dict[str, str]]:
        """Extract links from markdown content."""
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        matches = re.findall(link_pattern, content)
        return [{'text': text, 'url': url} for text, url in matches]
    
    def _parse_dependencies(self, repo_path: Path) -> Dict[str, Any]:
        """Parse dependency files for different languages."""
        dependencies = {}
        
        for language, files in self.dependency_files.items():
            for file_pattern in files:
                if '*' in file_pattern:
                    # Handle glob patterns
                    matches = list(repo_path.glob(file_pattern))
                    for match in matches:
                        deps = self._parse_dependency_file(match, language)
                        if deps:
                            dependencies[language] = dependencies.get(language, {})
                            dependencies[language][match.name] = deps
                else:
                    # Handle exact file names
                    file_path = repo_path / file_pattern
                    if file_path.exists():
                        deps = self._parse_dependency_file(file_path, language)
                        if deps:
                            dependencies[language] = dependencies.get(language, {})
                            dependencies[language][file_pattern] = deps
        
        return dependencies
    
    def _parse_dependency_file(self, file_path: Path, language: str) -> Optional[Dict[str, Any]]:
        """Parse a specific dependency file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if language == 'python':
                return self._parse_python_deps(file_path, content)
            elif language == 'node':
                return self._parse_node_deps(file_path, content)
            elif language == 'java':
                return self._parse_java_deps(file_path, content)
            # Add more parsers as needed
            
            return {'raw_content': content[:500]}  # Fallback
            
        except Exception as e:
            print(f"⚠️ Could not parse {file_path}: {e}")
            return None
    
    def _parse_python_deps(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Parse Python dependency files."""
        if file_path.name == 'requirements.txt':
            deps = []
            for line in content.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):
                    deps.append(line)
            return {'dependencies': deps}
        
        elif file_path.name == 'package.json':
            try:
                data = json.loads(content)
                return {
                    'dependencies': data.get('dependencies', {}),
                    'dev_dependencies': data.get('devDependencies', {}),
                    'scripts': data.get('scripts', {})
                }
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON'}
        
        return {'raw_content': content[:500]}
    
    def _parse_node_deps(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Parse Node.js dependency files."""
        if file_path.name == 'package.json':
            try:
                data = json.loads(content)
                return {
                    'name': data.get('name'),
                    'version': data.get('version'),
                    'description': data.get('description'),
                    'dependencies': data.get('dependencies', {}),
                    'dev_dependencies': data.get('devDependencies', {}),
                    'scripts': data.get('scripts', {})
                }
            except json.JSONDecodeError:
                return {'error': 'Invalid JSON'}
        
        return {'raw_content': content[:500]}
    
    def _parse_java_deps(self, file_path: Path, content: str) -> Dict[str, Any]:
        """Parse Java dependency files."""
        # Basic parsing for now
        return {'raw_content': content[:500]}
    
    def _detect_languages(self, repo_path: Path) -> Dict[str, int]:
        """Detect programming languages used in the repository."""
        language_extensions = {
            'python': ['.py', '.pyw'],
            'javascript': ['.js', '.jsx', '.mjs'],
            'typescript': ['.ts', '.tsx'],
            'java': ['.java'],
            'go': ['.go'],
            'rust': ['.rs'],
            'cpp': ['.cpp', '.cc', '.cxx', '.c++'],
            'c': ['.c'],
            'csharp': ['.cs'],
            'php': ['.php'],
            'ruby': ['.rb'],
            'swift': ['.swift'],
            'kotlin': ['.kt', '.kts'],
            'scala': ['.scala'],
            'html': ['.html', '.htm'],
            'css': ['.css', '.scss', '.sass'],
            'shell': ['.sh', '.bash', '.zsh'],
            'yaml': ['.yml', '.yaml'],
            'json': ['.json'],
            'xml': ['.xml'],
            'markdown': ['.md', '.markdown']
        }
        
        language_counts = {}
        
        for file_path in repo_path.rglob('*'):
            if file_path.is_file():
                suffix = file_path.suffix.lower()
                for language, extensions in language_extensions.items():
                    if suffix in extensions:
                        language_counts[language] = language_counts.get(language, 0) + 1
                        break
        
        return dict(sorted(language_counts.items(), key=lambda x: x[1], reverse=True))
    
    def _find_config_files(self, repo_path: Path) -> List[str]:
        """Find configuration files in the repository."""
        found_configs = []
        
        for config_file in self.config_files:
            if (repo_path / config_file).exists():
                found_configs.append(config_file)
        
        return found_configs
    
    def _find_entry_points(self, repo_path: Path) -> List[str]:
        """Find potential entry points (main files)."""
        entry_points = []
        
        common_entry_points = [
            'main.py', 'app.py', 'server.py', 'run.py',
            'index.js', 'app.js', 'server.js', 'main.js',
            'Main.java', 'Application.java',
            'main.go',
            'main.rs'
        ]
        
        for entry_point in common_entry_points:
            if (repo_path / entry_point).exists():
                entry_points.append(entry_point)
        
        return entry_points
    
    def _find_documentation(self, repo_path: Path) -> List[str]:
        """Find documentation files and directories."""
        docs = []
        
        doc_patterns = ['docs/', 'doc/', 'documentation/', '*.md']
        
        for pattern in doc_patterns:
            if pattern.endswith('/'):
                # Directory pattern
                dir_path = repo_path / pattern.rstrip('/')
                if dir_path.exists() and dir_path.is_dir():
                    docs.append(pattern)
            else:
                # File pattern
                matches = list(repo_path.glob(pattern))
                docs.extend([str(m.relative_to(repo_path)) for m in matches])
        
        return docs
    
    def _find_tests(self, repo_path: Path) -> Dict[str, Any]:
        """Find test files and directories."""
        test_info = {
            'directories': [],
            'files': [],
            'frameworks': []
        }
        
        # Test directories
        test_dirs = ['test/', 'tests/', 'spec/', '__tests__/']
        for test_dir in test_dirs:
            dir_path = repo_path / test_dir.rstrip('/')
            if dir_path.exists() and dir_path.is_dir():
                test_info['directories'].append(test_dir)
        
        # Test files
        test_patterns = ['*test*.py', '*_test.py', 'test_*.py', '*.test.js', '*.spec.js']
        for pattern in test_patterns:
            matches = list(repo_path.rglob(pattern))
            test_info['files'].extend([str(m.relative_to(repo_path)) for m in matches])
        
        # Test frameworks (basic detection)
        if any('pytest' in str(f) for f in repo_path.rglob('*')):
            test_info['frameworks'].append('pytest')
        if any('jest' in str(f) for f in repo_path.rglob('*')):
            test_info['frameworks'].append('jest')
        
        return test_info
    
    def _find_ci_cd(self, repo_path: Path) -> List[str]:
        """Find CI/CD configuration files."""
        ci_cd_files = []
        
        ci_patterns = [
            '.github/workflows/*.yml',
            '.github/workflows/*.yaml',
            '.gitlab-ci.yml',
            '.travis.yml',
            'circle.yml',
            'appveyor.yml',
            'azure-pipelines.yml'
        ]
        
        for pattern in ci_patterns:
            matches = list(repo_path.glob(pattern))
            ci_cd_files.extend([str(m.relative_to(repo_path)) for m in matches])
        
        return ci_cd_files
    
    def _find_license(self, repo_path: Path) -> Optional[str]:
        """Find license file."""
        license_files = ['LICENSE', 'LICENSE.txt', 'LICENSE.md', 'COPYING']
        
        for license_file in license_files:
            license_path = repo_path / license_file
            if license_path.exists():
                return license_file
        
        return None
    
    def _calculate_statistics(self, repo_path: Path) -> Dict[str, int]:
        """Calculate basic repository statistics."""
        stats = {
            'total_files': 0,
            'total_directories': 0,
            'total_lines': 0,
            'code_files': 0
        }
        
        code_extensions = {'.py', '.js', '.ts', '.java', '.go', '.rs', '.cpp', '.c', '.cs', '.php', '.rb'}
        
        for item in repo_path.rglob('*'):
            if item.is_file():
                stats['total_files'] += 1
                
                if item.suffix.lower() in code_extensions:
                    stats['code_files'] += 1
                    
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            stats['total_lines'] += sum(1 for _ in f)
                    except (UnicodeDecodeError, PermissionError):
                        pass  # Skip binary or inaccessible files
            
            elif item.is_dir():
                stats['total_directories'] += 1
        
        return stats


if __name__ == "__main__":
    # Test the parser
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python parser.py <repo_path>")
        sys.exit(1)
    
    repo_path = Path(sys.argv[1])
    if not repo_path.exists():
        print(f"Repository path does not exist: {repo_path}")
        sys.exit(1)
    
    parser = RepoParser()
    repo_data = parser.parse_repository(repo_path)
    
    print("\n📊 Repository Analysis:")
    print(json.dumps(repo_data, indent=2, default=str))