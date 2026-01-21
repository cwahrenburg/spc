from cs50 import SQL
from pprint import pp
from helpers import lookup

# # Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

session = {"user_id" : 1}

# # print(db.execute("SELECT * FROM users"))

# userData = db.execute(("SELECT * FROM users"))


# USERS = [i["username"] for i in userData]
# print(USERS)

# from werkzeug.security import check_password_hash, generate_password_hash
# hash = generate_password_hash("chris")
# print(hash)

# pp(userData)

# sharesOwned = db.execute("SELECT shares FROM account WHERE user_id = ? AND symbol = ?", 1, "rtx")[0]["shares"]
# print(f"test number of rtx shares owned: {sharesOwned}")

# sharesOwned = db.execute("SELECT shares FROM account WHERE user_id = ? AND symbol = ?", 1, "msft")[0]["shares"]
# print(f"test number of msft shares owned: {sharesOwned}")

# BUY ====
# userStocks = db.execute("SELECT * FROM account WHERE user_id = ?", session["user_id"])

# for stock in userStocks:
#     stock["price"] = lookup(stock["symbol"])["price"]
#     stock["value"] = stock["price"] * stock["shares"]

# pp(userStocks)

# l = [1, 2, 3, 4,]

# print(sum(l))


#===  Sell   ====

holdings = db.execute("SELECT * FROM account WHERE user_id = 1")

for stock in stocks:


print(data)

userID = 1
cashBalance = round(db.execute("SELECT cash FROM users WHERE id = ?", userID)[0]["cash"])
print(cashBalance)
