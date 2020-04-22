#!/usr/bin/python3
"""Flask web application.
Host: 0.0.0.0 
port: 5000
Routes:
    /states: HTML template with all State.
    /states/<id>: HTML template given state with <id>.
"""
from models import storage
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/states", strict_slashes=False)
def states():
    """Render an HTML template with all States.

    Arguments:
        None
    Returns:
        Render (Html) template 9-states.html
    """
    states = storage.all("State")
    return render_template("9-states.html", state=states)


@app.route("/states/<id>", strict_slashes=False)
def states_id(id):
    """Render an HTML template with given state <id>

    Arguments:
        id: params state id
    Returns:
        Render (Html) template 9-states.html    
    """
    for state in storage.all("State").values():
        if state.id == id:
            return render_template("9-states.html", state=state)
    return render_template("9-states.html")

@app.teardown_appcontext
def teardown(exc):
    """Remove the current SQLAlchemy session."""
    storage.close()


if __name__ == "__main__":
    app.run(host="0.0.0.0")
