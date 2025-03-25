# CSI 3450 Backend

## How to setup

To run the scripts in the intended manner, run the following commands in a terminal:
1. `python -m venv .venv`
2. If on Mac/Linux: `source ./.venv/bin/activate` or on Windows: `.\.venv\Scripts\Activate.bat`
3. `pip install -r requirements.txt`

## How to run the app

1. In a terminal, run on Mac/Linux: `source ./.venv/bin/activate` or on Windows: `.\.venv\Scripts\Activate.bat`
2. `python src/main.py`


###Flask dependency
pip install flask flask-cors psycopg2

### DATABASE_PASSWORD 
 DATABASE_PASSWORD = "postgres" in main.py
 Make sure this matches the password for your Bank Server in PGAdmin

