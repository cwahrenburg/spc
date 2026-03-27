from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required, cs50_query_to_df
from spc import SPC

import plotly.io as pio
import pandas as pd

# Import Database
from config import DB
from config import qryMeasurementSQL, insertNoteSQL


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
@app.route("/controlchart")
def controlCharts():
    """Generate charts for all features in database"""
    
    df = cs50_query_to_df(DB=DB, qry=qryMeasurementSQL)

    df["feature_id"] = df["feature_id"].fillna(0).astype(int)

    htmlFigList= []
    
    for featureID in df["feature_id"].unique(): 
        try: 
            chart = SPC(df.query("feature_id == @featureID").reset_index(drop=True), valueColumn="value").control_chart()
            htmlFig = pio.to_html(chart)
            htmlFigList.append(htmlFig)
        except: 
            pass

    return render_template("controlchart.html", htmlFigList=htmlFigList)

@app.route("/metrics")
def metrics():
    """Generate summary table of all metrics"""
    
    df = cs50_query_to_df(qry = qryMeasurementSQL, DB=DB)

    L = [] 
    for featureID in df["feature_id"].unique():
        try:     
            spc = SPC(df.query("feature_id == @featureID").copy(), valueColumn="value", uslCol="usl", lslCol="lsl")
            L.append(spc.metrics)
        except: 
            pass

    metrics = pd.concat(L).reset_index(drop=True)

    htmlMetrics = metrics.to_html(classes = "table table-striped table-responsive")

    return render_template("metrics.html", htmlMetrics=htmlMetrics) 

@app.route("/engineering", methods = ["GET", "POST"])
def engineering(): 
    """Control charts with additional abilities to update underlying data"""


    df = cs50_query_to_df(DB=DB, qry=qryMeasurementSQL)

    df["feature_id"] = df["feature_id"].fillna(0).astype(int)

    htmlFigList= []
    
    for featureID in df["feature_id"].unique(): 
        try: 
            chart = SPC(df.query("feature_id == @featureID").reset_index(drop=True), valueColumn="value").control_chart()
            htmlFig = pio.to_html(chart)
            htmlFigList.append(htmlFig)
        except: 
            pass

    if request.method == "GET": 
        return render_template("engineering.html", htmlFigList=htmlFigList)
    else: 
        measurementID = request.form.get("measurementID")
        noteText = request.form.get("noteText")
        DB.execute(insertNoteSQL, measurementID, noteText)
        return redirect("/engineering")


    
    return apology("TODO")

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