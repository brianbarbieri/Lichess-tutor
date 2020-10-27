#!/usr/bin/python3
from app import create_app
app = create_app()

if __name__ == "__main__":
    app.config.update(PROPAGATE_EXCEPTIONS=False)
    app.run(debug=True)

    # to run: env FLASK_APP=run.py env FLASK_DEBUG=1 python -m flask run
