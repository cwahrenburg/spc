import requests

from flask import redirect, render_template, session
from functools import wraps


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


def lookup(symbol):
    """
    Look up quote for symbol.
    If symbol is valid, return a dictionary containing name, price, and symbol
    Is symbol is not valid return none
    """

    url = f"https://finance.cs50.io/quote?symbol={symbol.upper()}"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for HTTP error responses
        quote_data = response.json()
        return {
            "name": quote_data["companyName"],
            "price": quote_data["latestPrice"],
            "symbol": symbol.upper(),
            "displayPrice": usd(quote_data["latestPrice"])
        }
    except requests.RequestException as e:
        print(f"Request error: {e}")
    except (KeyError, ValueError) as e:
        print(f"Data parsing error: {e}")
    return None


def usd(value):
    """Format value as USD."""
    return f"${value:,.2f}"


def lookup_cash(db, userID: int):
    """Look up a user's current cash balance via sqlite"""
    cashBalance = round(db.execute("SELECT cash FROM users WHERE id = ?", userID)[0]["cash"])
    return cashBalance


def log_transaction(db, userID: int, transactionType, stockSymbol, stockPrice, sharesCount, shareValue):
    # Log Transaction

    if transactionType not in ["buy", "sell", "deposit", "withdrawl"]:
        raise Exception
    else:
        pass

    db.execute("INSERT INTO transactions (user_id, transaction_type, symbol, price, shares, total) \
                VALUES(?, ?, ?, ?, ?, ?)",
               userID, transactionType, stockSymbol, stockPrice, sharesCount, shareValue)

    return None


def update_cash(db, userID, newBalance):
    """Update user's cash in user table"""
    db.execute("UPDATE users SET cash = ? WHERE id = ?", newBalance, userID)
    return None
