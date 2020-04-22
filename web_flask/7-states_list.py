#!/usr/bin/python3
"""Flask web application.
Host: 0.0.0.0
port: 5000
Routes:
    /states_list: HTML page with a list of all States in DB.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    """Render an HTML template with a list of all states.

    Arguments:
        None
    Returns:
        Render (Html) tmeplate 7-states_list.html
    """
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
