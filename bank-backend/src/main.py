#!/usr/bin/env python

from server import app
# do not delete. this imports our routes (very important)
from routes import people, accounts, banks, transactions # type: ignore

if __name__ == "__main__":
    app.run(debug=True, port=8000)
