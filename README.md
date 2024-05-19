# E-Blogger
Group project for SPM WOX7016


## Basic Setup

**Development Environment:**
- Windows 11 (should work on Linux or MacOS also)
- Python 3.11.5 

**Setup Virtual Environment:**
```bash
python -m venv .  # create virtual environment
source bin/activate  # activate venv (on Linux / MacOS)
Scripts/activate  # activate venv (on Windows)
pip install -r requirements.txt  # install all requirements 
```

**Configuration:**

See comments in `config.py`.

**Start server:**
```bash
uvicorn main:app --reload
```

**API Document:**

Open `http://host:port/redoc` after starting server. 
