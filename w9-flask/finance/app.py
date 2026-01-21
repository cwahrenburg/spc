import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
# from flask_login import LoginManager, current_user
from werkzeug.security import check_password_hash, generate_password_hash

# CS50 Helper Functions
from helpers import apology, login_required, lookup, usd

# SQL Helper Functions
from helpers import lookup_cash, log_transaction, update_cash

# Configure application
app = Flask(__name__)

app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


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
    """Show portfolio of stocks"""

    # (1) List of stocks
    portfolio = db.execute("SELECT * FROM account WHERE user_id = ?", session["user_id"])

    valueOfHoldings = []
    for stock in portfolio:
        stock["price"] = lookup(stock["symbol"])["price"]
        stock["value"] = stock["price"] * stock["shares"]
        valueOfHoldings.append(stock["value"])

    valueOfStocks = round(sum(valueOfHoldings), 2)

    # Display user's current cash balance
    cashAvail = lookup_cash(db, session["user_id"])

    # Display grand total
    totalAccountBalance = round(valueOfStocks + cashAvail, 2)

    return render_template("index.html", portfolio=portfolio, cashAvail=cashAvail, valueOfStocks=valueOfStocks, totalAccountBalance=totalAccountBalance)

# DONE


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""

    cashAvail = lookup_cash(db, session["user_id"])

    # Ask for symbol and number of shares
    if request.method == "GET":
        return render_template("buy.html", cashAvail=cashAvail)

    elif request.method == "POST":
        # Placeholders for form data
        symbol = request.form.get("symbol")
        sharesPurchased = request.form.get("shares")

        stock = lookup(symbol)  # Dict of stock data

        try:
            sharesPurchased = float(sharesPurchased)
        except ValueError:
            return apology("Number of shares must be valid number")

        else:
            sharesPurchased = float(sharesPurchased)

        # Data Input Validation
        if sharesPurchased <= 0:
            return apology("Number of shares must be a positive integer", code=400)

        if sharesPurchased != int(sharesPurchased):
            return apology("Number of shares must be a positive integer", code=400)

        if stock == None:
            return apology("Stock symbol invalid")

        # Purchase stock stock:
        stockPrice = float(stock["price"])
        purchaseCost = stockPrice * sharesPurchased

        if purchaseCost > cashAvail:
            return apology("Insufficient cash avaialble for purhcase")

        else:
            # Log Transaction
            log_transaction(db,
                            userID=session["user_id"],
                            transactionType="buy",
                            stockSymbol=symbol,
                            stockPrice=stockPrice,
                            sharesCount=sharesPurchased,
                            shareValue=purchaseCost)

            # Update Cash Balance
            cashBalance = cashAvail - purchaseCost
            db.execute(
                "UPDATE users SET cash = ? WHERE id = ?", cashBalance, session["user_id"])

            # Update User Account
            # Determine if user owns any of shares of current stock already
            try:
                # If they own a particular stock, update database record
                sharesOwned = db.execute(
                    "SELECT shares FROM account WHERE user_id = ? AND symbol = ?", session["user_id"], symbol)[0]["shares"]
                sharesOwned = sharesOwned + sharesPurchased
                db.execute("UPDATE account SET shares = ? WHERE user_id = ? AND symbol = ?",
                           sharesOwned, session["user_id"], symbol, )
            except:
                # Create a new record for this particular stock in databsae
                db.execute("INSERT INTO account (user_id, symbol, shares) VALUES(?, ?, ?)",
                           session["user_id"], symbol, sharesPurchased)
            finally:
                return redirect("/")

    return apology("TODO")


# DONE
@app.route("/history")
@login_required
def history():
    """Show history of transactions"""

    history = db.execute("SELECT * FROM transactions WHERE user_id = ?", session["user_id"])

    return render_template("history.html", history=history)


