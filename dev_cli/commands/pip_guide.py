# cnb_cli/templates/pip_guide.py

PIP_GUIDE = """\
# ----------------------------
# Zackry / FastAPI & Python Pip Guide
# ----------------------------

# 1️⃣ Save only used packages in your project
pipreqs . --force          # Generates requirements.txt based on actual imports

# 2️⃣ Optional: Backup all installed packages
pip freeze > full-requirements-backup.txt

# 3️⃣ Clean environment setup
deactivate                 # Exit current virtual environment
rm -rf venv/               # Remove old venv (Linux/macOS)
venv\\Scripts\\activate     # Windows equivalent

# 4️⃣ Create and activate a new virtual environment
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\\Scripts\\activate     # Windows

# 5️⃣ Install project dependencies
pip install -r requirements.txt

# 6️⃣ Upgrade or manage packages
pip install --upgrade [package]           # Upgrade a package
pip install --force-reinstall [package]   # Reinstall a package
pip install --no-deps [package]          # Install without dependencies

# 7️⃣ Pip info and help
pip --version            # Show pip version
pip help                 # General help
pip help install         # Help for a specific command

# ----------------------------
# FastAPI / Development Tips
# ----------------------------

# Kill FastAPI/Uvicorn server if stuck
lsof -ti :8000 | xargs kill -9       # Linux/macOS
taskkill /F /PID <PID>               # Windows, replace <PID> with process id

# Run FastAPI app
uvicorn app.main:app --reload        # Dev mode with hot reload
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker  # Production

# ❗ Workers explanation:
# -w 1 : 1 worker, single process, suitable for dev/testing
# -w 2 : 2 workers, can handle 2 requests simultaneously
# -w 4 : 4 workers, common default for small production servers
# -w N : N workers, improves concurrency on CPU-bound tasks
# Each worker is a separate process serving requests.

# ----------------------------
# CLI Tips
# ----------------------------

| i      cnb i    –     Initialize a new FastAPI project ⚡                                                                      │
│ init   cnb init –     Initialize a new FastAPI project ⚡                                                                   │
│ e      cnb e    –     Encryption Tools 🔐                                                                                      │
│ b      cnb b    –     Docker Build Tools 🐳                                                                                    │
│ d      cnb d    –     Docker Deployment Tool 🚀                                                                                │
│ g      cnb g    –     Component Generator 🛠️                                                                                    │
│ r      cnb r    –     Request Management System 🎫   


# ----------------------------
# Testing Your App
# ----------------------------

# Quick test endpoints
python -c "import requests; print(requests.get('http://127.0.0.1:8000/health/').json())"

# Check environment variables
python -c "import os; print(os.getenv('ENABLE_LOG_REQUEST_HEADER'))"

# Check encryption/decryption
python -c \\
\"\"\"from cryptography.fernet import Fernet
key=open('.env').read().splitlines()[0].split('=')[1]
f=Fernet(key.encode())
token=f.encrypt(b'test')
print(f.decrypt(token))\"\"\"

# Run tests
pytest tests/                        # Run all tests
python -m unittest discover          # Alternative test runner

# View logs
tail -f logs/app.log                 # Follow logs (if logging configured)

# ----------------------------
# Recommended workflow
# ----------------------------
# 1. Generate a clean requirements.txt using pipreqs
# 2. Backup your full environment with pip freeze
# 3. Create a new virtual environment
# 4. Install only the required packages
# 5. Generate encryption key with Zackry CLI
# 6. Use uvicorn for dev, gunicorn with multiple workers for production
# 7. Write and run tests with pytest or unittest
# ----------------------------

# ----------------------------
# Created by : Hour Zackry
# Check out my profile and projects:
# LinkedIn: https://www.linkedin.com/in/pho-keanghour-27133b21b/
# GitHub: https://github.com/Keanghour
# Portfolio: https://keanghour.github.io/keanghour.me/
# ----------------------------

"""
