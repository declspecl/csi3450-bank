# CSI 3450 Backend

## How to setup

To run the scripts in the intended manner, run the following commands in a terminal:
1. `python -m venv .venv`
2. If on Mac/Linux: `source ./.venv/bin/activate` or on Windows: `.\.venv\Activate.bat`
    - If on Windows, and you get an error like `cannot be loaded because the execution of scripts is disabled on this system`, run this command: `Set-ExecutionPolicy Unrestricted -Force`, restart your terminal/editor, and then retry
3. `pip install -r requirements.txt`

## How to run the app

1. In a terminal, run on Mac/Linux: `source ./.venv/bin/activate` or on Windows: `.\.venv\Scripts\Activate.bat`
    - If on Windows, and you get an error like `cannot be loaded because the execution of scripts is disabled on this system`, run this command: `Set-ExecutionPolicy Unrestricted -Force`, restart your terminal/editor, and then retry
2. `python -m flask --app src/main.py run`