# COMPLETE (PROVIDED)
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

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
        rows = db.execute(
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


# COMPLETE (PROVIDED)
@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


# DONE
@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""

    stockSymbol = request.form.get("symbol")

    # If requested via GET, display form to request stock quote
    if request.method == "GET":
        return render_template("quote.html")

    # If form submitted via post, look up stock symbol by calling `lookup()` function to display results
    elif request.method == "POST":
        stock = lookup(stockSymbol)

        if not stock:
            return apology("invalid symbol", code=400)

    return render_template("quoted.html", stock=stock)

    # if stock is successfully looked up, display information about stock back to user


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
        elif username in [i["username"] for i in db.execute(("SELECT * FROM users"))]:
            return (apology(message="Username already taken"))

        else:
            # Add user to database
            hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash, cash) VALUES(?, ?, ?)",
                       username, hash, 10000)

            # Pull user id from new row in database table:
            userID = db.execute("SELECT id FROM USERS WHERE username = ?", username)[0]["id"]

            session["user_id"] = userID
            session["username"] = username

            print("user ID: ", session["user_id"])

            # Log Transaction
            log_transaction(db,
                            userID=session["user_id"],
                            sharesCount="",
                            stockPrice="",
                            shareValue=10000,
                            stockSymbol="",
                            transactionType="deposit"
                            )

            return (redirect("/"))

    else:
        pass

    return apology("TODO")


# DONE
@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""

    if request.method == "GET":

        # Query database to populate all stocks owned by user
        holdings = db.execute("SELECT * FROM account WHERE user_id = ?", session["user_id"])

        return render_template("sell.html", holdings=holdings)

    elif request.method == "POST":

        # Pull data from web page for specific stock user would like to sell
        symbol = request.form.get("symbol")
        sharesToSell = int(request.form.get("shares"))

        stockPrice = lookup(symbol)["price"]

        # Determine how many shares of stock user currently owns so they cann't sell more
        sharesOwned = int(db.execute("SELECT * FROM account WHERE user_id = ? AND symbol = ?",
                          session["user_id"], symbol)[0]["shares"])

        # Exception handling:
        if sharesToSell > sharesOwned:
            return apology("Number of shares sold cannot exceed number of shares owned")

        elif sharesToSell < 1:
            return apology("Cannot sell less than 1 share")

        else:
            # Update quantity of shares owned
            sharesOwned = sharesOwned - sharesToSell

            oldBalance = lookup_cash(db, session["user_id"])
            transactionValue = (sharesToSell * stockPrice)
            newBalance = oldBalance + transactionValue

            db.execute("UPDATE account SET shares = ? WHERE user_id = ? AND symbol = ?",
                       sharesOwned, session["user_id"], symbol)
            db.execute("UPDATE users SET cash = ? WHERE id = ?", newBalance, session["user_id"])

            log_transaction(
                db,
                userID=session["user_id"],
                transactionType="sell",
                stockSymbol=symbol,
                stockPrice=stockPrice,
                sharesCount=sharesToSell,
                shareValue=transactionValue)

            return redirect("/")

    else:
        return apology("todo")

# TODO 2026-01-16


@app.route("/deposit", methods=["GET", "POST"])
@login_required
def deposit():
    """Deposit cash into account"""

    oldCashBalance = lookup_cash(db, userID=session["user_id"])

    if request.method == "GET":
        return render_template("deposit.html", oldCashBalance=usd(oldCashBalance))

    elif request.method == "POST":

        # Pull form data fields
        depositAmount = int(request.form.get("amount"))

        # Exception handling:
        if depositAmount <= 0:
            return apology("Deposit must be greater than zero")

        else:
            # Update cash balance
            newCashBalance = oldCashBalance + depositAmount

            update_cash(db, userID=session["user_id"], newBalance=newCashBalance)

            log_transaction(
                db,
                userID=session["user_id"],
                transactionType="deposit",
                stockSymbol="-",
                stockPrice="-",
                sharesCount=0,
                shareValue=depositAmount)

            return redirect("/")

    else:
        return apology("todo")
