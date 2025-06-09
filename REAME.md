## 🔧 Setup Guide

### 1. Install Python (via `pyenv`)
Use `pyenv` to manage Python versions:

```bash
brew install pyenv
pyenv install 3.11.8
pyenv local 3.11.8

2. Create and activate a virtual environment

python -m venv .venv
source .venv/bin/activate

3. Upgrade pip and install dependencies

pip install --upgrade pip
pip install -r requirements.txt

#If you encounter an "externally-managed-environment" error, ensure you're inside the virtual environment (.venv) before installing packages.



