import requests

from flask import redirect, render_template, session
from functools import wraps
from cs50 import SQL
import pandas as pd


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


def cs50_query_to_df(DB: SQL, qry:str) -> pd.DataFrame:
    """
    Converts a CS50 SQL query to a pandas DataFrame.

    Parameters:
    DB (SQL): The CS50 database connection object.
    qry (str): The SQL query to execute.

    Returns:
    pd.DataFrame: A DataFrame containing the query results.
    """

    qry = DB.execute(qry)
    return pd.DataFrame.from_records(qry)

