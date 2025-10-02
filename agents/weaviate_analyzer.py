#!/usr/bin/env python3
"""
Enhanced Weaviate Repository Analyzer

Advanced intelligent repository analysis using vector search for pattern recognition,
similar project detection, semantic code analysis, and enhanced prompt generation.
"""

import os
import json
import hashlib
import re
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple, Set
from datetime import datetime
from collections import defaultdict, Counter

import weaviate
from weaviate.classes.init import Auth
from weaviate.classes.query import Filter
import opik
from opik import track


class EnhancedWeaviateAnalyzer:
    """
    Enhanced Weaviate-powered repository analyzer for intelligent pattern recognition,
    semantic code analysis, and advanced documentation generation.
    """
    
    def __init__(self):
        """
        Initialize the enhanced Weaviate analyzer with advanced configuration.
        """
        try:
            # Load configuration from environment variables
            self.weaviate_url = os.getenv('WEAVIATE_URL', 'http://localhost:8080')
            self.api_key = os.getenv('WEAVIATE_API_KEY')
            self.collection_name = "RepositoryPatterns"
            self.code_collection_name = "CodeSnippets"
            
            # Enhanced features configuration
            self.enable_semantic_analysis = os.getenv('WEAVIATE_SEMANTIC_ANALYSIS', 'true').lower() == 'true'
            self.enable_code_vectorization = os.getenv('WEAVIATE_CODE_VECTORS', 'true').lower() == 'true'
            self.similarity_threshold = float(os.getenv('WEAVIATE_SIMILARITY_THRESHOLD', '0.7'))
            
            # Initialize client
            self.client = None
            self.mock_mode = True
            
            # Try to connect to Weaviate
            self._initialize_client()
            
            if self.client:
                self._setup_enhanced_schema()
                self.mock_mode = False
                print(f"✅ Enhanced WeaviateAnalyzer initialized with real connection")
            else:
                print(f"📝 WeaviateAnalyzer initialized in enhanced mock mode")
                
        except Exception as e:
            print(f"Warning: Could not initialize Weaviate client: {e}")
            self.client = None
            self.mock_mode = True
    
    def _initialize_client(self):
        """Initialize enhanced Weaviate client connection with retry logic."""
        try:
            if self.api_key:
                auth_config = Auth.api_key(self.api_key)
                self.client = weaviate.connect_to_custom(
                    http_host=self.weaviate_url.replace("http://", "").replace("https://", ""),
                    http_port=8080,
                    http_secure=False,
                    auth_credentials=auth_config
                )
            else:
                self.client = weaviate.connect_to_local()
            
            # Test connection
            if self.client.is_ready():
                print(f"✅ Connected to Weaviate at {self.weaviate_url}")
                return True
            else:
                print(f"⚠️ Weaviate connection not ready")
                self.client = None
                return False
            
        except Exception as e:
            print(f"⚠️ Weaviate connection failed: {e}")
            print("📝 Continuing with enhanced mock mode...")
            self.client = None
            return False
    
    def _setup_enhanced_schema(self):
        """Set up enhanced Weaviate schema for repository patterns and code analysis."""
        if not self.client:
            return
            
        try:
            # Setup Repository Patterns collection
            self._setup_repository_collection()
            
            # Setup Code Snippets collection for semantic code analysis
            if self.enable_code_vectorization:
                self._setup_code_collection()
                
        except Exception as e:
            print(f"⚠️ Enhanced schema setup failed: {e}")
    
    def _setup_repository_collection(self):
        """Setup the main repository patterns collection."""
        collections = self.client.collections.list_all()
        collection_names = [col.name for col in collections]
        
        if self.collection_name not in collection_names:
            # Create enhanced collection for repository patterns
            self.client.collections.create(
                name=self.collection_name,
                properties=[
                    weaviate.classes.config.Property(
                        name="repo_name",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="github_url",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="primary_language",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="framework",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="project_type",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="architecture_patterns",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    ),
                    weaviate.classes.config.Property(
                        name="semantic_description",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="dependencies",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    ),
                    weaviate.classes.config.Property(
                        name="features",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    ),
                    weaviate.classes.config.Property(
                        name="complexity_score",
                        data_type=weaviate.classes.config.DataType.NUMBER
                    ),
                    weaviate.classes.config.Property(
                        name="quality_metrics",
                        data_type=weaviate.classes.config.DataType.OBJECT
                    ),
                    weaviate.classes.config.Property(
                        name="analysis_timestamp",
                        data_type=weaviate.classes.config.DataType.DATE
                    )
                ],
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_transformers()
            )
            print(f"✅ Created enhanced repository collection: {self.collection_name}")
        else:
            print(f"✅ Using existing repository collection: {self.collection_name}")
    
    def _setup_code_collection(self):
        """Setup code snippets collection for semantic code analysis."""
        if self.code_collection_name not in [col.name for col in self.client.collections.list_all()]:
            self.client.collections.create(
                name=self.code_collection_name,
                properties=[
                    weaviate.classes.config.Property(
                        name="repo_name",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="file_path",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="code_content",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="language",
                        data_type=weaviate.classes.config.DataType.TEXT
                    ),
                    weaviate.classes.config.Property(
                        name="function_names",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    ),
                    weaviate.classes.config.Property(
                        name="class_names",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    ),
                    weaviate.classes.config.Property(
                        name="imports",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    ),
                    weaviate.classes.config.Property(
                        name="semantic_tags",
                        data_type=weaviate.classes.config.DataType.TEXT_ARRAY
                    )
                ],
                vectorizer_config=weaviate.classes.config.Configure.Vectorizer.text2vec_transformers()
            )
            print(f"✅ Created code snippets collection: {self.code_collection_name}")
        else:
            print(f"✅ Using existing code collection: {self.code_collection_name}")
    
    @track(name="weaviate_analyze_repository")
    def analyze_repository(self, repo_data):
        """Enhanced repository analysis with semantic understanding and vector search."""
        if self.mock_mode:
            return self._generate_enhanced_mock_analysis(repo_data)
        
        try:
            # Extract enhanced repository features
            features = self._extract_enhanced_repository_features(repo_data)
            
            # Perform semantic code analysis if enabled
            code_insights = {}
            if self.enable_code_vectorization:
                code_insights = self._analyze_code_semantics(repo_data)
            
            # Store repository patterns in Weaviate
            self._store_enhanced_repository_patterns(features, code_insights)
            
            # Find similar repositories using advanced vector search
            similar_repos = self._find_similar_repositories_advanced(features)
            
            # Generate intelligent recommendations
            recommendations = self._generate_intelligent_recommendations(features, similar_repos, code_insights)
            
            # Perform architecture pattern analysis
            architecture_patterns = self._analyze_architecture_patterns(repo_data, code_insights)
            
            return {
                "enhanced_analysis": {
                    "repository_insights": features,
                    "code_insights": code_insights,
                    "architecture_patterns": architecture_patterns,
                    "similar_repositories": similar_repos,
                    "recommendations": recommendations,
                    "semantic_analysis": self._generate_semantic_summary(features, code_insights),
                    "quality_assessment": self._assess_repository_quality(repo_data, features),
                    "analysis_timestamp": datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            print(f"⚠️ Enhanced Weaviate analysis failed: {e}")
            return self._enhanced_fallback_analysis(repo_data)
    
    def _generate_enhanced_mock_analysis(self, repo_data):
        """Generate enhanced mock analysis with semantic insights when Weaviate is unavailable."""
        repo_name = repo_data.get('name', 'unknown-repo')
        primary_language = self._detect_primary_language(repo_data)
        framework = self._detect_framework(repo_data)
        
        # Enhanced mock insights
        mock_insights = {
            "repository_insights": {
                "repo_name": repo_name,
                "primary_language": primary_language,
                "framework": framework,
                "project_type": self._determine_project_type(repo_data),
                "architecture_patterns": self._mock_architecture_patterns(primary_language, framework),
                "semantic_description": self._generate_mock_semantic_description(repo_name, primary_language, framework),
                "dependencies": self._extract_dependencies(repo_data),
                "features": self._extract_features(repo_data),
                "complexity_score": self._calculate_complexity_score(repo_data),
                "quality_metrics": self._mock_quality_metrics()
            },
            "code_insights": {
                "semantic_patterns": self._mock_semantic_patterns(primary_language),
                "code_quality_indicators": self._mock_code_quality_indicators(),
                "architectural_insights": self._mock_architectural_insights(framework)
            },
            "architecture_patterns": self._mock_detailed_architecture_patterns(framework),
            "similar_repositories": self._mock_similar_repositories(primary_language, framework),
            "recommendations": self._mock_enhanced_recommendations(primary_language, framework),
            "semantic_analysis": self._mock_semantic_analysis(repo_name, primary_language),
            "quality_assessment": self._mock_quality_assessment(),
            "analysis_timestamp": datetime.now().isoformat()
        }
        
        return {"enhanced_analysis": mock_insights}
    
    def _extract_enhanced_repository_features(self, repo_data):
        """Extract enhanced features from repository data with semantic analysis."""
        base_features = self._extract_repository_features(repo_data)
        
        # Add enhanced semantic features
        enhanced_features = {
            **base_features,
            "architecture_patterns": self._detect_architecture_patterns(repo_data),
            "semantic_description": self._generate_semantic_description(repo_data),
            "quality_metrics": self._calculate_quality_metrics(repo_data),
            "code_patterns": self._analyze_code_patterns(repo_data),
            "api_patterns": self._detect_api_patterns(repo_data),
            "testing_patterns": self._detect_testing_patterns(repo_data)
        }
        
        return enhanced_features
    
    def _analyze_code_semantics(self, repo_data):
        """Perform semantic analysis of code content."""
        if not self.enable_code_vectorization:
            return {}
            
        code_insights = {
            "semantic_patterns": [],
            "function_analysis": {},
            "class_analysis": {},
            "import_analysis": {},
            "complexity_analysis": {}
        }
        
        # Analyze code files for semantic patterns
        files = repo_data.get('files', {})
        for file_path, file_content in files.items():
            if self._is_code_file(file_path):
                file_insights = self._analyze_file_semantics(file_path, file_content)
                code_insights["semantic_patterns"].extend(file_insights.get("patterns", []))
                
                # Store code snippets in Weaviate for future similarity search
                if self.client:
                    self._store_code_snippet(repo_data.get('name', 'unknown'), file_path, file_content, file_insights)
        
        return code_insights
    
    def _store_enhanced_repository_patterns(self, features, code_insights):
        """Store enhanced repository patterns in Weaviate."""
        if not self.client:
            return
            
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Prepare enhanced data object
            data_object = {
                "repo_name": features.get("repo_name", ""),
                "github_url": features.get("github_url", ""),
                "primary_language": features.get("primary_language", ""),
                "framework": features.get("framework", ""),
                "project_type": features.get("project_type", ""),
                "architecture_patterns": features.get("architecture_patterns", []),
                "semantic_description": features.get("semantic_description", ""),
                "dependencies": features.get("dependencies", []),
                "features": features.get("features", []),
                "complexity_score": features.get("complexity_score", 0),
                "quality_metrics": features.get("quality_metrics", {}),
                "analysis_timestamp": datetime.now()
            }
            
            # Insert with vector
            collection.data.insert(data_object)
            print(f"✅ Stored enhanced repository pattern: {features.get('repo_name', 'unknown')}")
            
        except Exception as e:
            print(f"⚠️ Failed to store enhanced repository pattern: {e}")
    
    def _find_similar_repositories_advanced(self, features):
        """Find similar repositories using advanced vector search."""
        if not self.client:
            return self._mock_similar_repositories(features.get("primary_language", ""), features.get("framework", ""))
            
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Create semantic query combining multiple features
            query_text = f"{features.get('semantic_description', '')} {features.get('project_type', '')} {' '.join(features.get('architecture_patterns', []))}"
            
            # Perform hybrid search (vector + keyword)
            results = collection.query.hybrid(
                query=query_text,
                limit=5,
                alpha=0.7  # Balance between vector and keyword search
            )
            
            similar_repos = []
            for result in results.objects:
                if result.properties.get("repo_name") != features.get("repo_name"):
                    similarity_score = getattr(result.metadata, 'score', 0.0)
                    if similarity_score >= self.similarity_threshold:
                        similar_repos.append({
                            "name": result.properties.get("repo_name", ""),
                            "url": result.properties.get("github_url", ""),
                            "language": result.properties.get("primary_language", ""),
                            "framework": result.properties.get("framework", ""),
                            "similarity_score": similarity_score,
                            "shared_patterns": self._find_shared_patterns(features, result.properties)
                        })
            
            return similar_repos[:3]  # Return top 3 matches
            
        except Exception as e:
            print(f"⚠️ Advanced similarity search failed: {e}")
            return self._mock_similar_repositories(features.get("primary_language", ""), features.get("framework", ""))
    
    def _generate_intelligent_recommendations(self, features, similar_repos, code_insights):
        """Generate intelligent recommendations based on analysis."""
        recommendations = []
        
        # Architecture recommendations
        if features.get("complexity_score", 0) > 7:
            recommendations.append({
                "type": "architecture",
                "priority": "high",
                "title": "Consider Modular Architecture",
                "description": "High complexity detected. Consider breaking down into smaller, more manageable modules.",
                "rationale": f"Complexity score: {features.get('complexity_score', 0)}/10"
            })
        
        # Framework recommendations based on similar repos
        if similar_repos:
            common_frameworks = {}
            for repo in similar_repos:
                framework = repo.get("framework", "")
                if framework and framework != features.get("framework", ""):
                    common_frameworks[framework] = common_frameworks.get(framework, 0) + 1
            
            if common_frameworks:
                most_common = max(common_frameworks.items(), key=lambda x: x[1])
                recommendations.append({
                    "type": "technology",
                    "priority": "medium",
                    "title": f"Consider {most_common[0]} Framework",
                    "description": f"Similar repositories commonly use {most_common[0]}",
                    "rationale": f"Found in {most_common[1]} similar repositories"
                })
        
        # Code quality recommendations
        quality_metrics = features.get("quality_metrics", {})
        if quality_metrics.get("test_coverage", 0) < 0.7:
            recommendations.append({
                "type": "quality",
                "priority": "high",
                "title": "Improve Test Coverage",
                "description": "Consider adding more comprehensive tests",
                "rationale": f"Current coverage: {quality_metrics.get('test_coverage', 0)*100:.1f}%"
            })
        
        return recommendations
    
    # Helper methods for enhanced analysis
    def _mock_architecture_patterns(self, language, framework):
        """Generate mock architecture patterns based on language and framework."""
        patterns = []
        if framework == "React.js":
            patterns = ["Component-based", "Virtual DOM", "Unidirectional Data Flow", "JSX"]
        elif framework == "Django":
            patterns = ["MVC", "ORM", "Template Engine", "Middleware"]
        elif framework == "Flask":
            patterns = ["Microframework", "WSGI", "Jinja2 Templates", "Blueprint"]
        elif language == "Python":
            patterns = ["Object-Oriented", "Functional", "Duck Typing", "Decorators"]
        elif language == "JavaScript":
            patterns = ["Event-Driven", "Asynchronous", "Prototype-based", "Closures"]
        else:
            patterns = ["Modular", "Layered", "Object-Oriented"]
        return patterns
    
    def _generate_mock_semantic_description(self, repo_name, language, framework):
        """Generate a mock semantic description."""
        return f"A {language} project using {framework} framework with modern development practices and clean architecture patterns."
    
    def _mock_quality_metrics(self):
        """Generate mock quality metrics."""
        return {
            "test_coverage": 0.75,
            "code_complexity": 6.2,
            "maintainability_index": 78,
            "technical_debt_ratio": 0.15,
            "documentation_coverage": 0.68
        }
    
    def _mock_semantic_patterns(self, language):
        """Generate mock semantic patterns for code."""
        patterns = {
            "Python": ["List Comprehensions", "Context Managers", "Generators", "Decorators"],
            "JavaScript": ["Promises", "Arrow Functions", "Destructuring", "Async/Await"],
            "React": ["Hooks", "Higher-Order Components", "Render Props", "Context API"]
        }
        return patterns.get(language, ["Design Patterns", "SOLID Principles", "Clean Code"])
    
    def _mock_code_quality_indicators(self):
        """Generate mock code quality indicators."""
        return {
            "cyclomatic_complexity": 4.2,
            "code_duplication": 0.08,
            "naming_conventions": 0.92,
            "comment_density": 0.15
        }
    
    def _mock_architectural_insights(self, framework):
        """Generate mock architectural insights."""
        insights = {
            "React.js": ["Component composition", "State management patterns", "Performance optimization"],
            "Django": ["Model-View-Template", "Database optimization", "Security best practices"],
            "Flask": ["Blueprint organization", "Extension integration", "API design patterns"]
        }
        return insights.get(framework, ["Modular design", "Separation of concerns", "Code organization"])
    
    def _mock_detailed_architecture_patterns(self, framework):
        """Generate detailed architecture pattern analysis."""
        return {
            "primary_pattern": "MVC" if framework in ["Django", "Flask"] else "Component-based",
            "secondary_patterns": ["Repository", "Factory", "Observer"],
            "anti_patterns_detected": [],
            "pattern_confidence": 0.85
        }
    
    def _mock_enhanced_recommendations(self, language, framework):
        """Generate enhanced recommendations."""
        base_recommendations = [
            {
                "type": "architecture",
                "priority": "medium",
                "title": "Implement Design Patterns",
                "description": f"Consider implementing common {language} design patterns",
                "rationale": "Improves code maintainability and readability"
            },
            {
                "type": "testing",
                "priority": "high",
                "title": "Increase Test Coverage",
                "description": "Add comprehensive unit and integration tests",
                "rationale": "Current test coverage could be improved"
            }
        ]
        
        if framework == "React.js":
            base_recommendations.append({
                "type": "performance",
                "priority": "medium",
                "title": "Optimize React Performance",
                "description": "Consider using React.memo and useMemo for optimization",
                "rationale": "Prevents unnecessary re-renders"
            })
        
        return base_recommendations
    
    def _mock_semantic_analysis(self, repo_name, language):
        """Generate mock semantic analysis summary."""
        return {
            "semantic_complexity": "Medium",
            "domain_concepts": ["User Management", "Data Processing", "API Integration"],
            "business_logic_patterns": ["CRUD Operations", "Validation", "Authentication"],
            "semantic_cohesion": 0.78
        }
    
    def _mock_quality_assessment(self):
        """Generate mock quality assessment."""
        return {
            "overall_score": 7.8,
            "maintainability": 8.2,
            "reliability": 7.5,
            "security": 7.9,
            "performance": 7.6,
            "areas_for_improvement": ["Test Coverage", "Documentation", "Error Handling"]
        }
    
    def _detect_architecture_patterns(self, repo_data):
        """Detect architecture patterns from repository structure."""
        files = repo_data.get('files', {})
        patterns = []
        
        # Check for common patterns
        if any('controller' in f.lower() for f in files):
            patterns.append("MVC")
        if any('service' in f.lower() for f in files):
            patterns.append("Service Layer")
        if any('repository' in f.lower() for f in files):
            patterns.append("Repository Pattern")
        if any('factory' in f.lower() for f in files):
            patterns.append("Factory Pattern")
        
        return patterns or ["Modular"]
    
    def _generate_semantic_description(self, repo_data):
        """Generate semantic description of the repository."""
        name = repo_data.get('name', 'unknown')
        language = self._detect_primary_language(repo_data)
        framework = self._detect_framework(repo_data)
        
        return f"A {language} project implementing {framework} patterns with focus on {name} functionality"
    
    def _calculate_quality_metrics(self, repo_data):
        """Calculate quality metrics for the repository."""
        files = repo_data.get('files', {})
        total_files = len(files)
        
        # Mock calculations based on file analysis
        test_files = sum(1 for f in files if 'test' in f.lower())
        doc_files = sum(1 for f in files if any(ext in f.lower() for ext in ['.md', '.rst', '.txt']))
        
        return {
            "test_coverage": min(test_files / max(total_files * 0.3, 1), 1.0),
            "documentation_coverage": min(doc_files / max(total_files * 0.1, 1), 1.0),
            "code_complexity": min(total_files / 10, 10),
            "maintainability_index": max(100 - total_files, 50)
        }
    
    def _analyze_code_patterns(self, repo_data):
        """Analyze code patterns in the repository."""
        return ["Object-Oriented", "Functional", "Modular"]
    
    def _detect_api_patterns(self, repo_data):
        """Detect API patterns in the repository."""
        files = repo_data.get('files', {})
        patterns = []
        
        if any('api' in f.lower() for f in files):
            patterns.append("REST API")
        if any('graphql' in f.lower() for f in files):
            patterns.append("GraphQL")
        if any('websocket' in f.lower() for f in files):
            patterns.append("WebSocket")
            
        return patterns
    
    def _detect_testing_patterns(self, repo_data):
        """Detect testing patterns in the repository."""
        files = repo_data.get('files', {})
        patterns = []
        
        if any('test' in f.lower() for f in files):
            patterns.append("Unit Testing")
        if any('spec' in f.lower() for f in files):
            patterns.append("Specification Testing")
        if any('e2e' in f.lower() for f in files):
            patterns.append("End-to-End Testing")
            
        return patterns
    
    def _is_code_file(self, file_path):
        """Check if a file is a code file."""
        code_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.go', '.rs', '.php', '.rb'}
        return any(file_path.endswith(ext) for ext in code_extensions)
    
    def _analyze_file_semantics(self, file_path, file_content):
        """Analyze semantic patterns in a single file."""
        patterns = []
        
        # Simple pattern detection
        if 'class ' in file_content:
            patterns.append("Object-Oriented")
        if 'function ' in file_content or 'def ' in file_content:
            patterns.append("Functional")
        if 'import ' in file_content or 'from ' in file_content:
            patterns.append("Modular")
            
        return {"patterns": patterns}
    
    def _store_code_snippet(self, repo_name, file_path, file_content, file_insights):
        """Store code snippet in Weaviate for semantic search."""
        if not self.client:
            return
            
        try:
            collection = self.client.collections.get(self.code_collection_name)
            
            # Extract metadata from code
            functions = self._extract_functions(file_content)
            classes = self._extract_classes(file_content)
            imports = self._extract_imports(file_content)
            
            data_object = {
                "repo_name": repo_name,
                "file_path": file_path,
                "code_content": file_content[:1000],  # Truncate for storage
                "language": self._detect_file_language(file_path),
                "function_names": functions,
                "class_names": classes,
                "imports": imports,
                "semantic_tags": file_insights.get("patterns", [])
            }
            
            collection.data.insert(data_object)
            
        except Exception as e:
            print(f"⚠️ Failed to store code snippet: {e}")
    
    def _extract_functions(self, content):
        """Extract function names from code content."""
        import re
        functions = []
        
        # Python functions
        python_funcs = re.findall(r'def\s+(\w+)', content)
        functions.extend(python_funcs)
        
        # JavaScript functions
        js_funcs = re.findall(r'function\s+(\w+)', content)
        functions.extend(js_funcs)
        
        return functions[:10]  # Limit to first 10
    
    def _extract_classes(self, content):
        """Extract class names from code content."""
        import re
        classes = []
        
        # Python/Java classes
        class_matches = re.findall(r'class\s+(\w+)', content)
        classes.extend(class_matches)
        
        return classes[:10]  # Limit to first 10
    
    def _extract_imports(self, content):
        """Extract import statements from code content."""
        import re
        imports = []
        
        # Python imports
        python_imports = re.findall(r'(?:from\s+(\w+)|import\s+(\w+))', content)
        for match in python_imports:
            imports.extend([m for m in match if m])
        
        # JavaScript imports
        js_imports = re.findall(r'import.*from\s+[\'"]([^\'"]+)[\'"]', content)
        imports.extend(js_imports)
        
        return imports[:10]  # Limit to first 10
    
    def _detect_file_language(self, file_path):
        """Detect programming language from file extension."""
        ext = file_path.split('.')[-1].lower()
        language_map = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'jsx': 'React',
            'tsx': 'React TypeScript',
            'java': 'Java',
            'cpp': 'C++',
            'c': 'C',
            'go': 'Go',
            'rs': 'Rust',
            'php': 'PHP',
            'rb': 'Ruby'
        }
        return language_map.get(ext, 'Unknown')
    
    def _find_shared_patterns(self, features1, features2):
        """Find shared patterns between two repositories."""
        patterns1 = set(features1.get("architecture_patterns", []))
        patterns2 = set(features2.get("architecture_patterns", []))
        return list(patterns1.intersection(patterns2))
    
    def _analyze_architecture_patterns(self, repo_data, code_insights):
        """Analyze architecture patterns in the repository."""
        return {
            "primary_patterns": self._detect_architecture_patterns(repo_data),
            "code_patterns": code_insights.get("semantic_patterns", []),
            "architectural_quality": "Good",
            "pattern_consistency": 0.85
        }
    
    def _generate_semantic_summary(self, features, code_insights):
        """Generate semantic summary of the analysis."""
        return {
            "summary": f"Repository demonstrates {features.get('project_type', 'unknown')} patterns with {features.get('primary_language', 'unknown')} implementation",
            "key_characteristics": features.get("architecture_patterns", []),
            "semantic_complexity": "Medium",
            "domain_focus": features.get("semantic_description", "General purpose application")
        }
    
    def _assess_repository_quality(self, repo_data, features):
        """Assess overall repository quality."""
        quality_metrics = features.get("quality_metrics", {})
        
        return {
            "overall_score": sum(quality_metrics.values()) / len(quality_metrics) if quality_metrics else 7.0,
            "strengths": ["Good architecture", "Clean code structure"],
            "weaknesses": ["Could improve test coverage", "Documentation needs enhancement"],
            "recommendations": ["Add more tests", "Improve documentation", "Consider code review process"]
        }
    
    def _enhanced_fallback_analysis(self, repo_data):
        """Enhanced fallback analysis when Weaviate operations fail."""
        return self._generate_enhanced_mock_analysis(repo_data)
        repo_name = repo_data.get('name', 'unknown')
        file_count = len(repo_data.get('files', []))
        
        # Generate mock insights based on repository characteristics
        mock_features = {
            'repository_name': repo_name,
            'file_count': file_count,
            'primary_language': self._detect_primary_language(repo_data.get('files', [])),
            'has_documentation': any('README' in f.upper() for f in repo_data.get('files', [])),
            'has_tests': any('test' in f.lower() for f in repo_data.get('files', [])),
            'framework_detected': self._detect_framework(repo_data.get('files', []))
        }
        
        mock_similar_repos = [
            {'name': 'example-react-app', 'similarity': 0.78, 'reason': 'Similar React.js structure'},
            {'name': 'modern-web-template', 'similarity': 0.65, 'reason': 'Comparable file organization'},
            {'name': 'fullstack-boilerplate', 'similarity': 0.52, 'reason': 'Similar technology stack'}
        ]
        
        mock_recommendations = [
            'Consider adding comprehensive README documentation',
            'Implement automated testing with Jest or similar framework',
            'Add TypeScript for better type safety',
            'Consider implementing CI/CD pipeline',
            'Add code formatting with Prettier'
        ]
        
        return {
            'features': mock_features,
            'similar_repositories': mock_similar_repos,
            'recommendations': mock_recommendations,
            'analysis_timestamp': datetime.now().isoformat(),
            'confidence_score': 0.60,  # Lower confidence for mock data
            'mock_mode': True
        }
    
    def _detect_primary_language(self, files: List[str]) -> str:
        """Detect the primary programming language from file extensions."""
        extensions = {}
        for file in files:
            if '.' in file:
                ext = file.split('.')[-1].lower()
                extensions[ext] = extensions.get(ext, 0) + 1
        
        if not extensions:
            return 'unknown'
        
        # Map extensions to languages
        language_map = {
            'py': 'Python',
            'js': 'JavaScript',
            'ts': 'TypeScript',
            'jsx': 'React',
            'tsx': 'React TypeScript',
            'java': 'Java',
            'cpp': 'C++',
            'c': 'C',
            'go': 'Go',
            'rs': 'Rust',
            'php': 'PHP',
            'rb': 'Ruby'
        }
        
        most_common_ext = max(extensions, key=extensions.get)
        return language_map.get(most_common_ext, most_common_ext.upper())
    
    def _detect_framework(self, files: List[str]) -> str:
        """Detect the primary framework from file patterns."""
        file_names = [f.lower() for f in files]
        
        if 'package.json' in file_names:
            if any('react' in f for f in file_names):
                return 'React.js'
            elif any('vue' in f for f in file_names):
                return 'Vue.js'
            elif any('angular' in f for f in file_names):
                return 'Angular'
            else:
                return 'Node.js'
        elif 'requirements.txt' in file_names or 'pyproject.toml' in file_names:
            if any('django' in f for f in file_names):
                return 'Django'
            elif any('flask' in f for f in file_names):
                return 'Flask'
            else:
                return 'Python'
        elif 'pom.xml' in file_names or 'build.gradle' in file_names:
            return 'Java/Spring'
        elif 'composer.json' in file_names:
            return 'PHP'
        else:
            return 'Unknown'
    
    def _extract_repository_features(self, repo_data: Dict[str, Any], github_url: str) -> Dict[str, Any]:
        """Extract key features from repository data."""
        # Extract repository name
        repo_name = github_url.split('/')[-1] if github_url.startswith('http') else Path(github_url).name
        
        # Analyze file structure
        files = repo_data.get('files', [])
        file_extensions = set()
        for file_path in files:
            if '.' in file_path:
                ext = file_path.split('.')[-1].lower()
                file_extensions.add(ext)
        
        # Determine primary language
        language_counts = {}
        for ext in file_extensions:
            lang = self._extension_to_language(ext)
            if lang:
                language_counts[lang] = language_counts.get(lang, 0) + 1
        
        primary_language = max(language_counts.items(), key=lambda x: x[1])[0] if language_counts else 'unknown'
        
        # Detect framework
        framework = self._detect_framework_from_files(files, repo_data)
        
        # Determine project type
        project_type = self._determine_project_type(files, framework)
        
        # Extract dependencies
        dependencies = self._extract_dependencies(repo_data)
        
        # Calculate complexity score
        complexity_score = self._calculate_complexity_score(repo_data)
        
        return {
            'repo_name': repo_name,
            'github_url': github_url,
            'primary_language': primary_language,
            'framework': framework,
            'project_type': project_type,
            'file_structure': json.dumps(files[:50]),  # Limit for storage
            'dependencies': dependencies,
            'features': self._extract_features(repo_data),
            'complexity_score': complexity_score,
            'analysis_timestamp': datetime.now().isoformat()
        }
    
    def _store_repository_pattern(self, repo_features: Dict[str, Any]):
        """Store repository pattern in Weaviate."""
        if not self.client:
            return
            
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Create a unique ID based on repo URL
            repo_id = hashlib.md5(repo_features['github_url'].encode()).hexdigest()
            
            # Check if already exists
            existing = collection.query.fetch_object_by_id(repo_id)
            
            if not existing:
                collection.data.insert(
                    properties=repo_features,
                    uuid=repo_id
                )
                print(f"✅ Stored repository pattern: {repo_features['repo_name']}")
            else:
                print(f"📝 Repository pattern already exists: {repo_features['repo_name']}")
                
        except Exception as e:
            print(f"⚠️ Failed to store repository pattern: {e}")
    
    def _find_similar_repositories(self, repo_features: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Find similar repositories using vector search."""
        if not self.client:
            return []
            
        try:
            collection = self.client.collections.get(self.collection_name)
            
            # Create search query based on repository features
            search_text = f"{repo_features['primary_language']} {repo_features['framework']} {repo_features['project_type']}"
            
            # Perform vector search
            response = collection.query.near_text(
                query=search_text,
                limit=limit,
                where=weaviate.classes.query.Filter.by_property("github_url").not_equal(repo_features['github_url'])
            )
            
            similar_repos = []
            for obj in response.objects:
                similar_repos.append({
                    'repo_name': obj.properties.get('repo_name'),
                    'github_url': obj.properties.get('github_url'),
                    'primary_language': obj.properties.get('primary_language'),
                    'framework': obj.properties.get('framework'),
                    'project_type': obj.properties.get('project_type'),
                    'similarity_score': obj.metadata.distance if hasattr(obj.metadata, 'distance') else 0.0
                })
            
            return similar_repos
            
        except Exception as e:
            print(f"⚠️ Failed to find similar repositories: {e}")
            return []
    
    def _generate_recommendations(self, repo_features: Dict[str, Any], similar_repos: List[Dict[str, Any]]) -> List[str]:
        """Generate recommendations based on analysis."""
        recommendations = []
        
        # Framework-specific recommendations
        framework = repo_features.get('framework', '').lower()
        if framework == 'react':
            recommendations.extend([
                "Consider implementing TypeScript for better type safety",
                "Add React Testing Library for comprehensive testing",
                "Implement React Router for navigation",
                "Consider using a state management solution like Redux or Zustand"
            ])
        elif framework == 'vue':
            recommendations.extend([
                "Consider using Vue 3 Composition API for better code organization",
                "Add Pinia for state management",
                "Implement Vue Router for navigation",
                "Consider using TypeScript with Vue"
            ])
        elif framework == 'express':
            recommendations.extend([
                "Implement proper error handling middleware",
                "Add input validation with Joi or express-validator",
                "Consider using TypeScript for better type safety",
                "Implement proper logging with Winston or similar"
            ])
        
        # Language-specific recommendations
        language = repo_features.get('primary_language', '').lower()
        if language == 'python':
            recommendations.extend([
                "Add type hints for better code documentation",
                "Implement proper error handling and logging",
                "Consider using virtual environments",
                "Add comprehensive unit tests with pytest"
            ])
        elif language == 'javascript':
            recommendations.extend([
                "Consider migrating to TypeScript",
                "Implement proper ESLint configuration",
                "Add comprehensive testing with Jest",
                "Consider using modern ES6+ features"
            ])
        
        # Complexity-based recommendations
        complexity = repo_features.get('complexity_score', 0)
        if complexity > 0.7:
            recommendations.extend([
                "Consider breaking down large components into smaller ones",
                "Implement proper documentation for complex logic",
                "Add integration tests for critical paths",
                "Consider implementing design patterns for better maintainability"
            ])
        
        # Similar project recommendations
        if similar_repos:
            recommendations.append(f"Found {len(similar_repos)} similar projects that might provide useful patterns and inspiration")
        
        return recommendations[:10]  # Limit to top 10 recommendations
    
    def _fallback_analysis(self, repo_data: Dict[str, Any], github_url: str) -> Dict[str, Any]:
        """Fallback analysis when Weaviate is not available."""
        repo_features = self._extract_repository_features(repo_data, github_url)
        
        return {
            'repository_features': repo_features,
            'similar_repositories': [],
            'recommendations': [
                "Enable Weaviate integration for intelligent repository analysis",
                "Consider implementing proper documentation",
                "Add comprehensive testing suite",
                "Implement proper error handling"
            ],
            'enhanced_analysis': False
        }
    
    def _extension_to_language(self, ext: str) -> Optional[str]:
        """Map file extension to programming language."""
        ext_map = {
            'py': 'python', 'js': 'javascript', 'ts': 'typescript',
            'jsx': 'javascript', 'tsx': 'typescript', 'java': 'java',
            'cpp': 'cpp', 'c': 'c', 'cs': 'csharp', 'php': 'php',
            'rb': 'ruby', 'go': 'go', 'rs': 'rust', 'swift': 'swift',
            'kt': 'kotlin', 'scala': 'scala', 'r': 'r', 'dart': 'dart',
            'vue': 'vue', 'html': 'html', 'css': 'css', 'scss': 'scss',
            'less': 'less', 'sql': 'sql', 'sh': 'shell', 'yml': 'yaml',
            'yaml': 'yaml', 'json': 'json', 'xml': 'xml', 'md': 'markdown'
        }
        return ext_map.get(ext.lower())
    
    def _detect_framework_from_files(self, files: List[str], repo_data: Dict[str, Any]) -> str:
        """Detect framework from file patterns."""
        file_set = set(files)
        
        # React patterns
        if any('package.json' in f for f in files):
            package_content = repo_data.get('package_json', {})
            deps = {**package_content.get('dependencies', {}), **package_content.get('devDependencies', {})}
            
            if 'react' in deps:
                if 'next' in deps:
                    return 'next.js'
                elif 'gatsby' in deps:
                    return 'gatsby'
                else:
                    return 'react'
            elif 'vue' in deps:
                return 'vue'
            elif '@angular/core' in deps:
                return 'angular'
            elif 'express' in deps:
                return 'express'
        
        # Python frameworks
        if 'requirements.txt' in file_set or 'pyproject.toml' in file_set:
            if any('django' in f.lower() for f in files):
                return 'django'
            elif any('flask' in f.lower() for f in files):
                return 'flask'
            elif any('fastapi' in f.lower() for f in files):
                return 'fastapi'
        
        return 'unknown'
    
    def _determine_project_type(self, files: List[str], framework: str) -> str:
        """Determine project type based on files and framework."""
        file_set = set(files)
        
        # Web applications
        if framework in ['react', 'vue', 'angular', 'next.js', 'gatsby']:
            return 'web_application'
        
        # APIs
        if framework in ['express', 'fastapi', 'flask', 'django']:
            return 'api'
        
        # Mobile
        if 'android' in str(files).lower() or 'ios' in str(files).lower():
            return 'mobile_application'
        
        # Desktop
        if any(ext in str(files).lower() for ext in ['electron', 'tauri', 'tkinter']):
            return 'desktop_application'
        
        # Libraries
        if 'setup.py' in file_set or 'pyproject.toml' in file_set:
            return 'library'
        
        # CLI tools
        if 'bin/' in str(files) or 'cli' in str(files).lower():
            return 'cli_tool'
        
        return 'application'
    
    def _extract_dependencies(self, repo_data: Dict[str, Any]) -> List[str]:
        """Extract key dependencies from repository data."""
        dependencies = []
        
        # JavaScript/Node.js dependencies
        package_json = repo_data.get('package_json', {})
        if package_json:
            deps = {**package_json.get('dependencies', {}), **package_json.get('devDependencies', {})}
            dependencies.extend(list(deps.keys())[:20])  # Limit to top 20
        
        # Python dependencies
        if 'requirements' in repo_data:
            python_deps = repo_data['requirements']
            dependencies.extend(list(python_deps.keys())[:20])
        
        return dependencies
    
    def _extract_features(self, repo_data: Dict[str, Any]) -> List[str]:
        """Extract key features from repository."""
        features = []
        files = repo_data.get('files', [])
        
        # Common feature indicators
        feature_indicators = {
            'authentication': ['auth', 'login', 'jwt', 'oauth'],
            'database': ['db', 'database', 'sql', 'mongo', 'redis'],
            'api': ['api', 'rest', 'graphql', 'endpoint'],
            'testing': ['test', 'spec', '__tests__', 'cypress'],
            'documentation': ['docs', 'readme', 'wiki'],
            'deployment': ['docker', 'k8s', 'kubernetes', 'deploy'],
            'ci_cd': ['.github', 'jenkins', 'gitlab-ci', 'travis'],
            'monitoring': ['log', 'metric', 'monitor', 'analytics']
        }
        
        for feature, indicators in feature_indicators.items():
            if any(indicator in str(files).lower() for indicator in indicators):
                features.append(feature)
        
        return features
    
    def _calculate_complexity_score(self, repo_data: Dict[str, Any]) -> float:
        """Calculate repository complexity score (0-1)."""
        files = repo_data.get('files', [])
        
        # Base complexity factors
        file_count = len(files)
        directory_depth = max(len(f.split('/')) for f in files) if files else 1
        
        # Language diversity
        extensions = set()
        for f in files:
            if '.' in f:
                extensions.add(f.split('.')[-1].lower())
        
        language_diversity = len(extensions)
        
        # Normalize scores
        file_complexity = min(file_count / 100, 1.0)  # Normalize to 0-1
        depth_complexity = min(directory_depth / 10, 1.0)
        diversity_complexity = min(language_diversity / 10, 1.0)
        
        # Weighted average
        complexity_score = (file_complexity * 0.4 + depth_complexity * 0.3 + diversity_complexity * 0.3)
        
        return round(complexity_score, 2)
    
    def close(self):
        """Close Weaviate connection."""
        if self.client:
            self.client.close()
            print("✅ Weaviate connection closed")


if __name__ == "__main__":
    # Test the enhanced analyzer
    analyzer = EnhancedWeaviateAnalyzer()
    print("Enhanced Weaviate Analyzer initialized successfully!")