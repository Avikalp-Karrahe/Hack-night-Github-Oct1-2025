#!/usr/bin/env python3
"""
PromptSwitch API Server - Flask-based HTTP API for GitBlueprint integration

Provides HTTP endpoints to interact with PromptSwitch functionality
for real-time repository analysis and documentation generation.
"""

import os
import sys
import json
import threading
from pathlib import Path
from datetime import datetime
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import logging

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from main import PromptSwitchAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend integration

# Global storage for processing status
processing_status = {}
processing_results = {}

class ProcessingThread(threading.Thread):
    """Background thread for processing repositories"""
    
    def __init__(self, job_id, github_url, agent):
        super().__init__()
        self.job_id = job_id
        self.github_url = github_url
        self.agent = agent
        
    def run(self):
        """Execute the PromptSwitch processing pipeline"""
        try:
            processing_status[self.job_id] = {
                'status': 'processing',
                'message': 'Analyzing repository...',
                'progress': 10,
                'start_time': datetime.now().isoformat()
            }
            
            # Process the repository
            results = self.agent.process_repository(
                self.github_url,
                enable_testing=True,
                enable_review=True
            )
            
            # Store results
            processing_results[self.job_id] = results
            processing_status[self.job_id] = {
                'status': 'completed' if results['success'] else 'error',
                'message': 'Analysis completed successfully!' if results['success'] else 'Analysis failed',
                'progress': 100,
                'end_time': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Processing failed for job {self.job_id}: {str(e)}")
            processing_status[self.job_id] = {
                'status': 'error',
                'message': f'Processing failed: {str(e)}',
                'progress': 0,
                'error': str(e)
            }

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'PromptSwitch API',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/analyze', methods=['POST'])
def analyze_repository():
    """Start repository analysis"""
    try:
        data = request.get_json()
        github_url = data.get('github_url')
        
        if not github_url:
            return jsonify({'error': 'github_url is required'}), 400
        
        # Generate unique job ID
        job_id = f"job_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{len(processing_status)}"
        
        # Initialize PromptSwitch agent
        agent = PromptSwitchAgent()
        
        # Start background processing
        thread = ProcessingThread(job_id, github_url, agent)
        thread.start()
        
        # Initialize status
        processing_status[job_id] = {
            'status': 'started',
            'message': 'Analysis started...',
            'progress': 0,
            'github_url': github_url
        }
        
        return jsonify({
            'job_id': job_id,
            'status': 'started',
            'message': 'Repository analysis started'
        })
        
    except Exception as e:
        logger.error(f"Failed to start analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/status/<job_id>', methods=['GET'])
def get_status(job_id):
    """Get processing status for a job"""
    if job_id not in processing_status:
        return jsonify({'error': 'Job not found'}), 404
    
    status = processing_status[job_id]
    
    # If completed, include results
    if status['status'] == 'completed' and job_id in processing_results:
        results = processing_results[job_id]
        status['results'] = {
            'success': results['success'],
            'repo_name': results.get('repo_name'),
            'output_filename': results.get('output_filename'),
            'quality_metrics': results.get('quality_metrics', {}),
            'outputs': {
                'weaviate_analysis': results.get('outputs', {}).get('weaviate_analysis'),
                'repo_data': {
                    'file_count': len(results.get('outputs', {}).get('repo_data', {}).get('files', [])),
                    'languages': results.get('outputs', {}).get('repo_data', {}).get('languages', []),
                    'structure': results.get('outputs', {}).get('repo_data', {}).get('structure', {})
                }
            }
        }
    
    return jsonify(status)

@app.route('/api/results/<job_id>', methods=['GET'])
def get_results(job_id):
    """Get full results for a completed job"""
    if job_id not in processing_results:
        return jsonify({'error': 'Results not found'}), 404
    
    results = processing_results[job_id]
    return jsonify(results)

@app.route('/api/blueprint/<job_id>', methods=['GET'])
def get_blueprint(job_id):
    """Get generated blueprint for a job"""
    if job_id not in processing_results:
        return jsonify({'error': 'Results not found'}), 404
    
    results = processing_results[job_id]
    
    # Extract repository data
    repo_data = results.get('outputs', {}).get('repo_data', {})
    repo_name = results.get('repo_name', 'Unknown')
    
    # Generate blueprint content
    blueprint = f"""# {repo_name} - Development Blueprint

## Environment Requirements
- **Runtime**: {', '.join(repo_data.get('languages', ['Unknown']))}
- **Package Manager**: npm/yarn (if Node.js), pip (if Python), etc.
- **Node Version**: 16+ (if applicable)

## Dependencies
{chr(10).join([f"- {dep}" for dep in repo_data.get('dependencies', ['See package.json/requirements.txt'])])}

## Setup Instructions

### 1. Clone Repository
```bash
git clone {results.get('github_url', '')}
cd {repo_name}
```

### 2. Install Dependencies
```bash
# For Node.js projects
npm install
# or
yarn install

# For Python projects
pip install -r requirements.txt
```

### 3. Environment Configuration
```bash
# Copy environment template
cp .env.example .env
# Edit .env with your configuration
```

## Golden Path

### Development Workflow
1. **Start Development Server**
   ```bash
   npm run dev  # or appropriate start command
   ```

2. **Run Tests**
   ```bash
   npm test     # or appropriate test command
   ```

3. **Build for Production**
   ```bash
   npm run build
   ```

## Required Secrets
- API_KEY: Your API key
- DATABASE_URL: Database connection string
- JWT_SECRET: JWT signing secret

## Port Configuration
- **Development**: 3000 (default)
- **Production**: 8080 or PORT environment variable

## File Structure
```
{repo_name}/
├── src/           # Source code
├── public/        # Static assets
├── tests/         # Test files
└── docs/          # Documentation
```

Generated by PromptSwitch Agent v2 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
    
    return Response(blueprint, mimetype='text/plain')

if __name__ == '__main__':
    print("🚀 Starting PromptSwitch API Server...")
    print("📡 API will be available at: http://localhost:5000")
    print("🔗 Health check: http://localhost:5000/api/health")
    
    app.run(host='0.0.0.0', port=5000, debug=True)