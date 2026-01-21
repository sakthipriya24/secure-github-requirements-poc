# Secure GitHub Credentials in Requirements.txt - POC

## Overview

This proof of concept demonstrates how to securely manage GitHub Personal Access Tokens (PAT) and usernames in Python `requirements.txt` files using environment variables, eliminating the security risk of hardcoded credentials.

## Problem Statement

Python's `pip` does not natively support environment variable substitution in `requirements.txt` files. This forces developers to either:
- Hardcode credentials directly in the file (security risk)
- Manually edit the file before installation (inconvenient and error-prone)
- Use complex workarounds

## Solution

A Python helper script (`install_requirements.py`) that:
1. Reads GitHub credentials from `.env` file using `python-decouple`
2. Processes `requirements.txt` and replaces placeholders with actual values
3. Installs packages using the processed requirements file
4. Automatically cleans up temporary files

## Files Included

- `install_requirements.py` - Helper script for secure installation
- `requirements.txt` - Example requirements file with placeholders
- `.env.example` - Template for environment variables (optional)
- `README_GITHUB_ENV_VARS.md` - This documentation

## Quick Start

### 1. Set Up Environment Variables

Create a `.env` file in your project root:

```bash
GITHUB_USERNAME=your_github_username_or_org
GITHUB_PAT=ghp_your_personal_access_token_here
```

### 2. Update requirements.txt

Use placeholders in your `requirements.txt`:

```txt
git+https://${GITHUB_USERNAME}:${GITHUB_PAT}@github.com/${GITHUB_USERNAME}/private-package
```

### 3. Install Requirements

Run the helper script instead of pip directly:

```bash
python install_requirements.py
```

**Important:** Do NOT run `pip install -r requirements.txt` directly - it will fail because pip doesn't support environment variable substitution.

## How It Works

```
┌─────────────────┐
│   .env file     │
│  GITHUB_USERNAME│
│  GITHUB_PAT     │
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ install_requirements│
│      .py            │
│  - Reads .env       │
│  - Processes file   │
│  - Replaces vars    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ requirements_temp   │
│      .txt          │
│  (processed file)   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│   pip install       │
│  (installs packages)│
└─────────────────────┘
```

## Security Benefits

✅ **No hardcoded credentials** - Credentials stored in `.env` (gitignored)  
✅ **Environment-specific** - Different tokens for dev/staging/production  
✅ **Easy rotation** - Update `.env` without touching code  
✅ **Version control safe** - No secrets committed to git  
✅ **Team friendly** - Each developer uses their own credentials  

## Example Usage

### requirements.txt
```txt
# Public packages
Django==5.0.3
requests==2.32.2

# Private GitHub packages
git+https://${GITHUB_USERNAME}:${GITHUB_PAT}@github.com/${GITHUB_USERNAME}/private-package-1
git+https://${GITHUB_USERNAME}:${GITHUB_PAT}@github.com/${GITHUB_USERNAME}/private-package-2
```

### .env
```bash
GITHUB_USERNAME=my-org
GITHUB_PAT=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Installation
```bash
$ python install_requirements.py
Using GitHub username: my-org
Using GitHub PAT: ghp_...xxxx

Installing requirements...
✓ Requirements installed successfully!
```

## Requirements

- Python 3.6+
- `python-decouple` package (for reading `.env` files)
- `.env` file with `GITHUB_USERNAME` and `GITHUB_PAT` variables

## Integration with CI/CD

### GitHub Actions Example

```yaml
- name: Install requirements
  env:
    GITHUB_USERNAME: ${{ secrets.GITHUB_USERNAME }}
    GITHUB_PAT: ${{ secrets.GITHUB_PAT }}
  run: python install_requirements.py
```

### GitLab CI Example

```yaml
install_requirements:
  script:
    - python install_requirements.py
  variables:
    GITHUB_USERNAME: $GITHUB_USERNAME
    GITHUB_PAT: $GITHUB_PAT
```
## Troubleshooting

### Error: "GITHUB_USERNAME is not set"
- Ensure `.env` file exists in project root
- Check that variable name matches exactly (case-sensitive)
- Verify `python-decouple` is installed

### Error: "Repository not found"
- Verify GitHub username/organization name is correct
- Check that PAT has access to the repository
- Ensure PAT has `repo` scope enabled

### Error: "python-decouple is not installed"
```bash
pip install python-decouple
```
