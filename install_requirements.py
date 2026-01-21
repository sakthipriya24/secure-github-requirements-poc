#!/usr/bin/env python3
"""
Helper script to install requirements with GitHub username and Personal Access Token from environment variables.
This script processes requirements.txt and replaces ${GITHUB_USERNAME} and ${GITHUB_PAT} with actual values from .env
"""
import os
import subprocess
import sys
from pathlib import Path

try:
    from decouple import config
except ImportError:
    print("ERROR: python-decouple is not installed. Install it first:")
    print("  pip install python-decouple")
    sys.exit(1)

def install_requirements():
    """Install requirements with GitHub username and PAT from environment variables"""
    # Get GitHub username and PAT from .env file using decouple (same as Django settings)
    github_username = config('GITHUB_USERNAME', default=None)
    github_pat = config('GITHUB_PAT', default=None)
    
    if not github_username:
        print("ERROR: GITHUB_USERNAME is not set in your .env file!")
        print("Please add it to your .env file:")
        print("  GITHUB_USERNAME=your_github_username_here")
        sys.exit(1)
    
    if not github_pat:
        print("ERROR: GITHUB_PAT is not set in your .env file!")
        print("Please add it to your .env file:")
        print("  GITHUB_PAT=your_github_personal_access_token_here")
        sys.exit(1)
    
    # Read requirements.txt
    requirements_path = Path(__file__).parent / 'requirements.txt'
    
    if not requirements_path.exists():
        print(f"ERROR: {requirements_path} not found!")
        sys.exit(1)
    
    # Read and process requirements
    with open(requirements_path, 'r') as f:
        content = f.read()
    
    # Replace ${GITHUB_USERNAME} and ${GITHUB_PAT} with actual values
    processed_content = content.replace('${GITHUB_USERNAME}', github_username)
    processed_content = processed_content.replace('${GITHUB_PAT}', github_pat)
    
    # Show what we're using (mask the token for security)
    masked_pat = github_pat[:4] + '...' + github_pat[-4:] if len(github_pat) > 8 else '****'
    print(f"Using GitHub username: {github_username}")
    print(f"Using GitHub PAT: {masked_pat}")
    print()
    
    # Write to temporary file
    temp_requirements = Path(__file__).parent / 'requirements_temp.txt'
    with open(temp_requirements, 'w') as f:
        f.write(processed_content)
    
    try:
        # Install from processed requirements
        print("Installing requirements...")
        result = subprocess.run(
            [sys.executable, '-m', 'pip', 'install', '-r', str(temp_requirements)],
            check=True
        )
        print("\n✓ Requirements installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"ERROR: Failed to install requirements: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary file
        if temp_requirements.exists():
            temp_requirements.unlink()

if __name__ == '__main__':
    install_requirements()
