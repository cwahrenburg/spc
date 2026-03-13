from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, cs50_query_to_df
from spc import SPC

import plotly.io as pio

# Plottong Functions to pass to html page
from charts import test_chart

# Import Database
from config import DB

# CS50 Helper Functions

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# DONE
@app.route("/")
@login_required
def index():
    """Show hompepage"""

    return render_template("index.html")

# COMPLETE (PROVIDED)
@app.route("/login", methods=["GET", "POST"])
def login():
    
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = DB.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

# TODO 
@app.route("/features")
def features():
    """Generate charts for all features in database"""
    
    # Select all measurements
    qry = f"SELECT * FROM measurements"

    df = cs50_query_to_df(DB=DB, qry=qry)
    print(df["feature_id"].unique())

    htmlFigList= []
    for featureID in df["feature_id"].unique(): 
        chart = SPC(df.query("feature_id == @featureID"), valueColumn="value").control_chart()
        htmlFig = pio.to_html(chart)
        htmlFigList.append(htmlFig)

    return render_template("features.html", htmlFigList=htmlFigList)

@app.route("/control-charts")
def control_charts():
    pass



# DONE
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    username = request.form.get("username")
    password = request.form.get("password")
    password_check = request.form.get("confirmation")

    # When form requested via GET, display registration form

    if request.method == "GET":
        return render_template("register.html")

    # Server-side validation

    elif request.method == "POST":

        # Server - Side Validation

        if not username:
            return (apology(message="Missing username"))

        elif not password:
            return (apology(message="Missing password"))

        # Check if passwords do not match
        elif password != password_check:
            return (apology(message="Passwords must match"))

        # Unique username
        elif username in [i["username"] for i in DB.execute(("SELECT * FROM users"))]:
            return (apology(message="Username already taken"))

        else:
            # Add user to database
            hash = generate_password_hash(password)
            DB.execute("INSERT INTO users (username, hash) VALUES(?, ?)",
                       username, hash)

            # Pull user id from new row in database table:
            userID = DB.execute("SELECT id FROM USERS WHERE username = ?", username)[0]["id"]

            session["user_id"] = userID
            session["username"] = username

            print("user ID: ", session["user_id"])

            return (redirect("/"))

    else:
        pass

    return apology("TODO")



# COMPLETE (PROVIDED)
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')