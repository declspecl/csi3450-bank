# csi-3450 scripts

To run the scripts in the intended manner, run the following commands in a terminal:
1. `python -m venv .venv`
2. If on Mac/Linux: `source ./.venv/bin/activate` or on Windows: `./.venv/bin/Activate.ps1`
    - If on Windows, and you get an error like `cannot be loaded because the execution of scripts is disabled on this system`, run this command: `Set-ExecutionPolicy Unrestricted -Force`, restart your terminal/editor, and then retry
3. `pip install -r requirements.txt`
4. `python <script-name>.py`
