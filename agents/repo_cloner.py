#!/usr/bin/env python3
"""
Repo Cloner Agent

Handles cloning GitHub repositories using GitPython.
Follows DX best practices with error handling and cleanup.
"""

import os
import shutil
import tempfile
from pathlib import Path
from urllib.parse import urlparse

try:
    import git
except ImportError:
    print("GitPython not found. Install with: pip install GitPython")
    raise


class RepoCloner:
    """Agent responsible for cloning GitHub repositories."""
    
    def __init__(self, temp_dir=None):
        self.temp_dir = temp_dir or tempfile.gettempdir()
        self.cloned_repos = []  # Track for cleanup
    
    def clone_repo(self, github_url, target_dir=None):
        """
        Clone a GitHub repository to a temporary or specified directory.
        
        Args:
            github_url (str): GitHub repository URL
            target_dir (str, optional): Target directory for cloning
            
        Returns:
            Path: Path to the cloned repository
            
        Raises:
            ValueError: If URL is invalid
            git.GitCommandError: If cloning fails
        """
        # Validate GitHub URL
        if not self._is_valid_github_url(github_url):
            raise ValueError(f"Invalid GitHub URL: {github_url}")
        
        # Determine target directory
        if target_dir is None:
            repo_name = self._extract_repo_name(github_url)
            target_dir = Path(self.temp_dir) / f"gitread_{repo_name}"
        else:
            target_dir = Path(target_dir)
        
        # Remove existing directory if it exists
        if target_dir.exists():
            shutil.rmtree(target_dir)
        
        try:
            print(f"Cloning {github_url} to {target_dir}...")
            
            # Clone repository with shallow clone for efficiency
            repo = git.Repo.clone_from(
                github_url,
                target_dir,
                depth=1,  # Shallow clone
                single_branch=True  # Only main/master branch
            )
            
            # Track for cleanup
            self.cloned_repos.append(target_dir)
            
            print(f"✅ Successfully cloned to {target_dir}")
            return target_dir
            
        except git.GitCommandError as e:
            print(f"❌ Failed to clone repository: {e}")
            # Clean up partial clone if it exists
            if target_dir.exists():
                shutil.rmtree(target_dir)
            raise
        except Exception as e:
            print(f"❌ Unexpected error during cloning: {e}")
            if target_dir.exists():
                shutil.rmtree(target_dir)
            raise
    
    def _is_valid_github_url(self, url):
        """
        Validate if the URL is a valid GitHub repository URL.
        
        Args:
            url (str): URL to validate
            
        Returns:
            bool: True if valid GitHub URL
        """
        try:
            parsed = urlparse(url)
            
            # Check if it's a GitHub URL
            if parsed.netloc not in ['github.com', 'www.github.com']:
                return False
            
            # Check if path has at least owner/repo format
            path_parts = parsed.path.strip('/').split('/')
            if len(path_parts) < 2:
                return False
            
            # Remove .git suffix if present
            if path_parts[-1].endswith('.git'):
                path_parts[-1] = path_parts[-1][:-4]
            
            return True
            
        except Exception:
            return False
    
    def _extract_repo_name(self, github_url):
        """
        Extract repository name from GitHub URL.
        
        Args:
            github_url (str): GitHub repository URL
            
        Returns:
            str: Repository name
        """
        parsed = urlparse(github_url)
        path_parts = parsed.path.strip('/').split('/')
        
        # Get repo name (last part of path)
        repo_name = path_parts[-1]
        
        # Remove .git suffix if present
        if repo_name.endswith('.git'):
            repo_name = repo_name[:-4]
        
        return repo_name
    
    def get_repo_info(self, repo_path):
        """
        Get basic information about the cloned repository.
        
        Args:
            repo_path (Path): Path to the cloned repository
            
        Returns:
            dict: Repository information
        """
        try:
            repo = git.Repo(repo_path)
            
            # Get remote URL
            remote_url = None
            if repo.remotes:
                remote_url = repo.remotes.origin.url
            
            # Get current branch
            current_branch = repo.active_branch.name if repo.active_branch else 'detached'
            
            # Get latest commit info
            latest_commit = repo.head.commit
            
            return {
                'path': str(repo_path),
                'remote_url': remote_url,
                'current_branch': current_branch,
                'latest_commit': {
                    'sha': latest_commit.hexsha[:8],
                    'message': latest_commit.message.strip(),
                    'author': str(latest_commit.author),
                    'date': latest_commit.committed_datetime.isoformat()
                },
                'is_dirty': repo.is_dirty()
            }
            
        except Exception as e:
            print(f"⚠️ Could not get repo info: {e}")
            return {
                'path': str(repo_path),
                'error': str(e)
            }
    
    def cleanup(self, repo_path=None):
        """
        Clean up cloned repositories.
        
        Args:
            repo_path (Path, optional): Specific repo to clean up.
                                      If None, cleans up all tracked repos.
        """
        if repo_path:
            # Clean up specific repository
            repo_path = Path(repo_path)
            if repo_path.exists():
                try:
                    shutil.rmtree(repo_path)
                    print(f"🧹 Cleaned up {repo_path}")
                    if repo_path in self.cloned_repos:
                        self.cloned_repos.remove(repo_path)
                except Exception as e:
                    print(f"⚠️ Could not clean up {repo_path}: {e}")
        else:
            # Clean up all tracked repositories
            for repo_path in self.cloned_repos.copy():
                self.cleanup(repo_path)
    
    def __del__(self):
        """Cleanup on object destruction."""
        self.cleanup()


if __name__ == "__main__":
    # Test the repo cloner
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python repo_cloner.py <github_url>")
        sys.exit(1)
    
    github_url = sys.argv[1]
    cloner = RepoCloner()
    
    try:
        repo_path = cloner.clone_repo(github_url)
        repo_info = cloner.get_repo_info(repo_path)
        
        print("\n📊 Repository Information:")
        for key, value in repo_info.items():
            print(f"  {key}: {value}")
        
        input("\nPress Enter to cleanup...")
        cloner.cleanup(repo_path)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)