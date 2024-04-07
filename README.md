# E-Blogger
Group project for SPM WOX7016


## Basic Setup

Development Environment: 
- Windows 11 (should work on Linux or MacOS also)
- Python 3.11.5 

Setup Virtual Environment: 
```bash
python -m venv .  # create virtual environment
bin/activate  # activate venv 
pip install -r requirements.txt  # install all requirements 
```

Start server: 
```bash
uvicorn main:app --reload
```
