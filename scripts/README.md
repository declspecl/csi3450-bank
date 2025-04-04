# csi-3450 scripts

To run the scripts in the intended manner, run the following commands in a terminal:
1. `python -m venv .venv`
2. If on Mac/Linux: `source ./.venv/bin/activate` or on Windows: `.\.venv\Scripts\Activate.bat`
3. `pip install -r requirements.txt`
4. `python <script-name>.py`

For ex, `python init-db.py`

### DATABASE_PASSWORD 
 DATABASE_PASSWORD = "postgres"
 Make sure this matches the password for your Bank Server in PGAdmin
