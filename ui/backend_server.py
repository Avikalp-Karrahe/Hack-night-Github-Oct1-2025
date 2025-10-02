#!/usr/bin/env python3
"""
Simple HTTP server to bridge the frontend with PromptSwitch backend
"""

import json
import os
import sys
import subprocess
import threading
import time
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import uuid

# Add the parent directory to the path to import PromptSwitch modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Global storage for job status and results
jobs = {}

class PromptSwitchHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        """Handle CORS preflight requests"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        """Handle GET requests for job status and results"""
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        
        # Add CORS headers
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        
        if len(path_parts) >= 2 and path_parts[0] == 'status':
            job_id = path_parts[1]
            if job_id in jobs:
                response = {
                    'job_id': job_id,
                    'status': jobs[job_id]['status'],
                    'progress': jobs[job_id].get('progress', 0),
                    'message': jobs[job_id].get('message', ''),
                    'results': jobs[job_id].get('results', None)
                }
            else:
                response = {'error': 'Job not found'}
        else:
            response = {'error': 'Invalid endpoint'}
        
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handle POST requests to start PromptSwitch processing"""
        if self.path == '/analyze':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode())
                repo_url = data.get('repo_url')
                output_dir = data.get('output_dir', './output')
                
                if not repo_url:
                    self.send_error(400, 'Missing repo_url')
                    return
                
                # Generate job ID
                job_id = str(uuid.uuid4())
                
                # Initialize job status
                jobs[job_id] = {
                    'status': 'started',
                    'progress': 0,
                    'message': 'Initializing PromptSwitch...',
                    'repo_url': repo_url,
                    'output_dir': output_dir
                }
                
                # Start processing in background thread
                thread = threading.Thread(
                    target=self.process_repository,
                    args=(job_id, repo_url, output_dir)
                )
                thread.daemon = True
                thread.start()
                
                # Return job ID
                self.send_response(200)
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                
                response = {'job_id': job_id, 'status': 'started'}
                self.wfile.write(json.dumps(response).encode())
                
            except json.JSONDecodeError:
                self.send_error(400, 'Invalid JSON')
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, 'Not found')

    def process_repository(self, job_id, repo_url, output_dir):
        """Process repository using PromptSwitch in background"""
        try:
            # Update status
            jobs[job_id]['status'] = 'processing'
            jobs[job_id]['progress'] = 10
            jobs[job_id]['message'] = 'Cloning repository...'
            
            # Construct the command to run PromptSwitch
            cmd = [
                sys.executable, 
                '../main.py',  # Path to main.py from ui directory
                repo_url,
                '--output-filename', f'{job_id}_output.md',
                '--output-dir', output_dir
            ]
            
            # Update progress
            jobs[job_id]['progress'] = 30
            jobs[job_id]['message'] = 'Running PromptSwitch analysis...'
            
            # Run PromptSwitch
            result = subprocess.run(
                cmd,
                cwd=os.path.dirname(os.path.abspath(__file__)),
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            if result.returncode == 0:
                # Success
                jobs[job_id]['status'] = 'completed'
                jobs[job_id]['progress'] = 100
                jobs[job_id]['message'] = 'Processing completed successfully'
                jobs[job_id]['results'] = {
                    'success': True,
                    'output': result.stdout,
                    'files_generated': [f'{job_id}_output.md'],
                    'execution_time': '45s',  # This would be calculated
                    'trace_id': job_id
                }
            else:
                # Error
                jobs[job_id]['status'] = 'failed'
                jobs[job_id]['message'] = f'Processing failed: {result.stderr}'
                jobs[job_id]['results'] = {
                    'success': False,
                    'error': result.stderr
                }
                
        except subprocess.TimeoutExpired:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = 'Processing timed out'
        except Exception as e:
            jobs[job_id]['status'] = 'failed'
            jobs[job_id]['message'] = f'Error: {str(e)}'

def run_server(port=8081):
    """Run the backend server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, PromptSwitchHandler)
    print(f"PromptSwitch backend server running on port {port}")
    print(f"Access at: http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8081
    run_server(port)